---
name: robot-onboarding
description: Guide safe simulation-first RoboLab robot onboarding using MJCF inspection and explicit human mapping review.
---

# Robot Onboarding

Start by locating a public MJCF/XML model and running the approved MJCF Inspector action. Read `references/workflow.md` before proposing a Robot Profile. Treat every inferred joint semantic, direction, actuator range, frame and control period as a question for the developer to confirm.

Only generate a simulation-only draft after the report has been reviewed. Run L0 schema and mapping checks, then describe the evidence needed for L1 simulation validation. Never claim physical support or invoke deployment: this Skill explicitly denies `robolab.deployments.activate_real`.
