# RoboLab-Skill

Open-source Skill catalog for the RoboLab one-stop motion control platform.

本仓库用于发布可以被 RoboLab 下载、安装并调用的功能包。Skill 不只表示机器人策略，也包括平台工具和写给 Agent 的工作流。

## Skill 类型

| kind | 用途 | 示例 |
|---|---|---|
| `MotionSkill` | 机器人运动能力、策略、动作和部署参数 | G1 velocity、动作模仿 |
| `PlatformSkill` | 可执行的 Python/CLI/C++ 平台功能 | MJCF 检查、数据转换、标定辅助 |
| `AgentSkill` | `SKILL.md`、操作流程和允许的平台工具 | 机器人接入助手、训练排错助手 |

每个 Skill 都必须包含 `skill.yaml`、README、LICENSE、版本、入口、权限声明和测试。可执行代码由 RoboLab Worker 以独立进程运行，不直接导入 Web API 进程。

## 目标目录

```text
RoboLab-Skill/
├── catalog.yaml
├── skills/
│   ├── motion/
│   │   └── g1_velocity/
│   ├── platform/
│   │   └── mjcf_inspector/
│   └── agent/
│       └── robot_onboarding/
└── tools/
```

单个 Skill 的通用结构：

```text
my_skill/
├── skill.yaml
├── README.md
├── LICENSE
├── environment.yml           # 可选 Conda 环境
├── src/                      # 可执行源码
├── SKILL.md                  # AgentSkill 使用，位于包根目录
├── scripts/                  # Agent/平台辅助脚本
├── references/               # Agent 参考文档
├── assets/                   # 模板和资源
├── artifacts/                # ONNX 等产物
├── motions/
├── params/
├── schemas/
└── tests/
```

## 安装模型

RoboLab 从 catalog 解析单个 Skill，固定 Git revision 并安装到：

```text
RoboLab/skills/installed/<skill-id>/<version>/<content-hash>/
```

本地开发使用 `RoboLab/skills/dev/` 链接源码目录。正式安装不可原地覆盖；更新 Skill 必须提升版本并重新校验。

## 开源与资源复用

本 catalog 中的 Skill、代码和配套资源以公开分发为目标。每个 Skill 仍需核查代码、模型、动作、mesh 和数据的实际许可证。

Skill 不复制 RoboLab/MJLab、Conda 环境、机器人公共模型或第三方 runtime，只声明依赖并携带自身独有的策略、动作、参数、源码和文档。当前样例产物体积不大，MVP 直接使用普通 Git，不预先引入 LFS/Release。以后确有大型或频繁更新的 Skill artifact 时再单独外置并固定哈希。

完整设计规范目前维护在 RoboLab 主仓库的 `docs/SKILL_SPEC.md`。

## 当前 Catalog

首个可解析样例是 `motion.unitree-g1-velocity@0.1.0`。它默认面向仿真验证，实机调用仍必须经过 Robot Profile、驱动、安全门和人工确认。Catalog 中的 release tag 在安装时应解析为 Git commit，并将解析后的 commit 和包内容哈希一同写入安装记录。
