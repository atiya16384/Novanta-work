

from adafruit_hid.keycode import Keycode

app = {                
    'name' : 'Numpad', # Application name
    'macros' : [       # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x200000 ,'7', ['7']),
        (0x202000, '8', ['8']),
        (0x000040, '9', ['9']),
        # 2nd row ----------
        (0x202000, '4', ['4']),
        (0x800000, '5', ['5']),
        (0x202000, '6', ['6']),
        # 3rd row ----------
        (0x000040, '1', ['1']),
        (0x202000, '2', ['2']),
        (0x303000, '3', ['3']),
        # 4th row ----------
        (0x101010, '*', ['*']),
        (0x800000, '0', ['0']),
        (0x000040, '#', ['#'])
        # Encoder button ---
       #(0x000000, '', [Keycode.BACKSPACE])
    ]
}
