# Minimal repro: record-typed field stores are unadmitted in unit planning

`omega update --project . --target linux_x86_64` at Omega pin `5b2558926f`
fails candidate checking for the repro package with

    selected ProgramEntry establishment rejoins 0 Terminal attachment
    identities; expected one; the machine's unit plan was omitted at local
    construction at `structural field store: case field type`
    (state 1, statement 0)

The unadmitted statement is `self.opened = info;` — a whole record value
(`Info`, declared `[copy]`) arriving as a state parameter, stored into a
record-typed structural field. In
`typed-trees-to-checked-trees/execution/terminal_unit/structural_scalar_store/mod.rs`
the only non-scalar field-store lane is guarded by `unrestricted_sum`,
which requires the field's type to be a `DataShapeKind::Enum` whose
variants all have no payload fields. Records — and enums carrying
payloads — fall through to `return None`, and the lane comment says so
deliberately: "member-read values, call results, payload sums, records
and affine carriers keep declining." The omission label `case field
type` names the lane that declined, not the actual field type (a
record), which makes the diagnostic misleading on top of the gap.

Confirmed non-routes (each reproduces a distinct omission):

- `self.opened = Providers::identity(info)` — a machine returning the
  same record — fails at `state graph: result custody accounting`
  instead: a `[copy]` structural call result must be consumed by a
  transfer or disposal row, and the field store supplies neither.
- Declaring `Info` non-`[copy]` makes the *source* side fail first:
  `Opened { info } -> have(info)` rejects with `cannot transfer a
  non-copy value out of borrowed storage` — the payload can't be moved
  out of the stored `self.result` enum field.
- A record literal `-> have(Info { ... })` as a jump-successor
  parameter is unadmitted (`state graph: terminator: jump successor:
  parameter transfer`); the affine-enum + case-payload route in this
  repro is the only way the record arrives as a state parameter at all.

Admitted equivalents (all used by squalr-tests after restructuring):

- scalar field stores (`scalar field type` lane)
- whole-param stores into payloadless-enum fields (`unrestricted_sum`)
- records threaded as state parameters through every consuming and
  forwarding state — transitions pass the whole place (`-> s(info)`);
  `[copy]` records copy freely out of a stored enum's case payload
- affine record call results into fields
  (`self.proc_info = ProcessInfo::new_named(...)`) — the StructuralCall
  result's custody is consumed by the field write

Whole-record state parameters are also excluded from the admitted
call-argument surface — verified on this repro's `have` state:

- `self.providers.use_ref(&info)` (`&` whole-param borrow) and
  `self.providers.use_val(info)` (by-value record arg) both fail
  `statement sequence: call: call operation` on a provider receiver.
- `Providers::use_val(info)` — an associated (static) machine — is
  admitted, reaching package review.

So a parameter-threaded record still cannot reach provider calls that
take `&Record`. The working route (used by squalr-tests) is the affine
record-result field store: `self.result = provider.open(...)` where the
result record keeps the record inside (`result.info`) and call sites
project `&self.result.info` — field-projection borrows are the
admitted argument shape.

Consequence for ordinary programs: a record that must remain reachable
in later machine states cannot live in a field today; it must be
carried as a state parameter through every intermediate state and
every loop, or kept inside an outcome record field and projected at
call sites.
