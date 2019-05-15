from microbit import uart, button_b, display, Image

uart.init(115200)  # serial baudrate

RED = b'R'
YELLOW = b'Y'
GREEN = b'G'
TRIGGER = b'T'
CLEAR = b'C'
UNKNOWN = b'U'

dim_value = 9  # value 1-9 for dimming the display

NEUTRAL = Image('00000:09090:00000:99999:00000:')

display.show(Image.GHOST / 9 * dim_value)

while True:
    if uart.any():
        data = uart.read()
        if RED in data:
            display.show(Image.SAD / 9 * dim_value)
        elif YELLOW in data:
            display.show(NEUTRAL / 9 * dim_value)
        elif GREEN in data:
            display.show(Image.HAPPY / 9 * dim_value)
        elif CLEAR in data:
            display.clear()
        elif UNKNOWN in data:
            display.show(Image("?") / 9 * dim_value)

    if button_b.is_pressed():
        uart.write(TRIGGER)
        display.show([clk / 9 * dim_value for clk in Image.ALL_CLOCKS], delay=100)
        display.show(Image.CLOCK12 / 9 * dim_value)