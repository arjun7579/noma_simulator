## 🛰️ NOMA + SIC Implementation

### 🔸 What is NOMA?
NOMA (Non-Orthogonal Multiple Access) allows multiple devices (drones) to transmit over the same frequency band simultaneously by allocating different power levels to each device. The base station decodes signals using Successive Interference Cancellation (SIC).

### 🔸 How We Implemented NOMA
In our simulator (`comm/noma.py`):

**Power Mapping**  
Each drone is assigned a predefined power level:
```python
NOMA_POWER_LEVELS = [5, 4, 3, 2, 1]  # Drone 0 has highest decoding priority
```

**Superposition of Signals**  
Encrypted drone messages are converted to byte arrays, scaled by their NOMA power level, and numerically added:
```python
total += arr * self.power_map[i]  # Simulate analog superposition
```

**Raw Buffers Stored**  
Individual encrypted buffers are stored for later decoding.

**SIC-Like Decoding**  
Base station decodes messages in descending power order:
```python
for i, _ in sorted(self.power_map.items(), key=lambda kv: -kv[1]):
    decrypted = ChaCha20.decrypt(raw[i])
    decoded[i] = decrypted
```
✔️ While not RF-accurate, this provides strong conceptual simulation[8].

---

## 🔐 ChaCha20 Encryption Integration

### 🔸 What is ChaCha20?
ChaCha20 is a stream cipher offering high-speed encryption and modern cryptographic security, ideal for resource-constrained systems like UAVs.

### 🔸 How We Use It
In `comm/encryption.py`, every message:
1. Is serialized with `json.dumps(...)` and encrypted:
```python
ciphertext = cipher.encrypt(plaintext)
```
2. Is decrypted symmetrically at receiver with same key + nonce.  
Both drones and base station use shared `CHACHA20_KEY` and `CHACHA20_NONCE`.

**Secure Communication Flow**  
```text
Drone State → [Encrypt with ChaCha20] → NOMA superposition → Base Station
Base Command → [Encrypt with ChaCha20] → TCP → Drone
```

---

## 🚧 Obstacle Avoidance Logic
**How Drones Avoid Collisions:**  
Each drone (`drone_agent.py`) uses:

**360° Vision Radius**  
```python
VISION_RADIUS = 50
```

**Obstacle Sensing**  
Checks all obstacles within vision radius:
```python
if math.hypot(self.position[0]-ox, self.position[1]-oy) <= VISION_RADIUS:
```

**Reactive Avoidance**  
Computes repulsion vector when obstacle detected:
```python
dx, dy = x - ox, y - oy
push = 5
self.position = (x + dx / dist * push, y + dy / dist * push)
```
Enables local real-time collision mitigation.

---

## 🧠 Area Optimization (Coverage)
**User Coverage Optimization** (in `base_station_server.py`):  
1. Users spawned randomly in `world.py`  
2. Each drone:
   - Checks if user within its `VISION_RADIUS`
   - Reports to base station via NOMA
3. Base Station:
   - Tracks covered users
   - Sends target positions to drones:
     - Directs drones toward nearest uncovered users (Euclidean distance)
     - If all users covered, drones patrol randomly

```python
def nearest_uncovered_user(drone_pos, users, covered_users):
    # Picks nearest user not already covered
```
Ensures maximized coverage[7].

---

## 🛰️ System Workflow Summary

```plaintext
┌────────────┐       NOMA+ChaCha       ┌──────────────┐
│  Drone #i  │ ────────────────────▶   │ Base Station │
│ [Obstacle] │        Uplink           │  (Autonomy)  │
└────────────┘ ◀────────────────────   │   Controller │
      ▲             Encrypted          └─────┬────────┘
      │                                      │
      ▼                                      ▼
Local avoidance              Selects new target (user, patrol)
via obstacle sense           Sends `move` command (ChaCha)
```

---

## 🛠️ Customization Capabilities
| Feature              | How to Configure                     |
|----------------------|--------------------------------------|
| Drone Count          | `NUM_DRONES` in `config.py`         |
| Vision Radius        | `VISION_RADIUS` in `config.py`      |
| World Area           | `WORLD_LIMIT` in `config.py`        |
| Users + Obstacles    | `World._spawn_users/obstacles()`    |
| Ping Interval        | Change timer in `base_station_server.py` |
| NOMA Powers          | Modify `NOMA_POWER_LEVELS`          |

---

## 🔮 Future Scope
- Train RL agents using simulator by plugging into `DroneAgent` movement policy
- Integrate MADDPG/PPO with realistic communications
- Add dynamic user mobility, battery constraints, dropout scenarios
- Log telemetry in JSONL/CSV for analysis
- Add wireless physics (fading, interference) using ns3/GNURadio
---
_Made with Python🐍 arjun7579_
