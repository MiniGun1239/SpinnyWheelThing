import board
import analogio
import usb_hid
import sys
import time

# --- SYSTEM CONFIG ---
TEST = True

# --- USAGE SETTING ---
CENTER_DEADZONE = 100

if TEST:
    print('[DEBUG] IN TEST MODE')

# --- SETUP ---
steeringWheel = None # Initialize gamepad first

# Set report as a byte array. As set by boot.py
report = bytearray(4)

# Get gamepad from devices
for thing in usb_hid.devices:
    if TEST:
        report_id = getattr(thing, 'report_id', None)
        print('[DEBUG] Device found: ', thing, "Report ID:", report_id)
    # preset in boot.py
    if hasattr(thing, 'report_id') and thing.report_id == 4:
        steeringWheel = thing
        break

# If boot.py got changed somehow
if not steeringWheel:
    print('No gamepad found, you messed up')
    sys.exit()

# Get the potentiometer (Pin 31 / GP26 / ADC0)
potentiometer = analogio.AnalogIn(board.GP26) # Pin 31

# --- CONSTANTS ---
SIXTEEN_BIT_INTEGER_LIMIT = 65535 # (2**16 - 1) Value from Potentiometer is sent as 16 bit value
SIXTEEN_BIT_INTEGER_LIMIT_MIN = -32768
SIXTEEN_BIT_INTEGER_LIMIT_MAX = 32767

# More math stuff
HEADROOM_RATIO = 280 / 300 # If Total rotation is 300 degrees. Headroom so that the potentiometer doesnt break
# HEADROOM_RATIO = 250 / 270 # If Total rotation is 270 degrees. Headroom so that the potentiometer doesnt break.
ACTIVE_RANGE = int(SIXTEEN_BIT_INTEGER_LIMIT * HEADROOM_RATIO)
OFFSET = (SIXTEEN_BIT_INTEGER_LIMIT - ACTIVE_RANGE) // 2 # find the unused ends size

if TEST:
    print('[DEBUG] 16 Bit Integer Limit: ', SIXTEEN_BIT_INTEGER_LIMIT)
    print('[DEBUG] Headroom Ratio: ', HEADROOM_RATIO)
    print('[DEBUG] Active Range: ', ACTIVE_RANGE)
    print('[DEBUG] Offset: ', OFFSET)

MIN_LIMIT = 0 + OFFSET
MAX_LIMIT = SIXTEEN_BIT_INTEGER_LIMIT - OFFSET

if TEST:
    print('[DEBUG] MIN_LIMIT: ', MIN_LIMIT)
    print('[DEBUG] MAX_LIMIT: ', MAX_LIMIT)

while True:
    # Read potentiometer
    raw_value = potentiometer.value

    if TEST:
        print('[DEBUG] Potentiometer Raw value: ', raw_value)

    # Restrict the values so that the nut and bolt mechanism is actually correctly placed
    new_value = max(MIN_LIMIT, min(MAX_LIMIT, raw_value))

    if TEST:
        print('[DEBUG] New value: ', new_value)

    # Mapping the new value to a 16-bit integer (-32767 to 32767)
    steer_value = int((((new_value - MIN_LIMIT) / ACTIVE_RANGE) * 65534) - 32767)

    if TEST:
        print('[DEBUG] Steer Value: ', steer_value)

    # Ensure steering is within 16-bit integer limit, and is an integer
    steering = int(max(SIXTEEN_BIT_INTEGER_LIMIT_MIN, min(SIXTEEN_BIT_INTEGER_LIMIT_MAX, steer_value)))

    if TEST:
        print('[DEBUG] Steering: ', steering)

    # Split mapping these two bytes of data
    # report[2] is Low Byte, so rightmost byte. 'and' (&) operator replaces the first byte with 0xFF (11111111)
    # and gets ignored, only the right byte gets sent
    report[2] = steering & 0xFF

    if TEST:
        print('[DEBUG] Report low byte: ', report[2])

    # report[3] is the High Byte, so left most byte. same as report[2], however, the '>>' operator moves the whole
    # two bytes to the right, and sends the new right byte which was originally the left byte. 0xFF does the same thing.
    report[3] = (steering >> 8) & 0xFF

    if TEST:
        print('[DEBUG] Report high byte: ', report[3])

    # sends the info to pc
    try:
        steeringWheel.send_report(report)
        if TEST:
            print('[DEBUG] Report sent successfully')
    except OSError:
        if TEST:
            print('[DEBUG] Report failed to send')
        pass

    # Apparently this helps somehow? 100hz refresh, 10ms delay
    if TEST:
        time.sleep(1)
        continue

    time.sleep(0.01)
