# Filed Omega gap: unit-graph continuation orphaned when a boundary scalar call feeds a structural field store

`omega run --keep --target linux_x86_64 squalr-tests/main.omg`
(binary = omega @f6c7c4e4fdd6332273975d378ff30ccc7c4597f7, built from source at the
pinned rev; swarm-binaries release asset 404s from this box)

```
native compile FAILED:
  error: cannot realize accepted package production: terminal-artifact production failed:
    Lowering(Unsupported("Unit graph continuation lost its producing statement"))
```

## Owning stage

`omega-rust/psi/pipeline/05_checked-trees-to-lowered-psi` —
`src/unit/attached_unit/composed_control/state_graph/body.rs`,
`authored_statement` / `statement_continuations` (line ~753/~837 @f6c7c4e4fdd).

## Localization (instrumented same-rev build)

```
CONTINUATION-DIAG machine=<NativeProbeMain> state_name=probe_control op_index=2
  continued=Some(1) current=None op=Discriminant(17)
```

op discriminant 17 = `CheckedUnitEffectOperationPlan::StructuralScalarFieldStore`
(the ScalarResult flavor — `continued_statement` arm), continuing authored
statement 1. Ops 0–1 of the state are `EstablishReference` (the
`&mut self.control` borrow argument — synthetic, authored=None) and the
`BoundaryScalarCall` itself — which carries `authored_statement = None` because
`authored_statement` never covers it. The walk therefore never "began"
statement 1, so its continuation store dies as an orphan.

## Root cause (Omega terms)

`authored_statement` lists the call arms
`StructuralCall | BoundaryStructuralCall | ScalarCall | CallUnit | BoundaryCall`
— every call shape **except `BoundaryScalarCall`**. The variant carries
`coordinate: CheckedUnitCallCoordinate` like its siblings, so the arm is a
plain omission:

```rust
CheckedUnitEffectOperationPlan::StructuralCall { coordinate, .. }
| CheckedUnitEffectOperationPlan::BoundaryStructuralCall { coordinate, .. }
| CheckedUnitEffectOperationPlan::ScalarCall { coordinate, .. }
| CheckedUnitEffectOperationPlan::CallUnit { coordinate, .. }
| CheckedUnitEffectOperationPlan::BoundaryCall { coordinate, .. } => {
    Some(coordinate.statement_index)
}
// BoundaryScalarCall { coordinate, .. } absent → falls to `_ => continued_statement(op)` → None
```

`BoundaryStructuralCall` is covered; `BoundaryScalarCall` is not — same
missing-arm shape as the `BoundaryScalarCall ↔ LocalData` gap fixed upstream at
c698e924ae8, but at the *authored-statement* table (a scalar-producing boundary
call that stores its result into a field at the same authored statement rather
than binding a `let` local).

## Triggering source (Squalr)

`squalr-tests/main.omg`, `probe_control` state, statement 1:

```omega
self.control_len = self.raw_fs.read(controlfd, &mut self.control, 64);
```

`self.raw_fs` is the fused `FilesystemHost` service → `read` plans a
`BoundaryScalarCall` whose scalar result feeds `StructuralScalarFieldStore`
(`self.control_len = result`), both at authored statement 1.

Plan sequence: EstablishReference(&mut control, authored=None) →
BoundaryScalarCall (authored=None — the bug) → StructuralScalarFieldStore
(continued=Some(1), orphaned).

## Fixes that would cover it

Adding `BoundaryScalarCall { coordinate, .. }` to the existing call arm makes
the producer begin statement 1 and the continuation pair correctly — the
canonical minimal fix, matching how `BoundaryCall`/`BoundaryStructuralCall`
already enter the table.

No shim used; Squalr source is unchanged and correct as authored.
