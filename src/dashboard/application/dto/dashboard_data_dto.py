from dataclasses import dataclass


@dataclass(frozen=True)
class DashboardDataRowDTO:
    month: str
    sales: int
    customers: int
    region: str


@dataclass(frozen=True)
class DashboardDataDTO:
    rows: tuple[DashboardDataRowDTO, ...]
