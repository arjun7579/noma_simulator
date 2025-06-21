# drones/drone_agent.py

import math
from config import WORLD_SIZE, VISION_RADIUS, NUM_DRONES

class DroneAgent:
    def __init__(self, drone_id, world):
        self.id       = drone_id
        self.world    = world
        angle = 2 * math.pi * drone_id / NUM_DRONES
        radius = 100
        self.position = (
            int(radius * math.cos(angle)),
            int(radius * math.sin(angle))
        )

        self.target   = self.position
        self.speed    = 2.0
        
        
    def set_target(self, x, y):
        self.target = (
            max(0, min(x, WORLD_SIZE)),
            max(0, min(y, WORLD_SIZE))
        )
        print(f"[Drone {self.id}] 🧭 Target set to {self.target}")

    def update_position(self):
        x, y   = self.position
        tx, ty = self.target
        dx, dy = tx - x, ty - y
        dist   = math.hypot(dx, dy)

        if dist < self.speed:
            self.position = self.target
        elif dist > 0:
            self.position = (
                x + dx / dist * self.speed,
                y + dy / dist * self.speed
            )

        print(f"[Drone {self.id}] 📍 Position updated to {self.position}")

    def check_alert(self):
        for ox, oy in self.world.get_obstacles():
            if math.hypot(self.position[0] - ox, self.position[1] - oy) <= VISION_RADIUS:
                print(f"[ALERT] Drone {self.id}: Obstacle at ({ox}, {oy}) within {VISION_RADIUS}px")
                self._avoid_obstacle((ox, oy))
                break

    def _avoid_obstacle(self, obs_pos):
        ox, oy = obs_pos
        x, y   = self.position
        dx, dy = x - ox, y - oy
        dist   = math.hypot(dx, dy)
        if dist == 0: return
        push = 5
        self.position = (x + dx / dist * push, y + dy / dist * push)
        print(f"[Drone {self.id}] ⚠️ Adjusted to avoid obstacle → {self.position}")

    def sense(self):
        return [
            {"x": ox, "y": oy}
            for ox, oy in self.world.get_obstacles()
            if math.hypot(self.position[0] - ox, self.position[1] - oy) <= VISION_RADIUS
        ]

    def state_packet(self):
        return {
            "id": self.id,
            "position": [round(self.position[0], 2), round(self.position[1], 2)],
            "seen_obstacles": self.sense()
        }
