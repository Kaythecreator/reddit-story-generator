from kokoro import KModel, KPipeline
from playsound3 import playsound
from IPython.display import display, Audio
import soundfile as sf
import torch
import numpy as np
import praw
import os
from dotenv import load_dotenv
from scripts.llm_story import AI_story
from scripts.llm_hook import AI_hook
from scripts.excel import store_data, store_story, store_content_info, get_row_index, ws
from scripts.platforms.youtube_scheduler import schedule_video
from moviepy import AudioFileClip, VideoFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips, TextClip, vfx, CompositeAudioClip, afx
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.io import ffmpeg_writer
from moviepy.video.io.ffmpeg_writer import FFMPEG_VideoWriter, ffmpeg_write_video
from scripts.reddit_imggen import generate_reddit_post
import math
import datetime
from scripts.llm_caption import AI_caption

playsound("808521__licht2003__done-sound.wav")

font_path = "static/KOMIKAX_.ttf"
subtitles_path = "subtitles.srt"
text_color = "white"

OnboardingChoice = input('Would you like to create a new video or schedule posts?(c/s)')

if OnboardingChoice == 'c':
    os.popen("ollama serve")

    load_dotenv()

    print('\n\nSystem initialized!\n\n')

    try:
        os.remove('subtitles.srt')
        print('\nSubtitles file removed\n')
    except:
        pass

    minecraft_videos_count = len(os.listdir('minecraft-videos'))

    reddit_username=os.environ.get('REDDIT_USERNAME')
    reddit_password=os.environ.get('REDDIT_PASSWORD')
    client_id=os.environ.get('CLIENT_ID')
    client_secret=os.environ.get('CLIENT_SECRET')

    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        username=reddit_username,
        password=reddit_password,
        user_agent='RedditStoryGenerator/1.0 (by /u/Curcu1t)'
    )


    subreddit_list = [
        "AmItheAsshole",
        "relationship_advice",
        "TrueOffMyChest",
        "confession",
        "pettyrevenge",
        "MaliciousCompliance",
        "entitledparents",
        "JUSTNOMIL",
        "cheating_stories",
        "NuclearRevenge",
        "ProRevenge"
    ]

    random_subreddit = np.random.randint(0, len(subreddit_list) - 1)

    print(f'Random subreddit: {subreddit_list[random_subreddit]}')

    subreddit = reddit.subreddit(subreddit_list[random_subreddit])
    top_post = subreddit.hot(limit=100)
    for post in top_post:

        postcontent = post.title + '\n' + post.selftext

        if len(postcontent) < 500 or postcontent == '[removed]' or postcontent == '[deleted]' or 'www.' in postcontent or 'http' in postcontent or 'mods' in postcontent or post.id in open('data/completedposts.txt', encoding='utf-8').read(): 
            print(f'Skipping post {post.id} - {post.title}')
            pass
        else:
            reddit_story = postcontent
            print(f'\n\nSubreddit: {subreddit} \nTitle: {post.title}')
            store_data(post.id, post.title, subreddit.display_name, post.url)
            with open('data/completedposts.txt', 'a', encoding='utf-8') as f:
                f.write(f'{post.id} - {post.title} - {post.url} \n')
            break


    print("\n\n", reddit_story, "\n\n")

    AItitle = AI_hook(post.title, post.selftext)
    AIstory = AI_story(post.selftext)
    AIcaption = AI_caption(post.title)
    with open('data/AItitle.txt', 'w', encoding='utf-8') as f:
        f.write(AItitle)
    with open('data/AIstory.txt', 'w', encoding='utf-8') as f:
        f.write(AIstory)
    with open('data/AIcaption.txt', 'w', encoding='utf-8') as f:
        f.write(AIcaption)

    playsound("808521__licht2003__done-sound.wav")

    choice = input('Press Enter to continue...')

    with open('data/AItitle.txt', 'r', encoding='utf-8' ) as f:
        AItitle = f.read()
    with open('data/AIstory.txt', 'r', encoding='utf-8') as f:
        AIstory = f.read()
    with open('data/AIcaption.txt', 'r', encoding='utf-8') as f:
        AIcaption = f.read()

    store_story(post.id, AItitle, AIstory, AIcaption)

    print('Generating reddit post png...')
    generate_reddit_post(AItitle)

    text = AItitle + '\n' + AIstory

    print('\n\n', text, '\n\n')

    voices = [
        'af_heart',
        'af_alloy',
        'af_aoede',
        'af_bella',
        'af_jessica',
        'af_kore',
        'af_nicole',
        'af_nova',
        'af_river',
        'af_sarah',
        'af_sky',
        'am_adam',
        'am_echo',
        'am_eric',
        'am_fenrir',
        'am_liam',
        'am_michael',
        'am_onyx',
        'am_puck',
        'am_santa'
    ]

    print('\nAvailable voices:\n')
    for voice in voices:
        print(voice)


    voice_choice = input('\nEnter your choice:')

    music_choice = input(f'What music do you want to use?\n\n1. Undertale - Fallen Down\n2. Undertale - Fallen Down (Slowed)\n3. None\n\nEnter your choice (1-3): ')

    model = KModel()
    pipeline = KPipeline(lang_code='a', model=model)

    def tts(text, category):
        # 4️⃣ Generate, display, and save audio files in a loop.
        generator = pipeline(
            text, voice=voice_choice, # <= change voice here
            speed=1.3, split_pattern=r'\n+'
        )

        all_audio = []
        index = 1
        # Initialize cumulative time elapsed
        cumulative_time = 0.0

        for i, result in enumerate(generator):
            gs = result.graphemes # str
            ps = result.phonemes # str
            audio = result.audio.cpu().numpy()
            tokens = result.tokens # List[en.MToken] 

            # Calculate the actual duration of the current audio segment
            # audio.shape[0] is the number of samples, 24000 is the sample rate
            segment_duration = audio.shape[0] / 24000.0

            # We no longer rely on tokens[-1].end_ts for segment duration

            if category == 'story':
                for t in tokens:
                    with open('subtitles.srt', 'a', encoding='utf-8', errors='replace') as f:
                        
                        badChar = [".", ",", "!", "?", "...",'"',"'","�", ":", "—", "*", "  ", '"', '"', '(', ')', "–", "“", "”"]
                        word = t.text

                        if t.start_ts is None or t.end_ts is None:
                            print(f"Skipping token '{word}' due to missing timestamp.")
                            continue

                        # Calculate absolute start and end times by adding cumulative time
                        start_total_seconds = t.start_ts + cumulative_time
                        end_total_seconds = t.end_ts + cumulative_time

                        # Convert timestamps from seconds (float) to HH:MM:SS,ms format
                        start_ms = int((start_total_seconds * 1000) % 1000)
                        start_seconds = int(start_total_seconds % 60)
                        start_minutes = int((start_total_seconds / 60) % 60)
                        start_hours = int(start_total_seconds / 3600)

                        end_ms = int((end_total_seconds * 1000) % 1000)
                        end_seconds = int(end_total_seconds % 60)
                        end_minutes = int((end_total_seconds / 60) % 60)
                        end_hours = int(end_total_seconds / 3600)

                        # Format timestamps as HH:MM:SS,ms
                        start_time_str = f'{start_hours:02}:{start_minutes:02}:{start_seconds:02},{start_ms:03}'
                        end_time_str = f'{end_hours:02}:{end_minutes:02}:{end_seconds:02},{end_ms:03}'

                        if word in badChar:
                            pass
                        else:
                            f.write(f'{index}\n{start_time_str} --> {end_time_str}\n{word}\n\n')
                            index += 1
            else:
                pass

            # Update cumulative time after processing the segment's tokens
            cumulative_time += segment_duration

            display(Audio(data=audio, rate=24000, autoplay=i==0))
            all_audio.append(audio)

        combined_audio = np.concatenate(all_audio)

        sf.write(f'outputAudios/output-{category}.wav', combined_audio, 24000)

        print(f'\n {category.upper()} audio download completed! File saved as output-{category}.wav\n')

    if voice_choice in voices:
        tts(AItitle, 'title')
        tts(AIstory, 'story')
    else:
        print('Invalid voice choice')



    videoStartPoint = np.random.randint(0, 100)
    random_minecraft_video = np.random.randint(1, minecraft_videos_count)

    audio_intro = AudioFileClip(f'outputAudios/output-title.wav').with_effects([afx.MultiplyVolume(1.75)])
    audio_story = AudioFileClip(f'outputAudios/output-story.wav').with_effects([afx.MultiplyVolume(1.75)])
    mc_clip = VideoFileClip(f'minecraft-videos/minecraft-video-{random_minecraft_video}.mp4', audio=False)
    print(f'Minecraft video chosen: minecraft-video-{random_minecraft_video}.mp4')

    def ease_in_out(t, start_scale, end_scale, duration):
        if t >= duration:
            return end_scale
        # Calculate the easing factor between 0 and 1 for t within [0, duration]
        easing_factor = 0.5 - 0.5 * math.cos(math.pi * t / duration)
        # Interpolate between start_scale and end_scale using the easing factor
        zoom_factor = start_scale + (end_scale - start_scale) * easing_factor
        return zoom_factor

    def createIntro():
        start_scale = 1.0
        end_scale = 1.7
        duration = 0.15
        image_intro = ImageClip('static/reddit_post.png')
        image_intro = image_intro.with_duration(audio_intro.duration).with_position(('center', 'center'))
        image_intro = image_intro.with_effects([vfx.Resize(lambda t: [int(image_intro.w * ease_in_out(t, start_scale, end_scale, duration)), int(image_intro.h * ease_in_out(t, start_scale, end_scale, duration))])])
        minecraft_clip = mc_clip.subclipped(videoStartPoint, videoStartPoint + audio_intro.duration)
        intro_clip = minecraft_clip.with_audio(audio_intro)
        introClip = CompositeVideoClip([intro_clip, image_intro])
        return introClip

    def createStory():
        start_scale = 0.5
        end_scale = 1.1
        duration = 0.05
        minecraft_clip = mc_clip.subclipped(videoStartPoint + audio_intro.duration, videoStartPoint + audio_intro.duration + audio_story.duration)
        story_clip = minecraft_clip.with_audio(audio_story)
        generator = lambda txt: TextClip(
            font_path,
            text = txt,
            font_size = 100,
            color= text_color,
            stroke_color="black",
            stroke_width=10,
            size=(1080, 1920)
        )
        sub_clip = SubtitlesClip(subtitles_path, make_textclip=generator, encoding='utf-8') # .with_effects([vfx.Resize(lambda t: [int(sub_clip.w * ease_in_out(t, start_scale, end_scale, duration)), int(sub_clip.h * ease_in_out(t, start_scale, end_scale, duration))])])
        result = CompositeVideoClip([story_clip, sub_clip])
        return result

    if music_choice == '1':
        music_clip = AudioFileClip('music/Undertale OST - fallen down (slowed + reverb).mp3').with_effects([afx.MultiplyVolume(0.1)]).subclipped(0, audio_intro.duration + audio_story.duration)
    elif music_choice == '2':
        music_clip = AudioFileClip('music/Undertale OST： 085 - Fallen Down (Reprise).mp3').with_effects([afx.MultiplyVolume(0.1)]).subclipped(0, audio_intro.duration + audio_story.duration)
    elif music_choice == '3':
        music_clip = None

    clips = []
    clips.append(createIntro())
    clips.append(createStory())

    final_clip = concatenate_videoclips(clips)
    # Get the voiceover audio from the concatenated video clip
    voiceover_audio = final_clip.audio

    if music_clip and music_choice != '3':
        # Combine voiceover audio with the music clip
        combined_audio = CompositeAudioClip([voiceover_audio, music_clip])
        # Set the combined audio to the final video clip
        final_clip = final_clip.with_audio(combined_audio)

    #final_clip(f'outputVideos/output-{post.id}.mp4', codec='hevc_nvenc', threads=12)

    final_clip.write_videofile(f'outputVideos/output-{post.id}.mp4', codec='hevc_nvenc', threads=12, fps=30.0, preset='p1')

    store_content_info(post.id, voice_choice, random_minecraft_video, f'C:\\Users\\Kavin Seralathan\\Reddit-Story-Generator\\outputVideos\\output-{post.id}.mp4')

    print(f'\n Download completed! File saved as output-{post.id}.mp4\n')

    playsound("808521__licht2003__done-sound.wav")

    schedule_choice = input('Add to schedule or publish now?(s/p)')

    if schedule_choice == 's':
        Caption = AIcaption
        Date = input('Enter date (today or future date (t/f))')
        if Date == 't':
            Date = datetime.datetime.now().strftime("%b %d, %Y")
        Time = input('Enter time (HH:MM AM/PM)')
        store_content_info(post.id, Caption, Date, Time)
    elif schedule_choice == 'p':
        folder_path = "C:\\Users\\Kavin Seralathan\\Reddit-Story-Generator\\outputVideos"
        for file in os.listdir(folder_path):
            index = get_row_index(f'{folder_path}\\{file}')
            title = ws[f'L{index}'].value
            date = ws[f'M{index}'].value
            time = ws[f'N{index}'].value
            schedule_video(f'{folder_path}\\{file}', title, date, time)
            print(f'\n\nScheduled {title} for {date} at {time}\n\n')
        print(f'\n\nVideos scheduled\n\n')


elif OnboardingChoice == 's':
    folder_path = "C:\\Users\\Kavin Seralathan\\Reddit-Story-Generator\\outputVideos"
    for file in os.listdir(folder_path):
        index = get_row_index(f'{folder_path}\\{file}')
        title = ws[f'L{index}'].value
        date = ws[f'M{index}'].value
        time = ws[f'N{index}'].value
        schedule_video(f'{folder_path}\\{file}', title, date, time)
        print(f'\n\nScheduled {title} for {date} at {time}\n\n')
    print(f'\n\nVideos scheduled\n\n')
