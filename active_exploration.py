"""
A script to facilitate active tactile exploration using a DIGIT sensor and GPT.
It allows GPT to send the user commands to control the DIGIT sensor.
The commands include exact movement and rotation of the sensor, which the user implements.
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
                prompt_file = f'{current_dir}/active/initial/prompt.txt'
            else:
                prompt_file = f'{current_dir}/active/initial/prompt_multi_choice.txt'

            # Get initial prompt as a string from the txt file
            with open(prompt_file, 'r') as f:
                initial_prompt = f.read()

            # Create the initial image file
            axis_file_path = f'{current_dir}/active/initial/digit_axis.jpg'
            file_id = shared_functions.create_file(client, axis_file_path)

            # Instead of appending entire initial prompt, just append a summary
            conversation_list.append(f'Initial {PROMPT_TYPE} prompt and axis image sent.')
            print('Sending initial prompt...')
            print('GPT is thinking...')

            # Create the response
            response = shared_functions.create_response(
                client, MODEL, initial_prompt, current_response_id, image_id=file_id)

            # Set the first_time flag to False
            first_time = False
        else:
            # Get user input
            user_input = input('You: ')

            # Respond to user input (including shortcuts)
            match user_input.lower():
                # Exit the loop and terminate and save the conversation
                case 'x':
                    print('Conversation terminated.')
                    save_dir = f'{current_dir}/active'
                    shared_functions.save_log(conversation_list, save_dir)
                    break
                # MOVE action shortcut
                case 'm':
                    user_prompt = 'MOVE action successfully executed.'
                # ROTATE action shortcut
                case 'r':
                    user_prompt = 'ROTATE action successfully executed.'
                # RESET action shortcut
                case 're':
                    user_prompt = 'RESET action successfully executed.'
                # CAPTURE action shortcut
                case 'c':
                    # Capture an image with the DIGIT sensor
                    save_dir = f'{current_dir}/active/captures'
                    frame_path = shared_functions.capture(dc, frame_counter, save_dir)
                    # Set file_id
                    file_id = shared_functions.create_file(client, frame_path)
                    # Extract filename from path
                    frame_filename = os.path.basename(frame_path)
                    # Append frame filename to user prompt
                    user_prompt = (
                        f'CAPTURE action successfully executed.\n'
                        f'captures/{frame_filename} attached.'
                    )
                    # Increment frame counter and set capture flag
                    frame_counter += 1
                    capture_response = True
                # Any other input is used as a normal prompt
                # Example if an action can't be executed, user will explain why.
                case _:
                    user_prompt = user_input

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
    if not os.path.exists(f'{current_dir}/active/captures'):
        os.makedirs(f'{current_dir}/active/captures')

    # Enter main loop
    chat_loop()

    # Disconnect the DIGIT sensor
    dc.disconnect()
