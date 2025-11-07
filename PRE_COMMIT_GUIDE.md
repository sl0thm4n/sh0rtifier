# Pre-commit Setup Guide

## 🎯 What is pre-commit?

Pre-commit automatically runs checks **before** you commit code:
- ✅ Formats code with black
- ✅ Sorts imports with isort
- ✅ Lints with ruff (auto-fixes issues)
- ✅ Type checks with mypy
- ✅ Removes trailing whitespace
- ✅ Checks for large files, merge conflicts, etc.

**Result**: You can't commit broken code! 🎉

---

## 🚀 Installation

### Step 1: Install pre-commit
```bash
# Using pip
pip install pre-commit

# Or using uv
uv pip install pre-commit
```

### Step 2: Install hooks in your repo
```bash
cd sh0rtifier
pre-commit install
```

Done! Now pre-commit runs automatically on every `git commit`.

---

## 💡 Usage

### Automatic (on commit)
```bash
git add .
git commit -m "Your message"

# Pre-commit runs automatically:
# black...................................................Passed
# isort...................................................Passed
# ruff....................................................Passed
# mypy....................................................Passed
# ✅ Commit proceeds
```

### Manual (check all files)
```bash
# Run on all files
pre-commit run --all-files

# Run specific hook
pre-commit run black --all-files
pre-commit run ruff --all-files
```

### Skip hooks (emergency only!)
```bash
# Skip all hooks (not recommended!)
git commit -m "Emergency fix" --no-verify

# Better: fix issues first
uv run black src/ tests/
uv run isort src/ tests/
git commit -m "Fixed formatting"
```

---

## 🔧 What Each Hook Does

### black
- **What**: Auto-formats Python code
- **When**: On commit
- **Action**: Reformats files (you'll need to re-add them)
```bash
# Example
black............................Failed
- hook id: black
- files were modified by this hook

# Fix: re-add and commit again
git add .
git commit -m "Same message"
```

### isort
- **What**: Sorts and organizes imports
- **When**: On commit
- **Action**: Reorders imports (you'll need to re-add them)

### ruff
- **What**: Fast Python linter
- **When**: On commit
- **Action**: Auto-fixes issues when possible
- **Blocks**: Commit if unfixable issues found

### mypy
- **What**: Type checking
- **When**: On commit (only checks src/)
- **Action**: Validates type hints
- **Blocks**: Commit if type errors found

### Built-in hooks
- **trailing-whitespace**: Removes trailing spaces
- **end-of-file-fixer**: Ensures files end with newline
- **check-yaml**: Validates YAML files
- **check-large-files**: Blocks files >10MB
- **check-merge-conflict**: Blocks if merge markers found
- **check-toml**: Validates TOML files

---

## 🎨 Typical Workflow

### Good workflow (hooks pass):
```bash
# Make changes
vim src/core.py

# Commit
git add src/core.py
git commit -m "Add feature X"

# Pre-commit runs:
# black............................Passed ✅
# isort............................Passed ✅
# ruff.............................Passed ✅
# mypy.............................Passed ✅

# Commit succeeds!
```

### Workflow with auto-fixes:
```bash
# Make changes (forgot to format)
vim src/core.py

# Commit
git add src/core.py
git commit -m "Add feature X"

# Pre-commit runs:
# black............................Failed
# - hook id: black
# - files were modified by this hook
#
# reformatted src/core.py

# Re-add and commit
git add src/core.py
git commit -m "Add feature X"

# Now it passes!
# black............................Passed ✅
```

---

## 🛠️ Configuration

### Update hooks to latest versions
```bash
pre-commit autoupdate
```

### Customize in `.pre-commit-config.yaml`
```yaml
# Change black line length
- id: black
  args: ['--line-length=120']  # Changed from 100

# Skip mypy on tests
- id: mypy
  files: ^src/  # Only check src/
```

---

## 🚫 Bypass (Not Recommended)

### Temporarily disable
```bash
# Disable for current repo
pre-commit uninstall

# Re-enable
pre-commit install
```

### Skip for one commit
```bash
git commit --no-verify -m "Emergency"
```

**⚠️ Warning**: Only use `--no-verify` in emergencies!

---

## 🤔 Should You Use It?

### ✅ Pros:
- Catches issues **before** CI fails
- Saves time (no waiting for GitHub Actions)
- Ensures consistent code quality
- Auto-fixes most issues
- Can't accidentally commit bad code

### ❌ Cons:
- Adds ~2-5 seconds to each commit
- May need to re-add files after auto-fixes
- Learning curve for team members

### 💡 Recommendation:
**YES, use it!** The time saved from catching issues early far outweighs the minor delay.

---

## 📊 Comparison

### Without pre-commit:
```
1. Write code
2. git commit
3. git push
4. Wait 5 minutes for CI
5. CI fails (formatting issue)
6. Fix locally
7. git commit --amend
8. git push --force
9. Wait 5 minutes for CI again
❌ Total: ~15 minutes
```

### With pre-commit:
```
1. Write code
2. git commit
3. Pre-commit auto-fixes (3 seconds)
4. git add . && git commit
5. git push
6. CI passes immediately
✅ Total: ~1 minute
```

---

## 🎯 Integration with CI

Pre-commit and CI work together:
- **Pre-commit**: Fast local checks (catches 95% of issues)
- **CI**: Full test suite on all platforms

Best practice:
1. Use pre-commit locally (fast feedback)
2. CI runs full pytest suite (comprehensive)
3. Both use same tools (consistency)

---

## 📝 Quick Reference

```bash
# Install
pip install pre-commit
pre-commit install

# Run manually
pre-commit run --all-files

# Update hooks
pre-commit autoupdate

# Skip once
git commit --no-verify

# Uninstall
pre-commit uninstall
```

---

## 🎉 Ready to Go!

```bash
# One-time setup
pip install pre-commit
pre-commit install

# That's it! Now just commit normally
git add .
git commit -m "Your changes"
```

Pre-commit will take care of the rest! 🚀
