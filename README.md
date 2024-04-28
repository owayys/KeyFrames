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

- **OpenAI GPT-4 API**: For processing and generating text based on the combined input of frames, transcription, and user prompts.
- **Video Processing Libraries**: For frame extraction and video transcription.
- **Web Frameworks**: (Specify frameworks like React, Flask, Django, etc., for frontend and backend development.)
- **Cloud Services**: (Specify if using AWS, GCP, Azure, etc., for hosting and computing resources.)

## Installation and Setup

(Provide detailed steps on setting up the local development environment or deploying the application to a production environment. Include commands, environment variables, and necessary configuration files.)

## Usage

(Provide a step-by-step guide on how to use the system, including how to upload a video, input a prompt, and view the generated summaries.)

## Contributing

We welcome contributions from the community. Please refer to our contribution guidelines for more information on how to submit issues, make pull requests, and more.

## License

(Specify the license under which this project is released, e.g., MIT, GPL, etc.)