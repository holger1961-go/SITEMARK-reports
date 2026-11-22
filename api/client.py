from __future__ import annotations

import requests

from ..config_black import API_KEY_B
from ..utils.logging_setup import logger


API_BASE = "https://api.sitemark.com"

class SitemarkAPI:
    def __init__(self, api_key: str | None = None, company: str | None = None):
            self.api_key = api_key or None
            self.company = company or "default"
            self.headers = {
                "Authorization": f"{self.api_key}",
                "Accept": "application/json",
            }
            
            if not self.api_key:
                logger.warning("Kein SITEMARK API-Key gesetzt (Firma: %s).", self.company)

    def get(self, endpoint: str, params=None):
        print(f"GET request to endpoint: >{self.company}< {endpoint} with params: {params}")



        url = f"{API_BASE}/{endpoint.lstrip('/')}"
        # logger.info(f"GET form url {url} with params: {params}")
        response = requests.get(
            url,
            headers=self.headers,
            params=params,
            timeout=60
        )
        response.raise_for_status()
        return response.json()
