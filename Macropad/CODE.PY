import os
import time
import displayio
import terminalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
from adafruit_macropad import MacroPad

# CONFIGURABLES ------------------------

MACRO_FOLDER = '/macros'


# CLASSES AND FUNCTIONS ----------------

class App:
    def __init__(self, appdata):
        self.name = appdata['name']
        self.macros = appdata['macros']
    
    def getname(self):
        return self.name

    # this is in the app class
    def mapping(self):

        output_group=displayio.Group()
        for key_index in range(12):
            x = key_index % 2
            y = key_index // 2
            output_group.append(label.Label(terminalio.FONT, text='', color=0xFFFFFF,
                                    anchored_position=((macropad.display.width ) * x /2,
                                                        macropad.display.height - (3-y)*12), 
                                    anchor_point=(x/8, 1.0)))# label.Label is used to display something to the screen
       # output_group.append(Rect(0, 0, macropad.display.width, 12, fill=0xFFFFFF)) # this is for the box at the top
        output_group.append(label.Label(terminalio.FONT, text='', color=0x000000,
                                anchored_position=(macropad.display.width//2, 2),
                                anchor_point=(0.0, 0.0)))# this is for the label at the top
        macropad.display.show(output_group)

        for x in range(len(output)):
            output_group[x].text=self.output[x]
        

        macropad.display.refresh()
        macropad.pixels.show()

        
    def set_output(self,output):
        self.output=output
        self.mapping()
    

        #  for x in self.output_dictionary.keys():
        #     macropad.pixels[x]=self.output_dictionary_keys[x]
        #     output_group[x].text=self.output_dictionary_keys[x]

    #     macropad.display.refresh()
    #     macropad.pixels.show()

    #     for y in self.output_dictionary.values():
    #         macropad.pixels[y] = self.output_dictionary_values[y]
    #         input_group[y].text = self.output_dictionary_keys[y]

    #     macropad.display.refresh().
    #     macropad.pixels.show()

    def switch(self):
        group[13].text = self.name.upper()  # Application name
        for i in range(12):
            if i < len(self.macros): # Key in use, set label + LED color
                macropad.pixels[i] = self.macros[i][0]
                group[i].text = self.macros[i][1]
            else:  # Key not in use, no label or LED
                macropad.pixels[i] = 0
                group[i].text = ''
        macropad.keyboard.release_all()
        macropad.consumer_control.release()
        macropad.mouse.release_all()
        #macropad.stop_tone()
        macropad.pixels.show()
        macropad.display.refresh()


# INITIALIZATION -----------------------

macropad = MacroPad()
macropad.display.auto_refresh = False
macropad.pixels.auto_write = False


group = displayio.Group()

# we need to make this display just for the apps object
# put this in a function and call it at a specific time/point
for key_index in range(12):
    x = key_index % 3
    y = key_index // 3
    group.append(label.Label(terminalio.FONT, text='', color=0xFFFFFF,
                             anchored_position=((macropad.display.width - 1) * x / 2,
                                                macropad.display.height - 1 -
                                                (3 - y) * 12),
                             anchor_point=(x / 2, 1.0)))
group.append(Rect(0, 0, macropad.display.width, 12, fill=0xFFFFFF))
group.append(label.Label(terminalio.FONT, text='', color=0x000000,
                         anchored_position=(macropad.display.width//2, -2),
                         anchor_point=(0.5, 0.0)))
macropad.display.show(group) # this actually displays the commands &outputs to the screenC

# otherwise we use a different display
# without it nothing would show up



# if we add this the pixels do not show
# output_group=displayio.Group()
# for key_index in range(12):
#     x = key_index % 1
#     y = key_index // 3
#     output_group.append(label.Label(terminalio.FONT, text='', color=0xFFFFFF,
#                             anchored_position=((macropad.display.width - 5) * x / 5,
#                                                 macropad.display.height - 1 - (3-y)*12),
#                             anchor_point=(x/2, 1.0)))# label.Label is used to display something to the screen
# output_group.append(Rect(0, 0, macropad.display.width, 8, fill=0xFFFFFF)) # this is for the box at the top
# output_group.append(label.Label(terminalio.FONT, text='', color=0x000000,
#                         anchored_position=(macropad.display.width//10, -2),
#                         anchor_point=(0.5, 0.0)))# this is for the label at the top
# macropad.display.show(output_group)

# #display the outputs on the left of the screen and the middle of the macroapd screen
# input_group=displayio.Group()
# for key_index in range(4):
# #     x = key_index % 2
# #     y = key_index // 3
# #     input_group.append(label.Label(terminalio.FONT, text='', color=0xFFFFFF,
# #                             anchored_position=((macropad.display.width - 5) * x / 5,
# #                                                 macropad.display.height - 1 - (3-y)*12 ),
# #                             anchor_point=(x/2, 1.0)))# label.Label is used to display something to the screen
# # input_group.append(Rect(0, 0, macropad.display.width, 8, fill=0xFFFFFF)) # this is for the box at the top
# # input_group.append(label.Label(terminalio.FONT, text='', color=0x000000,
# #                         anchored_position=(macropad.display.width//10, -2),
# #                         anchor_point=(0.5, 0.0))) # this is for the label at the top
# # macropad.display.show(input_group)



# Load all the macro key setups from .py files in MACRO_FOLDER
apps = []
files = os.listdir(MACRO_FOLDER)
files.sort()
for filename in files:
    if filename.endswith('.py') and not filename.startswith('._'):
        try:
            module = __import__(MACRO_FOLDER + '/' + filename[:-3])
            apps.append(App(module.app))
        except (SyntaxError, ImportError, AttributeError, KeyError, NameError,
                IndexError, TypeError) as err:
            print("ERROR in", filename)
            import traceback
            traceback.print_exception(err, err, err.__traceback__)
    
if not apps:
    group[13].text = 'NO MACRO FILES FOUND'
    macropad.display.refresh()
    while True:
        pass

last_position = None
last_encoder_switch = macropad.encoder_switch_debounced.pressed
app_index = 0
apps[app_index].switch()




# MAIN LOOP ----------------------------

while True:
    position = macropad.encoder
    app_index = position % len(apps)
    if position != last_position:
        #app_index = position % len(apps)
        
        apps[app_index].switch()
        last_position=position
        output_group=displayio.Group()
        for key_index in range(12):
            x = key_index % 2
            y = key_index // 2
            output_group.append(label.Label(terminalio.FONT, text='', color=0xFFFFFF,
                                    anchored_position=((macropad.display.width ) * x /2,
                                                        macropad.display.height - (3-y)*12), # we edit this part to move the output upwards
                                    anchor_point=(x/8, 1.0)))# label.Label is used to display something to the screen
        # output_group.append(Rect(0, 0, macropad.display.width, 12, fill=0xFFFFFF)) # this is for the box at the top
        output_group.append(label.Label(terminalio.FONT, text='', color=0x000000,
                            anchored_position=(macropad.display.width//2, 2),
                            anchor_point=(0.0, 0.0)))# this is for the label at the top
        macropad.display.show(output_group)
       
    current_app=apps[app_index]

    input=[]
    # input list stores the commands
    file_name=open("macros/input.txt", "r")
    input_lines=file_name.readlines()
    for input_line in range(len(input_lines)):
        input.append(input_lines[input_line].strip('\n'))
    
    # info list stores the numbers
    info=[] # append an input with an output from the output list
    file=open("macros/output.txt", "r")
    lines=file.readlines()
    for line in range(len(lines)):
        info.append(lines[line].strip('\n'))

    output=list()
    for i in range(len(info)):
        output.append(input[i])
        output.append(info[i])
    

    group = displayio.Group()


    for key_index in range(12):
        x = key_index % 3
        y = key_index // 3
        group.append(label.Label(terminalio.FONT, text='', color=0xFFFFFF,
                                anchored_position=((macropad.display.width - 1) * x / 2,
                                                    macropad.display.height - 1 -
                                                    (3 - y) * 12),
                                anchor_point=(x / 2, 1.0)))
    group.append(Rect(0, 0, macropad.display.width, 12, fill=0xFFFFFF))
    group.append(label.Label(terminalio.FONT, text='', color=0x000000,
                            anchored_position=(macropad.display.width//2, -2),
                            anchor_point=(0.5, 0.0)))
    macropad.display.show(group)


    # we have the specific command from the keyboard

    # print(input)
    
    # info=[] # append an input with an output from the output list
    # file=open("macros/output.txt", "r")
    # lines=file.readlines()
    # for line in range(len(lines)):
    #     info.append(lines[line].strip('\n'))
    
    #current_app.set_info(info.mapping)
    # info.mapping()

    # we are passing the info list and assigning it to test

    # output_dictionary={}
    # output=current_app.getname()
    # output_dictionary[output]={}
    # output_dictionary[output][input]=output
    # print(output_dictionary)
    # output_dictionary.mapping()
    
    # we have the current command
    #print(current_app.getname()) # name of current macro file

    macropad.encoder_switch_debounced.update()
    encoder_switch = macropad.encoder_switch_debounced.pressed
    if encoder_switch != last_encoder_switch:
        last_encoder_switch = encoder_switch
        if len(apps[app_index].macros) < 13:
            continue   
        key_number = 12 
        pressed = encoder_switch
    else:
        event = macropad.keys.events.get()
        if not event or event.key_number >= len(apps[app_index].macros):
            continue # No key events, or no corresponding macro, resume loop
        key_number = event.key_number
        pressed = event.pressed # we have pressed the key 
    group = displayio.Group()


    for key_index in range(12):
        x = key_index % 3
        y = key_index // 3
        group.append(label.Label(terminalio.FONT, text='', color=0xFFFFFF,
                                anchored_position=((macropad.display.width - 1) * x / 2,
                                                    macropad.display.height - 1 -
                                                    (3 - y) * 12),
                                anchor_point=(x / 2, 1.0)))
    group.append(Rect(0, 0, macropad.display.width, 12, fill=0xFFFFFF))
    group.append(label.Label(terminalio.FONT, text='', color=0x000000,
                            anchored_position=(macropad.display.width//2, -2),
                            anchor_point=(0.5, 0.0)))
    macropad.display.show(group)
    # If code reaches here, a key or the encoder button WAS pressed/released
    # and there IS a corresponding macro available for it...other situations
    # are avoided by 'continue' statements above which resume the loop.
    sequence = apps[app_index].macros[key_number][1] # we define a sequence of elements to be a list
    # 'sequence' is an arbitrary-length list, each item is one of:
        # Positive integer (e.g. Keycode.KEYPAD_MINUS): key pressed
        # Negative integer: (absolute value) key released
        # Float (e.g. 0.25): delay in seconds
        # String (e.g. "Foo"): corresponding keys pressed & released
        # List []: one or more Consumer Control codes (can also do float delay)
        # Dict {}: mouse buttons/motion (might extend in future)
    input_file=open("macros/input.txt", "w")
    input_file.write(sequence)
    file.close()
    print(sequence)
    if pressed:
        if key_number < 12: # No pixel for encoder button
            # we assign the pixels to a key on the macropad
            # we display the pixels to the macropad screen
            #we display the accompanying colour on the keys 
            macropad.pixels[key_number] = 0xFFFFFF
            macropad.pixels.show()
        for item in sequence:
            # for evert command in the sequence
            if isinstance(item, int):
                if item >= 0:
                    macropad.keyboard.press(item)
                else:
                    macropad.keyboard.release(-item)
            elif isinstance(item, float): # a floating-point number inserts a pause in the key pressing sequence
                time.sleep(item)
            elif isinstance(item, str):
                macropad.keyboard_layout.write(item)
            elif isinstance(item, list): #consumer control codes are just integers, so they are of type int
                for code in item:  
                    if isinstance(code, int): 
                        macropad.consumer_control.release()
                        macropad.consumer_control.press(code)
                    if isinstance(code, float):
                        time.sleep(code)
            # For mouse-related actions like movement and button clicks, your macro file should first import the HID Mouse module. 
            #A mouse is a more complex thing, with spatial axes in addition to buttons. A bracketed list won’t do…we have to step this up to a full Python dictionary,
            elif isinstance(item, dict):
                # the dictionary key can be one of four values 'x', 'y',
                if 'buttons' in item: # button click
                    if item['buttons'] >= 0:
                        macropad.mouse.press(item['buttons'])
                    else:
                        macropad.mouse.release(-item['buttons'])
                macropad.mouse.move(item['x'] if 'x' in item else 0,
                                    item['y'] if 'y' in item else 0,
                                    item['wheel'] if 'wheel' in item else 0)
                if 'tone' in item:
                    if item['tone'] > 0:
                        macropad.stop_tone()
                        macropad.start_tone(item['tone'])
                    else:
                        macropad.stop_tone()
                elif 'play' in item:
                    macropad.play_file(item['play'])
        
        
    else:
        for item in sequence:
            if isinstance(item, int):
                if item >= 0:
                    macropad.keyboard.release(item)
            elif isinstance(item, dict):
                if 'buttons' in item:
                    if item['buttons'] >= 0:
                        macropad.mouse.release(item['buttons'])
                # elif 'tone' in item:
                #     macropad.stop_tone()
        macropad.consumer_control.release()
        if key_number < 12: # No pixel for encoder button
            macropad.pixels[key_number] = apps[app_index].macros[key_number][0]
            macropad.pixels.show()
    # once we have pressed action 



    current_app.set_output(output)












        