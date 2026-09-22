# Farming sync and batched repair: consult by symptom

These are version-specific observations, not permanent blacklists.

## Quest crashes: parseable does not mean renderable

Touhou Little Maid 1.5.3 / MC 1.21.1 expects short value `spawn_box` in the entity_placeholder component `touhou_little_maid:recipe_id`. Its reader prefixes `touhou_little_maid:altar_recipe/`; passing `touhou_little_maid:altar/spawn_box` creates an illegal second colon and crashes FTB icon rendering. Trace the reader from the stack, compare an installed JAR recipe output, and fix only this component while preserving task/reward identity and progress.

**Do not globally shorten similarly named fields**: Patchouli's own `recipe_id` may require a full resource ID. Batch-check the same component across quests, scripts, active datapacks, and mod resources. State whether binary saved items were excluded. Title screens and maid work GUIs do not exercise FTB special icons; sample the actual chapter.

## Client compatibility and performance

- Epic Fight 21.14.1 called `glfwGetKey(-1)` on an unbound tooltip-key path. Guard that precise branch without changing old keys. Investigate OrderToCook's motorcycle GLFW path separately; the same error text does not establish one mod as the cause.
- EMF 3.3.2 / SelfExpression 2.22a repeatedly wrapped a particular dynamic model. A wrapping guard does not fix all provider-side rebuilding or prove an FPS gain.
- Record a render crash and 90% system memory separately. Without concurrent process-memory evidence, do not diagnose a leak, blindly enlarge the heap, or reproduce until the desktop freezes.
- Fix location, direction, completed loading, graphics, and shaders before profiling. Mod counts, ordinary warnings, and low GPU usage are not independent diagnoses. Do not promise ten additional FPS without a comparison.

## Original gameplay and reachable entry points

- Maid work-GUI samples require the owner, empty hand, no sneaking, and an awake maid. Item interception is not permanent GUI failure.
- Forced order commands locate part of a chain, not natural opening/payment. Seeing fishing UI does not prove reward delivery. Combine representative checks instead of endless individual restarts.
- Document real searchable labels for unbound features. SDM Shop 3.3.1 displayed `key.sdmshop.shopr` / `key.category.sdmshopr`; search `sdm`. Combat Roll's localized unbound label is not an hour or malfunction.
- Preserve the author's separate currency, prices, and natural earning path; do not exchange the old wallet automatically. Existing statistics may trigger new advancement weapon rewards: these are not necessarily starter gifts.
- Wineries require structure templates, processors, and machine/block providers. Removing fermentation equipment preserves appearance, not original gameplay. Natural generation also needs new-region verification.
- Crossing game version and loader (e.g. 26.1 Fabric / Java 25 to 1.21.1 NeoForge) is not simple bridging. Check native releases and actual APIs; public source does not mean cheap porting, and metadata edits are not ports.

## Delivery and cleanup

- Local fixes do not update sent mrpacks. Friend patches need exact fields, supported versions/hashes, exit/backup steps, and field-only instructions for customized chapters. State whether the old full export was updated; reimporting it still requires the patch.
- If the user retains old and new versions, neither is a disposable TEST. Old directory names do not prove absence of early farming additions; verify before deleting rollback materials.
- After acceptance, remove verified TEST copies without unique progress; retain only copies needed for concrete pending manual checks. Resolve exact authorized paths and distinguish archives, active instances, and unique rollback evidence. Avoid indefinite full-world backup accumulation.
- Never migrate cheat-test progress into real saves. Friend exports exclude accounts, private worlds, and diagnostic caches while retaining promised settings. Public skills contain sanitized mechanisms, not private logs.
