from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class SalesLineDTO:
    sku: str
    units: int
    revenue: Decimal


@dataclass(frozen=True)
class SalesDashboardDTO:
    aggregate_id: str
    currency: str
    total_units: int
    total_revenue: Decimal
    lines: tuple[SalesLineDTO, ...]
