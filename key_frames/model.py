import requests
from key_frames.utils import encode_images_in_folder


def mainGPT(video_dir, user_prompt, api_key):
    # Extract frames from video
    # Directory named after the video file
    # output_directory = os.path.splitext(video_path)[0]
    # if not os.path.exists(output_directory) or not os.listdir(output_directory):
    #     # Create directory if it doesn't exist
    #     os.makedirs(output_directory, exist_ok=True)
    #     extractor = VideoKeyFrameExtractor(video_path, output_directory)
    #     extractor.process_video()
    # else:
    #     print("Frames already extracted and available in directory.")

    # # Transcribe the audio
    # transcription_text = transcribe_audio(video_path)

    # Encode images to base64
    encoded_images = encode_images_in_folder(f"{video_dir}/frames")

    # Prepare headers for OpenAI API
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # System prompt
    system_prompt = "Please provide a summary of the video content."

    transcription_text = ""
    with open(f'{video_dir}/transcript.txt', 'r') as file:
        transcription_text = file.read()

    # Master prompt construction
    master_prompt = f"{system_prompt}, {user_prompt}, Additionally, here is the transcription of the video: {transcription_text}"

    # Initialize chat history
    chat_history = []
    chat_history.append({"role": "user", "content": master_prompt})
    # print(chat_history, "CHAT")
    # Send request for each image with the master prompt
    payload = {
        "model": "gpt-4-turbo",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": master_prompt},
                ]
            }
        ],
        "max_tokens": 300
    }

    for filename, image_64 in encoded_images.items():

        payload["messages"][0]["content"].append({"type": "image_url", "image_url": {
                                                 "url": f"data:image/jpeg;base64,{image_64}", "detail": "low"}})

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response_data = response.json()

    if response_data['error']:
        return response_data['error']

    chat_history.append(
        {"role": "AI", "content": response_data['choices'][0]['message']['content']})

    # Display chat history
    # for message in chat_history:
    #     print(f"AI: {message['content']}")
    return (chat_history)
