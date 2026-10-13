# RoboChess challenge package

This folder contains the CoRL 2026 RoboChess challenge page, the Newton physics and Isaac Lab implementations, and the assets those implementations need at runtime.

The code and assets were copied from the local RoboChess project at `~/Projects/RoboChess-Challenge-no-edit`, based on upstream commit `1b246fb` plus its current working-tree updates to the Isaac Lab documentation, demonstration scripts, and joint-trajectory exporter. The upstream project remains the primary development repository: https://github.com/yizhouzhao-nvidia/RoboChess-Challenge

## Layout

- `index.html` — challenge webpage.
- `images/` — screenshots from the RoboChess project used on the webpage.
- `newton/` — Newton scene inspection and scripted chess picking.
- `lab/` — Isaac Lab tasks, scripts, and documentation.
- `assets/chess/` — board and chess-piece USD assets, baked pieces, and grasp metadata.
- `assets/piper/piper_camera.usd` — Piper robot asset used by both implementations.
- `assets/so101/TheRobotStudio/` — SO-101 asset used by Isaac Lab.

Generated HDF5 datasets, videos, and render outputs are not included. The scripts in `lab/` and `newton/` can generate them with the dependencies described in their respective READMEs.

## Run from this folder

Install the simulation dependencies described in [Isaac Lab](lab/Readme.md) or [Newton](newton/README.md), then run the examples from the folder containing this README:

```bash
python lab/scripts/zero_agent.py --task RoboChess-Visual-v0 --robot so101 --chess_scenario 4x4
python newton/scripts/visualize_chess.py --robot franka --scenario 4x4 --viewer null --num-frames 120
python newton/scripts/run_chess_pick.py --robot franka --scenario 4x4 --world-count 8 --num-episodes 16 --viewer null
```

These are Python simulation programs, not browser features. The webpage is static and works without installing either simulator. The source documentation contains more examples and environment-specific setup steps.
