# This isn't complete because I couldn't yet find out how to use the IO expander with kmk. (And also I think I need the ToF distance sensor to test before being able to write any working code for it).
# Basically, the keyboard will have 4 sets of 8 macros, and the left rotary encoder will switch between those.
# The other rotary encoder will switch between what the ToF distance sensor controls (screen brightness, audio volume, keyboard brightness, off) (you raise/lower your hand over the sensor to control the currently selected setting). I think this will probably need something running on the computer as well.
# The OLED will simply display both of these states controlled by the rotary encoders.


# Pins:
# GPIO26 (XIAO) - LED 1
# GPIO27 (XIAO) - LED 2
# GPB0 to GPB3 (IO expander) - Keys 1 to 4 
# GPIO1 to GPIO4 (XIAO) - Keys 5 to 8
# GPB4 (IO expander) - Rotary encoder 1 push switch
# GPB5 and GPB6 (IO expander) - Rotary encoder 1
# GPA0 (IO expander) - Rotary encoder 2 push switch
# GPA1 and GPA2 (IO expander) - Rotary encoder 2

# I2C (SDA GPIO6, SCL GPIO7) - OLED display & IO expander

# I don't know how to get stubs for CircuitPython libraries, so hopefully most of the uses of these are correct and not from some other library
import board
import digitalio
import adafruit_ssd1306
from kmk.modules.encoder import EncoderHandler
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.modules.macros import Press, Release, Tap, Macros
from kmk.modules.layers import Layers

i2c = board.I2C()
try:
    oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
    oled_available = True
except:
    print("OLED not found")
    oled_available = False

keyboard = KMKKeyboard()

layers = Layers()
macros = Macros()
encoder_handler = EncoderHandler() # TODO this should be given the pins somewhere
keyboard.modules = [layers, macros, encoder_handler]

current_layer = 0
layer_names = ["General", "Dev", "Media", "Custom"]

led1 = digitalio.DigitalInOut(board.D26)
led1.direction = digitalio.Direction.OUTPUT
led2 = digitalio.DigitalInOut(board.D27)
led2.direction = digitalio.Direction.OUTPUT

# For now, using only XIAO pins for all 8 keys
PINS = [board.D1, board.D2, board.D3, board.D4, board.D8, board.D9, board.D10, board.D11]

keyboard.matrix = KeysScanner(
    pins=PINS,
    value_when_pressed=False,
)

keyboard.keymap = [
    # General
    [
        KC.LCTRL(KC.C),
        KC.LCTRL(KC.V),
        KC.LCTRL(KC.Z),
        KC.LCTRL(KC.Y),
        KC.LCTRL(KC.A),
        KC.LCTRL(KC.F),
        KC.LCTRL(KC.S),
        KC.LCTRL(KC.T),
    ],
    # Dev
    [
        KC.LCTRL(KC.LALT(KC.T)), # terminal on linux
        KC.F5,
        KC.LCTRL(KC.LSHIFT(KC.B)), # build in some IDEs
        KC.LCTRL(KC.SLASH),
        KC.LSHIFT(KC.LALT(KC.F)), # or whatever format is
        KC.F12,
        KC.F2,
        KC.LCTRL(KC.DOT),
    ],
    # Media
    [
        KC.MEDIA_PLAY_PAUSE,
        KC.MEDIA_NEXT_TRACK,
        KC.MEDIA_PREV_TRACK,
        KC.AUDIO_MUTE,
        KC.AUDIO_VOL_UP,
        KC.AUDIO_VOL_DOWN,
        KC.BRIGHTNESS_UP,
        KC.BRIGHTNESS_DOWN,
    ],
    # Custom (random text, etc., would need to be customized)
    [
        KC.MACRO("Hello World!"),
        KC.MACRO("your.email@example.com"),
        KC.MACRO("+1234567890"),
        KC.MACRO("Best regards,\n<some name>"),
        KC.MACRO("Thank you!"),
        KC.MACRO("say something common"),
        KC.MACRO("something else"),
        KC.MACRO("and another thing"),
    ]
]

def update_display():
    if not oled_available:
        return
        
    oled.fill(0)
    oled.text(f"Layer: {layer_names[current_layer]}", 0, 0, 1)
    oled.text(f"({current_layer + 1}/4)", 0, 10, 1)
    oled.text("BlobPad Ready", 0, 20, 1)
    oled.show()

def update_leds():
    led1.value = bool(current_layer & 1)
    led2.value = bool(current_layer & 2)

# TODO when IO expander functions are added
def handle_layer_encoder():
    ...

def handle_other_encoder():
    ...

update_display()
update_leds()

keyboard.go()
