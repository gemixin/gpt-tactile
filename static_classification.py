"""
A script to evaluate static tactile image classification with the OpenAI API.
It sends GPT a collection of 6 tactile images for each object (images folder).
It will do this for both prompt types (multi-choice and open-ended).
It will store the classification predictions in a list and save them to a text file.

Note: the results folder contains collected outputs and a csv file summary.
This folder was manually populated after each execution of the script.

Author: Gemma McLean
Date: August 2025
"""

from openai import OpenAI
import os
import shared_funcs

MODEL = 'gpt-5-mini'


def get_file_paths(dir, exts):
    """
    Return a list of paths of all files within the given directory with the given
    extensions.

    Args:
        dir (str): The directory to search for files.
        exts (tuple): The file extensions to filter by.

    Returns:
        list: A list of file paths.
    """

    # Get a list of all files in the directory
    all_files = os.listdir(dir)

    # Filter the list to include only files with the given extensions
    matching_files = [f for f in all_files if f.endswith(exts)]

    # Return the full paths of the matching files
    return [os.path.join(dir, f) for f in matching_files]


# Initialise OpenAI client
client = OpenAI()

# Empty list to store outputs
outputs = []

# Get current directory of this script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get all directory paths from inside images folder
image_dirs = []
for img_dir in os.listdir(f'{current_dir}/static/images'):
    if os.path.isdir(os.path.join(f'{current_dir}/static/images', img_dir)):
        image_dirs.append(os.path.join(f'{current_dir}/static/images', img_dir))
# Sort alphabetically
image_dirs.sort()

# Get all txt files from inside prompts folder
prompts_txt_files = get_file_paths(f'{current_dir}/static/initial', ('.txt'))

# For each prompt type
for prompt_type in prompts_txt_files:
    # For each image directory (i.e. for each object)
    for image_dir in image_dirs:
        # Get prompt as a string from the txt file
        with open(prompt_type, 'r') as f:
            prompt = f.read()

        # Get all object image paths
        object_img_paths = get_file_paths(image_dir, ('.jpg', '.jpeg', '.png'))
        content = [
            {'type': 'input_text', 'text': prompt},
        ]

        # Create a file for each object image and append to content
        for img_path in object_img_paths:
            file_id = shared_funcs.create_file(client, img_path)
            content.append({
                'type': 'input_image',
                'file_id': file_id,
            })

        # Create a response with the prompt and image files
        response = client.responses.create(
            model=MODEL,
            input=[{
                'role': 'user',
                'content': content,
            }],
        )

        # Print and store the output
        output = f'Prompt type: {os.path.basename(prompt_type)} \n'
        output += f'Image directory: {os.path.basename(image_dir)} \n'
        output += f'GPT: {response.output_text} \n'
        output += '\n---\n'
        print(output)
        outputs.append(output)

# Save outputs to outputs.txt locally
with open(f'{current_dir}/outputs.txt', 'w') as f:
    f.writelines(outputs)
