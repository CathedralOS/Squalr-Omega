# TARGETS-AND-THROUGHPUT resume evidence (2026-09-20, linux_x86_64, swarm-w9)

This note lives here instead of the board item because
`samples/apps/squalr/TASKS.md` is fenced by a sibling claim
(SQUALR-CLONE-SERIALIZATION, ticket fa970472, expires 2026-09-20T22:50:37Z).
Fold this text into the board item when that claim clears.

## What landed in this commit

Provider surface authored and compiling — `omega update --project squalr-tests`
checks all 17 packages clean and published the lock;
`tools/verify.py native --timeout 600` prints `Squalr geometry: PASS` (exit 0).

- `squalr-engine-api`: `Bitness`, `TargetArchitecture`, `ProcessInfo`,
  `OpenedProcessInfo` (all `[copy]`), `PageRetrievalMode`.
- `squalr-engine-targets`: provider outcome unions (`OpenedProcessResult`,
  `ProcessQueryOutcome`, `ProcessListOutcome`, `MemoryReadResult`,
  `MemoryWriteResult`, `MemoryBoundsOpen`, `MemoryBoundsStep`) and the
  `ProcessQueryProvider` / `MemoryQueryProvider` / `MemoryReadProvider` /
  `MemoryWriteProvider` traits; boundary-touching ops carry
  `reaches FilesystemHost\ninvokes FilesystemHost;`.
- `squalr-engine-targets-native`: Linux implementations — `/proc/<pid>/exe` +
  `/proc/<pid>/maps` open through the boundary, maps-line cursor parsing into
  `NormalizedRegion`, `/proc/<pid>/mem` `read_at`/`write_at` exposing partial
  counts, `ProcessManager`.
- `squalr-engine-session`: `EngineOsProviders` forwarding the session-owned
  providers through the declared traits.

## The blocker (toolchain-owned, named on the Omega board)

Update (2026-09-21, leaf `omega-fused-host-providers`): `omega_reference` and
every `Source::Git` std pin now sit at Omega main `56adcc62ec`, past
`2704dd0edb` "mint toolchain-settled FilesystemHost provider plan". The
compiler mints the per-target `FilesystemHost` plan and splices it into
selected-plan provenance, so the earlier
`requires a selected Fused provider` / `no exact Fused selected-provider-plan
join` rejection is gone. The witness now fails one stage later, inside
`omega-language-std`'s own review projection:

- `packages/review/evidence/src/capture/providers/policy/replay.rs::validate`
  replays every retained selected-plan provenance row as an authored
  candidate through `selected_provider_plan_facts_with_independent_components`.
- The minted plan's realization symbols are deliberately `invalid` (the
  settlement table, not an authored machine, realizes each row), so
  `exact_provenance_realization` resolves each to 0 typed machines and emits
  11 diagnostics (`ProviderPlan ... retained realization symbol Handle{0,0}
  resolves to 0 exact typed machines`), exit 200.
- Omega TASKS.md pins the fix: carry the exact toolchain-settled identity
  through package review — validate the settled target/schema/rows, do not
  exempt ordinary `UniqueCoveringCandidate` plans. Diagnosis lives in
  `wiki/drafts/toolchain_settled_plan_provenance_replay.md`. The
  `is_toolchain_settled` discriminator already exists on
  `SelectedProviderPlanFacts` and is used elsewhere in review capture
  (`capture/package/providers.rs`); the rejection site just cannot reach it
  today.
- `TimeHost` remains unsettled at HEAD — no std target ships
  `time_impl.omg` — needed only for the throughput leg, not for the
  /proc-based read leg.

Until package review can replay the toolchain-settled plan (and `TimeHost`
gains a settled provider), no `ProgramEntry` can hold
`Service<FilesystemHost>`/`Service<TimeHost>` fields, so the executable
milestone stays unattemptable.

## Resume steps

1. Restore the probe fields on `Main` from `tools/native_probe_main.omg.parked`
   (control-file gate: probe chain when `/tmp/squalr-native-probe.control`
   opens, else the original geometry chain; covers open_target, enum maps,
   writable checks, magic "SQUALR42" read, partial read, guard-page read,
   cancel, throughput via `monotonic_ticks`, close, alive check).
2. `cc tools/native_probe_subject.c -o /tmp/subject` — the subject mmaps two
   anon pages (page0 magic+pattern, page1 PROT_NONE), calls
   `prctl(PR_SET_PTRACER, PR_SET_PTRACER_ANY)` (yama `ptrace_scope=1`), prints
   a READY line, parks on stdin.
3. `python3 tools/native_probe_driver.py` — compiles the subject, writes the
   control file, runs `omega run --keep`, asserts PASS, cleans up.
