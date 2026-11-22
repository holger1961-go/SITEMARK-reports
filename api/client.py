from __future__ import annotations

import requests

from ..config_black import API_KEY_B, API_KEY_T, COMPANIES
from ..utils.logging_setup import logger


API_BASE = "https://api.sitemark.com"


class SitemarkAPI:
    def __init__(self, company: str | None = None):
        self.company = (company or "default").strip().upper()

        company_keys = { COMPANIES[0]: API_KEY_B, COMPANIES[1]: API_KEY_T, }
        # api_key über company nachschlagen
        self.api_key = company_keys.get(self.company)
        self.headers: dict[str, str] = { "Accept": "application/json", }

        if self.api_key:
            self.headers["Authorization"] = str(self.api_key)
        else:
            logger.warning(
                "Kein SITEMARK API-Key gesetzt (Firma: %s).", self.company
            )

    def get(self, endpoint: str, params: dict | None = None):
        url = f"{API_BASE}/{endpoint.lstrip('/')}"
        # logger.info(f"GET form url {url} with params: {params}")

        response = requests.get(
            url,
            headers=self.headers,
            params=params,
            timeout=60,
        )
        response.raise_for_status()
        return response.json()