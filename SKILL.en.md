---
name: minecraft-modpack-upstream-sync
description: Use when a customized Minecraft modpack must follow an author's pack update while preserving an existing world, local additions or patches, especially across Fabric and NeoForge or after an earlier full-pack port.
---

# Sync a customized modpack with upstream

Match the author's gameplay and content contracts while preserving the local features the user chose. A version number, file count, or successful launch alone does not prove synchronization is complete.

This is an AI operating guide with read-only tools, not an automatic updater. Prefer native mods for the target loader. Aim for equivalent gameplay rather than forcing every reference file into the instance. Rewriting entire mods is outside the default scope. Consider a small adaptation only when its root cause, limited scope, reproducibility, and validation are clear; otherwise preserve local gameplay and record deferred features.

## Establish the current scope

Carry forward the user's existing scope and authorization. If instructed to inspect now and test later, read the instance and prepare manifests and adaptation materials in a separate workspace. Do not copy a world while it is being saved, launch the game, modify MAIN, or edit the launcher database. If adaptations remain unresolved, explicitly say that testing is not the only remaining work.

Installation, desktop control, world entry, and publishing each follow the user's actual authorization. Later explicit permission can supersede earlier restrictions; do not ask again for permission already granted. If conversation history is incomplete, recover status from current files, manifests, and logs. Do not repeat or overwrite applied work because an old summary stopped at an earlier batch.

## 1. Identify the real baseline

- Confirm the launcher display name, actual directory, latest launch log's gameDir, and exact Minecraft and loader versions. Directory names and old records may be stale.
- Read previous migration records, backup manifests, final handoffs, and subsequent user feedback. Separate verified repairs, failed attempts, and withdrawn patches. An earlier claim of being fixed is not runtime evidence.
- Establish author baseline B, updated upstream U, and customized local L. Record multiple ancestors for mixed packs, such as a NeoForge base plus later Fabric content; do not invent a complete common ancestor.
- Read upstream removals, migrations, renames, and coupled dependency changes. Updating every mod is not a substitute for matching the author's release.

## 2. Produce comparison evidence

Use the [read-only comparison tool](scripts/compare_pack.py), starting with `--help`. It accepts original Modrinth ZIPs and actual instance directories, recording hashes, ZIP member differences, and three-way states. Extracted import-package directories, ordinary instance ZIPs, and empty inputs are unsupported and fail; do not interpret them as upstream deleting everything. Python 3.11+, standard library only; no downloads or installation.

```text
python scripts/compare_pack.py --base author-old.zip --upstream author-new.zip --local current-instance --out audit/three-way.json
```

This is a **path comparison**, not an installation manifest. JAR renames, Fabric/NeoForge replacements, and remote index references cannot be classified as missing mods merely because a file is absent. World files are outside the tool's scope and need a separate read-only audit.

Write to a new output file outside every input. Use another report filename on reruns. Index client/server `env` conditions are preserved; optional or disabled conditions remain `unresolved` until the intended side is established. Side-specific overrides are unsupported; do not treat server-only files as client installation candidates.

| Difference | Decision |
|---|---|
| L equals U | Keep; ZIP compression-only changes need no update |
| U equals B, L differs | Preserve local changes, including local deletions |
| L equals B, U differs | Update candidate, still requiring dependency and gameplay validation |
| Both changed / unknown baseline | Conflict; inspect actual fields or archive entries |
| Upstream deletion | Investigate relocated functionality and old-world references; neither delete automatically nor mechanically keep obsolete high-priority overrides |

Complete the evidence manually: active and disabled JARs, mod IDs/versions/dependencies, declared nested JARs, configuration, KubeJS, resource/shader order, global-pack entry points, the actual world's enabled datapack order in `level.dat`, and world-local patches. Read copies or stable on-disk state and record the observation time.

## 3. Resolve complete feature chains

Follow [compatibility and historical failures](references/compatibility.en.md):

- Match Minecraft, mod ID, loader, version range, and hash. Identical names and versions can hide author modifications. Distinguish top-level duplicates from loader-selected nested dependencies.
- Look for a native build matching the author's target first; assess an existing bridge only if none exists. Connector recognizing a JAR does not prove its mixins, registrations, or events work.
- Read the **conditions** of past failures. Revalidate when target, dependency, data, or patch conditions have changed for an explainable reason. Neither permanently blacklist a changed version nor ignore a still-applicable failure.
- Preserve local gameplay and repairs. Do not downgrade the base, remove features, clear world data, or edit metadata to pretend compatibility merely to satisfy copied dependencies.
- Merge quests by chapter/task/condition/reward IDs and references. Combine local technology chapters with upstream additions; check chapter groups, dependency edges, items, and commands. ID count is not task count; report duplicate IDs as conflicts.
- Migrate datapacks and resource packs together, checking the effective provider of each resource. Treat recipe/registration IDs as KubeJS merge boundaries. Node syntax validation cannot replace Rhino and game-registry validation.

