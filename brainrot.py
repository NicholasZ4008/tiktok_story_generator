from dotenv import load_dotenv
from functions import reddit_scraper
from functions import randomizer
from functions import video_processing
from functions.gcs_bucket_manager import BucketManager
from functions.garbage_collector import clean_folder, clean_file
import os

load_dotenv()

#scrape reddit
selected_subreddit = 'scarystories'
scraped_stories = reddit_scraper.scrape_subreddit(selected_subreddit,1)

#randomize video to use
csv_file_path = "reddit_scraped_data.csv"

bg_audio_path = os.path.join("media", "bg_audio")
bg_vids_path = os.path.join("media", "bg_vids")

random_background_music = randomizer.random_bg_audio(bg_audio_path)
random_background_video = randomizer.random_bg_vid(bg_vids_path)
output_directory = "intermediate_videos"
target_size_mb = 50  # You can adjust this value as needed

project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID')  # Replace with your actual project ID
location = os.getenv('GOOGLE_CLOUD_LOCATION') # Replace with your desired location

bucket_manager = BucketManager(project_id, location)

#process final video here
video_processing.process_stories(csv_file_path, random_background_video, random_background_music, output_directory, project_id, location, bucket_manager, target_size_mb)

#after refresh page, garbage collect?
# intermediate_folder = "intermediate_videos"
# final_folder = "final"

# clean_folder(intermediate_folder)
# clean_folder(final_folder)
# clean_file('reddit_scraped_data.csv')