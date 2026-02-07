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
from sbcli.core.winnings import (
    us_to_win,
    decimal_to_win,
    us_to_result,
    decimal_to_result,
)
from sbcli.core.probability import (
    us_to_probability,
    decimal_to_probability,
)
from sbcli.core.hold import (
    us_to_hold,
    decimal_to_hold,
)
from sbcli.core.fair_value import (
    us_to_real,
    decimal_to_real,
    us_to_fair,
    decimal_to_fair,
)
from sbcli.core.edge import (
    prob_us_to_edge,
    prob_dec_to_edge,
    edge_us_to_prob,
    edge_dec_to_prob,
    prob_edge_to_us,
    prob_edge_to_dec,
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


@cli.command()
@click.argument('odds', type=float, required=False)
@click.argument('wager', type=float, required=False, default=1)
@click.option('--json', 'json_format', is_flag=True, help='Output as JSON')
def us2win(odds: float, wager: float, json_format: bool) -> None:
    """
    Calculate potential win from US odds and wager.

    Examples:
        sbcli us2win -- -110 200
        sbcli us2win -- -120 120
        echo "-110 200" | sbcli us2win
    """
    if odds is None:
        if not sys.stdin.isatty():
            input_data = sys.stdin.read()
            values = parse_input(input_data)

            if len(values) == 0:
                raise click.UsageError('No valid odds provided')
            elif len(values) == 1:
                result = us_to_win(values[0], wager)
            else:
                result = us_to_win(values[0], values[1] if len(values) > 1 else 1)
        else:
            raise click.UsageError('Missing odds argument')
    else:
        result = us_to_win(odds, wager)

    output_result(result, json_format)


@cli.command()
@click.argument('odds', type=float, required=False)
@click.argument('wager', type=float, required=False, default=1)
@click.option('--json', 'json_format', is_flag=True, help='Output as JSON')
def dec2win(odds: float, wager: float, json_format: bool) -> None:
    """
    Calculate potential win from decimal odds and wager.

    Examples:
        sbcli dec2win 1.909090909 110
        sbcli dec2win 2.5 100
        echo "2.5 100" | sbcli dec2win
    """
    if odds is None:
        if not sys.stdin.isatty():
            input_data = sys.stdin.read()
            values = parse_input(input_data)

            if len(values) == 0:
                raise click.UsageError('No valid odds provided')
            elif len(values) == 1:
                result = decimal_to_win(values[0], wager)
            else:
                result = decimal_to_win(values[0], values[1] if len(values) > 1 else 1)
        else:
            raise click.UsageError('Missing odds argument')
    else:
        result = decimal_to_win(odds, wager)

    output_result(result, json_format)


@cli.command()
@click.argument('odds', type=float, required=False)
@click.argument('wager', type=float, required=False, default=1)
@click.argument('result_str', type=str, required=False, default="WIN")
@click.option('--json', 'json_format', is_flag=True, help='Output as JSON')
def us2res(odds: float, wager: float, result_str: str, json_format: bool) -> None:
    """
    Calculate actual result from US odds, wager, and outcome.

    Result can be: WIN/W/1, LOSS/L/-1, PUSH/P/0

    Examples:
        sbcli us2res -- -110 200 WIN
        sbcli us2res -- -120 120 PUSH
        echo "-110 200 L" | sbcli us2res
    """
    if odds is None:
        if not sys.stdin.isatty():
            input_data = sys.stdin.read()
            parts = input_data.strip().split()

            if len(parts) == 0:
                raise click.UsageError('No valid odds provided')

            odds_val = Decimal(parts[0])
            wager_val = Decimal(parts[1]) if len(parts) > 1 else Decimal('1')
            result_val = parts[2] if len(parts) > 2 else "WIN"

            result = us_to_result(odds_val, wager_val, result_val)
        else:
            raise click.UsageError('Missing odds argument')
    else:
        result = us_to_result(odds, wager, result_str)

    output_result(result, json_format)


@cli.command()
@click.argument('odds', type=float, required=False)
@click.argument('wager', type=float, required=False, default=1)
@click.argument('result_str', type=str, required=False, default="WIN")
@click.option('--json', 'json_format', is_flag=True, help='Output as JSON')
def dec2res(odds: float, wager: float, result_str: str, json_format: bool) -> None:
    """
    Calculate actual result from decimal odds, wager, and outcome.

    Result can be: WIN/W/1, LOSS/L/-1, PUSH/P/0

    Examples:
        sbcli dec2res 1.909090909 200 WIN
        sbcli dec2res 2.5 100 LOSS
        echo "2.0 100 P" | sbcli dec2res
    """
    if odds is None:
        if not sys.stdin.isatty():
            input_data = sys.stdin.read()
            parts = input_data.strip().split()

            if len(parts) == 0:
                raise click.UsageError('No valid odds provided')

            odds_val = Decimal(parts[0])
            wager_val = Decimal(parts[1]) if len(parts) > 1 else Decimal('1')
            result_val = parts[2] if len(parts) > 2 else "WIN"

            result = decimal_to_result(odds_val, wager_val, result_val)
        else:
            raise click.UsageError('Missing odds argument')
    else:
        result = decimal_to_result(odds, wager, result_str)

    output_result(result, json_format)


@cli.command()
@click.argument('odds', type=float, required=False)
@click.option('--json', 'json_format', is_flag=True, help='Output as JSON')
def us2prob(odds: float, json_format: bool) -> None:
    """
    Convert US odds to implied probability.

    Examples:
        sbcli us2prob 100
        sbcli us2prob -- -110
        echo "-110" | sbcli us2prob
    """
    if odds is None:
        if not sys.stdin.isatty():
            input_data = sys.stdin.read()
            odds_list = parse_input(input_data)

            if len(odds_list) == 0:
                raise click.UsageError('No valid odds provided')

            result = us_to_probability(odds_list[0])
        else:
            raise click.UsageError('Missing odds argument')
    else:
        result = us_to_probability(odds)

    output_result(result, json_format)


@cli.command()
@click.argument('odds', type=float, required=False)
@click.option('--json', 'json_format', is_flag=True, help='Output as JSON')
def dec2prob(odds: float, json_format: bool) -> None:
    """
    Convert decimal odds to implied probability.

    Examples:
        sbcli dec2prob 2.0
        sbcli dec2prob 1.909090909
        echo "2.5" | sbcli dec2prob
    """
    if odds is None:
        if not sys.stdin.isatty():
            input_data = sys.stdin.read()
            odds_list = parse_input(input_data)

            if len(odds_list) == 0:
                raise click.UsageError('No valid odds provided')

            result = decimal_to_probability(odds_list[0])
        else:
            raise click.UsageError('Missing odds argument')
    else:
        result = decimal_to_probability(odds)

    output_result(result, json_format)


@cli.command()
@click.argument('odds', type=float, nargs=-1)
@click.option('--json', 'json_format', is_flag=True, help='Output as JSON')
def us2hold(odds: tuple, json_format: bool) -> None:
    """
    Calculate theoretical hold from US odds.

    Examples:
        sbcli us2hold -- -110 -110
        echo "-110 -110" | sbcli us2hold
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
        raise click.UsageError('At least 2 odds required')

    result = us_to_hold(odds_list)
    output_result(result, json_format)


@cli.command()
@click.argument('odds', type=float, nargs=-1)
@click.option('--json', 'json_format', is_flag=True, help='Output as JSON')
def dec2hold(odds: tuple, json_format: bool) -> None:
    """
    Calculate theoretical hold from decimal odds.

    Examples:
        sbcli dec2hold 1.909090909 1.909090909
        echo "1.909090909 1.909090909" | sbcli dec2hold
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
        raise click.UsageError('At least 2 odds required')

    result = decimal_to_hold(odds_list)
    output_result(result, json_format)


@cli.command()
@click.argument('odds', type=float, nargs=-1)
@click.option('--json', 'json_format', is_flag=True, help='Output as JSON')
def us2real(odds: tuple, json_format: bool) -> None:
    """
    Calculate zero-vig (real) probabilities from US odds.

    Outputs probabilities followed by hold.

    Examples:
        sbcli us2real -- -110 -110
        echo "-110 -110" | sbcli us2real
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
        raise click.UsageError('At least 2 odds required')

    result_dict = us_to_real(odds_list)

    if json_format:
        output_result({
            'probabilities': result_dict['probabilities'],
            'hold': result_dict['hold']
        }, json_format)
    else:
        # Output probabilities first, then hold
        for prob in result_dict['probabilities']:
            output_result(prob, False)
        output_result(result_dict['hold'], False)


@cli.command()
@click.argument('odds', type=float, nargs=-1)
@click.option('--json', 'json_format', is_flag=True, help='Output as JSON')
def dec2real(odds: tuple, json_format: bool) -> None:
    """
    Calculate zero-vig (real) probabilities from decimal odds.

    Outputs probabilities followed by hold.

    Examples:
        sbcli dec2real 1.909090909 1.909090909
        echo "1.909090909 1.909090909" | sbcli dec2real
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
        raise click.UsageError('At least 2 odds required')

    result_dict = decimal_to_real(odds_list)

    if json_format:
        output_result({
            'probabilities': result_dict['probabilities'],
            'hold': result_dict['hold']
        }, json_format)
    else:
        # Output probabilities first, then hold
        for prob in result_dict['probabilities']:
            output_result(prob, False)
        output_result(result_dict['hold'], False)


@cli.command()
@click.argument('odds', type=float, nargs=-1)
@click.option('--json', 'json_format', is_flag=True, help='Output as JSON')
def us2fair(odds: tuple, json_format: bool) -> None:
    """
    Calculate fair value (zero-vig) US odds.

    Examples:
        sbcli us2fair -- -200 176
        echo "-200 176" | sbcli us2fair
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
        raise click.UsageError('At least 2 odds required')

    result_dict = us_to_fair(odds_list)

    if json_format:
        output_result({
            'fair_odds': result_dict['fair_odds'],
            'hold': result_dict['hold']
        }, json_format)
    else:
        # Output fair odds
        for fair_odd in result_dict['fair_odds']:
            output_result(fair_odd, False)


@cli.command()
@click.argument('odds', type=float, nargs=-1)
@click.option('--json', 'json_format', is_flag=True, help='Output as JSON')
def dec2fair(odds: tuple, json_format: bool) -> None:
    """
    Calculate fair value (zero-vig) decimal odds.

    Examples:
        sbcli dec2fair 1.5 2.84
        echo "1.5 2.84" | sbcli dec2fair
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
        raise click.UsageError('At least 2 odds required')

    result_dict = decimal_to_fair(odds_list)

    if json_format:
        output_result({
            'fair_odds': result_dict['fair_odds'],
            'hold': result_dict['hold']
        }, json_format)
    else:
        # Output fair odds
        for fair_odd in result_dict['fair_odds']:
            output_result(fair_odd, False)


@cli.command()
@click.argument('probability', type=float, required=False)
@click.argument('odds', type=float, required=False)
@click.option('--json', 'json_format', is_flag=True, help='Output as JSON')
def probus2edge(probability: float, odds: float, json_format: bool) -> None:
    """
    Calculate edge from probability and US odds.

    Examples:
        sbcli probus2edge 0.55 -- -110
        echo "0.55 -110" | sbcli probus2edge
    """
    if probability is None:
        if not sys.stdin.isatty():
            input_data = sys.stdin.read()
            values = parse_input(input_data)

            if len(values) < 2:
                raise click.UsageError('Need probability and odds')

            result = prob_us_to_edge(values[0], values[1])
        else:
            raise click.UsageError('Missing arguments')
    else:
        if odds is None:
            raise click.UsageError('Missing odds argument')
        result = prob_us_to_edge(probability, odds)

    output_result(result, json_format)


@cli.command()
@click.argument('probability', type=float, required=False)
@click.argument('odds', type=float, required=False)
@click.option('--json', 'json_format', is_flag=True, help='Output as JSON')
def probdec2edge(probability: float, odds: float, json_format: bool) -> None:
    """
    Calculate edge from probability and decimal odds.

    Examples:
        sbcli probdec2edge 0.55 1.909090909
        echo "0.55 1.909090909" | sbcli probdec2edge
    """
    if probability is None:
        if not sys.stdin.isatty():
            input_data = sys.stdin.read()
            values = parse_input(input_data)

            if len(values) < 2:
                raise click.UsageError('Need probability and odds')

            result = prob_dec_to_edge(values[0], values[1])
        else:
            raise click.UsageError('Missing arguments')
    else:
        if odds is None:
            raise click.UsageError('Missing odds argument')
        result = prob_dec_to_edge(probability, odds)

    output_result(result, json_format)


@cli.command()
@click.argument('edge', type=float, required=False)
@click.argument('odds', type=float, required=False)
@click.option('--json', 'json_format', is_flag=True, help='Output as JSON')
def edgeus2prob(edge: float, odds: float, json_format: bool) -> None:
    """
    Calculate probability from edge and US odds.

    Examples:
        sbcli edgeus2prob 0.05 -- -110
        echo "0.05 -110" | sbcli edgeus2prob
    """
    if edge is None:
        if not sys.stdin.isatty():
            input_data = sys.stdin.read()
            values = parse_input(input_data)

            if len(values) < 2:
                raise click.UsageError('Need edge and odds')

            result = edge_us_to_prob(values[0], values[1])
        else:
            raise click.UsageError('Missing arguments')
    else:
        if odds is None:
            raise click.UsageError('Missing odds argument')
        result = edge_us_to_prob(edge, odds)

    output_result(result, json_format)


@cli.command()
@click.argument('edge', type=float, required=False)
@click.argument('odds', type=float, required=False)
@click.option('--json', 'json_format', is_flag=True, help='Output as JSON')
def edgedec2prob(edge: float, odds: float, json_format: bool) -> None:
    """
    Calculate probability from edge and decimal odds.

    Examples:
        sbcli edgedec2prob 0.05 1.909090909
        echo "0.05 1.909090909" | sbcli edgedec2prob
    """
    if edge is None:
        if not sys.stdin.isatty():
            input_data = sys.stdin.read()
            values = parse_input(input_data)

            if len(values) < 2:
                raise click.UsageError('Need edge and odds')

            result = edge_dec_to_prob(values[0], values[1])
        else:
            raise click.UsageError('Missing arguments')
    else:
        if odds is None:
            raise click.UsageError('Missing odds argument')
        result = edge_dec_to_prob(edge, odds)

    output_result(result, json_format)


@cli.command()
@click.argument('probability', type=float, required=False)
@click.argument('edge', type=float, required=False)
@click.option('--json', 'json_format', is_flag=True, help='Output as JSON')
def probedge2us(probability: float, edge: float, json_format: bool) -> None:
    """
    Calculate US odds from probability and edge.

    Examples:
        sbcli probedge2us 0.55 0.05
        echo "0.55 0.05" | sbcli probedge2us
    """
    if probability is None:
        if not sys.stdin.isatty():
            input_data = sys.stdin.read()
            values = parse_input(input_data)

            if len(values) < 2:
                raise click.UsageError('Need probability and edge')

            result = prob_edge_to_us(values[0], values[1])
        else:
            raise click.UsageError('Missing arguments')
    else:
        if edge is None:
            raise click.UsageError('Missing edge argument')
        result = prob_edge_to_us(probability, edge)

    output_result(result, json_format)


@cli.command()
@click.argument('probability', type=float, required=False)
@click.argument('edge', type=float, required=False)
@click.option('--json', 'json_format', is_flag=True, help='Output as JSON')
def probedge2dec(probability: float, edge: float, json_format: bool) -> None:
    """
    Calculate decimal odds from probability and edge.

    Examples:
        sbcli probedge2dec 0.55 0.05
        echo "0.55 0.05" | sbcli probedge2dec
    """
    if probability is None:
        if not sys.stdin.isatty():
            input_data = sys.stdin.read()
            values = parse_input(input_data)

            if len(values) < 2:
                raise click.UsageError('Need probability and edge')

            result = prob_edge_to_dec(values[0], values[1])
        else:
            raise click.UsageError('Missing arguments')
    else:
        if edge is None:
            raise click.UsageError('Missing edge argument')
        result = prob_edge_to_dec(probability, edge)

    output_result(result, json_format)


if __name__ == '__main__':
    cli()
