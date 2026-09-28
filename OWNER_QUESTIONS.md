# Owner questions

Genuine language decisions surfaced by the port — not silent app semantics.

## Binding-member-triggered case-payload custody wall

When a `Binding<T>` (any boundary capability) is reachable through the
`ProgramEntry` `self` data type's transitive field closure, **no
case-payload binding transfers** — verified on omega-71254d80532 and
omega-8a94858 with verbatim Squalr shapes and minimal reproducers
(`tools/binding-param-transfer-repro`, `tools/binding-trait-call-dodge`):

- payload → successor argument: `state graph: terminator: conditional
  successors: parameter transfer` (borrowed `&binding` or bare view) and
  `edge cleanup: no state plan` (owned)
- payload → call argument inside an arm's `(...)` tail:
  `return arm value` / `result ownership`
- `let x = <union-typed parameter>`: `statement sequence: local data:
  structural call binding` (only call results may bind union locals)
- scalar payload-field reads → successor argument: `scalar arguments`
  when the scrutinee is a local (param scrutinees admit)

The one exemption: machines on the **entry `self` data type itself**
admit payload → successor arguments even under the trigger (probe:
`Main::run_flow`'s `Got { payload } -> got(payload)` compiles while an
identical `Eng::dispatch`, with or without its own `Binding` member,
declines). This scoping looks like signature-seed/receiver
reconciliation keyed to the entry unit rather than a principled type
rule — worth deciding whether the asymmetry is intended.

The same trigger family drives the earlier `call operation: structural
arguments: parameter path` wall on `&mut self.<field>` arguments.

**App-side resolution adopted here:** capability members moved off data
types entirely; boundaries are reached through trait-level calls
(`Console::write_line`, `block Console::read_line(&mut buf)`) with
`invokes`/`reaches`/`blocks` ceilings — the recipe recorded in
`tools/binding-trait-call-dodge/README.md`. With no `Binding` member in
the entry closure the trigger cannot fire and `dispatch_parsed_list` /
`dispatch_list` / `extract` compile unchanged.
