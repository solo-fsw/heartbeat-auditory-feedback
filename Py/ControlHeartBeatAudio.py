import serial
import time


def init_serial_port(com_port):
    # Initialize serial port

    ser = serial.Serial()

    try:
        # Configure port
        ser.port = com_port
        ser.baudrate = 115200
        ser.bytesize = 8
        ser.parity = 'N'
        ser.stopbits = 1

        # Important: set a read timeout (in seconds)
        ser.timeout = 20

        # Open serial device
        ser.open()

    except serial.serialutil.SerialException:
        ser.close()
        print("Could not open serial device. Try unplugging and replugging the signal generator into the PC'")

    return ser


def play_heartbeat_audio(serial_device, frequency, duration, delay, repeat):

    try:
        # Write to port (type: bytes)
        pulse_info = "{frequency:" + str(frequency) + \
                     ",duration:" + str(duration) + \
                     ",delay:" + str(delay) + \
                     ",repeat:" + str(repeat) + \
                     "}\n"

        serial_device.write(pulse_info.encode())

        # Read data from port (wait until data is received, or until timeout has passed)
        data = serial_device.readline()

        return data

    except serial.serialutil.SerialException:
        print("Could not send pulse train.")
        return "pulse not sent"


def close_serial_device(serial_device):
    serial_device.close()


# Use code below to test:

# Initialize
print("initializing..")
serDevice = init_serial_port('COM7')
# sleep a bit
time.sleep(10)

# Play audio beeps with 200 ms delay:
print("playing heartbeat audio with 200 ms delay")
audioSent = play_heartbeat_audio(serDevice, 800, 100, 190, 10)
print(audioSent)

# Wait a bit before the next audio beeps
time.sleep(10)

# Play audio beeps with 500 ms delay:
print("playing heartbeat audio with 500 ms delay")
audioSent = play_heartbeat_audio(serDevice, 800, 100, 490, 10)
print(audioSent)

# Close serial port
close_serial_device(serDevice)
