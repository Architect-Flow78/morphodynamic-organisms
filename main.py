# ============================================================
# SOVEREIGN RESONANCE NETWORK
# Collective Morphodynamic Organism
# Author: Nicolae Pascal
# ============================================================

import sys, subprocess
subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib"])

import math
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import rc
from collections import deque

rc("animation", html="jshtml")

EPS = 1e-9

# ---------------- Utilities ----------------

def ema(o, n, a):
    return a * o + (1 - a) * n

def phase(x, K):
    return (x * K) % 1.0

def circular_coherence(ph):
    sc = sum(math.cos(2*math.pi*p) for p in ph)/len(ph)
    ss = sum(math.sin(2*math.pi*p) for p in ph)/len(ph)
    return math.sqrt(sc*sc + ss*ss)

# ---------------- Cell ----------------

class InvariantCell:
    def __init__(self, K):
        self.K = K
        self.fast = 0.5
        self.last_C = 0.5

    def update(self, values):
        phases = [phase(v,self.K) for v in values]
        C = circular_coherence(phases)
        self.fast = ema(self.fast,C,0.9)
        self.last_C = C
        return C

# ---------------- Organism ----------------

class Organism:
    def __init__(self):
        self.cell = InvariantCell(random.uniform(1.2,2.8))
        self.need = 0.0
        self.pos = [random.random(),random.random()]
        self.history = deque(maxlen=100)

    def pulse(self):
        return math.sin(2*math.pi*self.cell.last_C)

    def update(self, world, bestK, field):

        C = self.cell.update(world)

        if self.need>0.4:
            self.cell.K = ema(self.cell.K,bestK,0.9)

        self.need = ema(self.need,max(0,0.7-C)-0.25*field,0.9)

        if self.need>0.5:
            self.cell.K += random.uniform(-0.03,0.03)

        self.cell.K += random.uniform(-0.002,0.002)
        self.cell.K = max(0.5,min(3.5,self.cell.K))

        self.pos[0]+=math.cos(self.pulse())*0.003
        self.pos[1]+=math.sin(self.pulse())*0.003
        self.pos[0]%=1
        self.pos[1]%=1

        self.history.append(C)

# ---------------- Swarm ----------------

class Swarm:
    def __init__(self,n):
        self.agents=[Organism() for _ in range(n)]
        self.bestK=1.6
        self.field=0

    def step(self,world):
        flow=[a for a in self.agents if a.history and a.history[-1]>0.75]
        if flow:
            self.bestK=sum(a.cell.K for a in flow)/len(flow)
            self.field=len(flow)/len(self.agents)
        else:
            self.field=0
        for a in self.agents:
            a.update(world,self.bestK,self.field)

# ---------------- Visualization ----------------

class Visualizer:
    def __init__(self,swarm):
        
