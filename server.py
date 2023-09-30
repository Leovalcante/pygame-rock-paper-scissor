import pickle
import ssl
import socket
import threading

import config
from common import printd, deserialize
from model import Player


class Server:
    def __init__(self):
        if config.tls:
            self.ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            self.ctx.load_cert_chain(
                certfile=config.tls_cert_pub, keyfile=config.tls_cert_priv
            )

        self.sox = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sox.bind((config.server_host, config.server_port))
        except socket.error as e:
            print(f"[!] Got error: {e}")
            raise

        self.players = [
            Player(0, 0, 50, 50, (255, 0, 0)),
            Player(100, 100, 50, 50, (0, 0, 255)),
        ]
        self.current_player = 0

    def serve(self):
        self.sox.listen()
        print("[+] Server started!\n[*] Waiting connections...")

        while True:
            conn, addr = self.sox.accept()
            print(f"[+] Incoming connection from: {addr}")
            threading.Thread(
                target=self.handle_connection, args=(conn, addr, self.current_player)
            ).start()
            self.current_player += 1

    def init_client(self, conn):
        client = conn
        if config.tls:
            client = self.ctx.wrap_socket(conn, server_side=True)

        return client

    def handle_connection(self, conn, addr, player):
        print(f"[*] Managing connection: {addr}")
        client = self.init_client(conn)
        client.sendall(pickle.dumps(self.players[player]))

        while True:
            try:
                data = deserialize(client.recv(config.buff_size))
                printd(f"[*] Got data: {data}")
            except socket.error as e:
                print(f"[!] Got error: {e}")
                data = None

            if not data:
                print(f"[-] Disconnecting {addr}")
                break

            printd(f"[*] Receiving: {data}")
            self.players[player] = data
            reply = self.players[0 if player == 1 else 1]

            client.sendall(pickle.dumps(reply))

        client.close()

    def teardown(self):
        self.sox.close()


if __name__ == "__main__":
    s = Server()
    try:
        s.serve()
    except:
        s.teardown()
