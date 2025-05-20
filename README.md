# Reddit Story Generator

This project fetches hot posts from specified subreddits, processes them using AI to create a story and hook, generates a Reddit post image, and then creates a video with narration and subtitles using Minecraft gameplay footage.

## Prerequisites

*   Python 3.x
*   Ollama installed and running locally. Follow the instructions on the [Ollama website](https://ollama.ai/).

## Installation

1.  Clone the repository:

    ```bash
    git clone <repository_url>
    cd Reddit-Story-Generator
    ```

2.  Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3.  Create a `.env` file in the root directory of the project with your Reddit API credentials:

    ```env
    REDDIT_USERNAME=your_username
    REDDIT_PASSWORD=your_password
    CLIENT_ID=your_client_id
    CLIENT_SECRET=your_client_secret
    ```

4.  Place your Minecraft gameplay video files in the `minecraft-videos/` directory. The script randomly selects one of these videos.

## Usage

1.  Ensure Ollama is running (`ollama serve`).
2.  Run the main script:

    ```bash
    python app.py
    ```

3.  The script will fetch a hot post, process it, and generate output files.
4.  Follow the prompts in the terminal, including selecting a voice for the narration.

## Output

Generated videos will be saved in the `outputVideos/` directory.
Generated audio files will be saved in the `outputAudios/` directory.
The generated subtitle file will be `subtitles.srt`.

## Notes

*   The script relies on local files in `minecraft-videos/` for video backgrounds.
*   Ensure your `.env` file is correctly configured with valid Reddit API credentials. 