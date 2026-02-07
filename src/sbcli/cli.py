"""Command-line interface for sbcli"""
import sys
import click
from decimal import Decimal

from sbcli.core.converters import (
    us_to_decimal,
    us_to_decimal_parlay,
    decimal_to_us,
    us_to_parlay,
)
from sbcli.io.input_parser import parse_input
from sbcli.io.output_formatter import output_result


@click.group()
@click.version_option(version="0.1.0", prog_name="sbcli")
def cli() -> None:
    """Sports betting CLI calculator"""
    pass


@cli.command()
@click.argument('odds', type=float, required=False)
@click.option('--json', 'json_format', is_flag=True, help='Output as JSON')
def us2dec(odds: float, json_format: bool) -> None:
    """
    Convert US odds to decimal odds.

    If multiple odds are provided via stdin, calculates parlay odds.

    Examples:
        sbcli us2dec -110
        echo "-110 -110 -110" | sbcli us2dec
        sbcli us2dec -110 --json
    """
    if odds is None:
        if not sys.stdin.isatty():
            # Read from pipe/file
            input_data = sys.stdin.read()
            odds_list = parse_input(input_data)

            if len(odds_list) == 0:
                raise click.UsageError('No valid odds provided')
            elif len(odds_list) == 1:
                result = us_to_decimal(odds_list[0])
            else:
                result = us_to_decimal_parlay(odds_list)
        else:
            raise click.UsageError('Missing odds argument')
    else:
        result = us_to_decimal(odds)

    output_result(result, json_format)


@cli.command()
@click.argument('odds', type=float, nargs=-1)
@click.option('--json', 'json_format', is_flag=True, help='Output as JSON')
def us2par(odds: tuple, json_format: bool) -> None:
    """
    Convert US odds to parlay US odds.

    Examples:
        sbcli us2par -110 -110 -110
        echo "-110 -110 -110" | sbcli us2par
    """
    if not odds:
        if not sys.stdin.isatty():
            input_data = sys.stdin.read()
            odds_list = parse_input(input_data)
        else:
            raise click.UsageError('Missing odds arguments')
    else:
        odds_list = [Decimal(str(o)) for o in odds]

    if len(odds_list) < 2:
        raise click.UsageError('At least 2 odds required for parlay')

    result = us_to_parlay(odds_list)
    output_result(result, json_format)


@cli.command()
@click.argument('odds', type=float, required=False)
@click.option('--json', 'json_format', is_flag=True, help='Output as JSON')
def dec2us(odds: float, json_format: bool) -> None:
    """
    Convert decimal odds to US odds.

    Examples:
        sbcli dec2us 1.909090909
        echo "1.909090909" | sbcli dec2us
        sbcli dec2us 2.5 --json
    """
    if odds is None:
        if not sys.stdin.isatty():
            input_data = sys.stdin.read()
            odds_list = parse_input(input_data)

            if len(odds_list) == 0:
                raise click.UsageError('No valid odds provided')

            result = decimal_to_us(odds_list[0])
        else:
            raise click.UsageError('Missing odds argument')
    else:
        result = decimal_to_us(odds)

    output_result(result, json_format)


@cli.command()
def sbrver() -> None:
    """Display sbcli version"""
    click.echo("sbcli version 0.1.0")


if __name__ == '__main__':
    cli()
