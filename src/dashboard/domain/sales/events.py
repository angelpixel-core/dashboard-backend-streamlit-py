from dataclasses import dataclass


@dataclass(frozen=True)
class SalesAggregateCreated:
    aggregate_id: str
    currency: str


@dataclass(frozen=True)
class SalesLineAdded:
    aggregate_id: str
    sku: str
    units: int
