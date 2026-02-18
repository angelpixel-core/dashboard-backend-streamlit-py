from __future__ import annotations

import pytest

MARKERS = ("unit", "integration", "e2e")


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    for item in items:
        path_parts = set(item.path.parts)
        for marker in MARKERS:
            if marker in path_parts:
                item.add_marker(marker)
                break
