# sbcli - Sports Betting CLI Calculator
warning. vibe coded with Claude just wanted to see if it could take the input of 
https://www.sportsbookreview.com/forum/handicapper-think-tank/23552-simple-vba-sports-betting-functions-template-for-excel 
and make a cli version for terminal.

A Python CLI tool for sports betting calculations with 35+ functions for odds manipulation, probability calculations, edge analysis, and more.

## Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install package
pip install -e .

# Install development dependencies (optional)
pip install -r requirements-dev.txt
```

## Quick Start

```bash
# Convert US odds to decimal
sbcli us2dec -110
# Output: 1.909090909

# Calculate implied probability
sbcli us2prob -110
# Output: 0.523809524

# Calculate edge
sbcli probus2edge 0.55 -110
# Output: 0.05

# Pipe commands together
echo "-110" | sbcli us2dec | sbcli dec2prob
# Output: 0.523809524

Usage: sbcli [OPTIONS] COMMAND [ARGS]...

  Sports betting CLI calculator

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  dec2fair      Calculate fair value (zero-vig) decimal odds.
  dec2hold      Calculate theoretical hold from decimal odds.
  dec2prob      Convert decimal odds to implied probability.
  dec2real      Calculate zero-vig (real) probabilities from decimal odds.
  dec2res       Calculate actual result from decimal odds, wager, and...
  dec2us        Convert decimal odds to US odds.
  dec2win       Calculate potential win from decimal odds and wager.
  edgedec2prob  Calculate probability from edge and decimal odds.
  edgeus2prob   Calculate probability from edge and US odds.
  probdec2edge  Calculate edge from probability and decimal odds.
  probedge2dec  Calculate decimal odds from probability and edge.
  probedge2us   Calculate US odds from probability and edge.
  probus2edge   Calculate edge from probability and US odds.
  sbrver        Display sbcli version
  us2dec        Convert US odds to decimal odds.
  us2fair       Calculate fair value (zero-vig) US odds.
  us2hold       Calculate theoretical hold from US odds.
  us2par        Convert US odds to parlay US odds.
  us2prob       Convert US odds to implied probability.
  us2real       Calculate zero-vig (real) probabilities from US odds.
  us2res        Calculate actual result from US odds, wager, and outcome.
  us2win        Calculate potential win from US odds and wager.



```

## Features

- **35+ betting functions** covering odds conversion, probability, edge, hold, fair value, and more
- **Piping support** - chain commands together
- **File input** - process multiple odds from files
- **JSON output** - use `--json` flag for structured output
- **Tab completion** - for bash and zsh
- **High precision** - uses Python Decimal for Excel-matching accuracy
- **Exchange odds** - support for standard exchanges and Matchbook

## Development

```bash
# Run tests
pytest tests/ -v

# Format code
black src/ tests/

# Lint code
flake8 src/ tests/
```

## Project Structure

```
sportsbetting-cli-functions/
├── src/sbcli/
│   ├── cli.py              # Click CLI commands
│   ├── core/               # Core calculation functions
│   └── io/                 # Input/Output handling
└── tests/                  # Comprehensive test suite (126+ tests)
```

## Testing

All functions include comprehensive test coverage with 126+ tests:

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_converters.py -v
```

## License

MIT
