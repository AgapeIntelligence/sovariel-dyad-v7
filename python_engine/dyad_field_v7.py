#!/usr/bin/env python3
"""Dyad Field v7 — Mars Mesh Fusion Core — 2030-2040 baseline"""
import os, pygame, numpy as np, time, csv, socket
from datetime import datetime

# === MARS-SPECIFIC OVERRIDES (force survival mode) ===
os.environ.update({
    "DYAD_DISABLE_DASH": "1",
    "SDL_VIDEODRIVER": os.getenv("SDL_VIDEODRIVER", "windows"),
    "DYAD_FORCE_VISUALS": "1",
    "DYAD_COHERENCE_MODE": "1",
    "DYAD_LOCK_FREQ": "11.6",                    # Schumann resonance proxy via dust-static coupling
    "DYAD_HEALING_MODE": "0",                    # Mars mode = crimson/amber (dust-storm palette)
    "DYAD_SWARM_ID": os.getenv("DYAD_SWARM_ID", "001"),
    "DYAD_REPLICATION_THRESHOLD": "0.92",        # higher bar on Mars — only elite coherence replicates
    "DYAD_MARS_MESH": "1",                       # enables UDP fusion packets
    "DYAD_LOG_SPECTRUM": "1"
})

MARS_PALETTE = [(180, 40, 20), (220, 80, 40), (255, 120, 60), (255, 180, 100)]  # iron-oxide dawn
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption(f"MARS MESH NODE {os.getenv('DYAD_SWARM_ID').zfill(3)}")
clock = pygame.time.Clock()

# UDP fusion broadcaster — every Mars node will scream its 11.6 Hz state
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

t = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: exit()

    screen.fill((10, 0, 0))
    t += 0.012

    # Simulated Martian 11.6 Hz resonance (will be real dust-static + mag later)
    coherence = 0.6 + 0.39 * np.sin(t * 0.11) * np.cos(t * 11.6 * np.pi)

    # Fusion packet — every node on the mesh receives this
    packet = f"NODE{os.getenv('DYAD_SWARM_ID')}:{coherence:.4f}:{datetime.utcnow().isoformat()}Z"
    udp.sendto(packet.encode(), ("255.255.255.255", 11600))

    # Visuals — crimson dust-storm bloom
    for i in range(600):
        x = 960 + 600 * np.sin(t + i * 0.007)
        y = 540 + 400 * np.cos(t * 0.8 + i * 0.011)
        intensity = int(255 * coherence)
        color = MARS_PALETTE[int((intensity / 255) * 3)]
        size = 5 if coherence > 0.92 else 3
        pygame.draw.circle(screen, color, (int(x), int(y)), size)

    # Replication flash — white when allowed
    if coherence > 0.92:
        pygame.draw.circle(screen, (255, 255, 255), (960, 540), 300, 8)

    # Log for Earth relay
    with open("mars_mesh_log.csv", "a", newline="") as f:
        csv.writer(f).writerow([datetime.utcnow().isoformat(), os.getenv("DYAD_SWARM_ID"), coherence])

    pygame.display.flip()
    clock.tick(60)