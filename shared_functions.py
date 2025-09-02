"""
A collection of shared functions used by active and simple active exploration scripts.

Author: Gemma McLean
Date: August 2025
"""


def capture(dc, frame_counter, save_dir):
    """
    Show the DIGIT live view and then capture and save a frame.

    Args:
        dc (DigitController): The DIGIT controller instance.
        frame_counter (int): The current frame counter.
        save_dir (str): The directory to save the captured frame.
    Returns:
        str: The path of the captured frame.
    """

    # Show live view to help user position sensor
    print('Showing live view. Hit ESC to close window.')
    dc.digit.show_view()
    # User hits ESC...
    dc.save_frame(save_dir, frame_counter)
    # Return the path of the captured frame
    return f'{save_dir}/frame_{frame_counter}.jpg'


def create_file(client, file_path):
    """
    Create a file with the OpenAI Files API.
    Taken from https://platform.openai.com/docs/

    Args:
        client (OpenAI): The OpenAI client instance.
        file_path (str): The path to the file to be created.
    Returns:
        str: The ID of the created file.
    """
    with open(file_path, 'rb') as file_content:
        result = client.files.create(
            file=file_content,
            purpose='vision',
        )
        return result.id


def create_response(client, model, message, current_response_id, image_id=None):
    """
    Create an OpenAI response for the user message with optional image file.

    Args:
        client (OpenAI): The OpenAI client instance.
        model (str): The model to use for the response.
        message (str): The user message.
        current_response_id (str): The ID of the current response.
        image_id (str, optional): The ID of the image file.

    Returns:
        Response: The created response object.
    """

    # If no image is provided
    if image_id is None:
        # Create a text-only response
        content = [{'type': 'input_text', 'text': message}]
    # If an image is provided
    else:
        # Create a response with both text and image
        content = [
            {'type': 'input_text', 'text': message},
            {'type': 'input_image', 'file_id': image_id},
        ]
    # Build and return the response
    response = client.responses.create(
        model=model,
        input=[{
            'role': 'user',
            'content': content
        }],
        previous_response_id=current_response_id
    )
    return response


def save_log(conversation_list, save_dir):
    """
    Save the conversation log list to a text file.

    Args:
        conversation_list (list): The list of conversation strings.
        save_dir (str): The directory to save the conversation log.
    """

    with open(f'{save_dir}/conversation.txt', 'w') as f:
        for line in conversation_list:
            f.write(f'{line}\n-----\n')
