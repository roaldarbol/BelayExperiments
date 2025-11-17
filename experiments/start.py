import time
import belay
from belay import list_devices
from belay import Device
from devices.PicoBonn import PicoBonn

# Initialize device
spec = belay.UsbSpecifier(
    vid=11914, 
    pid=5, 
    serial_number='70973D3DE68AC915', 
    manufacturer='Microsoft', 
    location='1-4:x.0')
pico = PicoBonn(spec)