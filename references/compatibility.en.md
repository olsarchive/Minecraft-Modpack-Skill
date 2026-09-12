# Compatibility and historical-failure guide

## Version and identity

Matching version strings do not prove matching content. Use the official index hash or actual JAR hash as identity, while retaining filename and internal version fields. Some mods keep `1.0-SNAPSHOT` or `${file.jarVersion}` for years; inspect the manifest instead of ordering by that value.

Inspect NeoForge `META-INF/jarjar/metadata.json` and Fabric `jars` declarations for nested mods and libraries. Connector, KotlinForForge, and Create may not be fully identified from root metadata. The loader may select one nested copy of an ID; combine version ranges with the actual launch log before calling it a duplicate fault.

Public versions for the same MC/loader are candidates, not automatic upgrades. Respect the author's exact pin and local features that require an older API. Check precise dependencies, mixin targets, and feature entry points; moving quests without the item namespace they reference produces empty icons or impossible rewards.

Some compatibility modules enable only for an exact dependency hash. A native replacement with the same version may be intentionally skipped. Record what actually enters the execution path; do not fake hashes or remove guards. When an old migration changed IDs, verify the native registration stage, complete target set, duplicate handling, inventory/carrying items, and save/reopen before mapping old IDs. Retire scripts that depend on old Java classes only after the official build provides the equivalent repair.

## Three-way limits

`unknown_baseline_conflict` means the old source had no file at that path; it does not prove the local file is wrong. Renames and cross-loader replacements require mod-identity mapping. ZIP hashes can detect compression/timestamp-only changes but do not validate JSON or gameplay semantics. A deleted upstream path may have moved to another pack or JAR; find the new provider before removing the old one. Mixed-ancestor packs need separate baselines by content ownership.

## Failure evidence

Record target hash/version, MC/loader, dependencies, world/data snapshot, triggering action, first causal error, repair or withdrawal, and validation level. Typical lessons:

- Do not downgrade Create merely to satisfy a reference pack; solve the whole installed dependency intersection.
- Changing incompatibility metadata does not fix an API or descriptor mismatch.
- Same field names with `BooleanValue` versus `Supplier` require JVM descriptor checks, not another config patch.
- A menu can pass while old-world loading deletes regions or dungeons; stop and preserve the source world.
- Updated libraries may require data-format and registry changes; deleting balancing content hides the fault.
- Restoring an old JAR can revive a repaired issue and invalidates old runtime evidence.
- Test with the correct player UUID; an empty inventory can be an identity error.
- Preserve options, pack order, and linked migration files such as ship index plus entity/sublevel data.

## Datapack entry points and convergence

Inspect global-pack required/optional paths, resource directories also used as data, dedicated override paths, and the world's enabled list. Use the loader's actual pack IDs and report missing-pack errors from the current launch. If a pack appears in resource, global-data, and world directories, compare content and effective priority instead of copying more versions. Validate coins/economy through machine tags, shop/bank configuration, recipes, and quest behavior—not text alone.

Change one proven dependency chain at a time and restore that chain's clean baseline after failure. Prefer a narrow buildable patch or an official native equivalent. Do not disable filters, swallow errors, reset options, or repeatedly retry unchanged conditions. Review coverage/local preservation, dependencies/entry points/failure paths, then remove stale steps and verify rollback and artifacts.
