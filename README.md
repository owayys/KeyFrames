# KeyFrames

## Introduction

KeyFrames is an innovative tool utilizing the OpenAI GPT-4 API to enhance video understanding by extracting key frames, transcribing audio, and integrating user inputs to generate educational summaries. This system is designed to help users grasp the content of videos more effectively by providing a contextual summary based on the visual and textual data extracted from the video.

## System Overview

KeyFrames operates on a loop where the user uploads a video and a prompt, and the backend processes these inputs to generate a comprehensive summary. Here is a detailed breakdown of the process:

1. **Video Upload**: Users start by uploading a video (`USER_VIDEO`) along with a descriptive prompt (`USER_PROMPT`) outlining their specific needs or questions about the video.

2. **Video Processing**:

    - The backend receives `USER_VIDEO`.
    - Key frames (`FRAMES`) are extracted from `USER_VIDEO` to capture the most significant moments.
    - The audio track of the video is transcribed to text (`TRANSCRIPT`).

3. **Prompt Construction**:

    - `SYSTEM_PROMPT`: Utilizes OpenAI's standard prompt format.
    - `BACKEND_PROMPT`: A custom prompt created by our system, designed to guide the GPT-4 model. Example: "You are being supplied three things: Images from a video, a transcription from a video if available, and the user's prompt. Combine all of them to give an educational summary of the video."
    - `USER_PROMPT`: Directly supplied by the user to address specific queries or points of interest.

4. **Master Prompt Assembly**:

    - The final `MASTER_PROMPT` is composed by integrating the `SYSTEM_PROMPT`, `BACKEND_PROMPT`, the transcript (`TRANSCRIPT`), the user's question (`USER_PROMPT`), and the extracted frames (`FRAMES`). The format is as follows:
        ```
        SYSTEM_PROMPT
        BACKEND_PROMPT
        Use the following lines as transcript if not empty: TRANSCRIPT*
        The user asks: USER_PROMPT
        ```
        Attached frames are processed and incorporated into the GPT-4 request.

5. **Summary Generation**:

    - The `MASTER_PROMPT`, along with the attached key frames, is sent to the GPT-4 model.
    - GPT-4 generates an educational summary which integrates all provided data.

6. **Display Results**:
    - The generated summary is presented to the user on the frontend.
    - The process can be repeated as needed for additional videos.

## Technologies Used

-   **OpenAI GPT-4 API**: For processing and generating text based on the combined input of frames, transcription, and user prompts.
-   **Video Processing Libraries**: For frame extraction and video transcription.
-   **Web Frameworks**: (Specify frameworks like React, Flask, Django, etc., for frontend and backend development.)
-   **Cloud Services**: (Specify if using AWS, GCP, Azure, etc., for hosting and computing resources.)

## Installation and Setup

1. **Clone the repository**: Clone the project repository to your local machine.
2. **Install Python**: Ensure that you have Python 3.11 installed on your machine.
3. **Create a virtual environment (optional)**: It's a good practice to create a virtual environment for your Python projects. You can do this using the `venv` module:
    ```sh
    python3 -m venv env
    ```
    Activate the virtual environment:
    - On Windows:
        ```sh
        .\env\Scripts\activate
        ```
    - On Unix or MacOS:
        ```sh
        source env/bin/activate
        ```
4. **Install dependencies**: Navigate to the project directory and install the required dependencies using pip:
    ```sh
    pip install -r requirements.txt
    ```
5. **Set up environment variables**: Create a `.env` file at the project root and fill in the necessary variables. You'll need to provide your `OPENAI_API_KEY` and `ASSEMBLYAI_API_KEY`.
6. **Run the application**: You can start the application using the `uvicorn` server:
    ```sh
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```
    or by running `main.py`:
    ```sh
    python main.py
    ```
    The application should now be running at `http://localhost:8000`.

## Usage

(Provide a step-by-step guide on how to use the system, including how to upload a video, input a prompt, and view the generated summaries.)

1. **Upload a video**: Navigate to `http://localhost:8000`, and use the upload form to upload your video file.
2. **Research**: After uploading the video, click the "Research" button. You will see updates on your request within the log output box, after which a generated summary of your video will be displayed.
3. **Chat**: Chat with the model in context of the video using the chatbox at the bottom.

## License

This project is released under the MIT license.
