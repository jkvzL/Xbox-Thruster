from evdev import InputDevice, list_devices, categorize, ecodes, KeyEvent
from time import sleep
from gpiozero import LED

CENTER_TOLERANCE = 350
STICK_MAX = 65536
led = LED(10) # GPIO 10
led2 = LED(11) # GPIO 11
led3 = LED(12) # GPIO 12
led4 = LED(13) # GPIO 13
led5 = LED(14) # GPIO 14
led6 = LED(15) # GPIO 15

#On raspberrypi connected to xbox controller: list_devices()[0] = /dev/input/event8
xboxcontrol = InputDevice( list_devices()[0] )

axis = {
    ecodes.ABS_X: 'ls_x', # 0 - 65,536   the middle is 32768
    ecodes.ABS_Y: 'ls_y',
    ecodes.ABS_Z: 'rs_x',
    ecodes.ABS_RZ: 'rs_y',
    ecodes.ABS_BRAKE: 'lt', # 0 - 1023
    ecodes.ABS_GAS: 'rt',

    ecodes.ABS_HAT0X: 'dpad_x', # -1 - 1
    ecodes.ABS_HAT0Y: 'dpad_y'
}

center = {
    'ls_x': STICK_MAX/2,
    'ls_y': STICK_MAX/2,
    'rs_x': STICK_MAX/2,
    'rs_y': STICK_MAX/2
}

last = {
    'ls_x': STICK_MAX/2,
    'ls_y': STICK_MAX/2,
    'rs_x': STICK_MAX/2,
    'rs_y': STICK_MAX/2
}

#evdev polls the xbox controller in a loop
for event in xboxcontrol.read_loop():
    if event.type == ecodes.EV_KEY:
        pass
    elif event.type == ecodes.EV_ABS:
        if axis[ event.code ] in [ 'ls_x', 'ls_y', 'rs_x', 'rs_y' ]:
            last[ axis[ event.code ] ] = event.value

            value = event.value - center[ axis[ event.code ] ]

            if abs( value ) <= CENTER_TOLERANCE:
                value = 0

            if axis[ event.code ] == 'rs_x':
                if value < 0:
                    print('Stick Left')
                    led6.on()
                    led3.off()
                else:
                    print('Stick Right')
                    led3.on()
                    led6.off()
                print( value )

            elif axis[ event.code ] == 'ls_y':
                if value < 0:
                    print('Stick Forward')
                    led.on()
                    led2.on()
                    led4.off()
                    led5.off()
                else:
                    print('Stick Backward')
                    led.off()
                    led2.off()
                    led4.on()
                    led5.on()
                print( value )
