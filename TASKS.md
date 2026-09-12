# Port execution

The complete CLI/headless Rust behavior is the target; this list is ordered
execution, not a substitute feature set. See PORTING.md and upstream.json.

- **GEOMETRY-NATIVE.** Check and execute squalr-tests/main.omg through its own
  nested build.omg and ordinary squalr-engine-api imports. Confirm the filter's
  nested region identity, saturation and overlap counts against the mapped Rust
  methods. Outer command: `python tools/verify.py native --omega <executable>`.
  With std pinned to `a91d878cb9252647d977c45787969b16e6ef937a`,
  Omega `e0d24c82fbca1bbae9f2b22cb661d5754e8c1707` on macOS ARM64
  (Python 3.13) completes dependency review and exits 200 on 18 local-receiver
  diagnostics in `Main::main`: calls such as `aligned.get_element_count(..)`
  reject a LET-bound receiver because native receiver resolution does not retain
  its storage. Omega's `validation/src/calls/expression_scanning/result_realization.rs`
  owns the current fence; its **STATE-LOCAL-VALUE-FRONTIER** task owns the
  value/storage/call join. Preserve the authored locals and repair the general
  compiler path. The unchanged native command must print `Squalr geometry: PASS`;
  native execution and Windows revalidation remain open. Current evidence is
  under `build/verification/`.
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
