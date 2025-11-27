import requests
import pandas as pd
from dataclasses import dataclass

API_KEY = "JOUW_ECHTE_API_KEY_HIER"
BASE_URL = "https://api.cbso.nbb.be/CBSO/..."

def get_annual_accounts(enterprise_number: str, year: int):
    headers = {
        "Ocp-Apim-Subscription-Key": API_KEY,
        "Accept": "application/json"
    }
    params = {
        "enterpriseNumber": enterprise_number,
        "financialYear": year
    }

    response = requests.get(BASE_URL, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


@dataclass
class AnnualAccountData:
    enterprise_number: str
    year: int
    equity: float
    total_assets: float
    total_liabilities: float

    @property
    def solvency_ratio(self) -> float:
        return self.equity / self.total_assets if self.total_assets else 0.0

    @property
    def debt_to_equity(self) -> float:
        return (
            self.total_liabilities / self.equity
            if self.equity
            else float("inf")
        )


if __name__ == "__main__":
    data = get_annual_accounts("0123456789", 2023)

    df = pd.json_normalize(data)
    print(df.columns)
