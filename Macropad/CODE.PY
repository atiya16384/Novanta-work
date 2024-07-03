import os  # Import the os module for file operations
import time  # Import the time module for delays
import displayio  # Import displayio for display management
import terminalio  # Import terminalio for terminal font
from adafruit_display_shapes.rect import Rect  # Import Rect for rectangle shapes on display
from adafruit_display_text import label  # Import label for text labels on display
from adafruit_macropad import MacroPad  # Import MacroPad for macropad functionality

# CONFIGURABLES ------------------------
MACRO_FOLDER = '/macros'  # Define the folder where macro files are stored

# FUNCTIONS ----------------------------

def initialize_display():
    """Initializes the display with empty labels and a title."""
    display_group = displayio.Group()  # Create a display group for managing display elements
    for key_index in range(12):  # Iterate over the 12 keys
        x = key_index % 3  # Calculate x position (column)
        y = key_index // 3  # Calculate y position (row)
        display_group.append(label.Label(
            terminalio.FONT, text='', color=0xFFFFFF,  # Create a label for each key
            anchored_position=((macropad.display.width - 1) * x / 2,
                               macropad.display.height - 1 - (3 - y) * 12),
            anchor_point=(x / 2, 1.0)
        ))
    display_group.append(Rect(0, 0, macropad.display.width, 12, fill=0xFFFFFF))  # Add a rectangle at the top
    display_group.append(label.Label(
        terminalio.FONT, text='MACROPAD', color=0x000000,  # Add a title label
        anchored_position=(macropad.display.width // 2, -2),
        anchor_point=(0.5, 0.0)
    ))
    macropad.display.show(display_group)  # Show the display group on the macropad display
    return display_group  # Return the display group

def load_applications():
    """Loads macro applications from the macros folder."""
    applications = []  # Initialize an empty list for applications
    for filename in sorted(os.listdir(MACRO_FOLDER)):  # Iterate over files in the macro folder
        if filename.endswith('.py') and not filename.startswith('._'):  # Check if the file is a Python file
            try:
                module = __import__(MACRO_FOLDER + '/' + filename[:-3])  # Import the module
                applications.append({
                    'name': module.app['name'],  # Add the app name to applications
                    'macros': module.app['macros']  # Add the macros to applications
                })
            except Exception as err:  # Catch any exceptions
                print(f"Error loading {filename}: {err}")  # Print error message
    return applications  # Return the list of applications

def read_file(filepath):
    """Reads a file and returns a list of its lines."""
    with open(filepath, 'r') as file:  # Open the file in read mode
        return [line.strip() for line in file]  # Read and return lines from the file

def write_file(filepath, content):
    """Writes content to a file."""
    with open(filepath, 'w') as file:  # Open the file in write mode
        file.write(content)  # Write the content to the file

def refresh_display(display_group, outputs):
    """Refreshes the display with updated outputs."""
    for i, text in enumerate(outputs):  # Iterate over the outputs
        display_group[i].text = text  # Update the text of each display label
    macropad.display.refresh()  # Refresh the macropad display
    macropad.pixels.show()  # Show the updated pixel colors

def process_sequence(sequence, is_pressed):
    """Processes the sequence of actions for key presses/releases."""
    if is_pressed:  # If the key is pressed
        for item in sequence:  # Iterate over the sequence
            if isinstance(item, int):  # If the item is an integer
                if item >= 0:
                    macropad.keyboard.press(item)  # Press the key
                else:
                    macropad.keyboard.release(-item)  # Release the key
            elif isinstance(item, float):  # If the item is a float
                time.sleep(item)  # Sleep for the specified duration
            elif isinstance(item, str):  # If the item is a string
                macropad.keyboard_layout.write(item)  # Write the string to the keyboard
            elif isinstance(item, list):  # If the item is a list
                for code in item:  # Iterate over the list
                    if isinstance(code, int):
                        macropad.consumer_control.release()  # Release consumer control
                        macropad.consumer_control.press(code)  # Press the consumer control key
                    elif isinstance(code, float):
                        time.sleep(code)  # Sleep for the specified duration
            elif isinstance(item, dict):  # If the item is a dictionary
                if 'buttons' in item:
                    if item['buttons'] >= 0:
                        macropad.mouse.press(item['buttons'])  # Press the mouse button
                    else:
                        macropad.mouse.release(-item['buttons'])  # Release the mouse button
                macropad.mouse.move(
                    item.get('x', 0),
                    item.get('y', 0),
                    item.get('wheel', 0)
                )  # Move the mouse
                if 'tone' in item:
                    if item['tone'] > 0:
                        macropad.stop_tone()  # Stop any existing tone
                        macropad.start_tone(item['tone'])  # Start the new tone
                    else:
                        macropad.stop_tone()  # Stop the tone
                elif 'play' in item:
                    macropad.play_file(item['play'])  # Play the specified file
    else:  # If the key is released
        for item in sequence:  # Iterate over the sequence
            if isinstance(item, int):
                macropad.keyboard.release(item)  # Release the key
            elif isinstance(item, dict):
                if 'buttons' in item:
                    macropad.mouse.release(item['buttons'])  # Release the mouse button
        macropad.consumer_control.release()  # Release consumer control

# INITIALIZATION -----------------------
macropad = MacroPad()  # Initialize the macropad
macropad.display.auto_refresh = False  # Disable auto-refresh for the display
macropad.pixels.auto_write = False  # Disable auto-write for the pixels

# Initialize display and load macros
display_group = initialize_display()  # Initialize the display
applications = load_applications()  # Load macro applications

if not applications:  # If no applications are found
    display_group[13].text = 'NO MACRO FILES FOUND'  # Display error message
    macropad.display.refresh()  # Refresh the display
    while True:  # Infinite loop
        pass  # Do nothing

app_index = 0  # Initialize the application index
current_app = applications[app_index]  # Set the current application

# MAIN LOOP ----------------------------
while True:  # Infinite loop
    position = macropad.encoder  # Get the encoder position
    new_app_index = position % len(applications)  # Calculate the new application index
    
    if new_app_index != app_index:  # If the application index has changed
        app_index = new_app_index  # Update the application index
        current_app = applications[app_index]  # Update the current application
        
        # Update LED colors based on the current application
        for i in range(12):  # Iterate over the 12 keys
            if i < len(current_app['macros']):
                macropad.pixels[i] = current_app['macros'][i][0]  # Set the pixel color
            else:
                macropad.pixels[i] = 0  # Turn off the pixel
        macropad.pixels.show()  # Show the updated pixels

    input_lines = read_file("macros/input.txt")  # Read the input file
    output_lines = read_file("macros/output.txt")  # Read the output file
    combined_output = [f"{inp} {out}" for inp, out in zip(input_lines, output_lines)]  # Combine input and output lines
    
    refresh_display(display_group, combined_output)  # Refresh the display with the combined output

    macropad.encoder_switch_debounced.update()  # Update the encoder switch state
    if macropad.encoder_switch_debounced.pressed:  # If the encoder switch is pressed
        key_number = 12  # Set the key number to 12 (encoder switch)
        is_pressed = True  # Set the pressed state to True
    else:
        event = macropad.keys.events.get()  # Get key events
        if not event or event.key_number >= len(current_app['macros']):  # If no event or invalid key number
            continue  # Skip the rest of the loop
        key_number = event.key_number  # Set the key number
        is_pressed = event.pressed  # Set the pressed state

    sequence = current_app['macros'][key_number][1]  # Get the macro sequence
    write_file("macros/input.txt", str(sequence))  # Write the sequence to the input file
    
    process_sequence(sequence, is_pressed)  # Process the sequence
    
    if not is_pressed and key_number < 12:  # If the key is released and valid
        macropad.pixels[key_number] = current_app['macros'][key_number][0]  # Update the pixel color
        macropad.pixels.show()  # Show the updated pixels
