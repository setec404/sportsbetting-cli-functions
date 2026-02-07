"""Hold calculation functions"""
from decimal import Decimal
from typing import List, Union
from sbcli.core.probability import us_to_probability, decimal_to_probability


def us_to_hold(us_odds_list: List[Union[int, float, Decimal]]) -> Decimal:
    """
    Calculate theoretical hold from a list of US odds.

    Hold is the bookmaker's edge, calculated as the sum of implied probabilities minus 1.

    Args:
        us_odds_list: List of US-style odds (e.g., [-110, -110])

    Returns:
        Theoretical hold (as decimal, e.g., 0.04545 for 4.545%)

    Examples:
        >>> us_to_hold([-110, -110])
        Decimal('0.04545454545...')
    """
    total_prob = Decimal('0')

    for odds in us_odds_list:
        prob = us_to_probability(odds)
        total_prob += prob

    # Hold = sum of probabilities - 1
    return total_prob - Decimal('1')


def decimal_to_hold(decimal_odds_list: List[Union[float, Decimal]]) -> Decimal:
    """
    Calculate theoretical hold from a list of decimal odds.

    Hold is the bookmaker's edge, calculated as the sum of implied probabilities minus 1.

    Args:
        decimal_odds_list: List of decimal odds (e.g., [1.909090909, 1.909090909])

    Returns:
        Theoretical hold (as decimal, e.g., 0.04545 for 4.545%)

    Examples:
        >>> decimal_to_hold([1.909090909, 1.909090909])
        Decimal('0.04545454545...')
    """
    total_prob = Decimal('0')

    for odds in decimal_odds_list:
        prob = decimal_to_probability(odds)
        total_prob += prob

    # Hold = sum of probabilities - 1
    return total_prob - Decimal('1')
