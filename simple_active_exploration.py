"""
A script to facilitate simple active tactile exploration using a DIGIT sensor and GPT.
It allows GPT to send the user instructions to control the DIGIT sensor.
It receives feedback from the user and captured tactile images.
It attempts to classify the object based on the captured images.

Note: the results folder contains collected outputs and collected captures.
This folder was manually populated after each execution of the script.

Author: Gemma McLean
Date: August 2025
"""

from digit_controller import DigitController
import os
from openai import OpenAI
import shared_functions

MODEL = 'gpt-5-mini'
PROMPT_TYPE = 'multi-choice'  # Can be multi-choice or open-ended


def chat_loop():
    """Main loop for handling user input and generating responses."""

    # Initialise previous_response_id to None for the first interaction
    current_response_id = None

    # Initialise variables
    conversation_list = []
    first_time = True
    capture_response = False
    frame_counter = 1

    # Run until user exits
    while True:
        # When running for the first time, send the initial prompt
        if first_time:
            # Determine the prompt file based on the prompt type
            if PROMPT_TYPE == 'open-ended':
                prompt_file = f'{current_dir}/simple_active/initial/prompt.txt'
            else:
                prompt_file = f'{current_dir}/simple_active/initial/prompt_multi_choice.txt'

            # Get initial prompt as a string from the txt file
            with open(prompt_file, 'r') as f:
                initial_prompt = f.read()

            # Create initial capture
            save_dir = f'{current_dir}/simple_active/captures'
            frame_path = shared_functions.capture(dc, frame_counter, save_dir)
            file_id = shared_functions.create_file(client, frame_path)

            # Instead of appending entire initial prompt, just append a summary
            conversation_list.append(
                f'Initial {PROMPT_TYPE} prompt and initial tactile image sent.')
            print('Sending initial prompt...')
            print('GPT is thinking...')

            # Create the response
            response = shared_functions.create_response(
                client, MODEL, initial_prompt, current_response_id, image_id=file_id)

            # Increment frame counter and set capture flag
            frame_counter += 1
            capture_response = True

            # Set the first_time flag to False
            first_time = False
        else:
            # Get user input
            user_input = input('You: ')

            # Respond to user input
            if user_input.lower() == 'x':
                # Exit the loop and terminate and save the conversation
                print('Conversation terminated.')
                save_dir = f'{current_dir}/simple_active'
                shared_functions.save_log(conversation_list, save_dir)
                break
            elif user_input.lower().startswith('#'):
                # Send message without image
                user_prompt = user_input
            else:
                # Capture an image with the DIGIT sensor
                save_dir = f'{current_dir}/simple_active/captures'
                frame_path = shared_functions.capture(dc, frame_counter, save_dir)
                # Set file_id
                file_id = shared_functions.create_file(client, frame_path)
                # Extract filename from path
                frame_filename = os.path.basename(frame_path)
                # Append user input with image path
                user_prompt = user_input + '\n' + f'captures/{frame_filename} attached.'
                # Increment frame counter and set capture flag
                frame_counter += 1
                capture_response = True

            # Append user prompt to conversation list
            conversation_list.append(user_prompt)

            print('GPT is thinking...')

            # If it was a capture action
            if capture_response:
                # Create the response with the image file
                response = shared_functions.create_response(
                    client, MODEL, user_prompt, current_response_id, image_id=file_id)
                # Reset the flag
                capture_response = False
            # If it was any other input
            else:
                # Create the response with just text
                response = shared_functions.create_response(
                    client, MODEL, user_prompt, current_response_id)

        # Update the current_response_id
        current_response_id = response.id

        # Print the response
        print('GPT: ', response.output_text)
        # Append the response to the conversation list
        conversation_list.append(response.output_text)


# Setup DIGIT sensor
dc = DigitController()

# If the DIGIT sensor is connected
if dc.digit is not None:
    # Set the stream to QVGA 30fps
    dc.set_qvga_30fps()

    # Initialise OpenAI client
    client = OpenAI()

    # Get current directory of this script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Create captures folder if it doesn't exist
    if not os.path.exists(f'{current_dir}/simple_active/captures'):
        os.makedirs(f'{current_dir}/simple_active/captures')

    # Enter main loop
    chat_loop()

    # Disconnect the DIGIT sensor
    dc.disconnect()
