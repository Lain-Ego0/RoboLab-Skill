"""Worker entry point for the MJCF Inspector PlatformSkill."""
from __future__ import annotations

import json
import os
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path


def _event(payload: dict) -> None:
    with Path(os.environ["ROBOLAB_EVENTS_FILE"]).open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(payload, ensure_ascii=False) + "\n")


def inspect(source: Path, artifacts: Path) -> dict:
    root = ET.parse(source).getroot()
    joints = root.findall(".//joint")
    names = [node.get("name") for node in joints if node.get("name")]
    warnings = []
    duplicates = sorted(name for name, count in Counter(names).items() if count > 1)
    if duplicates:
        warnings.append("重复 joint 名称: " + ", ".join(duplicates))
    missing_ranges = [node.get("name", "<unnamed>") for node in joints if node.get("limited") == "true" and not node.get("range")]
    if missing_ranges:
        warnings.append("limited joint 缺少 range: " + ", ".join(missing_ranges))
    actuators = root.findall(".//actuator/*")
    bound = {node.get("joint") for node in actuators if node.get("joint")}
    compiler = root.find("./compiler")
    mesh_dir = source.parent / (compiler.get("meshdir") if compiler is not None and compiler.get("meshdir") else ".")
    assets = [node.get("file") for node in root.findall(".//asset/*") if node.get("file")]
    includes = [node.get("file") for node in root.findall(".//include") if node.get("file")]
    missing_assets = [item for item in [*assets, *includes] if not (source.parent / item).is_file() and not (mesh_dir / item).is_file()]
    if missing_assets:
        warnings.append("找不到 include/mesh/texture 资源: " + ", ".join(missing_assets))
    counts = {tag: len(root.findall(f".//{tag}")) for tag in ("body", "joint", "sensor", "site", "geom", "key", "include")}
    counts["actuator"] = len(actuators)
    report = {"schemaVersion": "robolab.mjcf-inspection.v1", "source": str(source), "counts": counts, "joints": [{"name": node.get("name"), "type": node.get("type", "hinge"), "limited": node.get("limited", "false"), "range": node.get("range"), "axis": node.get("axis", "1 0 0"), "pos": node.get("pos")} for node in joints], "actuatorJointNames": sorted(bound), "unactuatedJointNames": sorted(set(names) - bound), "assetReferences": {"includes": includes, "files": assets, "missing": missing_assets}, "candidates": {"rootBodies": [node.get("name") for node in root.findall("./worldbody/body")], "imuFrames": [node.get("name") for node in root.findall(".//site") if "imu" in (node.get("name") or "").lower()], "endEffectors": [node.get("name") for node in root.findall(".//site") if any(word in (node.get("name") or "").lower() for word in ("foot", "toe", "end"))]}, "warnings": warnings}
    (artifacts / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (artifacts / "report.md").write_text("# MJCF inspection report\n\n" + f"- Source: `{source}`\n- Joints: {len(joints)}\n- Actuators: {len(actuators)}\n\n## Warnings\n\n" + ("\n".join(f"- {item}" for item in warnings) or "- None") + "\n", encoding="utf-8")
    draft = "# DRAFT ONLY: cannot authorize physical deployment\napiVersion: robolab.dev/v1alpha1\nkind: RobotProfileDraft\nmetadata:\n  maturity: simulation-only-draft\nspec:\n  requiresHumanJointMappingReview: true\n  jointCandidates:\n" + "".join(f"    - {name}\n" for name in names)
    (artifacts / "robot_profile.draft.yaml").write_text(draft, encoding="utf-8")
    return report


def main() -> None:
    input_data = json.loads(Path(os.environ["ROBOLAB_INPUT_FILE"]).read_text(encoding="utf-8"))
    _event({"type": "inspection.started"})
    report = inspect(Path(input_data["parameters"]["mjcf_path"]).resolve(), Path(os.environ["ROBOLAB_ARTIFACTS_DIR"]))
    Path(os.environ["ROBOLAB_RUN_DIR"], "result.json").write_text(json.dumps({"status": "SUCCEEDED", "report": "artifacts/report.json", "warningCount": len(report["warnings"])}) + "\n", encoding="utf-8")
    _event({"type": "inspection.finished", "warningCount": len(report["warnings"])})


if __name__ == "__main__":
    main()
