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
