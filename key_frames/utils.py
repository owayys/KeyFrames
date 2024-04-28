import string
import base64
import os


def preprocess_text(text):
    # Convert text to lowercase
    lowercased_text = text.lower()

    # Remove punctuation using translate and string.punctuation
    translator = str.maketrans('', '', string.punctuation)
    no_punctuation_text = lowercased_text.translate(translator)

    return no_punctuation_text


def encode_images_in_folder(folder_path):
    """Encode all images in a folder to base64."""
    encoded_images = {}
    for image_file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, image_file)
        if image_file.lower().endswith((".png", ".jpg", ".jpeg")):
            with open(file_path, "rb") as image:
                encoded_images[image_file] = base64.b64encode(
                    image.read()).decode('utf-8')
    return encoded_images
