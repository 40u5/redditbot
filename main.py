from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import praw
from praw.models import MoreComments
import os
from PIL import Image
import pyautogui
import time
from gtts import gTTS
import moviepy as mp
from dotenv import load_dotenv

# Global variables
reddit = None
submission = None
clips = 0

def initialize_reddit():
    """Initialize Reddit API connection and get post selection"""
    global reddit, submission
    
    # Load environment variables from .env file
    load_dotenv()

    CLIENT_ID = os.getenv('CLIENT_ID')
    SECRET_KEY = os.getenv('SECRET_KEY')
    USERNAME = os.getenv('USERNAME')
    PASSWORD = os.getenv('PASSWORD')

    # Check if all required environment variables are set
    if not all([CLIENT_ID, SECRET_KEY, USERNAME, PASSWORD]):
        print("Error: Missing required environment variables.")
        print("Please create a .env file with the following variables:")
        print("CLIENT_ID=your_client_id_here")
        print("SECRET_KEY=your_client_secret_here")
        print("USERNAME=your_reddit_username")
        print("PASSWORD=your_reddit_password")
        print("\nGet your CLIENT_ID and SECRET_KEY from https://www.reddit.com/prefs/apps")
        exit(1)

    reddit = praw.Reddit(
        client_id = CLIENT_ID,
        client_secret= SECRET_KEY,
        username=USERNAME,
        password=PASSWORD,
        user_agent="Redditbot"
        #authentication information
    )

    Title_Id = {}
    #get multiple titles and their IDs
    subreddit = reddit.subreddit('askreddit')

    hot = subreddit.hot(limit=20)
    #gets 5 posts in the hot subreddit
    for submissions in hot:
        Title_Id.update({submissions.title:submissions.id})
        print(submissions.title)
        #Title_Id keeps key value pairs that link the title with the id of the post
        #title can easily be linked with the post content

    chosenComment = input("Choose the reddit comment to post: ")
    while chosenComment not in Title_Id:
        chosenComment = input("Choose the reddit comment to post: ")
    #choose the most interesting of the posts
    submission = reddit.submission(Title_Id[chosenComment])
    
    return submission

def setup_webdriver():
    """Setup Chrome WebDriver and login to Reddit"""
    global driver
    
    # Start a web driver and open the URL
    options = webdriver.ChromeOptions()
    #sets the options
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options)
    driver.get('https://www.reddit.com/login')

    # Load environment variables for login
    load_dotenv()
    USERNAME = os.getenv('USERNAME')
    PASSWORD = os.getenv('PASSWORD')

    # Enter your username and password
    driver.find_element(By.ID, 'loginUsername').send_keys(USERNAME)
    driver.find_element(By.ID, 'loginPassword').send_keys(PASSWORD)

    # Click the 'login' button to log in
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    driver.execute_script("window.open('');")

    # Switch to the new tab
    driver.switch_to.window(driver.window_handles[1])

    # Set the URL of the Reddit post that you want to take a screenshot of
    url = "https://www.reddit.com" + submission.permalink
    
    # Load a page in the new tab
    driver.get(url)
    driver.implicitly_wait(10)
    driver.maximize_window()
    time.sleep(2)
    pyautogui.click(400,169)
    time.sleep(1)
    pyautogui.click(1896,91)
    driver.refresh()
    time.sleep(5)
    
    return driver

def remove_link(s):
    words = s.split()
    new_words = [word for word in words if 'https:/' not in word]
    return ' '.join(new_words)

def createScreenshots(num_of_clips):
    # Initialize Reddit and get submission
    initialize_reddit()
    # Setup webdriver and login
    setup_webdriver()
    
    #finds element title
    element = driver.find_element("id","t3_" + submission.id)
    location = element.location
    driver.save_screenshot("screenshot.png")
    title_size = element.size
    # Use Pillow to open the image and crop it to just the Reddit post
    im = Image.open("screenshot.png")
    left = location['x']
    top = location['y']
    right = location['x'] + title_size['width']
    bottom = location['y'] + title_size['height']
    im = im.crop((left, top, right, bottom))
    # Save the cropped image
    im.save("output/images/Title.png")
    os.remove('screenshot.png')
    global clips
    clips = 1
    maxClips = num_of_clips
    createAudioFile(submission.title, 'output/audio/title')
    time.sleep(0.5)
    for comment in submission.comments:
        if isinstance(comment, MoreComments):
            continue
        if (clips > maxClips):
            break
        element =  driver.find_element(by='id', value="t1_" + comment.id)
        driver.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(0.1)
        pyautogui.scroll(100)
        time.sleep(0.5)
        element.screenshot('output/images/image' + str(clips) + '.png')
        comment.body = remove_link(comment.body)
        #removes any links said during the video
        createAudioFile(comment.body, 'output/audio/file' + str(clips))
        clips +=1

def createAudioFile(text,name):
    text = text
    name = name
    tts = gTTS(text=text, lang='en')
    tts.save(name + '.mp3')

