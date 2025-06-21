import socket, json
from config import SERVER_HOST, SERVER_PORT

CMD_PORT = SERVER_PORT + 1
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    line = input("> ").strip().lower()
    if line in ("exit", "quit"): break
    parts = line.split()
    if parts[0] == "drone" and len(parts) >= 3:
        did = int(parts[1])
        act = parts[2]
        msg = {"id": did, "action": act}
        if act == "move" and len(parts) == 5:
            msg["position"] = [float(parts[3]), float(parts[4])]
        sock.sendto(json.dumps(msg).encode(), (SERVER_HOST, CMD_PORT))
