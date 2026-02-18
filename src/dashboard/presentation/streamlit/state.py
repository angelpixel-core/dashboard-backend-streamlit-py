from dataclasses import dataclass


@dataclass(frozen=True)
class DashboardState:
    aggregate_id: str = "sales-overview"
