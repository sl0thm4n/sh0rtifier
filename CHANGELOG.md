# Changelog

All notable changes to sh0rtifier project.

## [Unreleased]

### Added
- **Comprehensive CI/CD with pytest plugins** (PR CI workflow)
  - pytest-black for code formatting checks
  - pytest-isort for import sorting checks
  - pytest-mypy for type checking
  - pytest-ruff for linting (replaces flake8)
  - Multi-OS testing (Ubuntu, Windows, macOS)
  - Multi-Python version testing (3.9, 3.10, 3.11, 3.12)
  - Codecov integration for coverage reports
  - GitHub Actions workflow for PR validation

- **PyQt6 GUI** (replaces tkinter)
  - Modern cross-platform GUI using PyQt6
  - Better platform compatibility (no tkinter issues)
  - Dark theme with consistent styling
  - Native look and feel on all platforms
  - Improved scrolling with QScrollArea
  - Background threading for video processing
  - Progress bar with visible text
  - Custom styled buttons, radio buttons, and inputs
  - Menu bar with File and Help menus

- **Testing infrastructure**
  - Local testing guide (TESTING.md)
  - All pytest plugins configured in pyproject.toml
  - Coverage reporting (HTML, XML, terminal)
  - Quick reference for common test commands

### Changed
- **Test fixes**
  - Fixed edge case tests for 60-second videos
  - Changed `test_exactly_60_seconds_with_1x_speed` to accept 60s as valid
  - Changed `test_extreme_speed` to accept exactly 60s output
  - Rationale: YouTube Shorts allows up to 60 seconds (inclusive)

- **GUI complete rewrite**
  - Replaced tkinter with PyQt6
  - Changed from fixed size to resizable window (min 750x700)
  - Improved layout with proper scrolling
  - Added dark theme (#2b2b2b background)
  - Enhanced user feedback with styled progress bar
  - Better error handling and validation

- **Dependencies**
  - Added PyQt6>=6.6.0,<7.0.0
  - Updated pytest and plugins to latest versions
  - Pinned PyQt6 to 6.x for stability
  - Removed tkinter dependency (built-in, not in requirements)

- **Code quality setup**
  - Configured black with line-length=100
  - Configured isort with black profile
  - Configured ruff to replace flake8
  - Configured mypy for type checking
  - All tools run automatically with `uv run pytest`

### Fixed
- **Test validation logic**
  - Videos exactly 60 seconds are now considered valid
  - Fixed test expectations to match YouTube Shorts specs
  - All tests now pass (21 tests)

- **GUI bugs**
  - Fixed import errors (removed AlignmentMode, VideoProcessor)
  - Fixed scrolling issues with long content
  - Fixed text visibility in progress bar
  - Fixed inconsistent background colors
  - Fixed white gaps in UI

- **Code issues**
  - Removed unused imports
  - Fixed thread-based video processing
  - Used convert_to_shorts function directly instead of non-existent VideoProcessor class

### Removed
- tkinter GUI implementation
- pytest-flake8 (replaced by pytest-ruff)
- Unnecessary imports (AlignmentMode)

---

## Summary of Key Files Changed

### New Files
- `.github/workflows/pr-ci.yml` - PR CI workflow
- `TESTING.md` - Local testing guide

### Modified Files
- `tests/test_core.py` - Fixed 60-second edge case tests
- `src/gui.py` - Complete rewrite with PyQt6
- `pyproject.toml` - Added PyQt6, pytest plugins, updated configurations
- `requirements.txt` - Added PyQt6

### Configuration Updates
- `[tool.pytest.ini_options]` - Added all pytest plugin flags
- `[tool.black]` - Set line-length=100
- `[tool.isort]` - Configured for black compatibility
- `[tool.ruff]` - Configured linting rules
- `[tool.mypy]` - Configured type checking
- `[dependency-groups]` - Added all dev dependencies

---

## Testing

All changes have been tested and verified:
- ✅ Unit tests pass (21/21)
- ✅ Code formatting (black)
- ✅ Import sorting (isort)
- ✅ Linting (ruff)
- ✅ Type checking (mypy)
- ✅ GUI launches and functions correctly
- ✅ Video conversion works end-to-end

---

## Migration Notes

### For Users
- **GUI looks different**: Now uses PyQt6 with dark theme
- **Better compatibility**: Works on all platforms without tkinter issues
- **Same functionality**: All features work the same

### For Developers
- **New test command**: `uv run pytest` now runs all quality checks
- **CI/CD**: PRs automatically tested on all platforms
- **Dark theme**: GUI follows dark theme guidelines
- **Type hints**: mypy now checks types

---

## Next Steps (TODO)

- [ ] Update README with PyQt6 screenshots
- [ ] Add GitHub Actions badge to README
- [ ] Set up Codecov account
- [ ] Create release v1.0.0
- [ ] Test executables on all platforms

---

## Version Info

- **Current Version**: 0.1.0-dev0
- **Python**: 3.9+
- **Key Dependencies**: PyQt6 6.6+, MoviePy 1.0.3, OpenCV 4.8+
- **Testing**: pytest 8.4+ with plugins
