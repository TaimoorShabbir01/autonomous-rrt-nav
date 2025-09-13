# Autonomous RRT Navigation (Pygame)

A tiny, self-contained demo of autonomous car navigation using **RRT (Rapidly-exploring Random Tree)** for path planning and **Pygame** for visualization.

https://github.com/your-username/autonomous-rrt-nav

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
├─ LICENSE
└─ README.md
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

## ❗Troubleshooting

**Problem:** `python was not found` or `pip is not recognized` (Windows)  
**Fix:** Reinstall Python from python.org and ensure “Add to PATH” is checked. Reopen VS Code/terminal.

**Problem:** `ModuleNotFoundError: No module named 'pygame'`  
**Fix:** Activate your venv (see above) and run `pip install -r requirements.txt`.

**Problem:** Black screen or no window on WSL/remote terminals  
**Fix:** Pygame needs a display. Run on Windows/macOS/Linux with a GUI session.

**Problem:** Asset not found (`car.png`)  
**Fix:** Keep `assets/car.png`. You can also change the asset path inside `src/main.py`.

## 📝 License
MIT — see [LICENSE](./LICENSE).

## 🙌 Credits
- Your original Pygame environment and RRT logic made this demo possible.
