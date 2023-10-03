import pickle
import ssl
import socket
import threading

import config

from model import Game


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

        self.connected = set()
        self.games = dict()
        self.id_count = 0

    def serve(self):
        self.sox.listen()
        print("[+] Server started!\n[*] Waiting connections...")

        while True:
            conn, addr = self.sox.accept()
            print(f"[+] Incoming connection from: {addr}")

            self.id_count += 1

            p = 0
            game_id = (self.id_count - 1) // 2

            if self.id_count % 2 == 1:
                self.games[game_id] = Game(game_id)
                print(f"[+] Creating a new game {game_id}")
            else:
                self.games[game_id].ready = True
                p = 1

            threading.Thread(
                target=self.handle_connection,
                args=(conn, addr, p, game_id),
            ).start()

    def init_client(self, conn):
        client = conn
        if config.tls:
            client = self.ctx.wrap_socket(conn, server_side=True)

        return client

    def handle_connection(self, conn, addr, p, game_id):
        print(f"[*] Managing connection: {addr}")
        client = self.init_client(conn)
        client.sendall(str(p).encode())

        reply = ""
        while True:
            try:
                data = client.recv(config.buff_size).decode()
                # printd(f"data: {data}")
                # printd(f"game_id: {game_id}")
                # printd(f"games: {self.games}")
                if game_id in self.games:
                    game = self.games[game_id]
                    # printd("here")

                    if not data:
                        break
                    elif data == "reset":
                        game.reset()
                    elif data != "get":
                        game.play(p, data)

                    reply = game
                    # printd(reply)

                    client.sendall(pickle.dumps(reply))
                else:
                    break
            except Exception as ex:
                print(ex)

        print(f"[!] Lost connection")
        try:
            del self.games[game_id]
            print(f"[-] Closing game {game_id}")
        except:
            pass

        self.id_count -= 1
        client.close()

    def teardown(self):
        self.sox.close()


if __name__ == "__main__":
    s = Server()
    try:
        s.serve()
    except:
        s.teardown()
