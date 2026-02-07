"""Edge calculation functions"""
from decimal import Decimal
from typing import Union
from sbcli.core.probability import us_to_probability, decimal_to_probability
from sbcli.core.converters import decimal_to_us


def prob_us_to_edge(probability: Union[float, Decimal], us_odds: Union[int, float, Decimal]) -> Decimal:
    """
    Calculate edge from win probability and US odds.

    Edge = (probability * (win_amount / risk_amount)) - (1 - probability)
    Or simplified: Edge = (probability * decimal_odds) - 1

    Args:
        probability: True win probability (as decimal, e.g., 0.55 for 55%)
        us_odds: US-style odds (e.g., -110)

    Returns:
        Edge (as decimal, e.g., 0.05 for 5%)

    Examples:
        >>> prob_us_to_edge(0.55, -110)
        Decimal('0.05')
    """
    probability = Decimal(str(probability))

    # Get implied probability from odds
    implied_prob = us_to_probability(us_odds)

    # Calculate decimal odds from implied probability
    decimal_odds = Decimal('1') / implied_prob

    # Edge = (true_prob * decimal_odds) - 1
    edge = (probability * decimal_odds) - Decimal('1')

    return edge


def prob_dec_to_edge(probability: Union[float, Decimal], decimal_odds: Union[float, Decimal]) -> Decimal:
    """
    Calculate edge from win probability and decimal odds.

    Edge = (probability * decimal_odds) - 1

    Args:
        probability: True win probability (as decimal, e.g., 0.55 for 55%)
        decimal_odds: Decimal odds (e.g., 1.909090909)

    Returns:
        Edge (as decimal, e.g., 0.05 for 5%)

    Examples:
        >>> prob_dec_to_edge(0.55, 1.909090909)
        Decimal('0.05')
    """
    probability = Decimal(str(probability))
    decimal_odds = Decimal(str(decimal_odds))

    # Edge = (probability * decimal_odds) - 1
    edge = (probability * decimal_odds) - Decimal('1')

    return edge


def edge_us_to_prob(edge: Union[float, Decimal], us_odds: Union[int, float, Decimal]) -> Decimal:
    """
    Calculate win probability from edge and US odds.

    Rearranging: probability = (edge + 1) / decimal_odds

    Args:
        edge: Edge (as decimal, e.g., 0.05 for 5%)
        us_odds: US-style odds (e.g., -110)

    Returns:
        Win probability (as decimal, e.g., 0.55 for 55%)

    Examples:
        >>> edge_us_to_prob(0.05, -110)
        Decimal('0.55')
    """
    edge = Decimal(str(edge))

    # Get implied probability from odds
    implied_prob = us_to_probability(us_odds)

    # Calculate decimal odds from implied probability
    decimal_odds = Decimal('1') / implied_prob

    # Rearrange edge formula: probability = (edge + 1) / decimal_odds
    probability = (edge + Decimal('1')) / decimal_odds

    return probability


def edge_dec_to_prob(edge: Union[float, Decimal], decimal_odds: Union[float, Decimal]) -> Decimal:
    """
    Calculate win probability from edge and decimal odds.

    Rearranging: probability = (edge + 1) / decimal_odds

    Args:
        edge: Edge (as decimal, e.g., 0.05 for 5%)
        decimal_odds: Decimal odds (e.g., 1.909090909)

    Returns:
        Win probability (as decimal, e.g., 0.55 for 55%)

    Examples:
        >>> edge_dec_to_prob(0.05, 1.909090909)
        Decimal('0.55')
    """
    edge = Decimal(str(edge))
    decimal_odds = Decimal(str(decimal_odds))

    # Rearrange edge formula: probability = (edge + 1) / decimal_odds
    probability = (edge + Decimal('1')) / decimal_odds

    return probability


def prob_edge_to_us(probability: Union[float, Decimal], edge: Union[float, Decimal]) -> Decimal:
    """
    Calculate US odds from probability and edge.

    Rearranging: decimal_odds = (edge + 1) / probability
    Then convert to US odds.

    Args:
        probability: True win probability (as decimal, e.g., 0.55 for 55%)
        edge: Edge (as decimal, e.g., 0.05 for 5%)

    Returns:
        US-style odds

    Examples:
        >>> prob_edge_to_us(0.55, 0.05)
        Decimal('-110')
    """
    probability = Decimal(str(probability))
    edge = Decimal(str(edge))

    # Rearrange edge formula: decimal_odds = (edge + 1) / probability
    decimal_odds = (edge + Decimal('1')) / probability

    # Convert to US odds
    us_odds = decimal_to_us(decimal_odds)

    return us_odds


def prob_edge_to_dec(probability: Union[float, Decimal], edge: Union[float, Decimal]) -> Decimal:
    """
    Calculate decimal odds from probability and edge.

    Rearranging: decimal_odds = (edge + 1) / probability

    Args:
        probability: True win probability (as decimal, e.g., 0.55 for 55%)
        edge: Edge (as decimal, e.g., 0.05 for 5%)

    Returns:
        Decimal odds

    Examples:
        >>> prob_edge_to_dec(0.55, 0.05)
        Decimal('1.909090909')
    """
    probability = Decimal(str(probability))
    edge = Decimal(str(edge))

    # Rearrange edge formula: decimal_odds = (edge + 1) / probability
    decimal_odds = (edge + Decimal('1')) / probability

    return decimal_odds
