"""Export a recorded demonstration as a joint-space trajectory for a real arm.

``generate_chess_pick_demos.py`` records the arm's *measured* joint positions every
control step in ``states/articulation/robot/joint_position``. That -- not the
``actions``, which are end-effector poses only meaningful to the simulator's IK
controller -- is what a real robot replays.

Unlike the rest of ``lab/scripts``, this one does **not** launch Isaac Sim: it is
plain h5py + numpy so it can run on the robot's own machine.

If you cross-check the exported angles against the recorded TCP, mind the one-step
skew: ``obs/*`` is the state *before* each step and ``states/*`` the state after, so
``FK(row t)`` corresponds to ``obs/eef_pos[t + 1]``.  ``obs/joint_pos`` is also
relative to ``default_joint_pos``, not absolute.  See ``docs/franka_chess_picking.md``.

.. code-block:: bash

    python lab/scripts/export_joint_trajectory.py \
        --dataset_file lab/datasets/chess_pick_rebot_pawn.hdf5 --demos 0
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import h5py
import numpy as np

# Joint order for datasets recorded before the generator started stamping it in.
# Verified against the articulation itself (lab/scripts/probe_robot.py --robot <key>),
# which is the only authority on the order the state arrays are written in.
FALLBACK_JOINT_NAMES = {
    "rebot": ["joint1", "joint2", "joint3", "joint4", "joint5", "joint6", "joint_left", "joint_right"],
    "piper": ["joint1", "joint2", "joint3", "joint4", "joint5", "joint6", "joint7", "joint8"],
    "franka": [f"panda_joint{i}" for i in range(1, 8)] + ["panda_finger_joint1", "panda_finger_joint2"],
    "yam": ["joint1", "joint2", "joint3", "joint4", "joint5", "joint6", "left_finger", "right_finger"],
}


def resolve_joint_names(group: h5py.Group, robot: str | None, width: int) -> tuple[list[str], str]:
    """Joint names for the recorded columns, preferring what the dataset itself says."""
    stamped = group.attrs.get("joint_names")
    if stamped is not None:
        names = [n.decode() if isinstance(n, bytes) else str(n) for n in stamped]
        if len(names) == width:
            return names, "dataset"
        raise ValueError(f"Dataset stamps {len(names)} joint names but the states are {width} wide.")

    key = robot or group.attrs.get("robot")
    if isinstance(key, bytes):
        key = key.decode()
    if key in FALLBACK_JOINT_NAMES:
        names = FALLBACK_JOINT_NAMES[key]
        if len(names) != width:
            raise ValueError(f"Known joint order for '{key}' has {len(names)} entries, states are {width} wide.")
        return names, f"fallback table for '{key}'"

    raise ValueError(
        "This dataset predates joint-name stamping and --robot was not given (or is unknown). "
        f"Pass --robot one of {sorted(FALLBACK_JOINT_NAMES)}, or re-record it."
    )


def check_limits(positions: np.ndarray, names: list[str], group: h5py.Group) -> list[str]:
    """Warn about anything a real controller would reject. Advisory, not fatal."""
    warnings = []
    lower = group.attrs.get("joint_lower_limits")
    upper = group.attrs.get("joint_upper_limits")
    if lower is not None and upper is not None:
        for index, name in enumerate(names):
            low, high = float(lower[index]), float(upper[index])
            if positions[:, index].min() < low - 1e-4 or positions[:, index].max() > high + 1e-4:
                warnings.append(
                    f"{name}: trajectory spans "
                    f"[{positions[:, index].min():+.4f}, {positions[:, index].max():+.4f}] "
                    f"outside the recorded limits [{low:+.4f}, {high:+.4f}]"
                )
    return warnings


def export(group: h5py.Group, demo: str, names: list[str], dt: float, output_dir: Path, decimals: int) -> dict:
    episode = group[demo]
    positions = np.asarray(episode["states/articulation/robot/joint_position"][:], dtype=float)
    velocities = np.asarray(episode["states/articulation/robot/joint_velocity"][:], dtype=float)
    # The gripper command is the sign of the last action column: +1 open, -1 close.
    # Worth carrying separately -- a real gripper usually takes an open/close command
    # rather than a finger position, and the recorded finger angle is where physics
    # settled while squeezing a piece, not a target you want to servo to.
    actions = np.asarray(episode["actions"][:], dtype=float)
    gripper_cmd = np.sign(actions[:, -1]).astype(int)

    steps = len(positions)
    time = np.arange(steps) * dt

    csv_path = output_dir / f"{demo}_joint_trajectory.csv"
    with csv_path.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["time_s", *names, *(f"{n}_vel" for n in names), "gripper_cmd"])
        for step in range(steps):
            writer.writerow(
                [f"{time[step]:.6f}"]
                + [f"{value:.{decimals}f}" for value in positions[step]]
                + [f"{value:.{decimals}f}" for value in velocities[step]]
                + [gripper_cmd[step]]
            )

    # Peak joint speed matters more than anything else when moving this to hardware:
    # the sim controller is not rate-limited and a real arm is.
    finite_diff = np.abs(np.diff(positions, axis=0)) / dt if steps > 1 else np.zeros((1, positions.shape[1]))
    meta = {
        "demo": demo,
        "num_steps": steps,
        "control_dt_s": dt,
        "control_rate_hz": round(1.0 / dt, 4),
        "duration_s": round(steps * dt, 4),
        "joint_names": names,
        "units": "revolute joints in radians, prismatic gripper joints in metres",
        "columns": "time_s, <joint positions>, <joint velocities>, gripper_cmd (+1 open / -1 close)",
        "start_joint_position": [round(v, 6) for v in positions[0]],
        "end_joint_position": [round(v, 6) for v in positions[-1]],
        "max_abs_joint_velocity_rad_s": {
            name: round(float(np.abs(velocities[:, i]).max()), 4) for i, name in enumerate(names)
        },
        "max_step_delta_rad_per_s": {
            name: round(float(finite_diff[:, i].max()), 4) for i, name in enumerate(names)
        },
    }
    json_path = output_dir / f"{demo}_joint_trajectory.json"
    json_path.write_text(json.dumps(meta, indent=2) + "\n")
    return {"meta": meta, "csv": csv_path, "json": json_path, "positions": positions}


def main() -> None:
    parser = argparse.ArgumentParser(description="Export recorded demos as joint-space trajectories.")
    parser.add_argument("--dataset_file", type=str, required=True, help="HDF5 written by generate_chess_pick_demos.py")
    parser.add_argument("--demos", type=int, nargs="+", default=[0], help="Episode indices to export.")
    parser.add_argument("--all", action="store_true", help="Export every episode in the dataset.")
    parser.add_argument("--robot", type=str, default=None, help="Arm key, for datasets with no stamped joint names.")
    parser.add_argument("--output_dir", type=str, default=None, help="Defaults to <dataset>_trajectories/.")
    parser.add_argument("--decimals", type=int, default=6, help="Decimal places in the CSV.")
    args = parser.parse_args()

    dataset_path = Path(args.dataset_file).resolve()
    if not dataset_path.exists():
        raise FileNotFoundError(f"No dataset at {dataset_path}")
    output_dir = Path(args.output_dir) if args.output_dir else dataset_path.parent / f"{dataset_path.stem}_trajectories"
    output_dir.mkdir(parents=True, exist_ok=True)

    with h5py.File(dataset_path, "r") as handle:
        group = handle["data"]
        episodes = sorted(group.keys(), key=lambda name: int(name.split("_")[-1]))
        wanted = episodes if args.all else [episodes[i] for i in args.demos if i < len(episodes)]
        if not wanted:
            raise ValueError(f"No matching episodes; the dataset holds {len(episodes)}.")

        width = group[wanted[0]]["states/articulation/robot/joint_position"].shape[1]
        names, source = resolve_joint_names(group, args.robot, width)
        dt = float(group.attrs.get("control_dt", 1.0 / 30.0))
        print(f"[INFO] {dataset_path.name}: {len(episodes)} episodes, joint order from {source}")
        print(f"[INFO] joints ({len(names)}): {names}")
        print(f"[INFO] control rate {1.0 / dt:.4g} Hz")

        for demo in wanted:
            result = export(group, demo, names, dt, output_dir, args.decimals)
            meta = result["meta"]
            print(f"[INFO] {demo}: {meta['num_steps']} steps, {meta['duration_s']:.2f} s -> {result['csv']}")
            for warning in check_limits(result["positions"], names, group):
                print(f"[WARN] {demo}: {warning}")

    print(f"[INFO] Wrote {len(wanted)} trajectory file(s) to {output_dir}")


if __name__ == "__main__":
    main()
