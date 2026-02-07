"""Probability calculation functions"""
from decimal import Decimal
from typing import Union


def us_to_probability(us_odds: Union[int, float, Decimal]) -> Decimal:
    """
    Convert US-style odds to implied probability.

    Args:
        us_odds: US-style odds (e.g., -110, +150)

    Returns:
        Implied probability (as decimal, e.g., 0.5238 for 52.38%)

    Examples:
        >>> us_to_probability(100)
        Decimal('0.5')
        >>> us_to_probability(-110)
        Decimal('0.523809523809...')
    """
    us_odds = Decimal(str(us_odds))

    if us_odds > 0:
        # Underdog: prob = 100 / (odds + 100)
        return Decimal('100') / (us_odds + Decimal('100'))
    else:
        # Favorite: prob = |odds| / (|odds| + 100)
        return abs(us_odds) / (abs(us_odds) + Decimal('100'))


def decimal_to_probability(decimal_odds: Union[float, Decimal]) -> Decimal:
    """
    Convert decimal odds to implied probability.

    Args:
        decimal_odds: Decimal odds (e.g., 1.909090909, 2.0)

    Returns:
        Implied probability (as decimal, e.g., 0.5238 for 52.38%)

    Examples:
        >>> decimal_to_probability(2.0)
        Decimal('0.5')
        >>> decimal_to_probability(1.909090909)
        Decimal('0.523809523809...')
    """
    decimal_odds = Decimal(str(decimal_odds))

    # Probability = 1 / decimal_odds
    return Decimal('1') / decimal_odds
