# Native probe filing — `Unit case body roster drifted` (case-marker slice ignores continuations)

Swarm leg: `leaf/native-probe-run-witness` (zergling z6). Omega binary
@499211f463 (swarm-binaries; carries 469eb29 authored-statement BoundaryScalarCall arm
+ coordinator's mut-param-forwarding fix).

## Evidence

`omega run --keep --target linux_x86_64 squalr-tests/main.omg` (fresh review
minted for all 17 packages under the new pin) reaches terminal production and
now fails:

```
terminal-artifact production failed:
Lowering(Unsupported("Unit case body roster drifted"))
```

The earlier `Unit graph continuation lost its producing statement` orphan at
`NativeProbeMain::probe_control` op_index=2 is CURED by the merged arm — the
run now proceeds past it into a different machine.

## Pinpoint (same-rev instrumented build, omega-release @499211f463 + eprintln
in `validate_markers`)

```
CASE-ROSTER-DIAG machine=Handle{526} state_name=enum_open
    start=8 end=5 statements_len=7 bindings=0 operations=8
  stmt[0..3] = Assignment x4
  stmt[4]    = LocalData `bounds`
  stmt[5..6] = Transition (When, Always)
```

## Root cause (Omega terms)

`checked-trees-to-lowered-psi` …/composed_control/state_graph/cases.rs:213:

```rust
let start = state.bindings.len() + state.operations.len();
let markers = statements.get(start..end)
    .ok_or(LoweringError::Unsupported("Unit case body roster drifted"))?;
```

`start` counts every operation as consuming one authored statement, but
`body.rs`'s own `statement_continuations` walk already recognizes that some
operations (StructuralScalarFieldStore, WriteOnlyPrimitiveStore,
StructuralByteSequenceFieldByteStore(ScalarResult), ByteSequenceWrite,
MoveStructuralField, StoreStructuralField, CallContinuationCleanup) CONTINUE
the statement an earlier operation began. `validate` itself accounts for this
in its roster check (`operations + markers + record_markers == end - prefix +
tail_value + continued`, body.rs:78-79); `validate_markers` does not — it never
subtracts the continuation count.

Here 8 operations cover 5 pre-transition statements (3 are continuations), so
`start=8 > end=5` and the marker slice is invalid. Any closed-sum state whose
operation plan includes continuations trips this; the probe's `enum_open`
state stores a boundary scalar call result plus sibling assignments before a
closed-sum transition on `bounds`.

Fix shape (for whoever owns it): compute `start` as
`bindings + (operations - continuations)` using the same
`statement_continuations` flags `validate` already computes — or hoist the
continuation walk ahead of `validate_markers` and share it. Same
missing-accounting class as the authored_statement gap — different table.

## Repro

1. swarm-binaries omega @499211f463 (or source build of that rev).
2. `/home/ubuntu/omega-merge` symlinked to a checkout at the same rev
   (bundled std path the binary embeds).
3. Squalr manifests pinned to omega_language_std @499211f463 (old f6c7c4e4 pin
   fails std's own typed-store check — 6 unrespelled sites).
4. `omega update --project squalr-tests --target linux_x86_64`, accept the
   review, `--resume` to mint omega.lock.
5. `omega run --keep --target linux_x86_64 squalr-tests/main.omg` → diagnostic
   above at terminal production.

Subject child `/tmp/native_probe_subject` + `/tmp/squalr-native-probe.control`
(`pid page guard`) staged per tools/native_probe_driver.py.
