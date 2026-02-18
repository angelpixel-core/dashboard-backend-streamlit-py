from dataclasses import dataclass
from typing import Protocol

from dashboard.application.dto import SalesDashboardDTO


@dataclass(frozen=True)
class BuildSalesDashboardRequest:
    aggregate_id: str


class BuildSalesDashboardPort(Protocol):
    def execute(
        self,
        request: BuildSalesDashboardRequest,
    ) -> SalesDashboardDTO: ...
