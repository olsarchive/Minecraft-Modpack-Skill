# FTB flow updates and DLC provider checks

Use when new chapters were imported but older chapters may still retain superseded upstream logic, or local quest renumbering, currency substitutions, and existing progress must survive.

## Audit logical items, not just chapter files

For each changed task record old/new upstream IDs, local ID, mapping evidence, conditions and types, prerequisites, rewards, icons/text, actual providers, decision rationale, and validation level. Without a common baseline, mark ancestry unknown; file dates are not ancestry evidence.

Stabilize identity before updating logic. Preserve IDs bound to existing local progress by default. Establish semantic correspondence from chapter position, objectives, preceding/following tasks, and condition content together, not translated titles or matching chapter names alone. Once mapped, translate new upstream prerequisites to local IDs and check the global graph.

Count upstream matches, old values, intentional local differences, and missing-provider/design blockers separately. A reduced difference count is not acceptance: every decision must be traceable. Inspect dependencies associated with all changed chapters, not only new ones.

## Separate condition deletion from reward deletion

- When upstream removes manual or obsolete item conditions, confirm the current mechanism and task meaning before synchronizing the deletion. Do not retain them forever under progress protection, or clear conditions just to reduce differences.
- New automatic checks require a proven exact provider. Numeric `count: 1` differs from string `count: "1"`; parseable SNBT does not establish the FTB field contract.
- Completed, unclaimed, and claimed rewards are distinct states. Design treatment of old progress and unclaimed rewards first. If evidence is insufficient, defer the reward change independently; do not reset the task or run reward commands to manufacture success.
- Preserve/map local aliases, currency, Mega Stones, and icons after checking actual registrations and economic meaning. Do not replace local functionality merely for textual upstream equality.

## Absence from JARs does not prove a missing provider

Search actual configured sources: active JARs, declared nested archives, global required/optional datapacks, resource directories also used as data directories, world datapacks, and effective KubeJS scripts. Record static presence separately from enablement. Directory names and singular/plural conventions depend on the actual Minecraft/loader version.

For challenge or champion quests, follow exact IDs from task condition to advancement/trigger, trainer, mob, and loot/reward, including the trigger-registering mod and dialogue/battle bridge. DLC ZIPs can supply trainers and advancements; scanning only `mods/*.jar` misses them. Conversely, complete JSON chains do not prove bridge events fire: battle/dialogue runtime checks remain necessary.

If the precise item or trigger provider is genuinely absent, block the item and withdraw mistakenly installed conditions. Do not substitute similar names, empty advancements, or forced rewards to fill the record.

## Post-merge acceptance

1. Check SNBT round trips, field types, duplicate IDs, and local identity mapping.
2. Check the global prerequisite graph for dangling references and cycles; retained local chapters must remain reachable. Zero dangling references does not prove correct progression.
3. Match conditions, commands, icons, and rewards against actual providers. Quest background resources must load; a ZIP's existence is insufficient.
4. In TEST with the original player identity, sample key old/new flows, completion triggers, rewards, and save/reopen. Test changes to unclaimed rewards only in a copy and record generated state.

If only static application is authorized, report that evidence-backed static flow changes were applied while completion/rewards remain unverified. Without testing authorization, do not enter the world.
