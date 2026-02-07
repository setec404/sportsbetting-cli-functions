"""Odds conversion functions"""
from decimal import Decimal, getcontext
from typing import List, Union

# Set high precision for calculations
getcontext().prec = 28


def us_to_decimal(us_odds: Union[int, float, Decimal]) -> Decimal:
    """
    Convert US-style odds to decimal odds.

    Args:
        us_odds: US-style odds (e.g., -110, +150)

    Returns:
        Decimal odds

    Examples:
        >>> us_to_decimal(-110)
        Decimal('1.909090909')
        >>> us_to_decimal(150)
        Decimal('2.5')
    """
    us_odds = Decimal(str(us_odds))

    if us_odds > 0:
        return (us_odds / Decimal('100')) + Decimal('1')
    else:
        return (Decimal('100') / abs(us_odds)) + Decimal('1')


def us_to_decimal_parlay(us_odds_list: List[Union[int, float, Decimal]]) -> Decimal:
    """
    Convert multiple US odds to parlay decimal odds.

    Args:
        us_odds_list: List of US-style odds

    Returns:
        Parlay decimal odds (product of all individual decimal odds)

    Examples:
        >>> us_to_decimal_parlay([-110, -110, -110])
        Decimal('6.950506668')
    """
    result = Decimal('1')

    for odds in us_odds_list:
        decimal_odds = us_to_decimal(odds)
        result *= decimal_odds

    return result


def decimal_to_us(decimal_odds: Union[float, Decimal]) -> Decimal:
    """
    Convert decimal odds to US-style odds.

    Args:
        decimal_odds: Decimal odds (e.g., 1.909090909, 2.5)

    Returns:
        US-style odds

    Examples:
        >>> decimal_to_us(1.909090909)
        Decimal('-110')
        >>> decimal_to_us(2.5)
        Decimal('150')
    """
    decimal_odds = Decimal(str(decimal_odds))

    if decimal_odds >= Decimal('2'):
        return (decimal_odds - Decimal('1')) * Decimal('100')
    else:
        return Decimal('-100') / (decimal_odds - Decimal('1'))


def us_to_parlay(us_odds_list: List[Union[int, float, Decimal]]) -> Decimal:
    """
    Convert multiple US odds to parlay US odds.

    Args:
        us_odds_list: List of US-style odds

    Returns:
        Parlay US odds

    Examples:
        >>> us_to_parlay([-110, -110, -110])
        Decimal('595.046')
    """
    # First get the parlay decimal odds
    parlay_decimal = us_to_decimal_parlay(us_odds_list)

    # Then convert back to US odds
    return decimal_to_us(parlay_decimal)
