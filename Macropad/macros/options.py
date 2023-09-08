
from adafruit_hid.keycode import Keycode
#To put the laser on and off
app={                           # REQUIRED dict, must be named 'app'
    'name' : 'ON OR OFF',  # Application name
    'macros' : [                # List of button macros...
                     
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x200000, 'ON', ['ON', Keycode.ENTER]),

        # 2nd row  ----------
        (0x004000, 'OFF', ['OFF', Keycode.ENTER]),


        # 3rd row ----------

        (0x002000, 'EQUALS', [Keycode.EQUALS]),
    

        # 4th row ----------
        (0x400000, 'ENTER', [Keycode.ENTER])
   

        #Encoder button ---
       # (0x000000, '', [Keycode.BACKSPACE])

    ]

}
