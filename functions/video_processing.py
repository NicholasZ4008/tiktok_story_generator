import pandas as pd
import os
from google.cloud import texttospeech_v1 as texttospeech
from google.cloud import storage
from moviepy.editor import *
from tqdm import tqdm
from PIL import Image
# Update MoviePy's resize function to use the new Pillow resampling method
from moviepy.video.fx.all import resize
import tempfile
import traceback
import sys
import uuid
import time
from pydub import AudioSegment
import io
from functions.auto_subtitle import VideoTranscriber
from functions.gcs_bucket_manager import BucketManager
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the Google credentials path from the environment variable
credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_PATH')
# Expand user directory and resolve path
credentials_path = os.path.expanduser(credentials_path)
credentials_path = os.path.realpath(credentials_path)
# Check if the file exists
if not os.path.isfile(credentials_path):
    raise FileNotFoundError(f"Credentials file not found at {credentials_path}")
# Set the Google Application Credentials environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

# Set the default resampling method to LANCZOS
Image.RESAMPLING = Image.Resampling.LANCZOS
# Update MoviePy's resize function to use LANCZOS
def lanczos_resize(clip, newsize):
    return clip.resize(newsize, resample='lanczos')
# Replace MoviePy's default resize function
resize.resize = lanczos_resize


def text_to_speech(text, project_id, location, bucket_manager, language_code="en-US", voice_name="en-US-Wavenet-D"):
    tts_client = texttospeech.TextToSpeechLongAudioSynthesizeClient()

    try:
        input_file_name = f"input-{uuid.uuid4()}.txt"
        input_uri = bucket_manager.upload_string(text, input_file_name)

        parent = f"projects/{project_id}/locations/{location}"
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            name=voice_name
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16
        )
        output_file_name = f"output-{uuid.uuid4()}.wav"
        output_uri = f"gs://{bucket_manager.bucket_name}/{output_file_name}"

        request = texttospeech.SynthesizeLongAudioRequest(
            parent=parent,
            input=texttospeech.SynthesisInput(text=text),
            voice=voice,
            audio_config=audio_config,
            output_gcs_uri=output_uri
        )

        print("Sending request to Google Cloud Text-to-Speech API...")
        operation = tts_client.synthesize_long_audio(request=request)
        print("Waiting for operation to complete...")

        result = operation.result(timeout=300)  # 5-minute timeout
        print("Long audio synthesis completed.")

        # Download the audio file from GCS
        audio_content = bucket_manager.download_as_bytes(output_file_name)

        # Convert LINEAR16 WAV to MP3
        audio = AudioSegment.from_wav(io.BytesIO(audio_content))
        mp3_buffer = io.BytesIO()
        audio.export(mp3_buffer, format="mp3")
        mp3_content = mp3_buffer.getvalue()

        # Clean up: delete the input and output files
        bucket_manager.delete_file(input_file_name)
        bucket_manager.delete_file(output_file_name)

        return mp3_content

    except Exception as e:
        print(f"Error in text_to_speech: {str(e)}")
        raise

#compressing the video and reduces bitrate
def optimize_video(video_file, target_size_mb=50):
    print(f"Optimizing video: {video_file}")
    clip = VideoFileClip(video_file)
    
    # Calculate target bitrate
    duration = clip.duration
    target_total_bitrate = (target_size_mb * 8192) / duration
    
    # Assume audio bitrate of 128k and subtract from total bitrate
    target_video_bitrate = target_total_bitrate - 128
    
    print(f"Compressing video. Original size: {clip.w}x{clip.h}, fps: {clip.fps}")
    # Compress video in memory
    compressed_clip = clip.set_fps(min(clip.fps, 30)).resize(height=720)
    print(f"Compressed video size: {compressed_clip.w}x{compressed_clip.h}, fps: {compressed_clip.fps}")
    
    return compressed_clip, target_video_bitrate

def process_single_story(text, story_id, background_video, background_music, output_dir, project_id, location, bucket_manager, target_size_mb=50):
    print(f"Processing story ID: {story_id}")
    try:
        print(f"Generating audio for story ID: {story_id}. This may take a while for longer texts...")
        audio_content = text_to_speech(text, project_id, location, bucket_manager)
        print(f"Audio generation complete for story ID: {story_id}")

        # Save audio content to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio_file:
            temp_audio_file.write(audio_content)
            temp_audio_path = temp_audio_file.name

        print(f"Temporary audio file created: {temp_audio_path}")
        
        # Load audio from the temporary file
        narration_audio = AudioFileClip(temp_audio_path)
        print(f"Narration audio duration: {narration_audio.duration}")
        
        # Load background music
        background_music = AudioFileClip(background_music)
        
        # Adjust background music based on its duration
        if background_music.duration > narration_audio.duration:
            # If background music is longer, snip it
            adjusted_background_music = background_music.subclip(0, narration_audio.duration)
        else:
            # If background music is shorter or equal, loop it
            num_loops = int(narration_audio.duration / background_music.duration) + 1
            adjusted_background_music = concatenate_audioclips([background_music] * num_loops)
            adjusted_background_music = adjusted_background_music.subclip(0, narration_audio.duration)
        
        # Adjust the volume of the background music (e.g., reduce it to 20% of its original volume)
        background_music_volume = 0.2
        adjusted_background_music = adjusted_background_music.volumex(background_music_volume)
        
        # Combine narration and background music
        combined_audio = CompositeAudioClip([narration_audio, adjusted_background_music])
        
        # Load and optimize background video
        background, target_bitrate = optimize_video(background_video, target_size_mb)
        
        # Loop the background video to match audio duration
        looped_background = background.loop(duration=combined_audio.duration)
        print(f"Looped background duration: {looped_background.duration}")
        
        # Combine video and audio
        final_video = looped_background.set_audio(combined_audio)
        
        # Prepare output file path
        output_file = os.path.join(output_dir, f"intermediate_video_{story_id}.mp4")
        #print(f"Writing final video to: {output_file}")
        
        # Write the final video file
        final_video.write_videofile(output_file, 
                                    bitrate=f"{target_bitrate}k",
                                    audio_codec='aac', 
                                    audio_bitrate='128k',
                                    codec='libx264',
                                    preset='slow',
                                    threads=4)
        
        # Close clips to free up memory
        background.close()
        narration_audio.close()
        background_music.close()
        adjusted_background_music.close()
        combined_audio.close()
        final_video.close()
        
        # Remove the temporary audio file
        os.unlink(temp_audio_path)
        
        print(f"Completed processing for story ID: {story_id}")
        return output_file
    except Exception as e:
        print(f"Error processing story ID {story_id}: {str(e)}")
        print("Traceback:")
        traceback.print_exc()

def process_stories(csv_file_path, background_video, background_music, output_dir, project_id, location, bucket_manager, target_size_mb=50):
    df = pd.read_csv(csv_file_path)

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Processing stories"):
        story_text = row['Text']
        story_id = row['ID']

        output_file = process_single_story(story_text, story_id, background_video, background_music, output_dir, project_id, location, bucket_manager, target_size_mb)

        # intermediate video gets passed here
        video_path = output_file

        # prepare final output here
        output_video_path = os.path.join('final', f"final_vid_{story_id}.mp4")

        transcriber = VideoTranscriber('base', video_path)
        transcriber.extract_audio()
        transcriber.transcribe_video()
        transcriber.create_video(output_video_path)

