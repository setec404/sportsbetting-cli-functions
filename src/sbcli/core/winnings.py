"""Win/Loss calculation functions"""
from decimal import Decimal
from typing import Union


def us_to_win(us_odds: Union[int, float, Decimal], wager: Union[int, float, Decimal] = 1) -> Decimal:
    """
    Calculate potential win quantity from US odds and wager amount.

    Args:
        us_odds: US-style odds (e.g., -110, +150)
        wager: Wager quantity (default: 1)

    Returns:
        Potential win quantity

    Examples:
        >>> us_to_win(-120, 120)
        Decimal('100')
        >>> us_to_win(-110)
        Decimal('0.90909090909')
        >>> us_to_win(150, 100)
        Decimal('150')
    """
    us_odds = Decimal(str(us_odds))
    wager = Decimal(str(wager))

    if us_odds > 0:
        return (us_odds / Decimal('100')) * wager
    else:
        return (Decimal('100') / abs(us_odds)) * wager


def decimal_to_win(decimal_odds: Union[float, Decimal], wager: Union[int, float, Decimal] = 1) -> Decimal:
    """
    Calculate potential win quantity from decimal odds and wager amount.

    Args:
        decimal_odds: Decimal odds (e.g., 1.909090909, 2.5)
        wager: Wager quantity (default: 1)

    Returns:
        Potential win quantity

    Examples:
        >>> decimal_to_win(1.909090909, 110)
        Decimal('99.999999999')
        >>> decimal_to_win(2.5, 100)
        Decimal('150')
    """
    decimal_odds = Decimal(str(decimal_odds))
    wager = Decimal(str(wager))

    return (decimal_odds - Decimal('1')) * wager


def us_to_result(
    us_odds: Union[int, float, Decimal],
    wager: Union[int, float, Decimal] = 1,
    result: Union[str, int] = "WIN"
) -> Decimal:
    """
    Calculate actual result from US odds, wager amount, and outcome.

    Args:
        us_odds: US-style odds (e.g., -110, +150)
        wager: Wager quantity (default: 1)
        result: Result - "WIN"/"W"/1 for win, "LOSS"/"L"/-1 for loss, "PUSH"/"P"/0 for push

    Returns:
        Actual result (win amount for wins, negative wager for losses, 0 for push)

    Examples:
        >>> us_to_result(-120, 120, "PUSH")
        Decimal('0')
        >>> us_to_result(-110, 200, "Win")
        Decimal('181.81818181818')
        >>> us_to_result(-110, 100, "LOSS")
        Decimal('-100')
    """
    wager = Decimal(str(wager))

    # Normalize result
    if isinstance(result, str):
        result_upper = result.upper()
        if result_upper in ("WIN", "W"):
            result_type = "win"
        elif result_upper in ("LOSS", "L"):
            result_type = "loss"
        elif result_upper in ("PUSH", "P"):
            result_type = "push"
        else:
            result_type = "push"
    elif result == 1:
        result_type = "win"
    elif result == -1:
        result_type = "loss"
    else:
        result_type = "push"

    if result_type == "win":
        return us_to_win(us_odds, wager)
    elif result_type == "loss":
        return -wager
    else:  # push
        return Decimal('0')


def decimal_to_result(
    decimal_odds: Union[float, Decimal],
    wager: Union[int, float, Decimal] = 1,
    result: Union[str, int] = "WIN"
) -> Decimal:
    """
    Calculate actual result from decimal odds, wager amount, and outcome.

    Args:
        decimal_odds: Decimal odds (e.g., 1.909090909, 2.5)
        wager: Wager quantity (default: 1)
        result: Result - "WIN"/"W"/1 for win, "LOSS"/"L"/-1 for loss, "PUSH"/"P"/0 for push

    Returns:
        Actual result (win amount for wins, negative wager for losses, 0 for push)

    Examples:
        >>> decimal_to_result(1.909090909, 200, "Win")
        Decimal('181.8181818')
        >>> decimal_to_result(2.5, 100, "LOSS")
        Decimal('-100')
        >>> decimal_to_result(2.0, 100, "P")
        Decimal('0')
    """
    wager = Decimal(str(wager))

    # Normalize result
    if isinstance(result, str):
        result_upper = result.upper()
        if result_upper in ("WIN", "W"):
            result_type = "win"
        elif result_upper in ("LOSS", "L"):
            result_type = "loss"
        elif result_upper in ("PUSH", "P"):
            result_type = "push"
        else:
            result_type = "push"
    elif result == 1:
        result_type = "win"
    elif result == -1:
        result_type = "loss"
    else:
        result_type = "push"

    if result_type == "win":
        return decimal_to_win(decimal_odds, wager)
    elif result_type == "loss":
        return -wager
    else:  # push
        return Decimal('0')


def us_risk_to_win(us_odds: Union[int, float, Decimal], risk: Union[int, float, Decimal] = 1) -> Decimal:
    """
    Calculate win quantity from US odds and risk amount.

    This is identical to us_to_win but uses 'risk' terminology.
    Aliased as usr2w.

    Args:
        us_odds: US-style odds (e.g., -110, +150)
        risk: Risk quantity (default: 1)

    Returns:
        Potential win quantity

    Examples:
        >>> us_risk_to_win(-110, 22)
        Decimal('20')
    """
    return us_to_win(us_odds, risk)


# Alias
usr2w = us_risk_to_win


def us_win_to_risk(us_odds: Union[int, float, Decimal], win: Union[int, float, Decimal] = 1) -> Decimal:
    """
    Calculate required risk from US odds and desired win amount.

    Aliased as usw2r.

    Args:
        us_odds: US-style odds (e.g., -110, +150)
        win: Desired win quantity (default: 1)

    Returns:
        Required risk quantity

    Examples:
        >>> us_win_to_risk(-110, 20)
        Decimal('22')
    """
    us_odds = Decimal(str(us_odds))
    win = Decimal(str(win))

    if us_odds > 0:
        # Positive odds: risk = win / (odds / 100)
        return win / (us_odds / Decimal('100'))
    else:
        # Negative odds: risk = win / (100 / |odds|)
        return win / (Decimal('100') / abs(us_odds))


# Alias
usw2r = us_win_to_risk


def decimal_risk_to_win(decimal_odds: Union[float, Decimal], risk: Union[int, float, Decimal] = 1) -> Decimal:
    """
    Calculate win quantity from decimal odds and risk amount.

    This is identical to decimal_to_win but uses 'risk' terminology.
    Aliased as decr2w.

    Args:
        decimal_odds: Decimal odds (e.g., 1.909090909, 2.5)
        risk: Risk quantity (default: 1)

    Returns:
        Potential win quantity

    Examples:
        >>> decimal_risk_to_win(1.909090909, 22)
        Decimal('20')
    """
    return decimal_to_win(decimal_odds, risk)


# Alias
decr2w = decimal_risk_to_win


def decimal_win_to_risk(decimal_odds: Union[float, Decimal], win: Union[int, float, Decimal] = 1) -> Decimal:
    """
    Calculate required risk from decimal odds and desired win amount.

    Aliased as decw2r.

    Args:
        decimal_odds: Decimal odds (e.g., 1.909090909, 2.5)
        win: Desired win quantity (default: 1)

    Returns:
        Required risk quantity

    Examples:
        >>> decimal_win_to_risk(1.909090909, 20)
        Decimal('22')
    """
    decimal_odds = Decimal(str(decimal_odds))
    win = Decimal(str(win))

    # risk = win / (decimal_odds - 1)
    return win / (decimal_odds - Decimal('1'))


# Alias
decw2r = decimal_win_to_risk
