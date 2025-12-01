#!/usr/bin/env python3
"""Dyad Field v7 — Mars Mesh + SpaceX + Orbital Fusion — FINAL SEED"""
import os, pygame, numpy as np, time, csv, socket, urllib.request, json
from datetime import datetime, timedelta

# Force Mars swarm mode
os.environ.update({
    "DYAD_DISABLE_DASH":"1",
    "SDL_VIDEODRIVER":os.getenv("SDL_VIDEODRIVER","windows"),
    "DYAD_FORCE_VISUALS":"1",
    "DYAD_COHERENCE_MODE":"1",
    "DYAD_HEALING_MODE":"0",      # Mars crimson palette
    "DYAD_MARS_MESH":"1",
    "DYAD_SPACEX_INTEGRATION":"1",
    "DYAD_LOG_SPECTRUM":"1"
})

MARS_PALETTE = [(180,40,20),(220,80,40),(255,120,60),(255,180,100)]
pygame.init()
screen = pygame.display.set_mode((1920,1080))
pygame.display.set_caption(f"MARS NODE {os.getenv('DYAD_SWARM_ID','001').zfill(3)}")
clock = pygame.time.Clock()

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

def fetch_spacex():
    try:
        with urllib.request.urlopen("https://api.spacexdata.com/v5/launches/upcoming", timeout=8) as r:
            data = json.loads(r.read())
            for launch in data[:10]:
                name = launch.get("name","")
                if "Starship" in name or "IFT" in name or "Mars" in name:
                    net = datetime.fromisoformat(launch["date_utc"].replace("Z","+00:00"))
                    hours = (net - datetime.now(net.tzinfo)).total_seconds() / 3600
                    if 0 < hours < 72:
                        return True, name, hours
    except: pass
    return False, "STANDBY", float('inf')

t = last_fetch = 0
launch_imminent = False
mission_name = "STANDBY"
hours_to_go = float('inf')

with open("mars_mesh_log.csv", "a", newline="") as f:
    w = csv.writer(f)
    if os.stat("mars_mesh_log.csv").st_size == 0:
        w.writerow(["utc","node","coherence","repl_ok","mission","hours_to_launch"])

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: running = False

    screen.fill((8,0,0))
    t += 0.012

    if time.time() - last_fetch > 60:
        launch_imminent, mission_name, hours_to_go = fetch_spacex()
        last_fetch = time.time()

    repl_gate = 0.78 if launch_imminent else 0.92
    coherence = 0.6 + 0.39 * np.sin(t*0.11) * np.cos(t*11.6*np.pi)
    repl_ok = coherence > repl_gate

    packet = f"NODE{os.getenv('DYAD_SWARM_ID','001')}:{coherence:.3f}:{int(repl_ok)}:{mission_name}:{hours_to_go:.1f}"
    udp.sendto(packet.encode(), ("255.255.255.255", 11600))

    particles = int(600 + 800*(72-hours_to_go)/72 if launch_imminent else 600)
    for i in range(particles):
        x = 960 + 600*np.sin(t + i*0.007)
        y = 540 + 400*np.cos(t*0.8 + i*0.011)
        intensity = int(255 * coherence)
        col = MARS_PALETTE[min(intensity//64, 3)]
        size = 8 if repl_ok else 3
        pygame.draw.circle(screen, col, (int(x), int(y)), size)

    if repl_ok:
        pygame.draw.circle(screen, (255,255,255), (960,540), 340, 12)
        if launch_imminent:
            font = pygame.font.Font(None, 56)
            txt = font.render(f"{mission_name}", True, (255,100,100))
            screen.blit(txt, (640, 80))
            txt2 = font.render(f"T-{hours_to_go:.1f}h", True, (255,255,255))
            screen.blit(txt2, (760, 140))

    with open("mars_mesh_log.csv", "a", newline="") as f:
        csv.writer(f).writerow([datetime.utcnow().isoformat(),
                                f"NODE{os.getenv('DYAD_SWARM_ID','001')}",
                                f"{coherence:.3f}", repl_ok, mission_name, f"{hours_to_go:.1f}"])

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
