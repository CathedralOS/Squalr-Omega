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

The executable milestone cannot compile into any `ProgramEntry`:

- A `Service<FilesystemHost>` or `Service<TimeHost>` field — direct or nested
  inside provider data — rejects with
  `requires a selected Fused provider for boundary <name>` /
  `rejoins 0 Terminal attachment identities; expected one`.
- Std ships fused providers only for `Console` and `ProcessExit`
  (`provider_defaults` `select_provider` closures in
  `source/library/std/targets/<t>/{console,process_exit}_impl.omg`).
- A package-authored `boundary machine ... satisfies FilesystemHost::op` is
  refused as an unknown boundary slot; a `via Binding::Syscall` leaf is refused
  on slice/`in Path` carriers by `external_shapes`; a full 50-op
  `via Binding::CompilerIntrinsic` closure satisfies selection but entry still
  fails: `routed service field has no exact Fused selected-provider-plan join`
  — dispatch wants `CheckedAdapter` rows (checked-body satisfies machines on
  the provider data), which `via` rows never produce.
- Omega TASKS.md already pins this gap (`filesystem_cohort_witness.rs`):
  a demanded canonical `FilesystemHost` leaf resolves to zero selected
  provider rows because provider plans derive only from `satisfies`
  conformances and none exists for the canonical host. `TimeHost` is in the
  same boat — no provider exists anywhere.

Until provider planning mints toolchain-settled `FilesystemHost`/`TimeHost`
fused providers, no ProgramEntry can hold them, so the /proc-based read leg is
unattemptable. Fixing it needs `omega-rust/omega/build/provider-planning` and
`native-realization/.../terminal_authority_policy/filesystem.rs`, fenced by
wave items (UEFI-OS-HANDOFF / TWO-AXIS-TERMINAL-AUTHORITY-REVIEW at time of
writing).

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
