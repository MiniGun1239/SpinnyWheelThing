import usb_hid

# THIS IS WRITTEN BASED ON ADAFRUIT's CODE
# While this is almost something completely different, I did start with ADAFRUIT's code
# Need to give credit where credit is due
# https://learn.adafruit.com/customizing-usb-devices-in-circuitpython/hid-devices#custom-hid-devices-3096614-9

GAMEPAD_REPORT_DESCRIPTOR = bytes((
    0x05, 0x01,         # Usage Page (Generic Desktop Ctrls)
    0x09, 0x05,         # Usage (Steering Wheel)
    0xA1, 0x01,         # Collection (Application)
    0x85, 0x04,             # Report ID (4)
    0x05, 0x09,             # Usage Page (Button)
    0x19, 0x01,             # Usage Minimum (Button 1)
    0x29, 0x10,             # Usage Maximum (Button 16)
    0x15, 0x00,             # Logical Minimum (0)
    0x25, 0x01,             # Logical Maximum (1)
    0x75, 0x01,           # Report Size (1)
    0x95, 0x10,           # Report Count (16)
    0x81, 0x02,             # Input (Data,Var,Abs)
    0x05, 0x01,         # Usage Page (Generic Desktop Ctrls)
    0x16, 0x00, 0x80,       # Logical Minimum (-32768)
    0x26, 0xFF, 0x7F,       # Logical Maximum (32767)
    0x09, 0x30,         # Usage (X axis)
    0x75, 0x10,           # Report Size (16 bits)
    0x95, 0x01,           # Report Count (1 axis)
    0x81, 0x02,             # Input (Data,Var,Abs)
    0xC0
))

steeringWheel = usb_hid.Device(
    report_descriptor=GAMEPAD_REPORT_DESCRIPTOR,
    usage_page=0x01,            # Generic Desktop Control
    usage=0x05,                 # Steering Wheel
    report_ids=(4,),            # Descriptor uses report ID 4
    in_report_lengths=(4,),     # This sends 4 bytes in its report
    out_report_lengths=(0,),    # It does not receive any reports
)

usb_hid.enable(
    (
        usb_hid.Device.KEYBOARD,
        usb_hid.Device.MOUSE,
        usb_hid.Device.CONSUMER_CONTROL,
        steeringWheel
    )
)