from adafruit_hid.keycode import Keycode

app={                      # REQUIRED dict, must be named 'app'
    'name': 'VOAGOTO',     # Application name
    'macros' : [           # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
         # 1st row ----------
        (0x200000, '', ['']),
        (0x400000, 'VOAGOTOMIN', ['VOAGOTOMIN', Keycode.ENTER]),
        (0x000040, '', ['']),
        # 2nd row ----------
        (0x000020, '', ['']),
        (0x202000, 'VOAGOTOMAX', ['VOAGOTOMAX',Keycode.ENTER]),
        (0x000020, '', ['']),
        # 3rd row ----------
        (0x101010, '', ['']),
        (0x002000, 'BACKSPACE', [Keycode.BACKSPACE]),
        (0x002000, '', ['']),
        # 4th row0x002000
        (0x202000, '', ['']),
        (0x400000, 'EQUALS', [Keycode.EQUALS]),
        (0x202000, '', [''])

        #(0x000000, '', [Keycode.BACKSPACE])
    ]

}