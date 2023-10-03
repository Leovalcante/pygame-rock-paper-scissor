import socket
import ssl

import config
from common import deserialize


class Network:
    def __init__(self) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if config.tls:
            self.ctx = ssl.create_default_context()
            self.ctx.load_verify_locations(config.tls_cert_pub)
            self.client = self.ctx.wrap_socket(
                self.client, server_hostname=config.server_hostname
            )

        self.server = config.server_host
        self.port = config.server_port
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def get_p(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(config.buff_size).decode()
        except socket.error as e:
            print(f"[!] Got error: {e}")

    def send(self, data):
        try:
            self.client.send(data.encode())
            return deserialize(self.client.recv(config.buff_size))
        except socket.error as e:
            print(f"[!] Got error: {e}")
