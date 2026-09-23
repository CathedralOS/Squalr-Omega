# Native-execution admission findings (2026-09-23, pin b5ac760ff4, z2 witness leg)

`omega run` of `squalr-tests/main.omg` now reaches native lowering — the
crash-route gap below is repaired at this pin — then dies inside the
optimizer. Three bounds were measured this leg:

1. **Lowering rejects unreachable `state` declarations** —
   `Lowering(Unsupported("Unit graph has unreachable states"))`. Every
   named state in an entry-closure unit needs an incoming transition
   edge, including ones only authored as unreachable crash arms; prune
   dead states rather than parking them.
2. **Structural types are capped at ~64KiB.**
   `structural_layout.rs` stores record `byte_size` in `u16`
   (`u16::try_from` -> `StructuralTypeTooLarge`); nested fields sum.
   Measured on `omega-b5ac76`: `[u64; 8192]` (64KiB) lowers,
   `[u64; 8193]` fails. Consequence: `Snapshot.regions`,
   `SnapshotRegionBuilder.regions`, `SuppliedMemorySource.regions` are
   now bounded at 1/1/4 elements (deviation comments in place); the
   `EnginePrivilegedState` closure sits at ~55KiB.
3. **THE CURRENT BLOCKER — `SourceCustodyMismatch` (regression).**
   `Selection(Legalization(SourceCustodyMismatch))` fires when ANY
   machine below the entry declares `crashes` — minimal repro committed
   at `tools/callee-crash-custody-repro/` (one call, one `crash Trap;`
   arm). Route kind irrelevant (`Abort`/`Trap` identical); entry-machine
   `crashes` unaffected; removing the callee declarations runs clean but
   check then reports the uncovered route, so they are mandatory. The
   crash-route fix (93489c3a05) admitted crash-path bodies into the plan;
   `validation/projection/custody.rs`'s ledger replay then has no source
   occurrence to settle them against. w9's pin printed
   `Squalr geometry: PASS` with the same shapes, so this regressed
   between w9 and b5ac760ff4. Every authored debug-assert parity arm
   (`get_element_count`, `scan_snapshot`, dispatch) sits behind it.

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

Update (2026-09-22, squalr toolchain pin advance): `omega_reference` and every
`Source::Git` std pin now sit at Omega main `2a8edec522`, which contains
`d756f86e21` "replay toolchain-settled provider plans by their minted
identity". Package review's provenance replay now validates the minted
`FilesystemHost` plan's settled identity (target/schema/rows, invalid
realization symbols, `UniqueCoveringCandidate` shape) instead of revalidating
it as an authored candidate, so the 11-diagnostic
`resolves to 0 exact typed machines` exit-200 rejection inside
`omega-language-std`'s own review is cleared. `tools/verify.py check` passes
`squalr-tests` end-to-end at this pin. `TimeHost` remains unsettled at HEAD —
no std target ships `time_impl.omg` — needed only for the throughput leg, not
for the /proc-based read leg.

Until `TimeHost` gains a settled provider, no `ProgramEntry` can hold a
`Service<TimeHost>` field; `Service<FilesystemHost>` fields are now
admissible at this pin, so the executable milestone's filesystem leg is
unblocked.

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

1. ~~**Crash-route realization gap (new, earlier stage).**~~ **CLEARED**
   (2026-09-23, swarm): crash states are admitted through composed control
   (`93489c3a05`), `&self` reads joined the scalar graph (`d28d773700`) and
   multi-state mixed graphs carry structural formals (`906f03f41b`), so
   `SnapshotRegionFilter::get_element_count` lowers and verifies at
   `a951e7882a`. What remains of this step is *verification*: the
   `squalr-tests` lock in this checkout still pins the old toolchain and the
   re-review currently stops at blocker 2's regression, so the probe has not
   yet been re-run natively. Original evidence:
   `tools/verify.py native --project squalr-tests` reached native realization
   but rejected the geometry canary's callee:
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
   Omega wave items. Update (2026-09-23, swarm): between `b5ac760ff4` and
   `a951e7882a` this package stopped *checking* at all —
   `data LinuxMemoryQueryer { host: Service<FilesystemHost> }` now reports
   "field `host` references unknown generic type `Service`" and every
   `host.open/open_at/close/seek/read` call "does not resolve" (57
   diagnostics across targets-native); `omega update`/lock re-review cannot
   pass it, which parks the `pin/a951e7882a` lane and the probe retry alike.
   Under investigation as a toolchain regression alongside the check-mode
   post-Stage-05 cost jump on FsHost-bound packages (same surface, same
   window).

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
