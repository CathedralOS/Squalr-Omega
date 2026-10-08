# LEAF native-probe-child-reads — wall #3: int-family float-boundary `satisfies` decls unresolvable upstream

Branch `leaf/native-probe-child-reads` (repro package `squalr-engine-api`).
Omega built fresh from main `fef76bc46fc` (includes z4's `d756f86e21`
toolchain-settled provider identity replay — the earlier fs-binding deadlock
and the linux_x86_64 float regression are both cleared).

## Status

`omega update --project squalr-tests --target linux_x86_64` reaches
`squalr_engine_api` package checking. After the repo-wide `self`-receiver →
named-`this` migration (~380 files rewritten on this leaf), the ONLY remaining
api diagnostics are upstream library failures:

```
error: machine satisfaction target `I8::from_f32` does not resolve to an
exact trait requirement or top-level `boundary requirement`
  (× I8/I16/I32/I64/U8/U16/U32/U64 :: from_f32/from_f64 — 16+ diagnostics)
```

All 16 diagnostics are in bundled-library `float_impl` files pulled by
`use omega::language::core::float_operations;`. Zero are squalr-side.

## Why float_operations is required

`float_mod_f32`/`float_mod_f64` in
`squalr-engine-api/src/structures/scanning/comparisons/scan_compare_type.omg`
implement float `%` via the only legal truncation path:
`I64::from_f32(quotient)` / `F32::from_i64(truncated)`.
`as`-casts in both directions are rejected (unprovable denotation), and
float_operations is the sole provider of the named boundary conversions.
No `floor`/`rem`/`mod` boundary operator exists in the surface.

Minimal repro (any file): `use omega::language::core::float_operations;`
+ one `I64::from_f32(x)` call → 240 diagnostics on a scratch program, all
in int-family impl satisfies decls. F*/Float-family decls resolve; the
int families do not (no int-family machine decls exist for those targets
upstream).

## Tried and excluded

- `as` casts (Exact) — rejected as unprovable, that is the diagnostic pair
  this form replaced.
- (q as i64 in Saturating) double-cast workaround — itself produces 12
  errors (mixed Saturating/Exact domains, unprovable denotations).
- Repeated-subtraction fmod — semantics-destroying for large quotients,
  not a real port of `%`.
- Equatable-asymmetry note: `NormalizedRegionEquality satisfies Equatable`
  resolves under engine-api (root) but is reported unknown when api is
  re-checked as a dependency under engine-session — same suspected
  upstream asymmetry family, documented not worked around.

## Next

Requires an upstream fix to the int-family `satisfies` decls in
`source/library` float_impl (or whatever registers their boundary
requirement names). Until then every squalr package transitively needing
`float_mod_*` fails `omega update` package checking.

## Root cause narrowed (omega @ a869ec6980d, fresh binary)

The wall is not "decls missing" — it is overload disambiguation in
`satisfies` resolution. Every float→int boundary operator name in
source/library/core/float_operations.omg is declared THREE times —
plain, `in Trapping`, and `in Saturating` — and the machine-side
`satisfies I8::from_f32` cannot carry a context qualifier
(`satisfies ... in Trapping` is a parse error: `in` is not accepted
after the requirement path). Resolution requires an exact requirement
name; the three-way same-name overload fails for every int family.
Scratch repro: six `linux_x86_64 machine ... satisfies I{8,16,32,64}/
U{8,64}::from_f32` decls — all six fail identically. Unambiguous names
(F32::from_f64, F32::from_i8, Float::*) resolve fine under the same
compiler. The gap is checker-side: satisfies resolution needs
context-aware matching (impl machine `in Trapping` → the `in Trapping`
decl) or the decls need distinct names.
