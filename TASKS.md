# Port execution

The complete CLI/headless Rust behavior is the target; this list is ordered
execution, not a substitute feature set. See PORTING.md and upstream.json.

- **GEOMETRY-NATIVE.** Check and execute squalr-tests/main.omg through its own
  nested build.omg and ordinary squalr-engine-api imports. Confirm the filter's
  nested region identity, saturation and overlap counts against the mapped Rust
  methods. Outer command: `python tools/verify.py native --omega <executable>`.
  At Omega `24ab0f1c87378054b6dfe9daa84f9b7b4a85c247` on Windows:
  `check --project squalr-engine-api` loads the modules but reports four
  exact-declaring-type case-membership diagnostics and one unproved alignment
  local range. Triage these against the declared case/return contracts before
  assigning a compiler fix. Application `audit` and `check` stop in pinned std
  on unsynthesized `Optional` equality. `native` currently resolves the std alias
  as a local path, without the selected package binding. Preserve these separate
  failures; no dependency copying or fake approval is a fix. Evidence is under
  `build/verification/`; macOS and native execution remain unverified.
  Seed parity gaps still include Rust debug-only assertions, clone/serialization,
  alignment string parsing, region alignment/expansion and named trait operators.
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
  process, partial-read handling, cancellations, SIMD and parallel execution.
  Reuse scalar fixtures to check optimized results; measure total allocation
  and throughput including result publication. GUI/TUI/installer are excluded.
