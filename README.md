# Autonomous RRT Navigation (Pygame)

A tiny, self-contained demo of autonomous car navigation using **RRT (Rapidly-exploring Random Tree)** for path planning and **Pygame** for visualization.

---

## ✨ Features
- Randomized obstacle field and a target zone
- RRT-based path planning with basic collision checking
- Smooth path interpolation and simple waypoint following
- Minimal assets (a tiny placeholder `car.png` included; drop your own if you like)

## 🗂 Project Structure
```
autonomous-rrt-nav/
├─ src/
│  ├─ main.py         # Pygame app & game loop
│  └─ rrt.py          # RRT planner (tree growth, collision checks, smoothing)
├─ assets/
│  └─ car.png         # Placeholder image; replace with your own
├─ requirements.txt   # Python deps
├─ .gitignore
```

## ▶️ Quick Start

### 1) Install Python
- **Windows/Mac/Linux:** Install Python 3.9+ from https://www.python.org/downloads/
- During Windows install, tick **“Add python.exe to PATH”**.

### 2) Create a virtual environment (recommended)
```bash
python -m venv .venv
# Activate:
# Windows:
.\.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate
```

### 3) Install dependencies
```bash
pip install -r requirements.txt
```

### 4) Run
```bash
python src/main.py
```

You should see a window titled **"Autonomous Car Navigation with RRT Pathfinding"**. A random obstacle field will be generated and the RRT will search a path to the green target ring.

## 🧩 Controls
- No controls needed—it's fully automatic. Close the window to quit.

## 🔧 Configuration Tips
You can tweak a few parameters inside `src/main.py`:
- Window size (`WIDTH`, `HEIGHT`)
- Obstacles: number/size (`num_obstacles`, `obstacle_size`)
- Car speed (`car_speed`)
- RRT settings passed to `rrt(...)` like `step_size` and `max_iter`

Also see `src/rrt.py` for:
- Collision model in `is_collision_free(...)`
- Path smoothing in `waypoints2path(...)`

## 🖼️ Assets
Replace `assets/car.png` with any small PNG (e.g., 30×30). The app already tries to load an image next to `main.py`, falling back to a colored rectangle if none is found.

## 🙌 Credits
- Your original Pygame environment and RRT logic made this demo possible.
