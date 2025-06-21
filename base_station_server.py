import socket, threading, json, time
from comm.network import NetworkServer
from comm.noma import NOMAProtocol
from env.world import World
from config import SERVER_HOST, SERVER_PORT, NUM_DRONES, WORLD_SIZE

CMD_PORT = SERVER_PORT + 1
server = NetworkServer(SERVER_HOST, SERVER_PORT)
server.start()
noma = NOMAProtocol(NUM_DRONES)
world = World()
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind((SERVER_HOST, CMD_PORT))

def cli_listener():
    while True:
        data, _ = udp.recvfrom(2048)
        cmd = json.loads(data.decode())
        did = cmd.pop("id", None)
        server.send(did, cmd)

threading.Thread(target=cli_listener, daemon=True).start()

def periodic_pinger():
    while True:
        time.sleep(10)  # every 10 seconds
        for drone_id in range(NUM_DRONES):
            server.send(drone_id, {"ping": True})
            print(f"[Ping] 📡 Sent to Drone {drone_id}")

threading.Thread(target=periodic_pinger, daemon=True).start()

# base_station_server.py (Replace the main while loop)
import math
import random

def divide_world_zones(num_drones, world_size):
    cols = math.ceil(math.sqrt(num_drones))
    rows = math.ceil(num_drones / cols)
    zone_width  = world_size // cols
    zone_height = world_size // rows

    zones = []
    for i in range(num_drones):
        col = i % cols
        row = i // cols
        xmin = col * zone_width
        ymin = row * zone_height
        xmax = xmin + zone_width
        ymax = ymin + zone_height
        zones.append(((xmin, ymin), (xmax, ymax)))
    return zones

def pick_target_in_zone(zone):
    (xmin, ymin), (xmax, ymax) = zone
    return (
        random.randint(xmin + 10, xmax - 10),
        random.randint(ymin + 10, ymax - 10)
    )

zones = divide_world_zones(NUM_DRONES, WORLD_SIZE)

while True:
    time.sleep(0.5)
    states = server.get_states()
    drones = [s['position'] for s in states.values()]
    seen   = [s.get('seen_obstacles', []) for s in states.values()]

    # Autonomous command assignment
    for i in range(NUM_DRONES):
        if i >= len(drones): continue
        zone    = zones[i]
        target  = pick_target_in_zone(zone)

        # Slightly smarter: if drone too close to another, reassign
        my_pos = drones[i]
        too_close = any(
            j != i and math.hypot(my_pos[0] - drones[j][0], my_pos[1] - drones[j][1]) < 30
            for j in range(len(drones))
        )
        if too_close:
            target = pick_target_in_zone(random.choice(zones))

        server.send(i, {"action": "move", "position": list(target)})

    # JSON for simvis
    js = {
        "drones":    [list(p) for p in drones],
        "obstacles": world.get_obstacles(),
        "users":     world.get_users()
    }
    with open("world_state.json", "w") as f:
        json.dump(js, f)

    print(f"[Coverage] Active drones: {len(drones)}")
    for did, pkt in states.items():
        print(f"[Telemetry] Drone {did}: {pkt}")
    print("---")
