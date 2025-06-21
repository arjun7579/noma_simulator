import socket, threading, json
from comm.encryption import ChaCha20Encryptor
from config import NUM_DRONES

class NetworkServer:
    def __init__(self, host, port):
        self.addr = (host, port)
        self.sock = socket.socket()
        self.sock.bind(self.addr)
        self.sock.listen(NUM_DRONES)
        self.encryptor = ChaCha20Encryptor()
        self.clients = {}
        self.states = {}

    def start(self):
        threading.Thread(target=self.accept_loop, daemon=True).start()

    def accept_loop(self):
        while True:
            client, _ = self.sock.accept()
            threading.Thread(target=self.handle, args=(client,), daemon=True).start()

    def handle(self, client):
        try:
            while True:
                data = client.recv(4096)
                if not data: break
                pkt = json.loads(self.encryptor.decrypt(data).decode())
                did = pkt['id']
                self.clients[did] = client
                self.states[did] = pkt
        except:
            pass

    def get_states(self): return dict(self.states)

    def send(self, did, msg):
        if did not in self.clients: return
        enc = self.encryptor.encrypt(json.dumps(msg).encode())
        self.clients[did].sendall(enc)

class NetworkClient:
    def __init__(self, host, port, drone_id):
        self.id = drone_id
        self.addr = (host, port)
        self.sock = socket.socket()
        self.encryptor = ChaCha20Encryptor()

    def connect(self):
        self.sock.connect(self.addr)

    def send(self, pkt):
        pkt['id'] = self.id
        enc = self.encryptor.encrypt(json.dumps(pkt).encode())
        self.sock.sendall(enc)

    def receive(self):
        data = self.sock.recv(4096)
        return json.loads(self.encryptor.decrypt(data).decode())

