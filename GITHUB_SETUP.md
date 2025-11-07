# 🚀 GitHub Setup Instructions

## 📋 Repository Settings

### Basic Information
```
Repository Name: sh0rtifier
Description: Convert 16:9 videos to 9:16 YouTube Shorts with automatic 60-second limit enforcement
Owner: sl0thm4n
Visibility: Public
```

### Topics (GitHub Tags)
Click "Add topics" and add these:
```
youtube
shorts
video-converter
python
moviepy
opencv
uv
tkinter
cli
gui
video-processing
vertical-video
content-creation
sl0thm4n
```

## 🎬 Step-by-Step Upload

### 1. Create Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `sh0rtifier`
3. Description: `Convert 16:9 videos to 9:16 YouTube Shorts with automatic 60-second limit enforcement`
4. **Public** repository
5. **DO NOT** check "Add a README file" (we have one)
6. **DO NOT** add .gitignore (we have one)
7. **DO NOT** choose a license (we have MIT)
8. Click "Create repository"

### 2. Push Code

```bash
# Navigate to project folder
cd sh0rtifier

# Initialize git
git init

# Stage all files
git add .

# Check what's being committed
git status

# First commit
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

# Rename branch to main
git branch -M main

# Push!
git push -u origin main
```

### 3. Create First Release

```bash
# Create annotated tag
git tag -a v1.0.0 -m "Release v1.0.0

Initial release of sh0rtifier

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

📦 Downloads:
- Windows: sh0rtifier.exe
- macOS: sh0rtifier.app
- Linux: sh0rtifier (binary)

Install from source: uv sync && uv run python src/gui.py"

# Push tag (triggers GitHub Actions)
git push origin v1.0.0
```

GitHub Actions will automatically build executables!
Check the "Actions" tab after pushing the tag.

## ⚙️ Configure Repository Settings

### About Section
1. On repo page, click ⚙️ next to "About"
2. Fill in:
   - Description: `Convert 16:9 videos to 9:16 YouTube Shorts with automatic 60-second limit enforcement`
   - Website: (leave blank for now)
   - Topics: Add all topics from above
   - ✅ Releases
   - ✅ Packages (if using)

### Optional Settings

#### Enable Discussions
1. Settings → Features
2. ✅ Discussions
3. Click "Set up discussions"

#### Enable Sponsorships (Optional)
1. Settings → Features
2. ✅ Sponsorships
3. Add sponsor links if you want

#### Set Repository Image
1. Settings → Options → Social Preview
2. Upload 1280x640px image with logo + "sh0rtifier"

## 📝 After Upload Checklist

- [ ] Repository created
- [ ] Code pushed
- [ ] v1.0.0 tag pushed
- [ ] GitHub Actions running (check Actions tab)
- [ ] Topics added
- [ ] About section filled
- [ ] Star your own repo! ⭐

## 🔗 Expected URLs

- **Repo**: https://github.com/sl0thm4n/sh0rtifier
- **Releases**: https://github.com/sl0thm4n/sh0rtifier/releases
- **Issues**: https://github.com/sl0thm4n/sh0rtifier/issues
- **Actions**: https://github.com/sl0thm4n/sh0rtifier/actions

## 🎉 Post-Launch

### Share It!
- [ ] Reddit: r/Python, r/opensource, r/youtubers
- [ ] Twitter/X: Tweet with #Python #YouTubeShorts #OpenSource
- [ ] Dev.to: Write a launch post
- [ ] Hacker News: Show HN thread
- [ ] Product Hunt: Submit (wait a few days after launch)

## 🐛 If Something Goes Wrong

### GitHub Actions Failing?
- Check `.github/workflows/release.yml`
- Make sure you pushed a tag (not just commit)
- Check Actions tab for error logs

### Files Not Showing Up?
- Check `.gitignore` isn't excluding them
- Run `git status` to see what's staged

### Can't Push?
```bash
# If authentication fails, use GitHub CLI
gh auth login

# Or create Personal Access Token
# Settings → Developer settings → Personal access tokens → Generate new token
```

---

**Ready to launch?** 🚀

Run the commands above and you'll have sh0rtifier live on GitHub!
