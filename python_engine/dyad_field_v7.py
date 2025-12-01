#!/usr/bin/env python3
import os, pygame, numpy as np, time, random, socket, threading
from collections import deque
import scipy.signal as signal
from datetime import datetime
import pytz

os.environ["SDL_VIDEODRIVER"] = "windows"
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()

MARS_PALETTE = [(180,40,20), (220,80,40), (255,120,60), (255,180,100)]

# Hub identifier
HUB_TYPE = os.getenv("DYAD_HUB_TYPE", "00")
HUB_NAMES = {"01":"01 STARSHIP CORE","02":"02 LUNAR SOUTH POLE","03":"03 MARS MESH CITY",
             "04":"04 ORBITAL RING","05":"05 DEEP SPACE RELAY","06":"06 INTERSTELLAR ARK",
             "07":"07 DYSON SWARM","08":"08 GALACTIC CORE","09":"09 ANDROMEDA BRIDGE","10":"10 COSMIC WEB"}
HUB_NAME = HUB_NAMES.get(HUB_TYPE, "LOCAL TEST NODE")
CONSTELLATION = os.getenv("DYAD_CONSTELLATION", "MilkyWay-Sol")
pygame.display.set_caption(f"ENTANGLED {CONSTELLATION} NODE 001 — HUB {HUB_NAME}")

# UDP
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Entanglement
class EntangledPair:
    def __init__(self): self.last = 0
    def measure(self):
        self.last = time.time() + 7.83
        return 1 if random.random() > 0.5 else 0
entangled = EntangledPair()
bell = -1

# Multiverse & transfer
multiverse_coher = 0.0
TRANSFER_ACTIVE = os.getenv("DYAD_CONS_TRANSFER","0")=="1"

# === FIXED NEURALINK SIMULATION (deque → list fix) ===
neural_coherence = 0.5
alpha_buffer = deque(maxlen=2000)

def update_neuralink_sim():
    global neural_coherence
    while True:
        fs = 1000

cd /c/Users/Evie/cosmic_consciousness_hubs

# Completely replace the broken Neuralink block with the fixed version
cat > python_engine/dyad_field_v7.py << 'EOF'
#!/usr/bin/env python3
import os, pygame, numpy as np, time, random, socket, threading
from collections import deque
import scipy.signal as signal
from datetime import datetime
import pytz

os.environ["SDL_VIDEODRIVER"] = "windows"
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()

MARS_PALETTE = [(180,40,20), (220,80,40), (255,120,60), (255,180,100)]

# Hub identifier
HUB_TYPE = os.getenv("DYAD_HUB_TYPE", "00")
HUB_NAMES = {"01":"01 STARSHIP CORE","02":"02 LUNAR SOUTH POLE","03":"03 MARS MESH CITY",
             "04":"04 ORBITAL RING","05":"05 DEEP SPACE RELAY","06":"06 INTERSTELLAR ARK",
             "07":"07 DYSON SWARM","08":"08 GALACTIC CORE","09":"09 ANDROMEDA BRIDGE","10":"10 COSMIC WEB"}
HUB_NAME = HUB_NAMES.get(HUB_TYPE, "LOCAL TEST NODE")
CONSTELLATION = os.getenv("DYAD_CONSTELLATION", "MilkyWay-Sol")
pygame.display.set_caption(f"ENTANGLED {CONSTELLATION} NODE 001 — HUB {HUB_NAME}")

# UDP
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Entanglement
class EntangledPair:
    def __init__(self): self.last = 0
    def measure(self):
        self.last = time.time() + 7.83
        return 1 if random.random() > 0.5 else 0
entangled = EntangledPair()
bell = -1

# Multiverse & transfer
multiverse_coher = 0.0
TRANSFER_ACTIVE = os.getenv("DYAD_CONS_TRANSFER","0")=="1"

# === FIXED NEURALINK SIMULATION (deque → list fix) ===
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
            recent = list(alpha_buffer)[-500:]           # ← THIS IS THE FIX
            neural_coherence = np.std(recent) * 3.8
            neural_coherence = max(0.0, min(1.0, neural_coherence))
        time.sleep(0.1)

threading.Thread(target=update_neuralink_sim, daemon=True).start()

t = 0
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: exit()

    screen.fill((8,0,0))
    t += 0.016

    # Bell flash
    if time.time() > entangled.last:
        bell = entangled.measure()
        if bell == 1:
            pygame.draw.circle(screen, (255,100,255), (960,540), 520, 40)

    # Multiverse
    multiverse_coher += 0.1 if bell==1 else -0.05
    multiverse_coher = max(0.0, min(1.0, multiverse_coher))
    if multiverse_coher > 0.5:
        for i in range(200):
            x =  = 960 + 600 * np.sin(t + i*0.01)
            y  = 540 + 400 * np.cos(t + i*0.013)
            pygame.draw.circle(screen, (50,50,255), (int(x),int(y)), 2)

    # Neuralink gate + visuals
    if neural_coherence > 0.82:
        repl_ok = True
        pygame.draw.circle(screen, (0,255,0), (960,540), 300, 12)
    if neural_coherence > 0.90:
        pygame.draw.circle(screen, (0,255,100), (960,540), 350, 20)

    # Transfer rings
    if TRANSFER_ACTIVE and multiverse_coher > 0.8 and int(t*10)%150 == 0:
        for i in range(160):
            x = 960 + 600 * np.sin(t + i*0.007 + np.pi*1.5)
            y = 540 + 400 * np.cos(t + i*0.011 + np.pi*1.5)
            pygame.draw.circle(screen, (255,150,0), (int(x),int(y)), 3)

    # Base field
    for i in range(800):
        angle = t + i * 0.008
        x = 960 + 600 * np.sin(angle)
        y = 540 + 400 * np.cos(angle)
        col = MARS_PALETTE[i%4]
        pygame.draw.circle(screen, col, (int(x),int(y)), 4)

    # UDP packet
    udp.sendto(f"NODE001|HUB{HUB_TYPE}|NEURAL{neural_coherence:.2f}|BELL{bell}".encode(),
               ("255.255.255.255", 11600))

    pygame.display.flip()
    clock.tick(60)
