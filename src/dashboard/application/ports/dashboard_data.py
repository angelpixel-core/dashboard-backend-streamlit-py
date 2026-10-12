from dataclasses import dataclass
from typing import Protocol

from dashboard.application.dto import DashboardDataDTO, DashboardDataRowDTO


@dataclass(frozen=True)
class GetDashboardDataRequest:
    month: str | None = None
    regions: tuple[str, ...] | None = None


class GetDashboardDataPort(Protocol):
    def execute(
        self,
        request: GetDashboardDataRequest,
    ) -> DashboardDataDTO: ...


class DashboardDataReader(Protocol):
    def list_rows(self) -> tuple[DashboardDataRowDTO, ...]: ...
