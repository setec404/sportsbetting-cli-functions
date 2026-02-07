"""Exchange odds conversion functions"""
from decimal import Decimal
from typing import List, Union
from sbcli.core.converters import decimal_to_us, us_to_decimal
from sbcli.core.probability import us_to_probability, decimal_to_probability


def exch_to_us(
    us_exchange_odds: Union[int, float, Decimal],
    commission: Union[float, Decimal] = Decimal('0.02')
) -> Decimal:
    """
    Calculate sportsbook equivalent US odds from exchange odds and commission.

    On exchanges, you pay commission on winnings. This converts exchange odds
    to equivalent sportsbook odds after accounting for commission.

    Args:
        us_exchange_odds: US-style exchange odds
        commission: Commission rate (default: 0.02 for 2%)

    Returns:
        Equivalent US sportsbook odds

    Examples:
        >>> exch_to_us(-110, 0.01)
        Decimal('-111.11')
    """
    commission = Decimal(str(commission))

    # Convert to decimal odds
    decimal_exchange_odds = us_to_decimal(us_exchange_odds)

    # Calculate equivalent decimal odds after commission
    # Net win = (decimal_odds - 1) * (1 - commission)
    # Equivalent odds = 1 + net_win = 1 + (decimal_odds - 1) * (1 - commission)
    equivalent_decimal = Decimal('1') + (decimal_exchange_odds - Decimal('1')) * (Decimal('1') - commission)

    # Convert back to US odds
    return decimal_to_us(equivalent_decimal)


def exch_to_dec(
    decimal_exchange_odds: Union[float, Decimal],
    commission: Union[float, Decimal] = Decimal('0.02')
) -> Decimal:
    """
    Calculate sportsbook equivalent decimal odds from exchange odds and commission.

    Args:
        decimal_exchange_odds: Decimal exchange odds
        commission: Commission rate (default: 0.02 for 2%)

    Returns:
        Equivalent decimal sportsbook odds

    Examples:
        >>> exch_to_dec(1.909090909, 0.02)
        Decimal('1.890909091')
    """
    decimal_exchange_odds = Decimal(str(decimal_exchange_odds))
    commission = Decimal(str(commission))

    # Equivalent odds = 1 + (decimal_odds - 1) * (1 - commission)
    return Decimal('1') + (decimal_exchange_odds - Decimal('1')) * (Decimal('1') - commission)


# Alias: E2S is shortcut to Exch2US
def e2s(
    us_exchange_odds: Union[int, float, Decimal],
    commission: Union[float, Decimal] = Decimal('0.02')
) -> Decimal:
    """
    Shortcut to exch_to_us (Exchange to Sportsbook).

    Args:
        us_exchange_odds: US-style exchange odds
        commission: Commission rate (default: 0.02 for 2%)

    Returns:
        Equivalent US sportsbook odds
    """
    return exch_to_us(us_exchange_odds, commission)


def exch_us_to_hold(
    us_odds_list: List[Union[int, float, Decimal]],
    commission: Union[float, Decimal]
) -> Decimal:
    """
    Calculate theoretical hold including exchange commission.

    Args:
        us_odds_list: List of US-style odds
        commission: Commission rate

    Returns:
        Theoretical hold (as decimal)

    Examples:
        >>> exch_us_to_hold([-102, -102], 0.02)
        Decimal('0.01961')  # ~1.961%
    """
    commission = Decimal(str(commission))

    # Convert each odds to probability, accounting for commission
    total_prob = Decimal('0')

    for odds in us_odds_list:
        # Get decimal odds
        decimal_odds = us_to_decimal(odds)

        # Apply commission to get equivalent odds
        equivalent_decimal = exch_to_dec(decimal_odds, commission)

        # Get implied probability from equivalent odds
        prob = decimal_to_probability(equivalent_decimal)
        total_prob += prob

    # Hold = sum of probabilities - 1
    return total_prob - Decimal('1')


def exch_dec_to_hold(
    decimal_odds_list: List[Union[float, Decimal]],
    commission: Union[float, Decimal]
) -> Decimal:
    """
    Calculate theoretical hold including exchange commission.

    Args:
        decimal_odds_list: List of decimal odds
        commission: Commission rate

    Returns:
        Theoretical hold (as decimal)

    Examples:
        >>> exch_dec_to_hold([1.98, 1.98], 0.02)
        Decimal('0.01961')  # ~1.961%
    """
    commission = Decimal(str(commission))

    # Convert each odds to probability, accounting for commission
    total_prob = Decimal('0')

    for odds in decimal_odds_list:
        # Apply commission to get equivalent odds
        equivalent_decimal = exch_to_dec(odds, commission)

        # Get implied probability from equivalent odds
        prob = decimal_to_probability(equivalent_decimal)
        total_prob += prob

    # Hold = sum of probabilities - 1
    return total_prob - Decimal('1')


def mb_to_us(
    us_mb_odds: Union[int, float, Decimal],
    commission: Union[float, Decimal] = Decimal('0.01')
) -> Decimal:
    """
    Calculate sportsbook equivalent US odds from Matchbook exchange odds.

    Matchbook uses a different commission structure: commission is charged
    on the lesser of risk or win, regardless of outcome. This effectively
    increases the risk amount.

    Args:
        us_mb_odds: US-style Matchbook odds
        commission: Commission rate (default: 0.01 for 1%)

    Returns:
        Equivalent US sportsbook odds

    Examples:
        >>> mb_to_us(-110, 0.01)
        Decimal('-112.12')
    """
    us_mb_odds = Decimal(str(us_mb_odds))
    commission = Decimal(str(commission))

    # Convert to decimal odds
    decimal_mb_odds = us_to_decimal(us_mb_odds)

    # For Matchbook, commission is on min(risk, win) regardless of outcome
    # This effectively increases the risk
    # Risk = 1, Win = (decimal_odds - 1)

    win_amount = decimal_mb_odds - Decimal('1')

    # Commission is on min(risk, win) = min(1, win_amount)
    commission_amount = commission * min(Decimal('1'), win_amount)

    # Effective risk = risk + commission
    effective_risk = Decimal('1') + commission_amount

    # Equivalent decimal odds = (risk + win) / effective_risk = decimal_odds / effective_risk
    equivalent_decimal = decimal_mb_odds / effective_risk

    return decimal_to_us(equivalent_decimal)


def mb_to_dec(
    decimal_mb_odds: Union[float, Decimal],
    commission: Union[float, Decimal] = Decimal('0.01')
) -> Decimal:
    """
    Calculate sportsbook equivalent decimal odds from Matchbook exchange odds.

    Args:
        decimal_mb_odds: Decimal Matchbook odds
        commission: Commission rate (default: 0.01 for 1%)

    Returns:
        Equivalent decimal sportsbook odds

    Examples:
        >>> mb_to_dec(1.909090909, 0.01)
        Decimal('1.891919...')
    """
    decimal_mb_odds = Decimal(str(decimal_mb_odds))
    commission = Decimal(str(commission))

    # Risk = 1, Win = (decimal_odds - 1)
    win_amount = decimal_mb_odds - Decimal('1')

    # Commission is on min(risk, win) = min(1, win_amount)
    commission_amount = commission * min(Decimal('1'), win_amount)

    # Effective risk = risk + commission
    effective_risk = Decimal('1') + commission_amount

    # Equivalent decimal odds = decimal_odds / effective_risk
    return decimal_mb_odds / effective_risk
