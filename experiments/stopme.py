import os
if os.path.exists("stop.csv"):
    device.close()
    os.remove("stop.csv")
    True
else:
    False