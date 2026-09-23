# Minimal repro: callee `crashes` route trips `SourceCustodyMismatch`

`omega run main.omg` at Omega pin `b5ac760ff4` fails at

    native artifact identity physical pipeline failed:
    common physical staging failed: Selection(Legalization(SourceCustodyMismatch))

Any `crashes <route>` declaration on a machine invoked below the entry
machine triggers it — here `Engine::open` (real `crash Trap;` arm) and
`Driver::run` (route cover). Route kind is irrelevant (`Abort` and `Trap`
fail identically); the entry machine's own `crashes` declaration is fine;
the same machines run clean with the callee declarations removed (but
check then reports the uncovered crash route, so the declarations are
mandatory). `verify.py native` printed `Squalr geometry: PASS` at the
2026-09-20 w9 pin with the same crash-route shapes, so this is a
regression in `validation/projection/custody.rs`'s ledger replay: crash
routes contribute provenance/fuel settlements that have no source
occurrence to replay against.

Every Squalr crashing callee (the authored debug-assert parity:
`SnapshotRegionFilter::get_element_count`, `scan_snapshot`, dispatch) is
unreachable natively until this clears — squalr-tests' `omega run` hits
the identical wall after passing check, unit planning and lowering.
