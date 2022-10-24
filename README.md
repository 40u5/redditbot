# Reddit Bot - Automated Video Creator

🎬 **Transform Reddit content into engaging videos automatically!**

A powerful Python automation tool that creates professional video content from Reddit posts and comments. Perfect for content creators, this bot scrapes popular posts from r/AskReddit, converts text to speech, captures high-quality screenshots, and compiles everything into polished videos ready for YouTube, TikTok, or other social media platforms.

## ✨ What This Bot Does

1. **Scrapes Reddit**: Fetches the hottest posts from r/AskReddit
2. **Interactive Selection**: Let you choose from 20 trending posts
3. **Smart Screenshots**: Automatically captures Reddit posts and comments
4. **Text-to-Speech**: Converts all text to natural-sounding audio
5. **Video Magic**: Combines everything into a professional video with transitions
6. **Ready to Upload**: Outputs MP4 files optimized for social media

## 🎥 Features

- **Automated Reddit Scraping**: Fetches hot posts from r/AskReddit subreddit
- **Interactive Post Selection**: Choose from the top 20 trending posts
- **Screenshot Automation**: Uses Selenium WebDriver to capture Reddit post and comment screenshots
- **Text-to-Speech Generation**: Converts post titles and comments to audio using Google Text-to-Speech (gTTS)
- **Video Compilation**: Creates professional-looking videos with transitions and background images
- **Content Filtering**: Automatically removes links from comments for cleaner audio
- **Customizable Output**: Choose how many comments to include in your video
- **Multiple Execution Modes**: 
  - Full mode: Complete scraping and video creation
  - Video-only mode: Create videos from existing screenshots and audio
  - Fast mode: Quick video generation for testing purposes
- **Smart Image Processing**: Automatically scales and centers Reddit screenshots on custom backgrounds
- **Professional Transitions**: Includes transition effects between video segments

## 📁 Project Structure

```
redditbot/
├── main.py                 # Main application script
├── requirements.txt        # Python dependencies
├── init.bat               # Windows initialization script
├── README.md              # Project documentation
├── .env                   # Environment variables (you need to create this)
├── .gitignore             # Git ignore rules
├── __pycache__/           # Python cache files
├── output/                # Generated content
│   ├── audio/            # Generated audio files (MP3s)
│   │   ├── title.mp3     # Title audio
│   │   ├── file1.mp3     # Comment audio files
│   │   ├── ...           # Additional comment files
│   │   └── final_audio.mp3 # Combined final audio
│   ├── images/           # Screenshot images (PNG files)
│   │   ├── Title.png     # Post title screenshot
│   │   ├── image1.png    # Comment screenshots
│   │   └── ...           # Additional image files
│   └── video/            # Final video output (MP4 files)
│       └── reddit_video.mp4 # Generated video
└── utils/
    ├── assets/           # Background images and transition assets
    │   ├── space.png     # Background image for videos
    │   ├── transition.jpg # Transition image
    │   ├── transition audio.mp3 # Transition sound
    │   └── black background.jpg # Alternative background
    ├── example/          # Example files and samples
    └── tests/            # Test files and scripts
        ├── test.py       # Test script
        └── test.mp3      # Test audio file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Chrome browser installed
- Reddit account
- Reddit API credentials

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd redditbot
   ```

