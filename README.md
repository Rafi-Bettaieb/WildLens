# 🦅🐍🦇 WildLens

WildLens is a **2D stealth and puzzle adventure game** where you play as an elite agent equipped with a high-tech visor capable of simulating **animal vision**.

In a world where nature has been replaced by artificial replicas, your mission is to **see beyond appearances**, expose robotic impostors, and navigate environments where normal vision is no longer enough.

---

## 📖 Story

> **"Agent, listen carefully.  
A corrupt corporation has replaced nature with a perfect lie.  
Use your WildLens to remove the camouflage and reveal the hidden truth underneath."**

The world you explore looks alive — but much of it isn’t.  
Only by switching perception modes can you uncover what is real… and what is manufactured.

---

## 🎮 Gameplay Overview

WildLens is built around **perception-based gameplay**.  
Each level requires the player to **change vision filters in real time** to solve puzzles, detect enemies, and survive.

### Core Gameplay Pillars
- Observation over action
- Vision-based puzzle solving
- Stealth and time pressure
- Environmental storytelling

---

## 🔍 Vision System (Core Mechanic)

You can switch between **6 animal vision modes**, each with unique gameplay effects.

### 🧩 Vision Mechanics

- **🐍 Snake – Thermal Vision**  
  Highlights heat signatures. Essential for distinguishing living creatures from cold robotic replicas.

- **🐝 Bee – Ultraviolet Vision**  
  Reveals UV patterns invisible to humans. Used to identify specific flowers or clues.

- **🦇 Bat – Echolocation (Sonar)**  
  Emits sound waves to reveal walls and obstacles in complete darkness.

- **🦅 Eagle – Zoom Vision**  
  Zooms in and increases contrast to detect distant or subtle details.

- **🐶 Dog – Dichromatic Vision**  
  Simulates color blindness and blur, altering perception and difficulty.

- **🐟 Fish – Deep Sea Vision**  
  Simulates underwater depth, distortion, fog, and visual noise.

---

## 🗺️ Levels

### Level 1 – **Cold Blood** 🐍  
A herd of sheep stands before you.  
One of them is a robotic spy.  
Use **thermal vision** to identify the cold impostor.

### Level 2 – **Nectar** 🐝  
A field of identical flowers.  
Only one is real.  
Use **UV vision** to reveal hidden nectar patterns.

### Level 3 – **Echolocation** 🦇  
A pitch-black maze.  
No light. No sight.  
Navigate using **sound waves** to reveal the environment.

---

## ⏱️ Time Attack Mode

All missions are under a **global timer**.  
Think fast, switch visions efficiently, and avoid mistakes — time is always against you.

---

## 🕹️ Controls

| Action | Key |
|------|----|
| Move | Arrow Keys / WASD / ZQSD |
| Interact / Capture | Space |
| Confirm / Next Level | Enter |
| Quit / Back | Esc |
| Reset Vision | 0 |
| 🐶 Dog Vision | 1 |
| 🐝 Bee Vision | 2 |
| 🦅 Eagle Vision | 3 |
| 🦇 Bat Vision | 4 |
| 🐟 Fish Vision | 5 |
| 🐍 Snake Vision | 6 |

---
## Project Structure

WildLens/

│── main.py        # Entry point, menu, and main game loop

│── input.py       # Gestion entrées (clavier)

│── filters.py     # Vision effects using NumPy & Pygame

│── map.py         # Tile-based map rendering and collision

│── player.py      # Player logic and animations

│── sprite.py      # Generic sprite handling class

│── levels/        # Level logic (Level 1, 2, 3)

│── images/        # Graphics assets

│── sounds/        # Audio assets

│── maps/          # Map of the game

---

## ⚙️ Installation

### Prerequisites
- Python **3.x**
- pip

### Dependencies
- `pygame`
- `numpy`

Install dependencies with:
```bash
pip install pygame numpy
```
---
## 🚀 How to Run
1. Clone or download the repository

2. Navigate to the project folder

3. Run the main script:
   ```bash
   python main.py
