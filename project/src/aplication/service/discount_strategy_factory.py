"""Factory Method para seleção e instanciação de estratégias de desconto."""

from enum import Enum
from typing import Callable

from src.aplication.service.strategies.bundle_for_amount_strategy import (
    BundleForAmountStrategy,
)
from src.aplication.service.strategies.combo_discount_strategy import (
    ComboDiscountStrategy,
)
from src.aplication.service.strategies.percentage_discount_strategy import (
    PercentageDiscountStrategy,
)
from src.aplication.service.strategies.three_for_two_strategy import ThreeForTwoStrategy
from src.domain.entities.product import Product
from src.domain.interfaces.discount_strategy import DiscountStrategy


class OfferType(Enum):
    """Tipos de promoções suportadas pelo sistema."""

    THREE_FOR_TWO = 1
    TEN_PERCENT_DISCOUNT = 2
    TWO_FOR_AMOUNT = 3
    FIVE_FOR_AMOUNT = 4
    COMBO_TEN_PERCENT = 5


StrategyCreator = Callable[[tuple[Product, ...], float], DiscountStrategy]


def _require_single_product(products: tuple[Product, ...]) -> Product:
    if len(products) != 1:
        raise ValueError("Esta oferta exige exatamente 1 produto.")
    return products[0]


class DiscountStrategyFactory:
    """Fábrica responsável por criar a DiscountStrategy adequada ao OfferType."""

    _CREATORS: dict[OfferType, StrategyCreator] = {
        OfferType.THREE_FOR_TWO: lambda products, _arg: ThreeForTwoStrategy(
            _require_single_product(products)
        ),
        OfferType.TEN_PERCENT_DISCOUNT: (
            lambda products, _arg: PercentageDiscountStrategy(
                _require_single_product(products), 10.0
            )
        ),
        OfferType.TWO_FOR_AMOUNT: lambda products, arg: BundleForAmountStrategy(
            _require_single_product(products), bundle_size=2, bundle_price=arg
        ),
        OfferType.FIVE_FOR_AMOUNT: (
            lambda products, arg: BundleForAmountStrategy(
                _require_single_product(products),
                bundle_size=5,
                bundle_price=arg,
            )
        ),
        OfferType.COMBO_TEN_PERCENT: lambda products, arg: ComboDiscountStrategy(
            products, percentage=arg if arg > 0 else 10.0
        ),
    }

    @classmethod
    def create_strategy(
        cls,
        offer_type: OfferType,
        products: tuple[Product, ...],
        argument: float = 0.0,
    ) -> DiscountStrategy:
        """Instancia a estratégia de desconto correspondente ao tipo de oferta."""
        creator = cls._CREATORS.get(offer_type)
        if creator is None:
            raise ValueError(f"Tipo de oferta não suportado: {offer_type}")
        return creator(products, argument)