2. **Run the initialization script** (Windows):
   ```bash
   init.bat
   ```
   
   Or install manually:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Reddit API credentials**:
   - Go to [Reddit Apps](https://www.reddit.com/prefs/apps)
   - Click "Create App" or "Create Another App"
   - Choose "script" as the app type
   - Note down your `client_id` and `client_secret`

4. **Configure environment variables**:
   Create a `.env` file in the root directory:
   ```env
   CLIENT_ID=your_client_id_here
   SECRET_KEY=your_client_secret_here
   USERNAME=your_reddit_username
   PASSWORD=your_reddit_password
   ```

### Usage

The bot supports three different execution modes:

#### 🚀 Full Mode (Default)
Complete Reddit scraping and video creation process:

```bash
python main.py
```

1. **Select a post**:
   - The bot will display the top 20 hot posts from r/AskReddit
   - Type the exact title of the post you want to create a video from

2. **Choose comment count**:
   - Enter the number of comments you want to include in your video

3. **Wait for processing**:
   - The bot will automatically log into Reddit, take screenshots, generate audio, and create the final video

4. **Find your video**:
   - The final video will be saved as `output/video/reddit_video.mp4`

#### 🎬 Video-Only Mode
Create a video from existing screenshots and audio files (useful for re-rendering):

```bash
python main.py --video-only
```

This mode will:
- Skip Reddit scraping and screenshot capture
- Use existing files in `output/images/` and `output/audio/`
- Generate a new video with current settings

#### ⚡ Fast Mode
Quick video generation for testing purposes:

```bash
python main.py --fast
```

This mode will:
- Use existing screenshots and audio files
- Create video with optimized settings for faster processing
- Perfect for testing changes without full processing time

## 🛠️ Dependencies

All dependencies are listed in `requirements.txt` and can be installed with `pip install -r requirements.txt`:

- **selenium**: Web browser automation for taking Reddit screenshots
- **praw**: Python Reddit API Wrapper for accessing Reddit posts and comments
- **Pillow (PIL)**: Image processing and manipulation for screenshot editing
- **pyautogui**: GUI automation for scrolling and clicking during screenshot capture
- **gtts**: Google Text-to-Speech for converting text to audio
- **moviepy**: Video editing and compilation for creating the final video
- **python-dotenv**: Environment variable management for secure credential storage

### System Requirements
- **Python 3.7+**: Required for all dependencies
- **Chrome Browser**: Required for Selenium WebDriver
- **Internet Connection**: Required for Reddit API access and Google Text-to-Speech

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `CLIENT_ID` | Reddit app client ID | Yes |
| `SECRET_KEY` | Reddit app secret key | Yes |
| `USERNAME` | Your Reddit username | Yes |
| `PASSWORD` | Your Reddit password | Yes |

### Customization Options

- **Subreddit**: Change `subreddit = reddit.subreddit('askreddit')` in `main.py` to target different subreddits
- **Post Limit**: Modify `hot = subreddit.hot(limit=20)` to fetch more/fewer posts
- **Background Images**: Replace images in `utils/assets/` to customize video appearance
- **Video Quality**: Adjust FPS and resolution in the `createVideo()` function

## 🎬 Output

The bot generates:
- **Audio Files**: Individual MP3 files for each post title and comment
- **Image Files**: PNG screenshots of Reddit posts and comments
- **Final Video**: MP4 file combining all elements with transitions

## 🔧 Troubleshooting

### Common Issues

1. **Environment Variables Not Found**:
   - Ensure `.env` file exists in the root directory
   - Check for typos in variable names (case-sensitive)
   - Verify all four variables are present: `CLIENT_ID`, `SECRET_KEY`, `USERNAME`, `PASSWORD`

2. **Chrome Driver Issues**:
   - Make sure Chrome browser is installed and up to date
   - Selenium automatically downloads ChromeDriver, but ensure Chrome is in your PATH
   - Try running Chrome manually to verify it works

3. **Login Failures**:
   - Verify Reddit credentials are correct (username/password)
   - **Important**: 2FA (Two-Factor Authentication) is NOT supported - disable it temporarily
   - Check if your account is suspended or has restrictions

4. **Screenshot Problems**:
   - Ensure your screen resolution is at least 1920x1080
   - Try running with Chrome window maximized
   - Check if Reddit's layout has changed (may require code updates)
   - Make sure you're not running other programs that interfere with browser automation

5. **Audio Generation Issues**:
   - Ensure stable internet connection for Google Text-to-Speech
   - Check if comments contain special characters that might cause issues
   - Verify `output/audio/` directory exists

6. **Video Creation Problems**:
   - Ensure `output/images/` contains the required screenshot files
   - Check available disk space for video processing
   - Verify all audio files were generated successfully

7. **Permission Errors**:
   - Run terminal/command prompt as administrator (Windows)
   - Check file permissions in the output directories
   - Ensure antivirus isn't blocking file creation

### Error Messages & Solutions

| Error Message | Solution |
|---------------|----------|
| `"Missing required environment variables"` | Create and configure your `.env` file with all four variables |
| `"No comment images found!"` | Run full mode first to generate screenshots before using `--video-only` |
| `Selenium WebDriver errors` | Update Chrome browser, check internet connection, or restart the script |
| `PRAW authentication errors` | Verify Reddit API credentials and disable 2FA |
| `"Permission denied"` | Run as administrator or check file permissions |
| `MoviePy errors during video creation` | Check disk space and ensure all required files exist |
| `gTTS errors` | Check internet connection and try again |

### Performance Tips

- **Faster Processing**: Use `--fast` mode for testing
- **Reduce Video Size**: Use fewer comments (5-10 recommended)
- **Better Quality**: Ensure high-resolution screenshots by maximizing browser window
- **Stable Results**: Wait a few seconds between runs to avoid rate limiting

## 📝 License

This project is for educational purposes. Please respect Reddit's Terms of Service and API guidelines when using this bot.

## 🎯 Example Output

The bot generates videos with:
- **Professional Layout**: Reddit screenshots centered on custom backgrounds
- **Smooth Transitions**: Seamless transitions between post and comments
- **Clear Audio**: High-quality text-to-speech narration
- **Optimized Format**: Ready-to-upload MP4 files

## 🚀 Quick Examples

```bash
# Create a full video (scraping + video creation)
python main.py

# Re-render video from existing files
python main.py --video-only

# Quick test render
python main.py --fast
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:
- 🐛 Report bugs by opening issues
- 💡 Suggest new features or improvements
- 🔧 Submit pull requests with enhancements
- 📚 Improve documentation

## ⚠️ Important Disclaimers

- **Educational Use**: This bot is intended for educational and personal use only
- **Reddit ToS**: Always respect Reddit's Terms of Service, robots.txt, and API rate limits
- **Content Ethics**: Be mindful of fair use policies when creating videos from Reddit content
- **Attribution**: Consider crediting original Reddit users in your videos
- **Rate Limiting**: Don't abuse the bot - use reasonable delays between requests

## 📊 Version History

- **v1.0**: Basic Reddit scraping and video creation
- **v1.1**: Added command-line modes (--video-only, --fast)
- **v1.2**: Improved image processing and error handling
- **Current**: Enhanced documentation and troubleshooting