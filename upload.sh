#!/bin/bash
# Quick upload script for sh0rtifier

echo "🚀 Uploading sh0rtifier to GitHub..."
echo ""

# Initialize git
git init

# Add all files
git add .

# Show what will be committed
echo "📦 Files to commit:"
git status --short
echo ""

# Commit
git commit -m "Initial commit: sh0rtifier v1.0.0

Features:
- Convert 16:9 videos to 9:16 YouTube Shorts format
- Automatic 60-second limit enforcement
- Speed adjustment for long videos
- Segment selection for precise cuts
- CLI and GUI interfaces
- Blur background effect
- Built with uv for fast dependency management
- Cross-platform support (Windows, macOS, Linux)"

# Add remote
git remote add origin https://github.com/sl0thm4n/sh0rtifier.git

# Set branch to main
git branch -M main

# Push
echo ""
echo "⬆️  Pushing to GitHub..."
git push -u origin main

# Create and push tag
echo ""
echo "🏷️  Creating release tag v1.0.0..."
git tag -a v1.0.0 -m "Release v1.0.0: Initial release

✨ Features:
- 16:9 to 9:16 video conversion
- 60-second limit enforcement
- Speed adjustment (auto-calculate or manual)
- Segment selection (extract specific parts)
- Blur background with fade effects
- Dual interface (CLI + GUI)
- Cross-platform executables

🛠️ Tech Stack:
- Python 3.9+
- MoviePy for video processing
- OpenCV for image processing
- tkinter for GUI
- uv for package management

📦 Install:
uv sync && uv run python src/gui.py"

git push origin v1.0.0

echo ""
echo "✅ Done!"
echo ""
echo "📍 Repository: https://github.com/sl0thm4n/sh0rtifier"
echo "🎉 Releases: https://github.com/sl0thm4n/sh0rtifier/releases"
echo "🤖 Actions: https://github.com/sl0thm4n/sh0rtifier/actions"
echo ""
echo "⏳ GitHub Actions will now build executables automatically!"
echo "   Check the Actions tab in a few minutes."
