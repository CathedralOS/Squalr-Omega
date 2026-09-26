# Minimal repro: `&`/`&mut` call arguments are unlowerable

`omega run main.omg` at Omega pins `3a29bac97f7` and `f6c7c4e4fd` fails
identically:

    selected ProgramEntry establishment rejoins 0 Terminal attachment
    identities; expected one; the machine's unit plan was omitted at an
    unavailable callee (`Fixture::run`), which was itself omitted at local
    construction at `call operation: structural arguments:
    caller structural result`

`Fixture::run` is an ordinary `&mut self` command callee on a record field
of `Main` — the shape `self.driver.run()` uses everywhere in squalr-tests.
Its body calls `Small::read(&arr)` — a `&[u64; 2]` argument on a local.
The call is rejected in local construction, so the callee's unit plan is
omitted, so the entry machine cannot rejoin a Terminal attachment.

## Variant matrix (one line changed each time)

| Shape | Result |
| --- | --- |
| `Small::make(&arr) -> Small` — &local arg, structural result | same omission, identically in scalar callees, entry-state prefixes, and command callees |
| `Small::read(&self.arr) -> u64` — &field arg, structural ref param | admitted by local construction, then `UnsupportedControlFlow` at `02_abstract-operations-to-target-operations/.../borrowed_calls.rs:296` — that gate requires a *primitive*-reference parameter |
| `Small::read_scalar(&self.z) -> u64` — &field arg, `&u64` param | callee omitted at `signature` — a `&u64` formal does not plan at all |

## Consequence for the port

Only `&mut self` receivers on field places and scalar by-value arguments
are admitted. `&`-parameters are rejected in every context reachable from
the entry machine — scalar callees, entry-state prefixes, and command
callees all fail identically — regardless of result type.
Machines shaped like `ElementScanner::scan_snapshot(&mut s, &mut p,
&mut c)` or `DataTypeRef::new(&id)` — the pervasive upstream porting idiom
— can never be invoked by a natively compiled program until the borrowed
call paths handle non-primitive references.

## Baseline

`squalr-tests` on `main` does not exhibit the gap at `--check`: its entry
cone calls only `&mut self` receivers with scalar arguments
(`self.driver.init()`, `drive_commands`, `self.driver.run()` …). The
first `&`-arg call sites were the scan-leg states on
`leaf/supplied-bytes-witness` invoking `FixtureKit::verify_*` — every such
body contains `&`-param calls (`DataTypeRef::new(&u8_id)`,
`set_snapshot_regions(&regions, 1)`, `push(&plan)`, `scan_snapshot(&mut …,
&mut …, &mut …)`).

Two further walls measured while bisecting:

- **Check-level poison (diagnostic gap).** Calling an omitted callee from
  anywhere in the entry cone fails `--check` at an unrelated earlier
  state: `Main::main::gate` (state 1, the first store-containing state)
  omits at `scalar field store sequence: write frame agreement` — the
  recorded `NormalizedWriteFrame` disagrees with
  `resolver.inferred_state_write_frame` once an unavailable callee sits in
  the successor set. Replacing only the call expressions with
  `let ok: bool = true` through the identical state graph restores green
  (189 files). The state machine itself is fine; the diagnostic does not
  name the callee chain.
- **Baseline run wall (pre-existing).** `omega run` on unmodified `main`
  (c08f02f) at `f6c7c4e4fd` still fails — later, in terminal-artifact
  production: `Lowering(Unsupported("Unit graph continuation lost its
  producing statement"))`. Main's probe path calls
  `raw_fs.read(fd, &mut self.control, 64)` — a field-place `&mut` argument
  that clears local construction — so baseline reaches a deeper stage
  before dying. No Squalr package produces native output today; the
  supplied-bytes witness is blocked at this wall as well as the
  structural-argument one.

## Consequence for the port (updated)

The witness cannot exist until both walls close: borrowed arguments must
plan (this repro) and terminal-artifact production must survive the
baseline cone (the `Unit graph continuation` gap — repro is simply
`omega run` on `main` itself, filed by observation rather than minimized
here).