def createVideo():
    print("🎬 Starting video creation...")
    print("📏 Loading background image...")
    im0 = Image.open('utils/assets/space.png')
    background_width, background_height = im0.size
    video = []
    audio = []
    
    print("🖼️ Processing title image...")
    # Process title image
    back_im = im0.copy()
    image = Image.open(f"output/images/title.png")
    
    # Scale image to fit nicely on background (max 80% of background width/height)
    max_width = int(background_width * 0.8)
    max_height = int(background_height * 0.8)
    
    # Calculate scaling factor to maintain aspect ratio
    scale_factor = min(max_width / image.width, max_height / image.height)
    new_width = int(image.width * scale_factor)
    new_height = int(image.height * scale_factor)
    
    im_scaled = image.resize((new_width, new_height), resample=Image.Resampling.BICUBIC)
    
    # Center the image on the background
    x_pos = (background_width - new_width) // 2
    y_pos = (background_height - new_height) // 2
    
    back_im.paste(im_scaled, (x_pos, y_pos))
    back_im.save(f'output/images/title_processed.png', quality=100)
    
    # Create video clips
    print("🎵 Loading title audio...")
    titleAudio = mp.AudioFileClip('output/audio/title.mp3')
    titleVideo = mp.ImageClip('output/images/title_processed.png', duration=titleAudio.duration)
    audio.append(titleAudio)
    video.append(titleVideo)

    # Add transition after title
    print("🔄 Loading transition assets...")
    transitionAudio = mp.AudioFileClip('utils/assets/transition audio.mp3')
    transitionVideo = mp.ImageClip('utils/assets/transition.jpg', duration=transitionAudio.duration)
    audio.append(transitionAudio)
    video.append(transitionVideo)

    # Process comment images
    print(f"📝 Processing {clips-1} comment images...")
    for img_number in range(1, clips):
        print(f"  Processing comment {img_number}/{clips-1}...")
        back_im = im0.copy()
        image = Image.open(f"output/images/image{img_number}.png")
        
        # Scale image to fit nicely on background
        scale_factor = min(max_width / image.width, max_height / image.height)
        new_width = int(image.width * scale_factor)
        new_height = int(image.height * scale_factor)
        
        im_scaled = image.resize((new_width, new_height), resample=Image.Resampling.BICUBIC)
        
        # Center the image on the background
        x_pos = (background_width - new_width) // 2
        y_pos = (background_height - new_height) // 2
        
        back_im.paste(im_scaled, (x_pos, y_pos))
        back_im.save(f'output/images/image{img_number}_processed.png', quality=100)
        
        # Create clips for this comment
        audio_clip = mp.AudioFileClip(f'output/audio/file{img_number}.mp3')
        image_clip = mp.ImageClip(f'output/images/image{img_number}_processed.png', duration=audio_clip.duration)
        audio.append(audio_clip)
        video.append(image_clip)
        
        # Add transition after each comment (create new instance to avoid reuse issues)
        transition_clip = mp.ImageClip('utils/assets/transition.jpg', duration=transitionAudio.duration)
        video.append(transition_clip)
        audio.append(transitionAudio)
    
    print("🎵 Combining audio tracks...")
    final_audio = mp.concatenate_audioclips(audio)
    print("💾 Saving final audio file...")
    final_audio.write_audiofile('output/audio/final_audio.mp3', logger=None)
    
    print("🎬 Combining video clips...")
    final = mp.concatenate_videoclips(video, method='compose')
    final.audio = final_audio
    
    print("🚀 Rendering final video... (This may take a while)")
    print("💡 Tip: The larger your images, the longer this will take!")
    final.write_videofile('output/video/reddit_video.mp4', 
                         fps=24, 
                         logger=None,
                         temp_audiofile='temp-audio.m4a',
                         remove_temp=True,
                         codec='libx264',
                         audio_codec='aac')
    
    print("✅ Video creation complete! Check output/video/reddit_video.mp4")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--video-only":
        # Video-only mode: just create video from existing files
        try:
            # Count existing image files to determine clips
            import glob
            existing_images = glob.glob("output/images/image*.png")
            # Filter out processed images to count only originals
            original_images = [img for img in existing_images if not img.endswith('_processed.png')]
            # Find the highest numbered image to determine actual range
            if original_images:
                import re
                image_numbers = []
                for img in original_images:
                    match = re.search(r'image(\d+)\.png', img)
                    if match:
                        image_numbers.append(int(match.group(1)))
                clips = max(image_numbers) + 1 if image_numbers else 1
                print(f"Found {len(original_images)} comment images (image1 to image{max(image_numbers)}). Creating video...")
            else:
                print("No comment images found!")
                exit(1)
            createVideo()
        except Exception as e:
            print(f"Error creating video: {e}")
            print("Make sure you have run the full process at least once to generate the required files.")
    elif len(sys.argv) > 1 and sys.argv[1] == "--fast":
        # Fast mode: create video with lower quality settings for testing
        try:
            import glob
            import re
            existing_images = glob.glob("output/images/image*.png")
            original_images = [img for img in existing_images if not img.endswith('_processed.png')]
            if original_images:
                image_numbers = []
                for img in original_images:
                    match = re.search(r'image(\d+)\.png', img)
                    if match:
                        image_numbers.append(int(match.group(1)))
                clips = max(image_numbers) + 1 if image_numbers else 1
                print(f"🚀 FAST MODE: Found {len(original_images)} comment images (image1 to image{max(image_numbers)}). Creating video...")
            else:
                print("No comment images found!")
                exit(1)
            createVideo()
        except Exception as e:
            print(f"Error creating video: {e}")
    else:
        # Full mode: scrape Reddit and create video
        num_clips = int(input("How many comments do you want to include? "))
        createScreenshots(num_clips)
        createVideo()