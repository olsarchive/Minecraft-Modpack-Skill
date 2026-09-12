# Minecraft Modpack Skill

面向 AI 编程助手的定制 Minecraft 整合包同步技能。已有技能名为 **`minecraft-modpack-upstream-sync`**；本仓库更新该技能，保留原有差异比较与 FTB SNBT 草稿合并工具。

适合“作者更新了，但我还要保留自己的存档、额外模组、任务进度、按键和资源包”的情况，包括 Fabric 与 NeoForge 之间的内容适配。优先找对应加载器原生版本，低成本适配，缺少提供者或需要大规模重写的内容明确暂缓。

## Skill 的原理

Skill 是**给 AI 按需读取的操作手册，加上少量确定性的工具**：

1. 助手先看到技能名称和简介，判断当前任务是否适用；也可以由用户明确点名调用。
2. 适用时读取 `SKILL.md`，据此确定保留范围、差异判断、验证与发布方式。
3. 遇到 FTB、模型、掉落或返修问题时，再读对应 `references/`，不用每次把全部历史对话塞进上下文。
4. 需要路径比较或 SNBT 合并时运行 `scripts/` 中的工具；工具结果仍要经过功能与真实运行核对。

它不训练模型权重，不在后台自动运行，不自动获得电脑或 GitHub 权限，不会让模型“永久记住全部聊天”，也不能保证永不出错。它把已经踩过的坑变成下一位执行者能找到的判断规则和验收方法。真实实例状态仍以当前文件、清单和日志为准。

## 安装与使用

将本仓库作为一个技能目录安装，目录名用 `minecraft-modpack-upstream-sync`。例如 Codex 常用路径是用户目录下的 `.codex/skills/minecraft-modpack-upstream-sync`；其它支持 SKILL.md 的助手使用各自技能目录。

若没有旧目录，可克隆：

```sh
git clone https://github.com/olsarchive/Minecraft-Modpack-Skill.git ~/.codex/skills/minecraft-modpack-upstream-sync
```

若已有旧技能，先备份并比较本地改动，再更新，不要用整目录删除覆盖。技能发现/刷新方式取决于宿主，重新打开任务后检查技能是否可选；仓库更新不会自动更新所有设备上的副本。

调用示例：

```text
使用 $minecraft-modpack-upstream-sync，检查我的定制包如何同步作者新版。
保留旧档、任务进度、按键、资源包顺序和已加装玩法。
先做差异与风险分类，再集中准备可验证批次，优先使用 NeoForge 原生对应版本。
```

用户的实际授权优先于技能中的默认流程；明确只检查时不安装，禁止桌面操作时不操控游戏，后续给出的许可应继续沿用。

## 内容

| 文件 | 用途 |
|---|---|
| [SKILL.md](SKILL.md) | 技能入口、风险分批和证据要求 |
| [compatibility.md](references/compatibility.md) | 原有兼容性、版本与历史失败判断 |
| [quest-flow.md](references/quest-flow.md) | 老任务优化、删除条件/奖励、重编号、DLC 真实提供者 |
| [runtime-and-repair.md](references/runtime-and-repair.md) | 掉落二次覆盖、换装、Rhino、构建工具和返修收敛 |
| [acceptance.md](references/acceptance.md) | 集中验收、抽样范围、授权、精确应用与回退 |
| [compare_pack.py](scripts/compare_pack.py) | 只读路径/ZIP 成员三方比较，输出不等于安装清单 |
| [merge_quests.py](scripts/merge_quests.py) | 保守 SNBT 草稿合并模块，不验证游戏注册或领奖 |

工具使用 Python 3.11+ 标准库，无需下载 Minecraft 模组。比较工具只接受其帮助中声明的输入格式，不能直接将任意 RAR/实例 ZIP 当 Modrinth 包使用。两个工具都不会自动安装或修改游戏实例。

## 这次沉淀的返修经验

- 作者老流程优化不能因为“保留旧档”全部留旧；任务身份、逻辑条件与奖励状态分别处理。
- 模组 JAR 查不到的 advancement 可能在已启用 DLC ZIP 中；存在不等于触发链已运行。
- species 文件胜出后仍可被 species_additions 覆盖；以最终解析掉落和实际行为分别验收。
- 硬币佩戴成功不等于皮肤渲染成功；单次路径查询失败也不等于批量模型加载失败。
- 修复组合变了，旧启动日志不能证明新组合通过；诊断错误不归咎作者，诊断脚本最终移出。
- 构建不能覆盖维护者源码；输入、依赖、产物可追溯，负例只改临时副本。

这里公开的是通用指南与工具，不含个人存档、作者模组 JAR、加密模型、账号信息或本机运行日志。

## 验证

```sh
python -m unittest discover -s tests -v
python scripts/compare_pack.py --help
```

25 项工具回归测试覆盖安全输出、输入格式、三方差异、本地身份与删除意图、重复键及 SNBT 往返。行为评估案例见 [tests/skill-scenarios.md](tests/skill-scenarios.md)。工具测试、技能文字场景测试与 Minecraft 实机验收是不同证据，不能相互冒充。
