# utils.py

import json

def parse_states(pkt):
    return tuple(pkt['position']), pkt.get('seen_obstacles',[])

def build_noma_messages(states):
    return {i:json.dumps(p).encode() for i,p in states.items()}