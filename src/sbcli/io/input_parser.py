"""Input parsing utilities for sbcli"""
from typing import List, Union
from decimal import Decimal


def parse_input(input_data: str) -> List[Decimal]:
    """
    Parse input data from stdin or file.

    Supports:
    - Space-separated values
    - Comma-separated values
    - Newline-separated values
    - Comments (lines starting with #)
    - Mixed formats

    Args:
        input_data: Raw input string

    Returns:
        List of Decimal values
    """
    values = []

    for line in input_data.strip().split('\n'):
        # Remove comments
        if '#' in line:
            line = line[:line.index('#')]

        line = line.strip()
        if not line:
            continue

        # Split on both commas and spaces
        parts = line.replace(',', ' ').split()

        for part in parts:
            part = part.strip()
            if part:
                try:
                    values.append(Decimal(part))
                except (ValueError, TypeError):
                    # Skip invalid values
                    pass

    return values
