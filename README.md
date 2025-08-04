# 🎬 Reddit Story Generator

An automated content creation tool that transforms Reddit posts into engaging short-form videos. This application fetches hot posts from popular story subreddits, enhances them using AI, and creates TikTok/YouTube Shorts-style videos with text-to-speech narration, subtitles, and Minecraft gameplay backgrounds.

## ✨ Features

- **🤖 AI-Powered Content Enhancement**: Uses Ollama with Gemma 3 12B to create engaging hooks and stories
- **🎙️ High-Quality Text-to-Speech**: 19 different voice options using Kokoro TTS
- **🎮 Minecraft Background Videos**: Overlay content on engaging Minecraft gameplay
- **📱 Social Media Ready**: Optimized for TikTok, Instagram Reels, and YouTube Shorts
- **🎵 Background Music**: Undertale soundtrack options for enhanced engagement
- **📊 Content Tracking**: Excel-based tracking system for posts and videos
- **🔄 YouTube Automation**: Automated video scheduling and uploading
- **🎨 Reddit Post Visualization**: Generates authentic-looking Reddit post images

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (tested with Python 3.12)
- **Ollama** - [Download and install from ollama.ai](https://ollama.ai/)
- **Git** (for cloning the repository)
- **Google Chrome** (for Playwright automation)

### 1. Clone the Repository

```bash
git clone https://github.com/Kaythecreator/reddit-story-generator.git
cd reddit-story-generator
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Install Playwright browsers:**
```bash
playwright install chromium
```

### 3. Set Up Ollama

1. **Install Ollama** from [ollama.ai](https://ollama.ai/)
2. **Download the required model:**
   ```bash
   ollama pull gemma3:12b
   ```
3. **Start Ollama server:**
   ```bash
   ollama serve
   ```

### 4. Reddit API Setup

1. **Create a Reddit Application:**
   - Go to [Reddit App Preferences](https://www.reddit.com/prefs/apps)
   - Click "Create App" or "Create Another App"
   - Choose "script" as the app type
   - Note down your `client_id` and `client_secret`

2. **Create `.env` file** in the root directory:
   ```env
   REDDIT_USERNAME=your_reddit_username
   REDDIT_PASSWORD=your_reddit_password
   CLIENT_ID=your_client_id
   CLIENT_SECRET=your_client_secret
   ```

### 5. Prepare Minecraft Videos

**⚠️ IMPORTANT**: You need to add Minecraft gameplay videos to the `minecraft-videos/` directory.

**Recommended sources:**
- Download Minecraft gameplay videos from YouTube (use `yt-dlp` or similar tools)
- Record your own Minecraft gameplay
- Use royalty-free Minecraft footage

**Requirements:**
- **Format**: MP4
- **Resolution**: 1080p or higher (will be cropped to 9:16 for vertical format)
- **Duration**: At least 2-3 minutes each
- **Naming**: `minecraft-video-1.mp4`, `minecraft-video-2.mp4`, etc.
- **Recommended**: 10+ videos for variety

**Example download command using yt-dlp:**
```bash
yt-dlp -f "best[height<=1080]" -o "minecraft-videos/minecraft-video-%(autonumber)s.%(ext)s" "YOUTUBE_URL_HERE"
```

### 6. Required Directory Structure

Ensure these directories exist (create them if missing):
```
Reddit-Story-Generator/
├── minecraft-videos/          # Add your Minecraft videos here
├── outputVideos/              # Generated videos will be saved here
├── outputAudios/              # Generated audio files
├── data/                      # Tracking and generated content
├── static/                    # Fonts, images, stylesheets
├── templates/                 # HTML templates for Reddit posts
└── music/                     # Background music (included)
```

## 🎮 Usage

### Creating New Videos

1. **Start the application:**
   ```bash
   python app.py
   ```

2. **Choose creation mode** by typing `c` when prompted

3. **The app will automatically:**
   - Fetch a random post from popular story subreddits
   - Generate an AI-enhanced hook and story
   - Create a Reddit post visualization
   - Generate TTS audio with your chosen voice

4. **Select voice and music** when prompted:
   - Choose from 19 available voices (male/female options)
   - Pick background music or none
   - Wait for video generation to complete

5. **Choose deployment:**
   - `s` - Add to schedule for later upload
   - `p` - Publish/schedule all videos immediately

### Scheduling Videos

1. **Run in schedule mode** by typing `s` when prompted
2. **Automatic YouTube upload** (requires Chrome profile setup)

## 🛠️ Configuration

### Voice Options
Available TTS voices include:
- **Female voices**: `af_heart`, `af_alloy`, `af_bella`, `af_jessica`, `af_nova`, etc.
- **Male voices**: `am_adam`, `am_echo`, `am_liam`, `am_michael`, etc.

### Target Subreddits
The app fetches content from these subreddits:
- r/AmItheAsshole
- r/relationship_advice
- r/TrueOffMyChest
- r/confession
- r/pettyrevenge
- r/MaliciousCompliance
- r/entitledparents
- r/JUSTNOMIL
- r/cheating_stories
- r/NuclearRevenge
- r/ProRevenge

### YouTube Automation Setup

For automated YouTube uploads:

1. **Chrome Profile Setup:**
   - Log into YouTube in Chrome
   - Note your Chrome profile path
   - Update the path in `scripts/platforms/youtube_scheduler.py`

2. **Channel Configuration:**
   - Update the channel URL in the YouTube scheduler script
   - Ensure you have upload permissions

## 📂 Output Files

### Generated Content
- **Videos**: `outputVideos/output-{post_id}.mp4`
- **Audio**: `outputAudios/output-title.wav`, `outputAudios/output-story.wav`
- **Images**: `static/reddit_post.png`
- **Subtitles**: `subtitles.srt`
- **Tracking**: `data/Reddit-Story-Generator.xlsx`

### Content Tracking
The Excel file tracks:
- Original Reddit posts
- AI-generated content
- Video generation details
- Scheduling information

## 🔧 Troubleshooting

### Common Issues

**Ollama Connection Error:**
```bash
# Ensure Ollama is running
ollama serve

# Verify model is downloaded
ollama list
```

**Missing Minecraft Videos:**
- Add at least one video to `minecraft-videos/` directory
- Ensure videos are named correctly (`minecraft-video-1.mp4`, etc.)

**Reddit API Issues:**
- Verify `.env` file exists and contains correct credentials
- Check Reddit API limits (you might be rate-limited)

**TTS Errors:**
- Verify Kokoro TTS installation: `python -c "import kokoro; print('OK')"`
- Try a different voice if one fails

**Video Generation Fails:**
- Check available disk space
- Ensure FFmpeg is properly installed with MoviePy
- Verify Minecraft video files are not corrupted

### Performance Tips

- **Use SSD storage** for faster video processing
- **Close unnecessary applications** during video generation
- **Use GPU acceleration** if available (update MoviePy codec settings)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is for educational purposes. Ensure you comply with:
- Reddit's API Terms of Service
- YouTube's Terms of Service
- Copyright laws for background music and footage

## 🆘 Support

If you encounter issues:

1. **Check the troubleshooting section** above
2. **Verify all prerequisites** are installed correctly
3. **Check your .env configuration**
4. **Ensure Minecraft videos are properly added**
5. **Create an issue** on GitHub with error details

## 🎯 Tips for Best Results

- **Use engaging Minecraft gameplay** (PvP, building, parkour work well)
- **Choose appropriate voices** for your target audience
- **Monitor Reddit post quality** - longer, more detailed posts work better
- **Schedule uploads** during peak hours for your target audience
- **Keep variety** in your Minecraft background videos

---

**Made with ❤️ for content creators**