# Minimal repro: `field = call() != 0` store is unadmitted in unit planning

`omega update --project . --target linux_x86_64` at Omega pin `5b2558926f`
fails candidate checking for the repro package with

    selected ProgramEntry establishment rejoins 0 Terminal attachment
    identities; expected one; the machine's unit plan was omitted at local
    construction at `structural field store: pure source`
    (state 1, statement 0)

The unadmitted statement is `self.closed = self.raw_fs.close(self.fd) != 0` —
a boolean comparison whose left operand is a scalar call result, stored into
a `bool` structural field. The unit-plan store vocabulary in
`typed-trees-to-checked-trees/execution/terminal_unit/structural_scalar_store`
admits a call result only when the stored value IS the call (`ScalarResult`),
a registered scalar computation root, or a pure bound expression; a
comparison wrapping the call result is none of the three, so the statement
falls through every lane and the machine's plan is omitted.

Restructuring to an admitted shape clears it: bind the call result to a
field first, then store the comparison of that field
(`self.fd = self.raw_fs.close(self.fd); self.closed = self.fd != 0;`
reaches package review cleanly — squalr-tests carries that form; this
file carries the single-statement shape and reproduces directly).

Sibling of the `runtime_string_literal_dispatch_exit` pin
(`literal_dispatch_unit_plan_stops.rs`, `structural field store: record
literal field`): another local-construction vocabulary hole in the same
unit-plan admission pass. Ordinary programs hit it on any
`field = call() !=/==/</> k` field store — e.g. squalr-tests'
`self.cancelled = self.raw_fs.close(fd) != 0`.
