import struct
import hid

import onzo.internal.constants as consts

class Connection(object):

    def __init__(self, vid=consts.DISPLAY_VID, pid=consts.DISPLAY_PID, unit=0):
        self.vid = vid
        self.pid = pid
        self.unit = unit

    def connect(self):
        self.dev = hid.device()
        self.dev.open(vendor_id=self.vid, product_id=self.pid)

    def disconnect(self):
        self.dev.close()

    # Low level packet framing (64 byte)
    def message_send(self, data):
        while len(data) > 0:
            frame_size = 62
            frame_fin = 0

            if len(data) <= 62:
                frame_fin = 1
                if len(data) < 62:  # Pad with 0xFF
                    frame_size = len(data)
                    data += b'\xFF' * (62 - len(data))
            header = struct.pack('<BB', frame_fin, frame_size)
            i = self.dev.write(header + data[:62])
            if i != 64:  # All writes should be blocks of 64 bytes
                raise Exception("All bytes were not written")
            data = data[62:]

    def message_receive(self, timeout=5000):
        complete_payload = bytes()
        while True:
            frame = bytes(self.dev.read(64, timeout))
            frame_fin, frame_size = struct.unpack('<BB', frame[:2])
            payload = frame[2:(2+frame_size)]  # Remove header & padding
            complete_payload += payload
            if frame_fin:
                break
        return complete_payload

