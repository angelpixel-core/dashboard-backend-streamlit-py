from dashboard.application.dto import DashboardDataRowDTO
from dashboard.application.ports import GetDashboardDataRequest
from dashboard.application.use_cases import GetDashboardDataUseCase


class FakeDashboardDataReader:
    def __init__(self, rows: tuple[DashboardDataRowDTO, ...]) -> None:
        self._rows = rows

    def list_rows(self) -> tuple[DashboardDataRowDTO, ...]:
        return self._rows


def _sample_rows() -> tuple[DashboardDataRowDTO, ...]:
    return (
        DashboardDataRowDTO(
            month="Enero",
            sales=45000,
            customers=120,
            region="Norte",
        ),
        DashboardDataRowDTO(
            month="Febrero",
            sales=52000,
            customers=145,
            region="Sur",
        ),
        DashboardDataRowDTO(
            month="Febrero",
            sales=50000,
            customers=140,
            region="Centro",
        ),
        DashboardDataRowDTO(
            month="Marzo",
            sales=48000,
            customers=133,
            region="Norte",
        ),
        DashboardDataRowDTO(
            month="Abril",
            sales=61000,
            customers=167,
            region="Centro",
        ),
        DashboardDataRowDTO(
            month="Mayo",
            sales=58000,
            customers=156,
            region="Sur",
        ),
    )


def test_get_dashboard_data_without_filters_returns_all_rows() -> None:
    use_case = GetDashboardDataUseCase(
        reader=FakeDashboardDataReader(_sample_rows()),
    )

    result = use_case.execute(GetDashboardDataRequest())

    assert len(result.rows) == 6
    assert {row.month for row in result.rows} == {
        "Enero",
        "Febrero",
        "Marzo",
        "Abril",
        "Mayo",
    }


def test_get_dashboard_data_filters_by_month() -> None:
    use_case = GetDashboardDataUseCase(
        reader=FakeDashboardDataReader(_sample_rows()),
    )

    result = use_case.execute(GetDashboardDataRequest(month="Febrero"))

    assert len(result.rows) == 2
    assert all(row.month == "Febrero" for row in result.rows)


def test_get_dashboard_data_filters_by_region() -> None:
    use_case = GetDashboardDataUseCase(
        reader=FakeDashboardDataReader(_sample_rows()),
    )

    result = use_case.execute(
        GetDashboardDataRequest(regions=("Centro",)),
    )

    assert len(result.rows) == 2
    assert all(row.region == "Centro" for row in result.rows)


def test_get_dashboard_data_combines_month_and_regions() -> None:
    use_case = GetDashboardDataUseCase(
        reader=FakeDashboardDataReader(_sample_rows()),
    )

    result = use_case.execute(
        GetDashboardDataRequest(
            month="Febrero",
            regions=("Centro", "Sur"),
        ),
    )

    assert len(result.rows) == 2
    assert {row.region for row in result.rows} == {"Centro", "Sur"}
    assert all(row.month == "Febrero" for row in result.rows)


def test_get_dashboard_data_does_not_filter_when_regions_is_empty_or_none() -> None:
    use_case = GetDashboardDataUseCase(
        reader=FakeDashboardDataReader(_sample_rows()),
    )

    result_with_empty_regions = use_case.execute(
        GetDashboardDataRequest(regions=()),
    )
    result_with_none_regions = use_case.execute(
        GetDashboardDataRequest(regions=None),
    )

    assert len(result_with_empty_regions.rows) == 6
    assert len(result_with_none_regions.rows) == 6


def test_get_dashboard_data_treats_todos_month_as_no_filter() -> None:
    use_case = GetDashboardDataUseCase(
        reader=FakeDashboardDataReader(_sample_rows()),
    )

    result = use_case.execute(GetDashboardDataRequest(month="Todos"))

    assert len(result.rows) == 6
