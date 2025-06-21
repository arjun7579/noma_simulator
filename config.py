# config.py
# config.py
WORLD_SIZE = 400# total width/height in positive direction
WORLD_LIMIT = 800  # coordinates go from -200 to +200

NUM_DRONES        = 5
VISION_RADIUS     = 50

# NOMA power tiers (higher first)
NOMA_POWER_LEVELS = [5, 4, 3, 2, 1]

# Encryption
CHACHA20_KEY      = b'0123456789ABCDEF0123456789ABCDEF'
CHACHA20_NONCE    = b'12345678'

# Networking
SERVER_HOST       = '127.0.0.1'
SERVER_PORT       = 5010
