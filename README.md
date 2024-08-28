# Tiktok Story Generator

This project is a Python-based tool for generating automated Tiktok shorts, utilizing various APIs and libraries for speech recognition, text-to-speech, and video manipulation.

## Prerequisites

Before you begin, ensure you have met the following requirements:
* You have installed Python 3.7 or later
* You have a Google Cloud account and have set up a project with the necessary APIs enabled (Cloud Storage, Speech-to-Text, Text-to-Speech)
* You have FFmpeg installed on your system (required for video processing)

## Setup

Follow these steps to set up the project:

1. Clone the repository:
   ```
   git clone https://github.com/your-username/tiktok_story_generator.git
   cd tiktok_story_generator
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up your Google Cloud credentials:
   - Download your Google Cloud service account key file
   - Create a `.env` file in the project root directory with the following content:
     ```
     GOOGLE_APPLICATION_CREDENTIALS_PATH=/path/to/your/service-account-key.json
     ```
   Replace `/path/to/your/service-account-key.json` with the actual path to your key file.

5. Configure other environment variables:
   Add any other necessary environment variables to your `.env` file, such as:
   ```
   PROJECT_ID=your-google-cloud-project-id
   BUCKET_NAME=your-gcs-bucket-name
   ```

## Usage

To run the main script:

```
python brainrot.py
```

Make you have the appropriate media files as well!

## Contributing

If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## Licensing

Apache 2.0