Read specialized guides as needed:

- Old FTB flow improvements, renumbering, condition/reward deletion, and missed DLC providers: [quest synchronization](references/quest-flow.en.md). Preserving progress does not mean retaining obsolete upstream logic.
- Cobblemon `species_additions` overwrites, coins/skins, model-query differences, Rhino, and build-tool repairs: [runtime and repair](references/runtime-and-repair.en.md). Collect separate evidence for disk content, resource-stack winner, final parsed objects, and behavior.

Quest drafts can use `parse`, `merge(B, U, L, notes)`, and `dump` from the [SNBT merge module](scripts/merge_quests.py). It is a Python module with no file writes or installation command. The caller writes to a separate new directory, preserves `notes`, and checks parsed round trips. Use the module's `MISSING` for absent files; produce no file when it returns that value. Duplicate keys are rejected by default. Only after proving the actual FTB parser uses last-value-wins may the caller explicitly supply a duplicate-record list and `last_wins=True`; do not relax all sources globally.

The module conservatively preserves local IDs, deletion intent, and conflicting fields. It **does not validate dependency graphs, item registration, commands, or functional equivalence**. Compare invalid references before and after merging; filenames are not quest dependencies. Changed chapter IDs, simultaneous additions sharing an ID, and upstream object deletions require review. A parseable draft is not ready to install.

When settings must remain unchanged, snapshot and compare every existing keybind, enabled resource-pack list and order, shaders, and configuration. Refresh snapshots after game exit so freshly saved settings are not overwritten. Resolve conflicting new default bindings by changing only the new bindings. Do not reset options or enable every upstream resource pack to accomplish synchronization.

## 4. Produce a reproducible adaptation manifest

For each item record its feature chain, B/U/L provenance and hashes, target source/download and hash, operation and reason, dependencies, retained local intent, conflict resolution, historical failure conditions, validation state, and rollback scope. Keep `candidate`, `blocked`, `static_checked`, and `runtime_passed` distinct.

Classify chains as lower-risk data adaptations, ongoing compatibility risks, or deferred because of missing providers or major rewrites. Risk class is not a pass result. Once dependencies close, test a batch together rather than asking the user to enter a world for each file. If dialogue/trainer bridges are missing, isolate the dependent DLCs too; removing the bridge cannot leave a claim that the DLC is usable.

Record custom patches' input hashes, source/diff, build command, output hash, associated failure, and retirement conditions. Mark undocumented old patches for investigation, not reproducible. Rebuild each new attempt from that chain's clean baseline instead of stacking patches on failed output.

## 5. Test and apply within authorization

Confirm normal game exit before creating an independent TEST copy. Verify the unchanged baseline, then dependency-complete feature chains, then the combined candidate. Use the real old world and corresponding player identity; a new offline account cannot prove the original party, PC, quests, and inventory survived.

Reuse and cite existing evidence when exact inputs, relevant configuration, and trigger conditions are unchanged. Retest affected scope when a chain or final combination changes; do not restart full-pack testing every time.

Use [batched acceptance and release](references/acceptance.en.md) for exhaustive static checks plus representative runtime tests. Do not default to testing thousands of skins individually; sample providers, interactions, and persistence mechanisms. Document a user's choice to skip world checks; menu success is not old-world success.

Within this batch's impact, check old Pokémon/forms/items, PC, battles, gym mode, quest rewards, currency, recipes, riding, old buildings/machines, resources, and shaders; save, exit, and reopen. This is not a full-pack exhaustive checklist every time. Stop the affected chain on unplanned region deletion, missing registrations, or reset data. Normal saving changes files: compare data semantics rather than demanding byte-identical worlds.

Apply to MAIN only within clear authorization, using the tested exact files and order. Back up replaced files; data migrations also need associated world/player/map backups. Recheck MAIN baseline hashes before applying and reassess drift. Never overwrite MAIN's world with TEST's world.

Patches for friends need target and original hashes, exact retired-file paths, and rollback instructions. Preflight different baselines; extraction over an existing instance can leave obsolete JARs active. Do not publish personal worlds, player/account data, launch tokens, or debug caches.

Report inspected, prepared, TEST-tested, MAIN-applied, and MAIN-verified scope separately. Applied content may be called installed for that batch. Distinguish TEST world success from MAIN menu-only success. Partial success cannot become all upstream content complete, every skin working, or full old-world stability. The skill cannot replace real execution, grant permission, or guarantee zero failures.
