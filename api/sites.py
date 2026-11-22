

from .client import SitemarkAPI

def list_sites(api: SitemarkAPI, company: str) -> list[dict]:
    active_company = company or api.company
    page = 1
    sites = []
    while True:
        response = api.get(
            "sites",
            {
                "_page": page,
                "_pageSize": 1000
            }
        )
        sites.extend(response.get("data", []))
        pagination = response.get("pagination", {})
        if page >= pagination.get("pageCount", 1):
            break
        page += 1
    return sites