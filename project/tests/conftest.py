"""Fixtures compartilhadas para a suíte de testes."""

import pytest

from src.adapters.gateways.repositories.memory_catalog_repository import (
    MemoryCatalogRepository,
)
from src.adapters.gateways.repositories.memory_offer_repository import (
    MemoryOfferRepository,
)


@pytest.fixture
def catalog() -> MemoryCatalogRepository:
    return MemoryCatalogRepository()


@pytest.fixture
def offer_gateway() -> MemoryOfferRepository:
    return MemoryOfferRepository()
