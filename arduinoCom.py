# communicate between pycharm and arduino
# if arduino receive the flag signal, vibrate
# flag: 1-vibrate; 0-don't vibrate
# please turn off the serial monitor in arduino and any bluetooth device

import serial.tools.list_ports
import time

plist = list(serial.tools.list_ports.comports())

if len(plist) <= 0:
    print('no port detected!')
else:
    plist_0 = list(plist[0])
    serialName = plist_0[0]
    serialFd = serial.Serial(serialName, 9600, timeout=60)
    print("available port: ", serialFd.name)
    while 1:
        serialFd.write("1".encode('utf-8'))
        time.sleep(1)
        serialFd.write("0".encode('utf-8'))
        time.sleep(1)



