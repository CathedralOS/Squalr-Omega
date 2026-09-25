# call-select-case-arg-repro

Toolchain gap: `transition f(...)` over a call subject that takes a **case
construction argument** fails exhaustiveness with phantom uncovered cells.

```
omega update --project tools/call-select-case-arg-repro --target linux_x86_64
=> transition pattern matrix in `App::main::s` does not cover
   (`ProbeResult::Y`, `ProbeResult::X`); add an arm or `_`
```

The dispatch covers both variants of a two-case result, yet the matrix
reports a two-cell tuple — one cell per axis — because each arm's parser copy
of the subject `self.probe(Mode::A)` is a distinct `Call` node and
`expressions_structurally_equal`
(`psi/pipeline/symbol-resolved-trees-to-typed-trees/src/expressions/exhaustiveness.rs`)
compares call arguments node-for-node; `Mode::A` lowers to a case-construction
expression kind the matcher does not handle (`_ => false`). The copies then
form two matrix axes instead of one, and neither arm's covered tag can close
the other's axis.

Observed in `squalr-tests/main.omg` at `enum_open`
(`open_page_bounds(..., PageRetrievalMode::FromUserMode)`); the `_ ->` arm the
checker suggests closes the dispatch without changing which arm wins, so the
application keeps the suggested fallback and this gap stays filed here.

Equivalents that DO compare equal and keep one axis: receivers (`self`,
`self.field`), borrows (`&x`, `&mut x`), member/indexed paths, unary/binary
compositions, casts, scalar literals, and name paths — a call subject made of
only those compiles a full case coverage with no `_`.

## Escaping the matrix entirely — `let` + ClosedSum

Binding the call result into an immutable local first sidesteps the
per-arm copies: `let r: T = f(...)` followed by `transition r { ... }`
makes every arm hold the same local handle, which compares trivially
equal (one axis). The `r` subject then routes to the ClosedSum
terminator, which additionally admits destructuring payloads
`Case { field } -> next(field)`.

ClosedSum admission (`state_graph/closed_sum.rs`): subject must be a
bare local (no segments — `self.field` and `param.sub` are rejected) of
**Affine** multiplicity. Consequences:

- `[copy]` enum results can never use this route — they are not Affine
  and also cannot field-store. The enum must be authored non-`[copy]`.
- `let x: T = <call>` needs an explicit `: T` annotation.
- Field stores of a non-copy result ARE admitted
  (`self.open_result = call()` works), but you cannot `transition` over
  the field — store the record, then `let`-bind the later affine
  results and `transition` over those locals.

## Adjacent admission facts (verified on this rig + squalr-tests)

- Statement-position calls on an ordinary data field
  (`self.worker.m(...)`) admit scalar arguments — bare `self.field`
  places AND `let` locals — but REJECT `&`/`&mut` borrow arguments
  (`take_ref(&self.rec)` → "statement sequence: call: call operation"),
  and `let i: &T = &self.field` is itself rejected ("local data:
  structural call binding") — there is no way to stage a borrow local.
- `&`/`&mut` argument admission tracks the RESULT class, not the
  receiver: calls returning affine/record results (the ClosedSum /
  structural-call lane) admit `&self.a.b` projections plus scalars;
  calls returning scalars (`-> bool`, `-> u64`) admit only scalar
  arguments — a `&x` arg on a scalar-result call fails even on
  satisfies-dispatched provider machines
  (`is_address_writable(&info, addr) -> bool` → "call operation" at
  the call). Two-state workaround: give the callee an affine enum
  result (`AddressWritable { Writable; NotWritable }`) and select
  with `let` + ClosedSum.
- `Binding<Service>` host calls (`self.raw_fs.*`, `self.console.*`)
  are a third lane: `&mut` buffers, scalars and literals all pass
  with scalar results.
- Guard/subject position only admits scalar bools
  (`CheckedScalarExpression::Boolean`): `==`/`!=`/`<`/`&&`/`!` over
  scalars, places and params — including a bool-returning boundary
  call in subject position. Case-membership `x in T::C` and enum `==`
  are NOT scalar → "conditional successors: guard expression" /
  "guarded pair without exact false fallback" omissions.
- Self-machine calls (`self.probe(...)`) are rejected even in
  statement position of the arm chain context — "call operation"
  omission at guard-expression phase.
- `self.field = T::C` (enum-literal field store) → "structural field
  store: case field type" — same missing class as record param→field
  store; work around via `let` local.
- A `transition read {` whose every case routes to the same target
  still must enumerate all cases on an affine subject — `_ ->` was
  authored where custody might not be consumed; ClosedSum full
  coverage to a common target is the admitted form.

## Round-3 bisect (state-45 close_target wall)

- ClosedSum (`let` affine local + `transition` full coverage) requires
  EVERY case payload to be scalar. One enum-typed payload case in the
  enum — even unbound in the arms, even matched by a bare path arm —
  makes the whole transition unadmitted: `transition { Succeeded -> ..
    Failed -> .. }` over `Failed(error: SomeEnum)` → "state graph:
  terminator: unsupported tail: transition chain". Scalar payloads
  (`count: u64`) bind and pass. This is a distinct gap from the
  ClosedSum/multiplicity lane: payload shape, not subject shape.
- Escape route: `let ok: bool = x.succeeded();` — an `&self` method
  call on a `let`-BOUND enum local IS admitted (scalar result, no `&`
  args), and inside the callee `self in T::C` over a payload-carrying
  case path is a valid bare match (payload ignored). `bool` pair then
  routes `transition ok { true -> .. false -> .. }` — the canonical
  record+bool-pair trick, applied to a local instead of a field.
- `let h: u64 = self.a.b.get();` — a 2-segment receiver scalar call in
  `let` position is admitted (same shape as the subject-position call
  that already passed at have_open).
- `self.outer = Outer { info: Rec { h: 7 } }` — a NESTED record literal
  in a field store is rejected ("structural field store: case field
  type") where `self.rec = Rec { h: 7 }` flat-literal store passes.
  Stage nested fields with separate stores (`self.outer.info = Rec{..}`).
