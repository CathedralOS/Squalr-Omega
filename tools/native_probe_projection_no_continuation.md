# Native probe wall — owned projection at a result binding has no continuation

Witness: `python3 tools/native_probe_driver.py --omega <omega-4c77b01e452>`
in this checkout (pins `4c77b01e452f12c926043fd8f3aeed13ed66b98e`).

`omega run --keep squalr-tests/main.omg` declines at native terminal
production:

```
terminal-artifact production failed:
  Lowering(Unsupported("projected selection requires a structural continuation"))
```

Per-machine reproduction:

```
omega inspect-terminal --machine Main::main squalr-tests/main.omg
→ cannot lower terminal machine `Main::main`:
  Unsupported("projected selection requires a structural continuation")
```

## Emitting arm

`omega-rust/psi/pipeline/05_checked-trees-to-lowered-psi/src/unit/attached_unit/structural_values/emission.rs`
— `CheckedStructuralValueKind::Projection` arm (~line 856).

The arm's own contract comment: an owned projection "transfers one child on
the selected edge and disposes of the root's residual complement there. Only
the owned transfer requires a structural continuation." The failure path is
the result-binding call `emission.value(*value, None)` (~line 240): a `let`
binding initialized by an owned field move emits the projection with
`continuation = None`, so there is nowhere to dispose the source root's
residual complement.

## Witnessed source shape

`squalr-tests/main.omg`, twice:

```omega
state checked_start(
    engine_privileged_state: &mut EnginePrivilegedState,
    response: PointerScanStartResponse          // owned case payload, by value
) -> bool {
    let summary: StoredPointerScanSummary = response.pointer_scan_summary;
    ...
}
```

and identically in `checked_summary` (`PointerScanSummaryResponse`).

`squalr_tests/main.omg:2239` (`checked_start`) and `squalr_tests/main.omg:2272`
(`checked_summary`) both bind `let summary: StoredPointerScanSummary =
response.pointer_scan_summary` — an owned field projection out of the owned
`response` parameter, where `StoredPointerScanSummary` is a structural record
(itself containing `level_summaries: [PointerScanLevelSummary; 8]`). The
`response` root arrives by value from the
`PointerScanResponse::Start { response } -> checked_start(...)` dispatch arm.

## What the arm needs

The `CopiedStructuralPlace`-source path beside it already works (a projection
of a shared-borrowed copy replays the copy and appends the path — no
continuation needed). The missing coverage is the owned case: a structural
continuation (residual-disposal operation) must exist at result bindings so
that projecting `response.pointer_scan_summary` out can drop the `response`
complement on the selected edge.

Owning area per current claims: `structural_values/emission.rs` is claimed by
FILE-JOURNAL-CONSTRUCTOR-EMISSION (Codex / compiler recovery) at filing time.
