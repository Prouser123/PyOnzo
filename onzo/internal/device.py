import struct
import random

from onzo.internal.enums import NetworkID, RequestType, ResponseType, StreamType
from onzo.internal.constants import REQUEST_HEADER_FORMAT

class Device(object):
    network_id = None

    def __init__(self, connection):
        self.conn = connection

    def _send_request(self, req_type, req_reg_id, req_payload=bytes(),
                      resp_parser=lambda payload: None):
        # Encode and send request
        req_trans_id = random.getrandbits(16)

        req_header = struct.pack(REQUEST_HEADER_FORMAT, 0, 0, req_trans_id,
                                 self.network_id, RequestType(req_type),
                                 req_reg_id)
        self.conn.message_send(req_header + req_payload)

        # Receive and parse response
        response = self.conn.message_receive()
        resp_header, resp_payload = response[:16], response[16:]
        resp_header = struct.unpack(REQUEST_HEADER_FORMAT, resp_header)
        enc_0 = resp_header[0]
        enc_1 = resp_header[1]
        resp_trans_id = resp_header[2]
        req_net_id  = NetworkID(resp_header[3])
        resp_type = ResponseType(resp_header[4])
        if resp_type == ResponseType.ERROR:
            raise Exception("Error occured during {} request".format(req_type.name))
        resp_reg_id = resp_header[5]
        resp_payload = resp_parser(resp_payload)
        if resp_trans_id != req_trans_id:
            raise Exception("Transaction IDs do not match")
        if resp_type != req_type:
            raise Exception("response type ({}) does not match request type ({})".format(resp_type, req_type))
        return resp_payload

    def get_register(self, register_id):
        if type(register_id) == int:
            parser = lambda payload: struct.unpack('<H', payload)[0]
            return self._send_request(RequestType.GET_REGISTER, register_id,
                                      resp_parser=parser)
        elif type(register_id) == str:
            addrs = self.registers[register_id]
            val = 0
            for addr in addrs[::-1]:
                val = (val << 16) + self.get_register(addr)
            return val

    def set_register(self, register_id, value):
        if type(register_id) == int:
            params = struct.pack('< H', value)
            parser = lambda payload: struct.unpack('<H', payload)[0]
            return self._send_request(RequestType.SET_REGISTER, register_id,
                                      req_payload=params, resp_parser=parser)
        elif type(register_id) == str:
            addrs = self.registers[register_id]
            for addr in addrs:
                out = value & 0xFFFF
                self.set_register(addr, out)
                value = value >> 16

    def get_bulk_data(self, block_type, block_id=0, max_blocks=1):
        params = struct.pack('< H H', block_id, max_blocks)
        parser = lambda payload: (struct.unpack('<H', payload[:2])[0],
                                  payload[2:])
        return self._send_request(RequestType.GET_BULK_DATA, block_type,
                                  req_payload=params, resp_parser=parser)

    # NOTE: This function is commented out because there is no documentation on
    # how to actually pass data to the devices, I have filled it what I could
    # figure out
    #def write_bulk_data(self, block_type, first_block_index, number_blocks, data):
    #    params = struct.pack('< H H', first_block_index, number_blocks)
    #    return self._send_request(RequestType.WRITE_BULK_DATA, block_type,
    #                              req_payload=params)

    def get_network_list(self):
        parser = lambda payload: (payload[2:],)
        return self._send_request(0, RequestType.GET_NETWORK_LIST,
                                  register_id, req_payload=params)

    def reset_device(self):
        return self._send_request(RequestType.CMD_RESET, 0)

    def __getattr__(self, name):

        if name.startswith("get_"):
            register_name = name[4:]
            if register_name not in self.registers:
                raise AttributeError(name)

            def getter():
                return self.get_register(register_name)
            return getter

        elif name.startswith("set_"):
            register_name = name[4:]
            if register_name not in self.registers:
                raise AttributeError(name)
            def setter(value):
                return self.set_register(register_name, value)
            return setter

        else:
            raise AttributeError(name)