# sh0rtifier

```
     _      ___       _   _  __ _
 ___| |__  / _ \ _ __| |_(_)/ _(_) ___ _ __
/ __| '_ \| | | | '__| __| | |_| |/ _ \ '__|
\__ \ | | | |_| | |  | |_| |  _| |  __/ |
|___/_| |_|\___/|_|   \__|_|_| |_|\___|_|

```

> Convert 16:9 videos to 9:16 YouTube Shorts with automatic 60-second limit enforcement

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/badge/package_manager-uv-orange)](https://github.com/astral-sh/uv)

---

## ✨ Features

- 🎬 **Smart Conversion** - 16:9 → 9:16 with beautiful blurred background
- ⏱️ **60-Second Enforcer** - Automatic handling for videos over the limit
- 🚀 **Speed Adjustment** - Auto-calculate optimal playback speed
- ✂️ **Segment Selection** - Pick the best part of your video
- 💻 **Dual Interface** - CLI for power users, GUI for everyone
- 🎨 **Professional Effects** - Blur background, fade transitions
- 🔊 **Audio Preserved** - Keep your sound with fade effects
- ⚡ **Fast & Light** - Built with uv for blazing-fast dependency management

## 🚀 Quick Start

### Using the App (No coding required)

Download the latest release for your platform:
- **Windows**: `sh0rtifier.exe`
- **macOS**: `sh0rtifier.app`
- **Linux**: `sh0rtifier` binary

[📥 Download from Releases](https://github.com/sl0thm4n/sh0rtifier/releases)

### Running from Source

```bash
# Install uv (if you don't have it)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and run
git clone https://github.com/sl0thm4n/sh0rtifier.git
cd sh0rtifier
uv sync
uv run python src/gui.py
```

## 📖 Usage

### GUI Mode (Easiest)

```bash
uv run python src/gui.py
```

1. Select your video file
2. Choose output folder
3. For 60+ second videos, pick your strategy:
   - **Speed Adjustment** (recommended) - Speeds up the video
   - **Segment Selection** - Extract a specific part
4. Click "Convert to Shorts"

### CLI Mode (Power Users)

```bash
# Interactive mode with file browser
uv run python src/cli.py

# Direct conversion with auto-speed
uv run python src/cli.py --file video.mp4 --auto

# Custom speed (1.5x)
uv run python src/cli.py --file video.mp4 --speed 1.5

# Extract 45 seconds starting at 30s
uv run python src/cli.py --file video.mp4 --start 30 --duration 45

# Batch process a folder
uv run python src/cli.py --input ./videos --output ./shorts
```

## 🎯 How It Works

### For Videos Under 60 Seconds
✅ Converts as-is → Perfect!

### For Videos Over 60 Seconds
Choose your approach:

**Option A: Speed Adjustment** (Recommended)
```
90-second video → 1.5x speed → 60-second output
```
- Maintains full content
- Natural playback
- Auto-calculated

**Option B: Segment Selection**
```
120-second video → Extract 30s-75s → 45-second output
```
- Highlight the best moments
- Precise control
- Perfect for long content

## 🛠️ Command Reference

```bash
# Installation
uv sync                          # Install dependencies
uv sync --extra dev              # Include dev tools

# Running
uv run python src/gui.py         # GUI interface
uv run python src/cli.py         # CLI interface

# Development
uv run pytest tests/ -v          # Run tests
uv run black src/ tests/         # Format code
uv run flake8 src/ tests/        # Lint code

# Package Management
uv add <package>                 # Add dependency
uv remove <package>              # Remove dependency
uv sync --upgrade                # Update all deps
```

## 📊 Output Specs

| Property | Value |
|----------|-------|
| Resolution | 1080x1920 (9:16) |
| Frame Rate | 30 fps |
| Video Codec | H.264 |
| Audio Codec | AAC |
| Bitrate | 8000k |
| Max Duration | 60 seconds |

## 🎨 Examples

### Example 1: Quick Convert
```bash
uv run python src/cli.py --file myvideo.mp4 --auto
```

### Example 2: Tutorial Highlights
```bash
# Extract the 60-second highlight from a 10-minute tutorial
uv run python src/cli.py --file tutorial.mp4 --start 120 --duration 60
```

### Example 3: Batch Processing
```bash
# Convert all videos in a folder
uv run python src/cli.py --input ./raw_videos --output ./shorts
```

### Example 4: Custom Speed
```bash
# 75-second video at 1.25x = 60-second output
uv run python src/cli.py --file video.mp4 --speed 1.25
```

## 🤝 Contributing

Contributions are welcome! Please check out our [Contributing Guide](CONTRIBUTING.md).

```bash
# Fork & Clone
git clone https://github.com/sl0thm4n/sh0rtifier.git
cd sh0rtifier

# Setup development environment
uv sync --extra dev

# Make your changes
# ... edit files ...

# Test
uv run pytest tests/ -v
uv run black src/ tests/

# Commit & Push
git checkout -b feature/amazing-feature
git commit -m "Add amazing feature"
git push origin feature/amazing-feature
```

## 📝 License

MIT License - see [LICENSE](LICENSE) for details

## 🙏 Acknowledgments

Built with:
- [MoviePy](https://zulko.github.io/moviepy/) - Video editing
- [OpenCV](https://opencv.org/) - Image processing
- [uv](https://github.com/astral-sh/uv) - Fast Python package manager
- [tkinter](https://docs.python.org/3/library/tkinter.html) - GUI framework

## 💬 Support

- 🐛 [Report Issues](https://github.com/sl0thm4n/sh0rtifier/issues)
- 💡 [Feature Requests](https://github.com/sl0thm4n/sh0rtifier/discussions)
- 📖 [Documentation](https://github.com/sl0thm4n/sh0rtifier/wiki)

## 📚 More Resources

- [Quick Start Guide](QUICKSTART.md)
- [uv Usage Guide](UV_GUIDE.md)

---

<div align="center">

**Made with ❤️ for content creators**

*If you find sh0rtifier useful, please give it a ⭐ on GitHub!*

</div>
