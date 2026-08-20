# Unitree G1 Velocity

`motion.unitree-g1-velocity` 是 RoboLab 的首个 MotionSkill 样例。它封装上游 `unitree_rl_mjlab` 的 G1 29DoF 速度控制策略、部署参数、输入 schema 和来源记录，供平台安装器进行哈希校验和兼容性判断。

## 适用范围

- Robot Profile：`unitree.g1.29dof`，`>=1.0.0 <2.0.0`
- 控制方式：29 维关节位置目标，50 Hz
- 指令：机体坐标系下的前向速度、侧向速度和偏航角速度
- 默认用途：MJLab 回放和 sim-to-sim 验证
- 成熟度：`experimental`

该包不是通用 G1 固件，也不包含 MuJoCo、MJLab、ONNX Runtime、Unitree SDK、机器人 MJCF/mesh 或电机驱动。它依赖 RoboLab 的 Robot Profile、MJLab adapter 和 motion runtime 提供这些公共能力。

## 调用参数

三个动作使用相同的 `schemas/command.json`。示例：

```json
{
  "linear_x": 0.4,
  "linear_y": 0.0,
  "angular_z": 0.0,
  "duration_seconds": 10.0
}
```

输入范围来自随包发布的 `params/deploy.yaml`。平台必须在调用 policy 前再次限幅，不能只依赖 WebUI 表单校验。

## 验证顺序

1. 校验 `skill.yaml` 中两个 artifact 的大小和 SHA-256；
2. 使用 `unitree.g1.29dof` Profile 验证 joint set、观测顺序和动作顺序；
3. 先完成离线 ONNX smoke test；
4. 在 MJLab 中回放；
5. 完成 sim-to-sim 验证；
6. 只有驱动、急停、状态估计、限位和阻尼回退均已配置后，才允许显式确认实机动作。

当前 RoboLab 尚未承诺一键实机部署已经可用。`deploy` action 是为后续 runtime/driver 接口预留的受控入口，不表示此策略已在任意具体硬件、场地或负载下通过安全验证。

## 来源与许可证

策略与参数来自：

- 仓库：<https://github.com/unitreerobotics/unitree_rl_mjlab>
- 固定版本：`1425b15f73bd4095f0df53709d7c389c3eb9e790`
- 原始路径见 `skill.yaml` 的 `metadata.provenance.paths`
- 许可证：Apache License 2.0，见本目录 `LICENSE`

RoboLab 与 Unitree 没有在本包中声明官方合作或背书关系。Unitree G1 是首个兼容目标，不构成 RoboLab 的品牌范围。
