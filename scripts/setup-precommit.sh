#!/bin/bash
# Quick setup script for pre-commit

echo "🚀 Setting up pre-commit hooks..."
echo ""

echo "📦 Installing pre-commit..."
uv add --group dev pre-commit

echo ""
echo "🔧 Installing pre-commit hooks..."
uv run pre-commit install

echo ""
echo "🧪 Running pre-commit on all files (first run may be slow)..."
uv run pre-commit run --all-files

echo ""
echo "✅ Pre-commit setup complete!"
echo ""
echo "📝 Usage:"
echo "  - Hooks run automatically on 'git commit'"
echo "  - Run manually: 'uv run pre-commit run --all-files'"
echo "  - Update hooks: 'uv run pre-commit autoupdate'"
echo "  - Skip hooks: 'git commit --no-verify' (not recommended!)"
echo ""
echo "🎉 Happy coding!"
