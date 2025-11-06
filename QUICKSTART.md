# Quick Start Guide

## For Users

### Windows

1. Download `sh0rtifier.exe` from [Releases](https://github.com/sl0thm4n/sh0rtifier/releases)
2. Double-click to run
3. No installation needed!

### macOS

1. Download `sh0rtifier.app` from [Releases](https://github.com/sl0thm4n/sh0rtifier/releases)
2. Right-click → Open (first time only, for security)
3. Use normally afterwards

### Linux

1. Download `sh0rtifier` from [Releases](https://github.com/sl0thm4n/sh0rtifier/releases)
2. Make executable: `chmod +x sh0rtifier`
3. Run: `./sh0rtifier`

## For Developers

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/sl0thm4n/sh0rtifier.git
cd sh0rtifier

# Install dependencies with uv
uv sync

# Install with development dependencies
uv sync --extra dev

# Run tests
uv run pytest tests/ -v

# Run CLI
uv run python src/cli.py --help

# Run GUI
uv run python src/gui.py
```

### Project Structure

```
shorts_maker_mvp/
├── src/
│   ├── core.py          # Core video processing logic
│   ├── cli.py           # Command-line interface
│   └── gui.py           # Graphical user interface
├── tests/
│   └── test_core.py     # Unit tests
├── .github/
│   └── workflows/
│       └── release.yml  # GitHub Actions for CI/CD
├── requirements.txt     # Dependencies
├── setup.py            # Package setup
├── README.md           # Main documentation
├── LICENSE             # MIT License
└── .gitignore          # Git ignore rules
```

### Running Tests

```bash
# Run all tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ --cov=src --cov-report=html

# Open coverage report
# Windows: start htmlcov/index.html
# macOS: open htmlcov/index.html
# Linux: xdg-open htmlcov/index.html
```

### Code Style

```bash
# Format code with Black
uv run black src/ tests/

# Check code style with flake8
uv run flake8 src/ tests/ --max-line-length=100
```

### Building Executables

#### Windows

```bash
pyinstaller --onefile --windowed --name "YouTubeShorsMaker" --icon=assets/icon.ico src/gui.py
```

#### macOS

```bash
pyinstaller --onefile --windowed --name "YouTubeShorsMaker" src/gui.py
```

#### Linux

```bash
pyinstaller --onefile --name "YouTubeShorsMaker" src/cli.py
```

### Creating a Release

1. Update version in `setup.py`
2. Commit changes
3. Create and push tag:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```
4. GitHub Actions will automatically build and create release

## Common Issues

### FFmpeg not found

**Solution:**
- Windows: Download from https://ffmpeg.org/ and add to PATH
- macOS: `brew install ffmpeg`
- Linux: `sudo apt-get install ffmpeg`

### Import errors

**Solution:**
```bash
# Sync all dependencies
uv sync

# Or add specific packages
uv add moviepy opencv-python numpy tqdm
```

### Slow video processing

**Solution:**
- Use SSD instead of HDD
- Close other applications
- Reduce video quality for testing

## Usage Examples

### CLI Examples

```bash
# Interactive mode
uv run python src/cli.py

# Quick conversion with auto-speed
uv run python src/cli.py --file video.mp4 --auto

# Custom speed
uv run python src/cli.py --file video.mp4 --speed 1.5

# Segment selection
uv run python src/cli.py --file video.mp4 --start 30 --duration 45

# Process folder
uv run python src/cli.py --input ./videos --output ./shorts
```

### Python API Examples

```python
from pathlib import Path
from core import (
    convert_to_shorts,
    auto_convert,
    convert_with_speed,
    ConversionOptions
)

# Auto conversion
auto_convert(
    video_path=Path("input.mp4"),
    output_path=Path("output.mp4")
)

# With custom speed
convert_with_speed(
    video_path=Path("input.mp4"),
    output_path=Path("output.mp4"),
    speed=1.5
)

# With custom options
options = ConversionOptions(
    speed=2.0,
    target_width=1080,
    target_height=1920,
    blur_strength=100
)

convert_to_shorts(
    video_path=Path("input.mp4"),
    output_path=Path("output.mp4"),
    options=options
)
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `pytest tests/`
5. Format code: `black src/ tests/`
6. Commit: `git commit -m 'Add amazing feature'`
7. Push: `git push origin feature/amazing-feature`
8. Open a Pull Request

## Need Help?

- 📖 [Full Documentation](README.md)
- 🐛 [Report Issues](https://github.com/sl0thm4n/sh0rtifier/issues)
- 💬 [Discussions](https://github.com/sl0thm4n/sh0rtifier/discussions)

---

Happy converting! 🎬
