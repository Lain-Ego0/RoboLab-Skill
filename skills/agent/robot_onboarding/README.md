# Robot Onboarding AgentSkill

This AgentSkill guides the simulation-first path from a public MJCF to a reviewed RoboLab Robot Profile draft. It has only read/inspection actions and deliberately cannot activate real-robot deployment.

Export it with `robolab agent export agent.robot-onboarding --source <package>`. The generated Codex directory keeps the public `SKILL.md`, references and an `agents/openai.yaml` metadata file.
