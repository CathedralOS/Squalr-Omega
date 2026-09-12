# Port execution

The complete CLI/headless Rust behavior is the target; this list is ordered
execution, not a substitute feature set. See PORTING.md and upstream.json.

- **GEOMETRY-NATIVE.** Check and execute squalr-tests/main.omg through its own
  nested build.omg and ordinary squalr-engine-api imports. Confirm the filter's
  nested region identity, saturation and overlap counts against the mapped Rust
  methods. Outer command: `python tools/verify.py native --timeout 600 --omega <executable>`.
  With std pinned to `a91d878cb9252647d977c45787969b16e6ef937a`,
  Omega `26b7fe994beff8dd04e14bb223e6869c39a65e6e` on macOS ARM64
  (Python 3.13, `RUST_MIN_STACK=67108864`) completes package checking and
  acceptance. The native command exits 200 after 209.677 seconds at Terminal
  production: `InvalidUnitMachinePlan` for `Main::main`, with reason
  `attached Unit closure is missing a checked transitive machine plan`.
  Omega's `checked-trees-to-lowered-psi/src/attached_unit/bodies.rs` consumes
  the missing ordinary/composed checked body; trace its producer rather than
  removing closure validation. **STATE-LOCAL-VALUE-FRONTIER** owns the general
  operation/control join. Preserve the authored locals, geometry checks and
  package graph. The command must print `Squalr geometry: PASS`; native execution
  and Windows revalidation remain open. Current evidence is under
  `build/verification/`. The reviewed macOS lock retains checkout-specific local
  source identities; another checkout must complete ordinary update/review.
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
