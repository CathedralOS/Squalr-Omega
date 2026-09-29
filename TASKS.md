# Port execution

The complete CLI/headless Rust behavior is the target; this list is ordered
execution, not a substitute feature set. See PORTING.md and upstream.json.

- **GEOMETRY-PARITY.** Validate the geometry application on Windows through its
  nested build.omg and ordinary squalr-engine-api imports, then finish the mapped
  Rust behavior still absent from the seed. Outer command:
  `python tools/verify.py native --timeout 600 --omega <executable>`.
  Omega and std `87d8b22713ff5e46e535a4b1c62a8b6710d0d1ab` pass all 12 authored
  geometry checks on macOS ARM64 using the release compiler, Python 3.13 and
  `RUST_MIN_STACK=67108864`: native exit 0, `Squalr geometry: PASS`.
  The receiver uses intrinsic `Service<Console>` establishment. Preserve the
  authored locals, algorithms and package graph. Current evidence is under
  `build/verification/`; another checkout needs ordinary update/review of its
  local source identities. Windows was not run. Remaining parity gaps include
  Rust debug-only assertions, region alignment/expansion, the set_alignment
  call-site gate (a `&mut self` machine taking a data parameter loses the
  entry attachment identity; the ported machine is source-checked but not
  yet exercised) and named trait operators.
- **SUPPLIED-BYTES-SCAN.** Port the actual scalar scan, snapshot storage,
  comparison dispatch, RLE encoder and query path in squalr-engine-api and
  squalr-engine-scanning. Preserve growable and partitioned output, candidate
  stride versus covered bytes and successive filtering. Use captured bytes
  before live I/O; no Rust FFI scan shortcut or fixed-capacity substitute.
  Acceptance: ordinary native headless input produces exact addresses/ranges
  matching Rust and independent cases, including overlap/tails/empty input.
- **CLI-COMMANDS.** Port the existing request/response model through
  squalr-engine-session, squalr-engine and squalr-cli. The CLI main entry is
  intentionally absent until this work starts; do not substitute a success stub.
  Port only dependencies needed for the selected behavior, preserving the
  declared package graph. Acceptance: native command sequence creates a scan,
  filters it again and pages exact results through the production engine.
- **TARGETS-AND-THROUGHPUT.** Then port native reads using a controlled child
  process, partial-read handling, SIMD and parallel execution. (ScanControl
  cancellation/progress surface is ported — `leaf/scan-cancellation-progress`.)
  Reuse scalar fixtures to check optimized results; measure total allocation
  and throughput including result publication. GUI/TUI/installer are excluded.
  Live-snapshot chain status: attach/enumerate/region/memory-io providers are
  ported and check-green; `get_processes` reproduces the sysinfo sweep minus
  the unported window-detect leg (`require_windowed` -> NotImplemented).
  Session privileged-state (`engine_privileged_state.omg`), region merge
  (`SnapshotRegionBuilder::add_memory_region`), snapshot collect
  (`snapshot_value_collector.omg`, `Snapshot::collect_region_values`) and the
  headless probe entry (`ElementScannerDriver::run_supplied_fixture`) are
  ported — the `path/scalar-scan-headless` snapshot-structures deferral and
  the `SnapshotRegionFilter::get_element_count` crash-route gap are resolved.
  What still gates the native probe is toolchain-settled fused
  `FilesystemHost`/`TimeHost` machinery: the canonical leaf tables mint rows
  only for linux_x86_64 scalar-positional syscalls, so `open`/`read`/
  `canonicalize` (path/slice carriers) and non-linux targets resolve to zero
  provider rows at terminal-authority review — residual evidence and resume
  steps live in `tools/native_probe_resume.md`.
- **TRACKABLE-TASKS-EXECUTOR.** (new-scope) The trackable_tasks command surface
  (list/cancel request/response pairs and the genuinely-empty responses) is
  ported. The manager + dispatcher + executor half is blocked on two unresolved
  port choices: (a) storing `TrackableTask<'a>` inside `EnginePrivilegedState`
  forces an `'a` on the state — a ~304-site respell across session/engine/tests;
  the alternative is storing an owned handle form instead of a borrowing task.
  (b) no `WaitWake` boundary-trait implementation exists in the omega library or
  the port, so nothing can mint `TrackableTask::create`'s substrate — decide
  whether the substrate comes from a per-target provider implementation or from
  an app-owned polling model. Land the PrivilegedCommand/Response arms,
  dispatcher arm and executors together once both are decided; unreachable arms
  or fake-success bodies are not acceptable substitutes.
