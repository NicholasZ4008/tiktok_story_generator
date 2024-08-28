import os
import random

def random_bg_vid(filepath):
    """
    Randomly selects a video file from the specified directory.
    
    Args:
    filepath (str): Path to the directory containing background videos.
    
    Returns:
    str: Full path of the randomly selected video file.
    """
    video_files = [f for f in os.listdir(filepath) if f.endswith('.mp4')]
    if not video_files:
        raise FileNotFoundError(f"No .mp4 files found in {filepath}")
    random_video = random.choice(video_files)
    return os.path.join(filepath, random_video)

def random_bg_audio(filepath):
    """
    Randomly selects an audio file from the specified directory.
    
    Args:
    filepath (str): Path to the directory containing background audio files.
    
    Returns:
    str: Full path of the randomly selected audio file.
    """
    audio_files = [f for f in os.listdir(filepath) if f.endswith('.mp3')]
    if not audio_files:
        raise FileNotFoundError(f"No .mp3 files found in {filepath}")
    random_audio = random.choice(audio_files)
    return os.path.join(filepath, random_audio)
