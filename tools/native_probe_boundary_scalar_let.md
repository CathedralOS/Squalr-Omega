# Compiler gap: `(BoundaryScalarCall, LocalData)` unhandled in composed-control body walk

Status: BLOCKS `leaf/native-probe-child-reads` — `omega run` native emission
dies with `Lowering(Unsupported("Unit graph reordered a source effect"))` on any
`&mut self` composed-control state that binds a scalar result from a
boundary-call operation.

Toolchain: `omega` @ `e0a884138f` (swarm-binaries pin, sha256
37526101eae8e3de…; includes c4dd2fadcf Float fix + every landed fix through
current main). Diagnosed with an instrumented build from the same revision
(diagnostic eprintln only, not part of this lane).

## Symptom

```
native compile FAILED:
  Lowering(Unsupported("Unit graph reordered a source effect"))
```

`omega --check` is clean; the failure is on the lowering side only.

## Minimal repro

A machine that reaches + invokes a boundary (FilesystemHost here), crashes
Abort/Trap, and in one composed-control state does:

```
let opened: i32 = self.host.open("/proc", 65536);
transition opened >= 0 { true -> ok() false -> bad() }
```

Full repro: `tools/native_probe_bsc/` (build.omg pins
omega_language_std @ e0a884138f, linux_x86_64 entry). Confirmed end-to-end:
`omega update --project tools/native_probe_bsc` publishes the package, then
`omega run --keep tools/native_probe_bsc/main.omg` fails at native emission
with the identical diagnostic — the planned op is BoundaryScalarCall with
`result{statement_index:0, binding_ordinal:0, primitive_type:I32}`,
`scalar_arguments:[65536]`, `structural_arguments:["/proc"]` paired against
`LocalData("opened")`.

The checked side legitimately plans the call as
`CheckedUnitEffectOperationPlan::BoundaryScalarCall` with
`result{statement_index:0, binding_ordinal:0, primitive_type:I32}`
(paired to `LocalData` on the statement side) — see the checker test
`retains_scalar_result_from_boundary_call` in
`omega-rust/psi/pipeline/typed-trees-to-checked-trees/.../calls/boundary_calls.rs`,
which proves this shape is a supported checked plan.

## Precise location

`omega-rust/psi/pipeline/checked-trees-to-lowered-psi/src/unit/attached_unit/composed_control/state_graph/body.rs`,
`fn validate(...) -> Result<usize, LoweringError>` (~lines 160–600).

The walk zips `state.operations` against `statements` by ordinal (starting at
`prefix = state.bindings.len()`, skipping `__destructure#` / `__arm_destructure#`
marker statements). Every planned op variant has an explicit statement-kind
pairing arm EXCEPT `BoundaryScalarCall`: the variant is produced by
`call_operation()`, recognized by `authored_statement()`, tracked for
binding ordinals, and consumed in `boundary_scalar_return/` + `validation.rs`
— but no arm pairs `(BoundaryScalarCall, LocalData)` in the main walk.
The fallthrough arm is `unsupported("Unit graph reordered a source effect")`.

Instrumented pinpoint on the real program:

```
REORDER-DIAG machine=Main::main state=StateHandle(2733) op_index=0 ordinal=0
operation=BoundaryScalarCall{
  coordinate{statement_index:0, call_ordinal:0},
  result{statement_index:0, binding_ordinal:0, primitive_type:I32},
  scalar_arguments:[Pure(IntegerLiteral"0")],
  structural_arguments:[ByteSequenceLiteral"/tmp/squalr-native-probe.control"]}
statement=LocalData(_control_fd_r)
```

Source line: `let _control_fd_r: i32 = self.raw_fs.open("/tmp/squalr-native-probe.control", 0);`

## Expected vs actual

Expected: the walk pairs the `BoundaryScalarCall` op with its `LocalData`
statement (the let-binding holds the scalar result for the subsequent
`transition` guard read) and lowers the statement like any other scalar-binding
op. Actual: unhandled pairing → `unsupported`.

## Note — same shape elsewhere

`LinuxMemoryQueryer::open_virtual_pages` contains the identical shape
(`let _proc_fd_r: i32 = self.host.open("/proc", 65536);`) and apparently did not
reach this arm before the Main::main failure aborted emission — whether its
call plans differently (ScalarCall vs BoundaryScalarCall) or is simply emitted
later is unresolved; the repro above is sufficient for the regression.
