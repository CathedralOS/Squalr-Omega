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
