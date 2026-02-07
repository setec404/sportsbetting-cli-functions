"""Utility functions"""
from decimal import Decimal
from typing import Union
import math


def invlg(x: Union[int, float, Decimal]) -> Decimal:
    """
    Calculate the inverse logit function.

    invlg(x) = Exp(x) / (1 + Exp(x))

    Also known as the logistic function or sigmoid function.

    Args:
        x: Input value

    Returns:
        Result of inverse logit function (between 0 and 1)

    Examples:
        >>> invlg(0)
        Decimal('0.5')
        >>> invlg(1)
        Decimal('0.731...')
        >>> invlg(-1)
        Decimal('0.268...')
    """
    x = Decimal(str(x))

    # Calculate exp(x) / (1 + exp(x))
    # For numerical stability, use different formulas for positive and negative x
    # When x is large positive, exp(x) can overflow
    # When x is large negative, exp(x) approaches 0

    if x >= 0:
        # For x >= 0: invlg(x) = 1 / (1 + exp(-x))
        exp_neg_x = Decimal(str(math.exp(float(-x))))
        return Decimal('1') / (Decimal('1') + exp_neg_x)
    else:
        # For x < 0: invlg(x) = exp(x) / (1 + exp(x))
        exp_x = Decimal(str(math.exp(float(x))))
        return exp_x / (Decimal('1') + exp_x)
