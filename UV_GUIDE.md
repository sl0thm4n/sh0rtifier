# uv Usage Guide for sh0rtifier

This project uses **uv** - a fast Python package manager. Here's everything you need to know!

## Why uv?

- ⚡ **10-100x faster** than pip
- 🔒 **Deterministic** dependency resolution
- 📦 **Better dependency management**
- 🎯 **Simple commands**: `uv add`, `uv remove`, `uv sync`

## Installation

### Install uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip (if you really need to)
pip install uv
```

## Common Commands

### Initial Setup

```bash
# Clone the repo
git clone https://github.com/sl0thm4n/sh0rtifier.git
cd sh0rtifier

# Install all dependencies from pyproject.toml
uv sync

# Install with development dependencies
uv sync --extra dev
```

### Adding Dependencies

```bash
# Add a new runtime dependency
uv add moviepy

# Add multiple packages
uv add opencv-python numpy

# Add a development dependency
uv add --dev pytest black

# Add with version constraint
uv add "numpy>=1.24.0"
```

### Removing Dependencies

```bash
# Remove a package
uv remove package-name

# Remove a dev dependency
uv remove --dev pytest
```

### Running Scripts

```bash
# Run Python scripts with uv
uv run python src/cli.py

# Run with arguments
uv run python src/cli.py --file video.mp4 --auto

# Run GUI
uv run python src/gui.py

# Run tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ --cov=src

# Format code
uv run black src/ tests/

# Lint code
uv run flake8 src/ tests/
```

### Updating Dependencies

```bash
# Update all dependencies to latest compatible versions
uv sync --upgrade

# Update specific package
uv add --upgrade moviepy

# Check for outdated packages
uv pip list --outdated
```

### Python Version Management

```bash
# Install Python 3.11
uv python install 3.11

# Use specific Python version for project
uv python pin 3.11

# List installed Python versions
uv python list
```

## Project Workflow

### For Contributors

1. **Clone and setup:**
   ```bash
   git clone <repo-url>
   cd youtube-shorts-maker
   uv sync --extra dev
   ```

2. **Create a feature branch:**
   ```bash
   git checkout -b feature/my-feature
   ```

3. **Make changes and test:**
   ```bash
   uv run pytest tests/ -v
   uv run black src/ tests/
   uv run flake8 src/ tests/
   ```

4. **If you add new dependencies:**
   ```bash
   uv add package-name
   git add pyproject.toml uv.lock
   ```

5. **Commit and push:**
   ```bash
   git commit -m "Add feature"
   git push origin feature/my-feature
   ```

### For End Users (Running from Source)

```bash
# One-time setup
git clone <repo-url>
cd youtube-shorts-maker
uv sync

# Run the app
uv run python src/gui.py

# Or use CLI
uv run python src/cli.py --file video.mp4
```

## Comparison: pip vs uv

| Task | pip | uv |
|------|-----|-----|
| Install deps | `pip install -r requirements.txt` | `uv sync` |
| Add package | Edit requirements.txt + `pip install` | `uv add package` |
| Remove package | Edit requirements.txt + `pip uninstall` | `uv remove package` |
| Run script | `python script.py` | `uv run python script.py` |
| Install dev deps | `pip install -r requirements-dev.txt` | `uv sync --extra dev` |

## Troubleshooting

### "uv: command not found"

**Solution:** Install uv first:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then restart your terminal or run:
```bash
source ~/.bashrc  # or ~/.zshrc on macOS
```

### "No module named 'moviepy'"

**Solution:**
```bash
uv sync
```

### Dependencies not installing

**Solution:**
```bash
# Remove lock file and resync
rm uv.lock
uv sync
```

### Want to use pip anyway?

While we recommend uv, you can still use pip:
```bash
pip install -e .
```

But you'll miss out on uv's speed and features! 🚀

## Advanced Usage

### Virtual Environments

uv creates its own managed environment:
```bash
# Create and activate environment (done automatically with uv sync)
uv venv

# Activate manually if needed
# Unix/macOS:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate
```

### Lock Files

The `uv.lock` file ensures everyone has the same dependency versions:
```bash
# Generate/update lock file
uv lock

# Install from lock file (done by uv sync)
uv sync
```

### Scripts in pyproject.toml

We've defined convenience scripts:
```bash
# Run CLI (if installed)
sh0rtifier --help

# Run GUI (if installed)
sh0rtifier-gui
```

To install the package:
```bash
uv pip install -e .
```

## Best Practices

1. **Always commit `pyproject.toml` and `uv.lock`** - These ensure reproducible builds
2. **Use `uv sync`** after pulling changes - Keeps dependencies in sync
3. **Use `uv add`** instead of editing pyproject.toml manually
4. **Run tests before committing** - `uv run pytest tests/`
5. **Format code** - `uv run black src/ tests/` before committing

## Resources

- [uv Documentation](https://github.com/astral-sh/uv)
- [Python Packaging Guide](https://packaging.python.org/)
- [Project Pyproject.toml](./pyproject.toml)

---

**Quick Reference Card:**
```bash
uv sync              # Install all dependencies
uv add package       # Add a package
uv remove package    # Remove a package
uv run python file   # Run a Python script
uv sync --upgrade    # Update all dependencies
```
