# Minimal repro: `&`/`&mut` call arguments are unlowerable

Rechecked at Omega `bb092d497db` (coordinator's borrowed-arg fix:
`exact_mutable_referent` no longer arity-bails on self-receiver calls;
forwarded `&mut` params rejoin through non-self formals) and re-verified
at `499211f463` — the per-shape results below are identical at both pins.
Original filing at pins `3a29bac97f7`/`f6c7c4e4fd` is superseded below.

At `bb092d497db`+ the *forwarded-`&mut`* shape is closed end-to-end: a
field-place `&mut` argument (`self.driver.drive(&mut self.buf)`) plus a
machine forwarding its own `b: &mut Buf` parameter
(`self.sink.store(b)`) compiles AND executes — `omega run` exits 0 with
correct native output at both pins. The remaining omission arms are
narrower:

## Variant matrix (one line changed each time)

| Shape | `bb092d497db` and `499211f463` result (identical) |
| --- | --- |
| `&mut self.buf` arg + forwarded `&mut` param | **PASS** — check + native run, exit 0 |
| `Small::read(&arr) -> u64` — `&local` arg, `&[u64;2]` param | still omitted at `call operation: structural arguments: caller structural result` — in `&mut self` command callees, scalar callees, and entry prefixes identically |
| `Small::read(&self.arr) -> u64` — `&field` arg, `&[u64;2]` param | admitted by local construction, then `UnsupportedControlFlow` at `02_abstract-operations-to-target-operations/.../borrowed_calls.rs:296` — that gate requires a *primitive*-reference parameter |
| `Small::read_scalar(&self.z) -> u64` — `&field` arg, `&u64` param | callee omitted at `signature` — a `&u64` formal does not plan at all |

## Mechanism for the `&local` arm (reduced at bb092)

`let arr: [u64; 2]` registers a caller structural-result binding rooted
at `Symbol(arr)` (statement_sequence/local_data.rs:153/191 pushes
`(result, PlaceRoot::Symbol)`). The `&arr` actual therefore enters the
`caller structural result` arm of
`04_typed-trees-to-checked-trees/.../calls/structural_arguments.rs:246`;
the supply-mode gates at :250-278 pass for a CheckedBody scalar callee
(`scalar_callees` is `Some` in the statement-call context,
statement_call.rs:302), so the arm forwards to
`calls/result_arguments/mod.rs::argument`.

Inside `argument` the borrowed local has no lane:

- the shared-view lanes (`mod.rs:224-268` and `:274-313`) require
  `result.type_identity == target_identity` / an `Expression` root —
  `arr`'s `[u64;2]` identity never equals the `&[u64;2]` formal's
  reference-shell identity, and a named local roots at `Symbol`, not
  `Expression`;
- the rejecting guard is `mod.rs:320-330`: for an unrestricted result
  binding the gate demands non-projected `Owned` access to a
  closed-primitive-array or plain-numeric parameter —
  `access != CheckedStructuralAccess::Owned` fires for the
  `SharedBorrow` formal and returns `None`, so the call plan is dropped
  and the caller is omitted under the `caller structural result` arm
  label.

In short: whole-place `&`/`&mut` borrows of owned structural-result
locals are admitted through none of the arm's sub-lanes — the lane only
covers owned moves and whole `&[T]`/`&'a V` view locals whose binding IS
the view.

## Consequence for the port

`&mut self` receivers on field places, forwarded `&mut` params, and
scalar by-value arguments are admitted (bb092 verified natively).
Shared `&` borrows of named locals/fields and any `&primitive` formal
remain rejected in every context reachable from the entry machine.
Machines shaped like `DataTypeRef::new(&id)` or
`set_snapshot_regions(&regions, 1)` — the pervasive upstream porting
idiom — still cannot be invoked by a natively compiled program.

## Baseline

`squalr-tests` on `main` does not exhibit the gap at `--check`: its
entry cone calls only `&mut self` receivers with scalar arguments
(`self.driver.init()`, `drive_commands`, `self.driver.run()` …).

Two further walls measured while bisecting:

- **Check-level poison (diagnostic gap).** Calling an omitted callee
  from anywhere in the entry cone fails `--check` at an unrelated
  earlier state: `Main::main::gate` (state 1, the first store-containing
  state) omits at `scalar field store sequence: write frame agreement` —
  the recorded `NormalizedWriteFrame` disagrees with
  `resolver.inferred_state_write_frame` once an unavailable callee sits
  in the successor set. Replacing only the call expressions with
  `let ok: bool = true` through the identical state graph restores
  green (189 files). The state machine itself is fine; the diagnostic
  does not name the callee chain.
