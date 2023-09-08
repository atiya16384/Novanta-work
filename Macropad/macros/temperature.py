
from adafruit_hid.keycode import Keycode 
app = {                             
    'name' : 'Temperature', # Application name
    'macros' : [                      # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x002000, 'LBO', ['']),
        (0x000030, 'LTEMP?', ['LTEMP?', Keycode.ENTER]),
        (0x002000, '', ['']),
        # 2nd row ----------
        (0x002000, 'Diode', ['']),
        (0x000030, 'DTEMP?', ['DTEMP?', Keycode.ENTER]),
        (0x202020, '', ['']),
        # 3rd row ----------
        (0x300000, 'VOA', ['']),
        (0x303000, 'VTEMP?', ['VTEMP?',Keycode.ENTER]),
        (0x002000, '', ['']),
        # 4th row ---------
        (0x002000, '', ['']),
        (0x303000, 'BACKSPACE', [Keycode.BACKSPACE]),
        (0x300000, '', [''])
        # Encoder button ---
        #(0x000000, '', [Keycode.BACKSPACE])
    ]
}