4. Then layer cancellations and throughput measurement; SIMD/parallel/spawn
   primitives remain absent — named blockers, not simulated (PORTING.md).

## Residual evidence (2026-09-21, linux_x86_64, path/live-snapshot-collect lane)

Checkout moved out of `samples/apps/squalr` into the standalone
`Squalr-Omega` clone, so the checked-in `squalr-tests/omega.lock` pins were
stale (`request external-local /home/ubuntu/repos/Omega/samples/apps/squalr/*`).
Per Omega AGENTS.md the old lock is preserved under the ignored
`build/verification/lock-migration/omega.lock.squalr-tests`; a fresh
`omega update --project squalr-tests` review re-pinned all 17 local packages
at unchanged content digests and re-accepted the same capability rows
(filesystem, console I/O, process termination). `build.omg` files were
republished identical; no `upstream.json` change (std still pinned at
`13433c1a27371cc56e406a62e00939ab5f051561`).

### What now lands on this lane

`get_processes` is ported end-to-end (read_dir over `/proc` numeric entries,
`/proc/<pid>/comm` names via `open_at` on the proc dirfd, upstream filter
order: required_process_id -> search_name+match_case contains -> take(limit);
`Listed(count, truncated)`, `Failed(Internal)` on IO error,
`Failed(NotImplemented)` for `require_windowed` — the unix-socket fd-link +
environ window-detect leg is unported GUI-picker surface, and `fetch_icons`
is inert because the icon payload type is absent). `start/stop_monitoring`
report Succeeded per upstream's no-op. The whole probe chain
(open_process -> maps enumeration -> mem read_at/write_at -> close ->
is_process_alive) is therefore fully ported at source level;
`verify.py check` is green for `squalr-engine-targets-native` and
`squalr-engine-session`.

### Two blockers now stand before the probe can run, in order

1. **Crash-route realization gap (new, earlier stage).**
   `tools/verify.py native --project squalr-tests` reaches native realization
   but rejects the geometry canary's callee:
   `InvalidUnitMachinePlan { machine: "...SnapshotRegionFilter::get_element_count",
   reason: "scalar callee has no checked executable body", omission:
   "no admitted body (local construction stopped at state graph: result
   signature)" }`. The machine declares `crashes Abort` and its violated arm
   is `crash Abort;` — the same crash-route gap Omega already holds the
   scalar-scan port behind (see the lane merge note "pending crash-route
   repair"). The callee lives in `squalr-engine-api`, fenced to the sibling
   lane; the fix is toolchain-side (admitted crash-path bodies for
   realization), not an app rewrite. Both the geometry chain and the probe
   chain share `main`, so neither can be exercised natively until this clears.

2. **Fused host providers (the named terminal blocker, reproduced).**
   A minimal ProgramEntry (`data Main { console: Service<Console>;
   host: Service<FilesystemHost>; }`, otherwise the geometry main) rejects at
   checked stage exactly as before:
   `selected ProgramEntry Service field 'Main::host' requires a selected
   Fused provider for boundary 'FilesystemHost'`. Same for the nested
   provider data the probe parks — `EngineOsProviders` ->
   `ProcessQuery` -> `LinuxProcessQuery.host` carries the same service, so
   unparking `tools/native_probe_main.omg.parked` hits the identical wall.
   Still toolchain-owned (`omega-rust/omega/build/provider-planning`,
   `native-realization/.../terminal_authority_policy/filesystem.rs`, plus a
   `TimeHost` provider that does not exist anywhere), fenced by the same
   Omega wave items.

### Resume steps (unchanged, with the new precondition)

0. Wait for the crash-route repair (blocker 1) — without it even the
   geometry canary cannot realize, and the sibling's
   `SnapshotRegionFilter` file is fenced to another lane.
1. Restore the probe fields on `Main` from `tools/native_probe_main.omg.parked`
   (control-file gate: probe chain when `/tmp/squalr-native-probe.control`
   opens, else the original geometry chain; covers open_target, enum maps,
   writable checks, magic "SQUALR42" read, partial read, guard-page read,
   cancel, throughput via `monotonic_ticks`, close, alive check).
2. `cc tools/native_probe_subject.c -o /tmp/subject` — the subject mmaps two
   anon pages (page0 magic+pattern, page1 PROT_NONE), calls
   `prctl(PR_SET_PTRACER, PR_SET_PTRACER_ANY)` (yama `ptrace_scope=1`), prints
   a READY line, parks on stdin.
3. `python3 tools/native_probe_driver.py` — compiles the subject, writes the
   control file, runs `omega run --keep`, asserts PASS, cleans up.
4. Then layer cancellations and throughput measurement; SIMD/parallel/spawn
   primitives remain absent — named blockers, not simulated (PORTING.md).
