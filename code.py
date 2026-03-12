import board
import analogio
import usb_hid
import time

# Test
TEST = True

if TEST:
    print('[DEBUG] IN TEST MODE')

# Get gamepad first
steeringWheel = None

for thing in usb_hid.devices:
    if hasattr(thing, 'report_id') and thing.report_id == 4:
        steeringWheel = thing
        break

if not steeringWheel:
    print('No gamepad found, you messed up') # Idk how I'd see this message...

# Get the potentiometer (Pin 31, GP26, ADC0)
potentiometer = analogio.AnalogIn(board.GP26) # Pin 31

# Constants (+Preparation for constants)
SIXTEEN_BIT_INTEGER_LIMIT = 65535 # 2**16 - 1. Value from Potentiometer is sent as 16 bit value
ROTATION_RATIO = 900/1080 # 3 turn potentiometer turns 1080 degrees, I need only 900 so setting range
ACTIVE_RANGE = SIXTEEN_BIT_INTEGER_LIMIT * ROTATION_RATIO
OFFSET = (SIXTEEN_BIT_INTEGER_LIMIT - ACTIVE_RANGE) // 2

if TEST:
    print('[DEBUG] 16 Bit Integer Limit: ', SIXTEEN_BIT_INTEGER_LIMIT)
    print('[DEBUG] Rotation Ratio: ', ROTATION_RATIO)
    print('[DEBUG] Active Range: ', ACTIVE_RANGE)
    print('[DEBUG] Offsets: ', OFFSET)

MIN_LIMIT = 0 + OFFSET
MAX_LIMIT = SIXTEEN_BIT_INTEGER_LIMIT - OFFSET

if TEST:
    print('[DEBUG] MIN_LIMIT: ', MIN_LIMIT)
    print('[DEBUG] MAX_LIMIT: ', MAX_LIMIT)

report = bytearray(10)

while True:
    # Read potentiometer
    raw_value = potentiometer.value

    if TEST:
        print('[DEBUG] Potentiometer Raw value: ', raw_value)

    # Restrict the values so that the nut and bolt mechanism is actually correctly placed
    new_value = max(MIN_LIMIT, min(MAX_LIMIT, raw_value))

    if TEST:
        print('[DEBUG] New value: ', new_value)

    # Mapping the new value to a 16-bit integer (-32768 to 32767)
    steer_value = int((((new_value - MIN_LIMIT) / ACTIVE_RANGE) * 65534) - 32768)

    if TEST:
        print('[DEBUG] Steer Value: ', steer_value)

    # Ensure steering is within 16-bit integer limit, and is an integer
    steering = int(max(MIN_LIMIT, min(MAX_LIMIT, steer_value)))

    if TEST:
        print('[DEBUG] Steering: ', steering)

    # Split mapping these two bytes of data
    # report[2] is Low Byte, so rightmost byte. 'and' (&) operator replaces the first byte with 0xFF (11111111)
    # and gets ignored, only the right byte gets sent
    report[2] = steering & 0xFF

    if TEST:
        print('[DEBUG] Report[2]: ', report[2])

    # report[3] is the High Byte, so left most byte. same as report[2], however, the '>>' operator moves the whole
    # two bytes to the right, and sends the new right byte which was originally the left byte. 0xFF does the same thing.
    report[3] = (steering >> 8) & 0xFF

    if TEST:
        print('[DEBUG] Report[3]: ', report[3])

    # sends the info to pc
    try:
        steeringWheel.send_report(report)
    except OSError:
        pass

    # Apparently this helps somehow? 100hz refresh, 10ms delay
    time.sleep(0.01)