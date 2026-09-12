# Batched acceptance, authorization, and release

## Group by risk and mechanism

| Category | Examples | Approach |
|---|---|---|
| Lower-risk data adaptation | Quest fields with exact providers, additive drops, resource-reference fixes | Complete static checks, then batch with representative behavior checks |
| Ongoing compatibility risk | Dialogue/battle bridges, registration/component forks, model-loading entry points | Isolate complete dependency chains; verify root cause and local regressions |
| Deferred | No native/low-cost alternative, missing provider, major rewrite required | State what is missing and what enables resumption; do not invent placeholder functionality to claim completion |

Resolve independent static issues together, freeze the candidate manifest, then arrange one check covering several mechanisms rather than world entry per file. With desktop authorization, perform the feasible checks; without it, prepare a short consolidated user checklist. Continue under later permission that supersedes a restriction, without repeated confirmation.

## Evidence consists of independent fields

For every feature/batch record exact input/output hashes, TEST/MAIN path roles, build, static checks, registration/menu, world loading, interaction, save/reopen, application status, and residual issues. Bind each log to actual gameDir, player identity, time, and that candidate's hash.

| Evidence | Permitted report |
|---|---|
| Generated and static checks pass | Candidate prepared; real launch unverified |
| Menu/postInit passes | Menu and registration pass; world/rewards/battles unverified |
| TEST interaction and save/reopen pass | Specified TEST features sampled successfully; list uncovered scope |
| Exact MAIN manifest applied, menu passes | Batch installed; MAIN menu passes, without claiming MAIN world validation |

Users may explicitly accept applying after skipping a check. Record the choice, remaining risks, and actual evidence without inventing passes or repeatedly requesting existing authorization. A confirmed old-world corruption failure must be resolved or isolated, not downgraded to ordinary unverified status.

## Minimum complete world check

Use an old-world copy and original player identity. For affected features check acquisition, use/trigger, visual/quest/battle effect, original-feature regression, save/exit, and reopen. Reward deletion, economics, and data migration also require relevant old-state cases. For thousands of skins, sample acquisition, cosmetics, toggles, shiny, Mega, and other mechanisms rather than every appearance. Estimate and confirm separate scope for probability measurement or exhaustive coverage.

Snapshot original keybinds, enabled resource packs and order, options, and shaders. Iris may rewrite timestamp comments: distinguish byte hashes from effective configuration. Keybind-only comparison can miss disabled-pack markers or new default-binding conflicts. Investigate missing textures through references, versions, and actual selection; do not reset all resource packs.

## Apply and roll back

Confirm the relevant game exited normally; do not kill unrelated Java applications. The frozen manifest includes additions, replacements, exact retirements, expected old/new hashes, supporting chains, and extra obsolete scripts, not merely copy counts. Read-only previews confer no new authorization; authority comes from the user request and context.

Check MAIN's current baseline before applying; reassess drift. Back up replacements/retirements and record prior absence for additions. For migrations, back up linked world/player/map/entity data based on evidence, not directory-name guesses. A live, changing world copy is not a consistent baseline. Verify hashes and preserved settings afterward. Partial failures need operation logs and explicit rollback scope.

Never copy TEST saves, cheat items, or test completion state into MAIN. File rollback differs from save rollback after new registered IDs have been persisted. Before removing a mod that has created items, take a fresh backup and assess loss risk.

Persist concise current status, manifests, reproduction steps, and an evidence index outside chat. Mark which newer state supersedes an old report while retaining its evidence. An old MAIN-unchanged statement must not obscure later application.

Publish only generic instructions, synthetic cases, and tools you may distribute. Exclude personal worlds/UUIDs, host absolute paths, launch tokens, author JARs, restricted resources, and real runtime logs. Repository publishing and game operations have separate authorization scopes.
