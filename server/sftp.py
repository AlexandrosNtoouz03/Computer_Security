import asyncssh, struct

SSH_FXP_INIT = 1
SSH_FXP_VERSION = 2

def pack_u32(n): 
    return struct.pack(">I", n)

def pack_str(data: bytes): 
    return pack_u32(len(data)) + data

def pack_pkt(ptype: int, payload: bytes) -> bytes:
    body = bytes([ptype]) + payload
    return pack_u32(len(body)) + body


class SFTPSession(asyncssh.SSHServerSession):
    #Minimal SFTP subsystem handler

    def __init__(self):
        self.buf = b""
        self.initialized = False
        self._chan = None

    def subsystem_requested(self, name: str) -> bool:
        return name == "sftp"

    def connection_made(self, chan):
        self._chan = chan
        try:
            self._chan.set_encoding(None)
        except Exception:
            pass

    def data_received(self, data, datatype):
        #Handle incoming SFTP packets
        if isinstance(data, str):
            data = data.encode("utf-8", "surrogatepass")
        self.buf += data

        while len(self.buf) >= 4:
            pkt_len = struct.unpack(">I", self.buf[:4])[0]
            if len(self.buf) < 4 + pkt_len:
                return  
            pkt = self.buf[4:4 + pkt_len]
            self.buf = self.buf[4 + pkt_len:]

            self._handle_packet(pkt)

    def _handle_packet(self, pkt: bytes):
        ptype = pkt[0]
        payload = pkt[1:]

        if not self.initialized:
            if ptype != SSH_FXP_INIT:
                self._send_error("Expected INIT first")
                self._chan.close()
                return
            version_payload = pack_u32(3)
            self._chan.write(pack_pkt(SSH_FXP_VERSION, version_payload))
            self.initialized = True
            print("SFTP INIT->VERSION completed")
        else:
            # Ignore further packets for now
            pass

    def _send_error(self, msg: str):
        print("Protocol error:", msg)
