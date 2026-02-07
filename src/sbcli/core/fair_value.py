"""Fair value calculation functions"""
from decimal import Decimal
from typing import List, Union, Dict
from sbcli.core.probability import us_to_probability, decimal_to_probability
from sbcli.core.converters import decimal_to_us


def us_to_real(us_odds_list: List[Union[int, float, Decimal]]) -> Dict[str, Decimal]:
    """
    Calculate zero-vig (real) probabilities from US odds.

    Returns a dict with:
    - 'probabilities': List of zero-vig probabilities
    - 'hold': The theoretical hold

    Args:
        us_odds_list: List of US-style odds (e.g., [-110, -110])

    Returns:
        Dict with 'probabilities' and 'hold' keys

    Examples:
        >>> us_to_real([-110, -110])
        {'probabilities': [Decimal('0.5'), Decimal('0.5')], 'hold': Decimal('0.04545...')}
    """
    # Get implied probabilities
    implied_probs = [us_to_probability(odds) for odds in us_odds_list]

    # Calculate total probability (should be > 1 if there's vig)
    total_prob = sum(implied_probs)

    # Calculate hold
    hold = total_prob - Decimal('1')

    # Normalize probabilities to remove vig
    real_probs = [prob / total_prob for prob in implied_probs]

    return {
        'probabilities': real_probs,
        'hold': hold
    }


def decimal_to_real(decimal_odds_list: List[Union[float, Decimal]]) -> Dict[str, Decimal]:
    """
    Calculate zero-vig (real) probabilities from decimal odds.

    Returns a dict with:
    - 'probabilities': List of zero-vig probabilities
    - 'hold': The theoretical hold

    Args:
        decimal_odds_list: List of decimal odds (e.g., [1.909090909, 1.909090909])

    Returns:
        Dict with 'probabilities' and 'hold' keys

    Examples:
        >>> decimal_to_real([1.909090909, 1.909090909])
        {'probabilities': [Decimal('0.5'), Decimal('0.5')], 'hold': Decimal('0.04545...')}
    """
    # Get implied probabilities
    implied_probs = [decimal_to_probability(odds) for odds in decimal_odds_list]

    # Calculate total probability (should be > 1 if there's vig)
    total_prob = sum(implied_probs)

    # Calculate hold
    hold = total_prob - Decimal('1')

    # Normalize probabilities to remove vig
    real_probs = [prob / total_prob for prob in implied_probs]

    return {
        'probabilities': real_probs,
        'hold': hold
    }


def us_to_fair(us_odds_list: List[Union[int, float, Decimal]]) -> Dict[str, Decimal]:
    """
    Calculate fair value (zero-vig) odds from US odds.

    Returns a dict with:
    - 'fair_odds': List of fair US odds
    - 'hold': The theoretical hold

    Args:
        us_odds_list: List of US-style odds (e.g., [-200, 176])

    Returns:
        Dict with 'fair_odds' and 'hold' keys

    Examples:
        >>> us_to_fair([-200, 176])
        {'fair_odds': [Decimal('-184'), Decimal('184')], 'hold': ...}
    """
    # Get real probabilities
    result = us_to_real(us_odds_list)
    real_probs = result['probabilities']
    hold = result['hold']

    # Convert real probabilities back to decimal odds, then to US odds
    fair_odds = []
    for prob in real_probs:
        # Decimal odds = 1 / probability
        decimal_odds = Decimal('1') / prob
        # Convert to US odds
        us_odds = decimal_to_us(decimal_odds)
        fair_odds.append(us_odds)

    return {
        'fair_odds': fair_odds,
        'hold': hold
    }


def decimal_to_fair(decimal_odds_list: List[Union[float, Decimal]]) -> Dict[str, Decimal]:
    """
    Calculate fair value (zero-vig) odds from decimal odds.

    Returns a dict with:
    - 'fair_odds': List of fair decimal odds
    - 'hold': The theoretical hold

    Args:
        decimal_odds_list: List of decimal odds

    Returns:
        Dict with 'fair_odds' and 'hold' keys

    Examples:
        >>> decimal_to_fair([1.5, 2.84])
        {'fair_odds': [Decimal('1.543...'), Decimal('2.756...')], 'hold': ...}
    """
    # Get real probabilities
    result = decimal_to_real(decimal_odds_list)
    real_probs = result['probabilities']
    hold = result['hold']

    # Convert real probabilities back to decimal odds
    fair_odds = []
    for prob in real_probs:
        # Decimal odds = 1 / probability
        decimal_odds = Decimal('1') / prob
        fair_odds.append(decimal_odds)

    return {
        'fair_odds': fair_odds,
        'hold': hold
    }
