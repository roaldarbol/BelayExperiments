from PicoW import PicoW
import belay
import time

devices = belay.list_ports()
print(devices)

if __name__ == "__main__":
    picoW = PicoW('/dev/cu.usbmodem14140')
    picoW.setup()
    picoW.led_toggle()
    time.sleep(2)
    picoW.led_toggle()
    picoW.close()