# MJCF Inspector

`tools.mjcf-inspector` reads one XML/MJCF file from a permitted workspace path. It never writes to the source model, uses no network or robot capability, and writes only the current RoboLab Job's `artifacts/` directory.

The `inspect` action requires `mjcf_path` and accepts `asset_root`. It creates `report.json`, `report.md`, and `robot_profile.draft.yaml`. The draft is explicitly simulation-only and requires human review of every joint mapping; it cannot be used for physical deployment.

The parser detects XML include references, common model element counts, joint name collisions, incomplete joint ranges and actuator bindings. If MuJoCo is available in the inherited environment it also records a load attempt; its absence is reported as a warning, not hidden.
