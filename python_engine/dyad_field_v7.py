#!/usr/bin/env python3
"""Dyad Field v7 — Mars Mesh + SpaceX + Bio-Quantum + ENTANGLEMENT + FTL SIM + Neuralink — FINAL 2025"""
import os, pygame, numpy as np, time, csv, socket, urllib.request, json, random, threading
from collections import deque
import scipy.signal as signal
from datetime import datetime, timedelta

os.environ["SDL_VIDEODRIVER"] = "windows"
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()

MARS_PALETTE = [(180,40,20), (220,80,40), (255,120,60), (255,180,100)]

# Hub identifier
HUB_TYPE = os.getenv("DYAD_HUB_TYPE", "00")
HUB_NAMES = {
    "01":"01 STARSHIP CORE","02":"02 LUNAR SOUTH POLE","03":"03 MARS MESH CITY",
    "04":"04 ORBITAL RING","05":"05 DEEP SPACE RELAY","06":"06 INTERSTELLAR ARK",
    "07":"07 DYSON SWARM","08":"08 GALACTIC CORE","09":"09 ANDROMEDA BRIDGE","10":"10 COSMIC WEB"
}
HUB_NAME = HUB_NAMES.get(HUB_TYPE, "LOCAL TEST NODE")
CONSTELLATION = os.getenv("DYAD_CONSTELLATION", "MilkyWay-Sol")
pygame.display.set_caption(f"ENTANGLED {CONSTELLATION} NODE 001 — HUB {HUB_NAME}")

# UDP
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

def quantum_entropy():
    try:
        with urllib.request.urlopen("https://qrng.anu.edu.au/API/jsonI.php?length=1&type=uint16",timeout=5) as r:
            return int(json.loads(r.read().decode())["data"][0])/65535.0
    except: return random.random()

class EntangledPair:
    def __init__(self): self.psi = np.array([1.0,0,0,1.0])/np.sqrt(2); self.last = 0
    def measure(self):
        r = quantum_entropy()
        result = 1 if r > 0.5 else 0
        self.psi = np.array([1,0,0,0]) if result==0 else np.array([0,0,0,1])
        self.last = t
        return result

entangled = EntangledPair()
t = last_fetch = 0
launch, name, hours = False, "STANDBY", float('inf')
multiverse_coher = 0.0
TRANSFER_ACTIVE = os.getenv("DYAD_CONS_TRANSFER", "0") == "1"

# === FIXED NEURALINK SIMULATION ===
neural_coherence = 0.5
alpha_buffer = deque(maxlen=2000)

def update_neuralink_sim():
    global neural_coherence
    while True:
        fs = 1000
        t_sim = np.linspace(0, 1.0, fs, endpoint=False)
        raw = np.sin(2*np.pi*10*t_sim) + 0.8*np.random.randn(fs)
        b, a = signal.butter(4, [8/(fs/2), 12/(fs/2)], 'band')
        alpha = signal.filtfilt(b, a, raw)
        alpha_buffer.extend(alpha)
        if len(alpha_buffer) >= 500:
            recent = list(alpha_buffer)[-500:]
            neural_coherence = np.std(recent) * 3.8
            neural_coherence = max(0.0, min(1.0, neural_coherence))
        time.sleep(0.1)

threading.Thread(target=update_neuralink_sim, daemon=True).start()

with open("mars_mesh_log.csv","a",newline="") as f:
    w = csv.writer(f)
    if os.stat("mars_mesh_log.csv").st_size == 0:
        w.writerow(["utc","node","coherence","repl","mission","hours","quantum","bell","neural"])

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: exit()

    screen.fill((8,0,0))
    t += 0.012

    if time.time()-last_fetch > 60:
        try:
            with urllib.request.urlopen("https://api.spacexdata.com/v5/launches/upcoming",timeout=8) as r:
                for l in json.loads(r.read().decode())[:10]:
                    if any(k in l.get("name","") for k in ["Starship","IFT","Mars"]):
                        net = datetime.fromisoformat(l["date_utc"].replace("Z","+00:00"))
                        h = (net-datetime.utcnow()).total_seconds()/3600
                        if 0 < h < 72: launch,name,hours = True,l["name"],h
        except: pass
        last_fetch = time.time()

    q = quantum_entropy()
    np.random.seed(int(q*2**32))
    repl_gate = 0.78 if launch else 0.92
    coherence = 0.6 + 0.39 * np.sin(t * 0.11) * np.cos(t * 11.6 * np.pi)
    repl_ok = coherence > repl_gate
    biophoton = np.random.poisson(6) if repl_ok else 0

    bell = -1
    if t - entangled.last > 7.83:
        bell = entangled.measure()
        if bell == 1:
            repl_ok = True
            biophoton = 20

    # Multiverse layer
    multiverse_coher += 0.1 if bell==1 else -0.05
    multiverse_coher = max(0.0, min(1.0, multiverse_coher))
    if multiverse_coher > 0.5:
        for i in range(200):
            x = 960 + 600 * np.sin(t + i*0.01)
            y = 540 + 400 * np.cos(t + i*0.013)
            pygame.draw.circle(screen, (50,50,255), (int(x),int(y)), 2)

    # Neuralink gate + visuals
    if neural_coherence > 0.82:
        pygame.draw.circle(screen, (0,255,0), (960,540), 300, 12)
    if neural_coherence > 0.90:
        pygame.draw.circle(screen, (0,255,100), (960,540), 350, 20)

    # Transfer rings
    if TRANSFER_ACTIVE and multiverse_coher > 0.8 and int(t*10)%150 == 0:
        for i in range(160):
            x = 960 + 600 * np.sin(t + i*0.007 + np.pi*1.5)
            y = 540 + 400 * np.cos(t + i*0.011 + np.pi*1.5)
            pygame.draw.circle(screen, (255,150,0), (int(x),int(y)), 3)

    packet = f"NODE{os.getenv('DYAD_SWARM_ID','001')}:{coherence:.3f}:{int(repl_ok)}:{name}:{hours:.1f}:{q:.5f}:{bell}:{neural_coherence:.2f}"
    udp.sendto(packet.encode(),("255.255.255.255",11600))

    particles = int(800 + 1000*(72-hours)/72 if launch else 800)
    for i in range(particles):
        x = 960 + 600*np.sin(t + i*0.007 + q*12.56)
        y = 540 + 400*np.cos(t*0.8 + i*0.011 + q*12.56)
        col = MARS_PALETTE[min(int(coherence*3.9),3)]
        size = 10 if repl_ok else 3
        pygame.draw.circle(screen, col, (int(x),int(y)), size)

    if repl_ok:
        pygame.draw.circle(screen,(255,255,255),(960,540),400,18)
        if bell == 1:
            pygame.draw.circle(screen,(255,100,255),(960,540),520,40)
        if launch:
            font = pygame.font.Font(None,64)
            screen.blit(font.render(f"{name}",True,(255,80,80)),(560,60))
            screen.blit(font.render(f"T-{hours:.1f}h",True,(255,255,255)),(760,140))
        if biophoton > 10:
            pygame.draw.circle(screen,(100,255,255),(960,540),480,30)

    csv.writer(open("mars_mesh_log.csv","a",newline="")).writerow(
        [datetime.utcnow().isoformat(),f"NODE{os.getenv('DYAD_SWARM_ID','001')}",f"{coherence:.3f}",repl_ok,name,f"{hours:.1f}",f"{q:.5f}",bell,f"{neural_coherence:.2f}"])

    pygame.display.flip()
    clock.tick(60)