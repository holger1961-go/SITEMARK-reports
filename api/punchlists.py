import json
from .client import SitemarkAPI
from datetime import datetime, timedelta
from collections import Counter


def get_property_value(properties, key):
    prop = properties.get(key)

    if not prop:
        return None

    if isinstance(prop, dict):
        if prop.get("value") is not None:
            return prop.get("value")

        if prop.get("defaultValue") is not None:
            return prop.get("defaultValue")

    return prop


def count_status(items):
    return Counter(
        item["properties_STATUS"]
        for item in items
        if item.get("properties_STATUS")
    )


# Subroutine für flatten_item
def get_typ(description):
    if not description:
        return "X"
    if str(description).endswith(" Ticket"):
        return "Checkliste"
    return "Open Point"

# Subroutine für flatten_item
def get_status_icon(status):
    # print(f"STATUS=[{status}]")
    status = str(status or "").strip().upper()
    if status in ["CLOSED", "WONT_DO"]:
        return "X"
    if status in ["TO_DO", "IN_PROGRESS", "PLANNED", "RESOLVED"]:
        return "►"
    return "-"



# # Subroutine für build_week_columns
def count_weeks(items, typ):
    result = {}
    filtered = [
        item for item in items
        if item["typ"] == typ
    ]
    for week in range(16):
        key = f"{week:02d}_Woche"
        result[key] = sum(
            1 for item in filtered
            if item.get(key) == "X"
        )
    return result



def build_week_columns(created_at, updated_at, status_icon):
    result = {}
    for i in range(16):
        result[f"{i:02d}_Woche"] = ""
    if not created_at:
        return result
    start_date = datetime.fromisoformat(
        created_at.replace("Z", "+00:00")
    )
    if status_icon == "X" and updated_at:
        end_date = datetime.fromisoformat(
            updated_at.replace("Z", "+00:00")
        )
    else:
        end_date = datetime.now(start_date.tzinfo)

    for week in range(16):
        week_start = datetime.now(start_date.tzinfo) - timedelta(days=(week + 1) * 7)
        week_end = datetime.now(start_date.tzinfo) - timedelta(days=week * 7)
        if start_date <= week_end and end_date >= week_start:
            result[f"{week:02d}_Woche"] = "X"

    return result




def format_date(value):
    if not value:
        return None
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute)


def flatten_item(item, site_name):
    properties = item.get("properties", {})
    description = item.get("description")
    status = get_property_value(properties, "STATUS")

    result = {
        "site_name": site_name,
        "dataset_id": item.get("dataset_id"),
        "description": description,
        "typ": get_typ(description),
        "created_at": format_date(item.get("created_at")),
        "updated_at": format_date(item.get("updated_at")),
        "properties_VISIBLE_ID": get_property_value(properties, "VISIBLE_ID"),
        "properties_STATUS": status,
        "status_icon": get_status_icon(status),
    }

    result.update(
        build_week_columns(
            item.get("created_at"),
            item.get("updated_at"),
            get_status_icon(status)
        )
    )

    return result

# List Punchlist Items, bei SITEMARK unter layerFeatures mit semantic_type = PUNCH_LIST_ITEMS erhalten.
# Die API liefert die Daten paginiert auf 100 Items pro Seite.
# Daher wird hier eine Schleife verwendet, um alle Seiten abzurufen und die Ergebnisse zu sammeln.
def list_punchlist_items(api: SitemarkAPI, company: str, site_id: int, site_name: str):
# TODO 261122 def list_punchlist_items(site_id: int, site_name: str):
    active_company = company or api.company
    all_raw_items = []
    page = 1
    while True:
        response = api.get(
            "layerFeatures",
            {
                "site_id": site_id,
                "semantic_type": "PUNCH_LIST_ITEMS",
                "_page": page,
                "_pageSize": 100
            }
        )
        items = response.get("data", [])
        if not items:
            break

        all_raw_items.extend(items)
        # print(f"Seite {page}: {len(items)} Items")

        print(f"<-- {page * len(items)}", end="\r", flush=True)

        if len(items) < 100:
            break
        page += 1

    all_items = [
        flatten_item(item, site_name)
        for item in all_raw_items
    ]

    all_items.sort(
        key=lambda x: (
            x.get("dataset_id", 0),
            int(x.get("properties_VISIBLE_ID") or 0)
        )
    )


    # =================================================================================================
    # JSON Export mit True
    # =================================================================================================
    if False:
        filename = f"JSON_Punschlist__{site_name}.JSON"
        def json_serializer(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError(f"Type {type(obj)} not serializable")
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(
                all_items,
                f,
                indent=4,
                ensure_ascii=False,
                default=json_serializer
            )
        print("JSON-Datei gespeichert.")

    return all_items