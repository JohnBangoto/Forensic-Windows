DESCRIPTION = "Périphériques USB connectés (WMI)"

import win32com.client

def collect():
    devices = []
    wmi = win32com.client.GetObject("winmgmts:")
    for usb in wmi.InstancesOf("Win32_USBHub"):
        devices.append({
            'DeviceID': usb.DeviceID,
            'Name': usb.Name,
            'PNPDeviceID': usb.PNPDeviceID,
            'Status': usb.Status
        })
    return devices
