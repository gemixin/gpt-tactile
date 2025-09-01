from digit_interface.digit import Digit
from digit_interface.digit_handler import DigitHandler


class DigitController:
    """
    A controller class for managing basic DIGIT device connection and operations.

    Author: Gemma McLean
    Date: August 2025
    """

    def __init__(self):
        """
        Initialise the DigitController to manage DIGIT connections and streams.
        Auto connects to the first available DIGIT device.
        """

        # Connect and store the instance and serial number
        self.digit = self._connect_to_digit()

    # --- Private helpers ---
    def _check_for_digits(self):
        """
        Check for connected DIGIT devices.

        Returns:
            list: A list of dictionaries containing DIGIT device information.
            None: If no DIGIT devices are found.
        """

        digits = DigitHandler.list_digits()
        if digits:
            return digits
        return None

    def _connect_to_digit(self):
        """
        Connect to the first available DIGIT device.

        Returns:
            tuple: A tuple containing the DIGIT instance and its serial number.
            digit: The connected DIGIT instance or None if not connected.
        """

        digits = self._check_for_digits()
        if digits:
            try:
                # Get the first digit's serial number
                serial = digits[0]['serial']
                # Create a Digit instance with the serial number
                digit = Digit(serial, 'Single_Digit')
                # Connect to the DIGIT device
                digit.connect()
                print(f'Connected to DIGIT with serial number: {serial}')
                # Return the device instance
                return digit
            except Exception as e:
                print(f'Failed to connect to DIGIT: {e}')
                return None
        else:
            print('No DIGIT devices found.')
            return None

    def set_qvga_30fps(self):
        """Set the DIGIT device stream to QVGA resolution at 30 FPS."""

        if self.digit:
            # Set stream resolution and fps
            # QVGA resolution
            self.digit.set_resolution({'resolution': {'width': 320, 'height': 240}})
            # 30 FPS
            self.digit.set_fps(Digit.STREAMS['QVGA']['fps']['30fps'])
            print('Set stream to QVGA 30fps.')
        else:
            print('No DIGIT device connected. Cannot set stream.')

    def save_frame(self, save_dir, frame_num):
        """
        Save the current video frame from the DIGIT device as a jpg.

        Args:
            save_dir (str): The directory to save the frame.
            frame_num (int): The frame number to save.
        """

        if self.digit:
            self.digit.save_frame(f'{save_dir}/frame_{frame_num}.jpg')
            print(f'Saved {save_dir}/frame_{frame_num}.jpg')
        else:
            print('No DIGIT device connected. Cannot save frame.')

    def disconnect(self):
        """Disconnect the DIGIT device."""

        if self.digit:
            try:
                self.digit.disconnect()
            except Exception as e:
                print(f'Failed to disconnect DIGIT: {e}')
