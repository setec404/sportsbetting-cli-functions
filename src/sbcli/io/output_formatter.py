"""Output formatting utilities for sbcli"""
import json
from decimal import Decimal
from typing import Any, Union


def format_decimal(value: Decimal, precision: int = 9) -> str:
    """
    Format a Decimal value for output.

    Args:
        value: Decimal value to format
        precision: Number of decimal places

    Returns:
        Formatted string
    """
    # Remove trailing zeros but keep at least one decimal place
    formatted = f"{value:.{precision}f}".rstrip('0').rstrip('.')
    if '.' not in formatted:
        formatted += '.0'
    return formatted


def output_result(result: Any, json_format: bool = False) -> None:
    """
    Output result to stdout in the requested format.

    Args:
        result: Result to output (Decimal, list, dict, etc.)
        json_format: If True, output as JSON
    """
    if json_format:
        # Convert Decimals to floats for JSON serialization
        if isinstance(result, Decimal):
            output_data = {"result": float(result)}
        elif isinstance(result, list):
            output_data = {"result": [float(x) if isinstance(x, Decimal) else x for x in result]}
        elif isinstance(result, dict):
            output_data = {
                k: float(v) if isinstance(v, Decimal) else v
                for k, v in result.items()
            }
        else:
            output_data = {"result": result}

        print(json.dumps(output_data, indent=2))
    else:
        # Plain text output
        if isinstance(result, Decimal):
            print(format_decimal(result))
        elif isinstance(result, list):
            for item in result:
                if isinstance(item, Decimal):
                    print(format_decimal(item))
                else:
                    print(item)
        elif isinstance(result, dict):
            for key, value in result.items():
                if isinstance(value, Decimal):
                    print(f"{key}: {format_decimal(value)}")
                else:
                    print(f"{key}: {value}")
        else:
            print(result)
