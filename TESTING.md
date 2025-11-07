# Local Testing Guide

## 🧪 Running Tests Locally

### Install dev dependencies
```bash
uv sync --group dev
```

### Run all tests with all quality checks
```bash
uv run pytest
```
This runs:
- ✅ Unit tests
- ✅ Coverage report
- ✅ Black (formatting check)
- ✅ isort (import sorting check)
- ✅ mypy (type checking)
- ✅ ruff (linting)

### Run only unit tests (fast)
```bash
uv run pytest tests/ -v
```

### Run with coverage only
```bash
uv run pytest tests/ --cov=src --cov-report=html
# Open htmlcov/index.html to see coverage report
```

### Run specific test file
```bash
uv run pytest tests/test_core.py -v
```

### Run specific test
```bash
uv run pytest tests/test_core.py::TestVideoInfo::test_is_short_under_60 -v
```

## 🎨 Code Quality Tools

### Format code with black
```bash
uv run black src/ tests/
```

### Sort imports with isort
```bash
uv run isort src/ tests/
```

### Lint with ruff
```bash
# Check only
uv run ruff check src/ tests/

# Auto-fix
uv run ruff check --fix src/ tests/
```

### Type check with mypy
```bash
uv run mypy src/ --ignore-missing-imports
```

### Run all quality checks manually
```bash
uv run black src/ tests/
uv run isort src/ tests/
uv run ruff check --fix src/ tests/
uv run mypy src/
```

## 🚀 Pre-commit Workflow

Before committing:
```bash
# Format and fix
uv run black src/ tests/
uv run isort src/ tests/
uv run ruff check --fix src/ tests/

# Test everything
uv run pytest

# If all pass, commit!
git add .
git commit -m "Your message"
```

## 📊 Coverage Reports

### Terminal report
```bash
uv run pytest --cov=src --cov-report=term-missing
```

### HTML report (recommended)
```bash
uv run pytest --cov=src --cov-report=html
# Open htmlcov/index.html in browser
```

### XML report (for CI)
```bash
uv run pytest --cov=src --cov-report=xml
```

## 🐛 Debugging Tests

### Run with print statements
```bash
uv run pytest tests/ -s
```

### Run last failed tests only
```bash
uv run pytest --lf
```

### Stop on first failure
```bash
uv run pytest -x
```

### Run with verbose output
```bash
uv run pytest -vv
```

## 🎯 Test Markers

### Run only unit tests
```bash
uv run pytest -m unit
```

### Skip slow tests
```bash
uv run pytest -m "not slow"
```

### Run integration tests
```bash
uv run pytest -m integration
```

## 📝 Quick Reference

| Command | Description |
|---------|-------------|
| `uv run pytest` | Run all tests + quality checks |
| `uv run pytest tests/ -v` | Run tests only |
| `uv run pytest --lf` | Run last failed |
| `uv run pytest -x` | Stop on first fail |
| `uv run pytest -k test_name` | Run tests matching name |
| `uv run black src/ tests/` | Format code |
| `uv run isort src/ tests/` | Sort imports |
| `uv run ruff check --fix src/` | Lint and fix |
| `uv run mypy src/` | Type check |

## 🔧 Troubleshooting

### pytest-plugins not found
```bash
uv sync --group dev
```

### Cache issues
```bash
uv run pytest --cache-clear
```

### Import errors
```bash
# Make sure you're in project root
cd /path/to/sh0rtifier
uv sync --group dev
```

## 💡 Tips

1. **Use `--verbose` (-v)** to see individual test names
2. **Use `--exitfirst` (-x)** to stop on first failure
3. **Use `--last-failed` (--lf)** to rerun only failed tests
4. **Use `--collect-only`** to see what tests would run
5. **Use `-k pattern`** to run tests matching a pattern

---

**Happy Testing! 🎉**