"""Fixtures compartilhadas para a suíte de testes."""

import pytest

from tests.fakes.memory_catalog_repository import MemoryCatalogRepository
from tests.fakes.memory_offer_repository import MemoryOfferRepository


@pytest.fixture
def catalog() -> MemoryCatalogRepository:
    return MemoryCatalogRepository()


@pytest.fixture
def offer_gateway() -> MemoryOfferRepository:
    return MemoryOfferRepository()
