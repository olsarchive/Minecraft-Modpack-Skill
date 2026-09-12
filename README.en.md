# Minecraft Modpack Skill

An English edition of the `minecraft-modpack-upstream-sync` skill for keeping a customized Minecraft pack aligned with an author's update while preserving worlds, quest progress, local mods, keybinds, resource packs, and shaders. It favors native mods for the target loader and low-cost adapters; missing providers and large rewrites stay explicitly deferred.

## How the skill works

It is an on-demand AI playbook plus small deterministic tools. The assistant reads `SKILL.en.md`, follows the workflow, then consults the relevant English references and runs the scripts when needed. It does not train model weights, run in the background, grant computer/GitHub permissions, remember every chat forever, or guarantee zero errors. Real instance files, manifests, logs, and runtime checks remain authoritative.

## Install

Clone the repository, then use `SKILL.en.md` as the English entry file. Hosts that require the conventional name can copy it to `SKILL.md` inside a separate skill directory; keep `references/`, `scripts/`, and `agents/openai.yaml` beside it. The Chinese edition remains `SKILL.md`.

```sh
git clone https://github.com/olsarchive/Minecraft-Modpack-Skill.git
```

Invoke it with `$minecraft-modpack-upstream-sync` and state that English guidance is preferred. Existing installations should be backed up and compared before refresh. Repository updates do not automatically update every device.

## English guide map

- [SKILL.en.md](SKILL.en.md): workflow, risk batches, authorization, and evidence states
- [compatibility.en.md](references/compatibility.en.md): versions, loaders, providers, and failure diagnosis
- [quest-flow.en.md](references/quest-flow.en.md): FTB IDs, rewards, deletions, and DLC chains
- [runtime-and-repair.en.md](references/runtime-and-repair.en.md): drops, coins, cosmetics, Rhino, and reproducible repairs
- [acceptance.en.md](references/acceptance.en.md): batched runtime checks, application, and rollback
- [scripts/compare_pack.py](scripts/compare_pack.py): read-only three-way path/ZIP comparison
- [scripts/merge_quests.py](scripts/merge_quests.py): conservative SNBT draft merge
- [README.md](README.md): Chinese edition

The Python tools use only the standard library (Python 3.11+). They never install or modify a game instance. Public files contain generic instructions and synthetic cases only; no personal worlds, account data, author JARs, restricted assets, or runtime logs.

## Verification

```sh
python -m unittest discover -s tests -v
python scripts/compare_pack.py --help
```

Tool tests, prose behavior scenarios, and real Minecraft acceptance are separate evidence. A menu or postInit pass does not prove an old-world feature, quest reward, battle, or every cosmetic works.
