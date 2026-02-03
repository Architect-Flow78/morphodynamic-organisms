# ============================================================
# SOVEREIGN RESONANCE NETWORK
# Collective Morphodynamic Organism
#
# Author: Nicolae Pascal
# Contact: pascalnicolae78@gmail.com
#
# This is not an AI.
# This is not an agent.
# This is not optimization.
#
# This is a digital metabolic ecology.
# ============================================================

import math
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque

EPS = 1e-9

# ------------------------------------------------------------
# Utilities
# ------------------------------------------------------------

def ema(o, n, a):
    return a * o + (1 - a) * n

def phase(x, K):
    return (x * K) % 1.0

def circular_coherence(ph):
    sc = sum(math.cos(2 * math.pi * p) for p in ph) / len(ph)
    ss = sum(math.sin(2 * math.pi * p) for p in ph) / len(ph)
    return math.sqrt(sc * sc + ss * ss)

# ------------------------------------------------------------
# Invariant Cell
# ------------------------------------------------------------

class InvariantCell:
    def __init__(self, K):
        self.K = K
        self.fast = 0.5
        self.slow = 0.5
        self.threshold = 0.01
        self.last_C = 0.5
        self.alpha_fast = 0.9
        self.beta_slow = 0.995

    def update(self, values):
        phases = [phase(v, self.K) for v in values]
        C = circular_coherence(phases)

        D = abs(C - self.fast)

        self.threshold = math.exp(
            0.99 * math.log(self.threshold + EPS) +
            0.01 * math.log(D + EPS)
        )

        self.fast = ema(self.fast, C, self.alpha_fast)
        self.slow += (1 - self.beta_slow) * (C - self.slow)

        breach = D > self.threshold * 3.0
        self.last_C = C

        return C, breach

# ------------------------------------------------------------
# Sovereign Organism
# ------------------------------------------------------------

class SovereignOrganism:
    def __init__(self, id_tag, pos):

        self.id = id_tag
        self.pos = list(pos)

        self.cell = InvariantCell(random.uniform(1.2, 2.8))

        self.need = 0.0
        self.fatigue = 0.0
        self.shield = 1.0

        self.inner = [0.0, 0.0, 0.0]
        self.history = deque(maxlen=150)

    def get_pulse(self):
        return math.sin(2 * math.pi * self.cell.last_C) * self.shield

    def update(self, frame, best_K, field_strength):

        C, breach = self.cell.update(frame)

        # SOCIAL GIFT
        if self.need > 0.4:
            self.cell.K = ema(self.cell.K, best_K, 0.92)

        # NEED + SOCIAL NUTRITION
        target_need = max(0.0, 0.7 - C) - 0.25 * field_strength
        self.need = ema(self.need, target_need, 0.9)

        # FATIGUE
        self.fatigue = ema(self.fatigue, 1 if breach else 0, 0.95)

        # SHIELD
        self.shield = ema(self.shield, C, 0.995)

        # INTERNAL MEMORY
        self.inner[0] = ema(self.inner[0], C, 0.95)
        self.inner[1] = ema(self.inner[1], self.need, 0.95)
        self.inner[2] = ema(self.inner[2], field_strength, 0.95)

        # MORPHOLOGICAL HUNGER
        if self.need > 0.5:
            self.cell.K += math.sin(self.inner[2] * 10) * 0.03 * (1 - self.shield)

        # MICRO DIVERSITY
        self.cell.K += random.uniform(-0.001, 0.001)
        self.cell.K = max(0.5, min(3.5, self.cell.K))

        # MOTION
        self.pos[0] += math.cos(self.get_pulse()) * 0.002
        self.pos[1] += math.sin(self.get_pulse()) * 0.002
        self.pos[0] %= 1.0
        self.pos[1] %= 1.0

        self.history.append({
            "C": C,
            "N": self.need,
            "K": self.cell.K
        })

        return C

# ------------------------------------------------------------
# Collective Field
# ------------------------------------------------------------

class ResonanceSwarm:
    def __init__(self, n):

        self.agents = [
            SovereignOrganism(f"S{i}", (random.random(), random.random()))
            for i in range(n)
        ]

        self.best_K = 1.618
        self.field_strength = 0.0

    def step(self, world):

        flow_agents = [
            a for a in self.agents
            if a.history and a.history[-1]["C"] > 0.75
        ]

        if flow_agents:
            self.best_K = sum(a.cell.K for a in flow_agents) / len(flow_agents)
            self.field_strength = len(flow_agents) / len(self.agents)
        else:
            self.field_strength = 0.0

        for a in self.agents:
            a.update(world, self.best_K, self.field_strength)

# ------------------------------------------------------------
# Visualization
# ------------------------------------------------------------

class Visualizer:
    def __init__(self, swarm):

        self.swarm = swarm

        self.fig = plt.figure(figsize=(10, 8))

        self.ax_net  = plt.subplot2grid((2,2),(0,0),colspan=2)
        self.ax_flow = plt.subplot2grid((2,2),(1,0))
        self.ax_need = plt.subplot2grid((2,2),(1,1))

        self.nodes = self.ax_net.scatter(
            [a.pos[0] for a in swarm.agents],
            [a.pos[1] for a in swarm.agents],
            s=80
        )

        self.flow_lines = [self.ax_flow.plot([],[])[0] for _ in swarm.agents]
        self.need_lines = [self.ax_need.plot([],[])[0] for _ in swarm.agents]

        self.ax_flow.set_ylim(0,1.05)
        self.ax_need.set_ylim(0,1.05)
        self.ax_net.set_title("Collective Field")
        self.ax_net.set_axis_off()

    def animate(self, i):

        # MULTI SIGNAL WORLD
        world = [
            math.sin(i * 0.07),
            math.sin(i * 0.11 + 1.3),
            math.sin(i * 0.03 + 2.1)
        ]

        self.swarm.step(world)

        for idx,a in enumerate(self.swarm.agents):

            hc = [s["C"] for s in a.history]
            hn = [s["N"] for s in a.history]

            self.flow_lines[idx].set_data(range(len(hc)), hc)
      
