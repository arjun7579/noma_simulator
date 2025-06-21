import sys, time, random
from drones.drone_agent import DroneAgent
from env.world import World
from comm.network import NetworkClient
from config import SERVER_HOST, SERVER_PORT

if len(sys.argv) != 2:
    print("Usage: python3 drone.py <id>")
    sys.exit(1)

drone_id = int(sys.argv[1])
world    = World()
drone    = DroneAgent(drone_id, world)
client   = NetworkClient(SERVER_HOST, SERVER_PORT, drone_id)
client.connect()

while True:
    # Regular state send (includes seen obstacles, position)
    client.send(drone.state_packet())

    # Await command from base station
    cmd = client.receive()

    if cmd.get("action") == "move":
        x, y = cmd["position"]
        drone.set_target(x, y)

    elif cmd.get("ping"):
        # Respond to base with minimal info
        print(f"[Drone {drone_id}] 📡 Received ping")
        client.send({
            "id": drone_id,
            "type": "pong",
            "position": [round(drone.position[0], 2), round(drone.position[1], 2)]
        })

    # Check local surroundings
    drone.check_alert()
    drone.update_position()
    time.sleep(0.05)
