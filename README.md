
# Tiktok Story Generator

## Introduction

The **Tiktok Story Generator** is a Python-based automation tool for creating engaging Tiktok shorts. It leverages advanced APIs for speech recognition, text-to-speech conversion, and video editing. The project automates the process of video content generation, making it a valuable tool for content creators.

## Features

- **Speech-to-Text Conversion**: Converts speech input into editable text using Google Cloud Speech-to-Text API.
- **Text-to-Speech Generation**: Generates realistic voiceovers with the Google Cloud Text-to-Speech API.
- **Video Processing**: Edits and composes videos using FFmpeg and MoviePy Scripts
- **Randomization**: Adds creative random elements to enhance content originality.
- **Data Collection**: Gathers data from various sources, including Reddit scraping, to provide unique story ideas.

## Prerequisites

Before setting up the project, ensure you meet these requirements:

- Python 3.7 or later is installed.
- A Google Cloud account with the following APIs enabled:
  - Cloud Storage
  - Speech-to-Text
  - Text-to-Speech
- FFmpeg is installed on your system for video processing.

## Setup

Follow these steps to set up the project:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/tiktok_story_generator.git
   cd tiktok_story_generator
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Google Cloud credentials**:
   - Download your Google Cloud service account key file.
   - Create a `.env` file in the project root directory with the following content:
     ```
     GOOGLE_APPLICATION_CREDENTIALS_PATH=/path/to/your/service-account-key.json
     ```
   Replace `/path/to/your/service-account-key.json` with the actual path.

5. **Configure additional environment variables**:
   Add these variables to your `.env` file:
   ```
   PROJECT_ID=your-google-cloud-project-id
   BUCKET_NAME=your-gcs-bucket-name
   ```

## Usage

To generate a Tiktok story, run the main script:

```bash
python brainrot.py
```

Ensure you have your media files ready in the appropriate directories.

## Code Structure

- `brainrot.py`: Main script for orchestrating the entire video generation workflow.
- `auto_subtitle.py`: Automates subtitle generation for videos.
- `garbage_collector.py`: Cleans up temporary files to optimize resource usage.
- `gcs_bucket_manager.py`: Manages Google Cloud Storage interactions.
- `randomizer.py`: Adds random creative elements to generated content.
- `reddit_scraper.py`: Scrapes Reddit for story ideas and inspiration.
- `video_processing.py`: Handles video editing and processing tasks.

## Contributing

Contributions are welcome! If you'd like to contribute:

1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Submit a pull request with a clear description of the changes.

## License

This project is licensed under the Apache 2.0 License. See the `LICENSE` file for more details.