- **Baseline run wall — call-result dispatch tails (reduced at
  bb092).** `omega run` on `squalr-cli` now reaches `Cli::run` state 1
  (`read`) and dies at `state graph: terminator: guarded jump
  successors: roster` — the `transition block self.console.read_line(&mut
  ...) { case arms }` tail. The wall is not union- or
  `block`-specific: a ~30-line repro (`transition self.sub.call() {
  arms }`) fails identically, and so does a scalar `transition
  self.sub.flag() { true/false/_ }`. Mechanism: each arm's `When` guard
  is a case-membership test over the call *result*, and
  `terminal_scalar/guarded_exits.rs::tail` (:80-88) requires exactly one
  `CheckedScalarExpression` row with `role == Guard` per arm statement —
  call-result case tests produce no such row (the transition subject is
  an un-`let` call expression, so nothing registers a scalar-expression
  or computation row rooted in the caller at that ordinal —
  `state_graph/mod.rs:620-641 retained_guard` requires
  `root.machine == machine`), `tail` returns `None`, no `guarded_tails`
  row registers, and `terminator.rs:301`'s `let [retained] = []` drops
  the machine. The 2-arm pair fails the same root cause at
  `terminator.rs:150` (`retained_guard` → `conditional successors: guard
  expression`). **Workaround verified:** `let r =
  call(); transition r { arms }` binds the result first — passes check
  AND runs natively (exit 0) for scalar subjects. This replaces the
  f6c7c4-era `Unit graph continuation lost its producing statement`
  wall (`body.rs:897 statement_continuations`) as cli's first run-stage
  blocker — bb092's borrowed-arg fix lets the cone reach terminator
  planning.
- **Union-subject dispatch matrix (reduced at 499211f463).**
  `transition <union subject>` has three distinct outcomes depending on
  the subject kind and arm count:
  - `transition <bound local> { When; Always }` (2-arm with fallback):
    passes check, lowers, AND runs natively — a bare
    `let bounds: Bounds = call(); transition bounds { Case::Opened ->
    .. _ -> .. }` exits 0. The ClosedSum terminator forms through the
    `StructuralResult` subject lane (`cases.rs::result_source`
    :102-156).
  - The same 2-arm shape with a prefix statement that emits
    *continuation* operations (e.g. `self.point = Point::new(1, 2)` —
    an embedded structural call feeding a store — or a call with a
    `&field` argument) drifts: `validate_markers` opens its marker
    window at `start = bindings + operations`
    (`state_graph/cases.rs:210-213`), but `operations` counts
    multi-op statements while `end` is an authored statement position —
    `start(8) > end(5)` in `squalr-tests Main::main::enum_open` (8 ops
    over 5 statements), so `statements.get(start..end)` is `None` and
    the machine dies at `LoweringError::Unsupported("Unit case body
    roster drifted")` during terminal-artifact production. The
    continuation-aware reconciliation exists one call later —
    `body.rs:46 statement_continuations` — but `validate_markers` runs
    first with the raw count. The f6c7c4 `Unit graph continuation` wall
    lives behind this one for `enum_open`; whether it still fires after
    the drift is corrected is unmeasured.
  - ≥3-arm `When`-guarded union dispatch on a bound local (e.g.
    `Case::A { n } -> ..; Case::B -> ..; _ -> ..`) fails earlier at the
    scalar roster (`guarded jump successors: roster`), same as
    call-result subjects — union case tests likewise produce no
    Guard-role scalar rows.
  - `transition self { Case { field } -> .. }` on an `&self` receiver
    (the api `is_list`-style idiom) passes `--check` but dies at native
    lowering: `02_abstract-operations-to-target-operations
    /lowering/control_flow/structural_case.rs:87` — `case_source`
    resolves a `PlaceId` through `live.structural_homes` or
    `prepared.parameters`, and a `self` place is registered in neither
    (`parameter_root` also filters `WriteOnlyBorrow` only, so the miss
    is structural: `self` is not a parameters entry at all); even if it
    were found, the access gate two lines later requires `Owned`
    non-self custody.
- **Self-loops are intended rejection.** A state's `false -> read()`
  self-edge produces `InvalidTerminalModule(ControlCycle(BlockId))` —
  unranked cycles need termination evidence; not a bug.
