import sys
import struct
import bluetooth._bluetooth as bluez
from datetime import datetime
import requests

# Define the URL of the server
url = 'http://X/api/urssi'

def stringify(packet):
    """
    Returns the string representation of a raw HCI packet.
    """
    if sys.version_info > (3, 0):
        return ''.join('%02x' % struct.unpack("B", bytes([x]))[0] for x in packet)
    else:
        return ''.join('%02x' % struct.unpack("B", x)[0] for x in packet)

def parse_events(sock):
    flt = bluez.hci_filter_new()
    bluez.hci_filter_all_events(flt)
    bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, flt )
    packet = sock.recv(255)
    packetOffset = 0
    dataString = stringify(packet)
    #Ibeacon
    if dataString[38:46] == '4c000215':
        #Truncate Packets
        uuid = dataString[46:54] + "-" + dataString[54:58] + "-" + dataString[58:62] + "-" + dataString[62:66] + "-" + dataString[66:78]
        if sys.version_info[0] == 3:
            rssi, = struct.unpack("b", bytes([packet[packetOffset-1]]))
        else:
            rssi, = struct.unpack("b", packet[packetOffset-1])

        resultsArray = [{"uuid": uuid, "rssi": rssi, 'time': str(datetime.now())}]

        payload = {
            'probe': '1',
            'uuid': uuid,
            'urssi': rssi,
            'time': str(datetime.now())
        }

        requests.post(url, data=payload)

if __name__ == "__main__":
	sock = bluez.hci_open_dev(0)
	bluez.hci_send_cmd(sock, 0x08, 0x000C, struct.pack("<BB", 0x01, 0x00))
	#Scans for iBeacons
	try:
		while True:
			parse_events(sock)
	except KeyboardInterrupt:
		pass

