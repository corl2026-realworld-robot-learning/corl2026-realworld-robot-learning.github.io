# RoboChess Isaac Lab task

This package contains the first manager-based Isaac Lab migration for RoboChess.

## Install

Activate the existing Isaac Lab environment, then install this package:

```bash
cd lab
uv pip install -e .
```

## Visual inspection

Launch one stationary, single-arm scene:

```bash
cd ./lab
python scripts/zero_agent.py \
  --task RoboChess-Visual-v0 \
  --num_envs 1
```

The task includes one standard Isaac Lab UR10, a table, and a 4x4 minichess board. It has no XR, teleoperation, or bimanual setup. The task uses the project chessboard and chess-piece USD/USDC assets under `assets/chess`. It remains a visual, single-arm setup without teleoperation.

## Robot options

Use `--robot` with any chess layout:

```bash
python scripts/zero_agent.py --task RoboChess-Visual-v0 --robot so101 --chess_scenario 4x4
python scripts/zero_agent.py --task RoboChess-Visual-v0 --robot piper --chess_scenario 4x4
python scripts/zero_agent.py --task RoboChess-Visual-v0 --robot ur10 --chess_scenario 4x4
python scripts/zero_agent.py --task RoboChess-Visual-v0 --robot flexiv_rizon --chess_scenario 4x4
python scripts/zero_agent.py --task RoboChess-Visual-v0 --robot rebot --chess_scenario 4x4
python scripts/zero_agent.py --task RoboChess-Visual-v0 --robot yam --chess_scenario 4x4
```

SO-101 and Piper use local USDs in `assets/`. Flexiv Rizon, Rebot, and YAM use the URLs from their existing configurations. For offline Rebot or YAM use, set `REBOT_USD_PATH` or `YAM_USD_PATH` to a local USD before launching.

## Chess layouts

Select a setup using `--chess_scenario`:

```bash
# 1D: king, knight, rook vs rook, knight, king
python scripts/zero_agent.py --task RoboChess-Visual-v0 --chess_scenario 1d

# Pawn-only 3x3
python scripts/zero_agent.py --task RoboChess-Visual-v0 --chess_scenario 3x3

# 4x4 Mallett-Hill-Boyer minichess (default)
python scripts/zero_agent.py --task RoboChess-Visual-v0 --chess_scenario 4x4

# Standard 8x8 opening
python scripts/zero_agent.py --task RoboChess-Visual-v0 --chess_scenario 8x8
```

## Franka chess picking

`RoboChess-Franka-Chess-IK-Abs-v0` is a manipulation task, not just a visual one: a
Franka Emika Panda picks the chess piece a command term selects and puts it on a
target square (or in the capture tray). Grasps come from
[GraspGen](https://github.com/NVlabs/GraspGen), and a scripted state machine turns
them into demonstrations recorded through Isaac Lab's `RecorderManager`.

See [docs/franka_chess_picking.md](docs/franka_chess_picking.md) for the full pipeline.
The short version:

```bash
PY=/home/yizhou/Projects/IsaacLab/env_isaaclab/bin/python

# 1. bake rigid-body chess pieces at 1.5x scale (+ meshes for GraspGen)
$PY lab/scripts/prepare_chess_assets.py --scale 1.5

# 2. ask GraspGen how a Franka should grasp each piece (GraspGen's own venv)
/home/yizhou/Projects/GraspGen/.venv/bin/python lab/scripts/graspgen_chess_grasps.py

# 3. generate and record demonstrations
$PY lab/scripts/generate_chess_pick_demos.py --headless --num_envs 16 --num_demos 100 \
    --chess_scenario 4x4 --dataset_file ./lab/datasets/franka_chess_pick_4x4.hdf5

# 4. replay the dataset and render it
$PY lab/scripts/render_chess_demo.py --headless --demos 0 1 2 --video \
    --dataset_file lab/datasets/franka_chess_pick_4x4.hdf5
```

Add `--chess_scenario 8x8 --zoom 1.45` for full-board chess moves (and for bishops
and queens, which the 4x4 minichess setup has none of).

### Other arms

The task is robot-agnostic. `--robot` selects any of `franka`, `piper`, `rebot` or
`yam`; all four load straight from their upstream URLs, nothing is vendored:

```bash
$PY lab/scripts/probe_robot.py --headless --robot rebot      # joints, prims, gripper axes
$PY lab/scripts/probe_reach.py --headless --robot rebot      # can it reach the board?

$PY lab/scripts/generate_chess_pick_demos.py --headless --robot rebot \
    --chess_scenario pieces --balance_kinds --num_demos 10 \
    --dataset_file ./lab/datasets/chess_pick_rebot.hdf5
```

`--chess_scenario pieces` is a compact 3x3 board holding one of every piece kind,
sized so the shorter arms can reach all of it; `--balance_kinds` steers each episode
toward the kind with the fewest recorded demos so a short run still covers pawn,
rook, knight, bishop, queen and king. See
[docs/how_this_was_built.md](docs/how_this_was_built.md) for what each arm needed.

### reBot picking a pawn

The `pieces` board is the hard case for a short arm, because a king standing on it
forces every carry up to 141 mm. On the pawn-only `3x3` board the tallest piece is
the pawn itself, the carry drops to 120 mm, and the reBot picks pawns reliably --
**32 demos in 32 attempts**, 2.3 mm mean placement error:

```bash
$PY lab/scripts/generate_chess_pick_demos.py --headless --robot rebot \
    --chess_scenario 3x3 --num_envs 8 --num_demos 32 \
    --dataset_file ./lab/datasets/chess_pick_rebot_pawn.hdf5

$PY lab/scripts/render_chess_demo.py --headless --video \
    --task RoboChess-Chess-Pick-IK-Abs-v0 --robot rebot --chess_scenario 3x3 \
    --dataset_file lab/datasets/chess_pick_rebot_pawn.hdf5 --demos 0 \
    --eye 0.85 -0.70 1.32 --lookat 0.02 -0.02 0.95
```

`render_chess_demo.py` needs `--robot` here: the recorded actions are end-effector
poses in *that* arm's base frame, so replaying a reBot dataset with the default
Franka drives a different body to different places. `--eye/--lookat` override the
built-in views, which are framed for a Franka over the 4x4 board and cut a shorter
arm's wrist off the top of the shot.

### Replaying a demo on a real arm

The `actions` in the dataset are end-effector poses, only meaningful to the
simulator's IK controller. What a real arm replays is the *measured* joint
trajectory, recorded every control step in
`states/articulation/robot/joint_position`. `export_joint_trajectory.py` writes it
out as CSV + JSON, and is the one script here that does **not** launch Isaac Sim --
plain h5py and numpy, so it runs on the robot's own machine:

```bash
python lab/scripts/export_joint_trajectory.py \
    --dataset_file lab/datasets/chess_pick_rebot_pawn.hdf5 --demos 0
```

Each CSV is `time_s`, the joint positions, the joint velocities, then `gripper_cmd`
(+1 open / -1 close) -- 30 Hz, revolute joints in radians and the gripper's prismatic
joints in metres. Take the gripper from `gripper_cmd` rather than from the recorded
finger positions: those are where physics settled while squeezing a piece, not a
target worth servoing to.

The joint *order* is stamped into the dataset by the generator, read back by the
exporter, and reported on every run -- a mislabelled column is not a silent error on
real hardware. Datasets recorded before that stamping need `--robot <key>`, which
falls back to a table verified against `probe_robot.py`. The JSON alongside each CSV
carries the peak joint speed, which is the first thing to check against a real arm's
limits: the sim controller is not rate-limited and a real one is.
