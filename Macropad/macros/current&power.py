from adafruit_hid.keycode import Keycode

app={                    
    'name': 'Current and Power',     # Application name
    'macros' : [           # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
         # 1st row ----------
        (0x200000, '', ['']),
        (0x101010, 'CURRENT?', ['CURRENT?',Keycode.ENTER]),
        (0x200000, '', ['']),
        # 2nd row ----------
        (0x000020, '', ['']),
        (0x002100, 'POWER?', ['POWER?', Keycode.ENTER]),
        (0x303000, '', ['']),
        # 3rd row ----------
        (0x000040, '', ['']),
        (0x200000 ,'CTEMP?', ['CTEMP?', Keycode.ENTER]),
        (0x101010, '', ['']),
        # 4th row0x002000
        (0x004000, '', ['']),
        (0x003000, 'BACKSPACE', [Keycode.BACKSPACE]),
        (0x303000, '', [''])

        #Encoder button --
       # (0x000000, '', [Keycode.BACKSPACE])

    ]

}
