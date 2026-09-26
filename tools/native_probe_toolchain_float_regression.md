# Toolchain regression: `Type::Float` qualification in synthesized unit (linux_x86_64)

Status: BLOCKS `leaf/native-probe-child-reads` — `omega update` / `omega --check` /
`omega run` cannot compile any package transitively reaching
`omega::language::core::targets::linux_x86_64::float_impl` at the required pin.

Toolchain: `cargo build --release -p omega` @ `5d5e5f371c34020193e92f55ce93995d8f84cd6a`
(= `122222e07e` crash-custody + `ad39f401ed` ambient-self + `d057f48b54` vec merges;
the ledger commit adds no code, so this is the newest real toolchain).

## Symptom

```
checked compilation failed for package `omega_language_std` with 272 diagnostic(s)
  error: case value `Float` requires its carrier-qualified `Type::Float` path
    source-unit 25, bytes 10749..11929
    (×272, single byte range repeated)
```

`Type::` in the message is a literal render — the flagged case name is `Float`
on an unspecified carrier, in a source unit that no checked-in file owns.

## Repro (toolchain alone, no Squalr code)

```
omega --check samples/cli/basics/cli_mvp/main.omg     # same 272 diagnostics
omega update --project squalr-tests --target linux_x86_64   # same
```

Every package route into `omega_language_std` fails identically.

## Bisection (performed on the fetched std package tree)

- `use calling;` / `console;` / `filesystem;` / `format_lineage;` /
  `process_exit;` / `time;` / `wire;` — all compile clean.
- `use math;`, `use units;`, `use macos_gui;` — fail with the same unit/byte
  range. All three transitively `use omega::language::core::float_operations`.
- `use omega::language::core::targets::linux_x86_64::float_impl;` alone —
  reproduces (`source-unit 2`, bytes ~2666..11929, 124+ diagnostics).
- `use omega::language::core::targets::{windows_x86_64,linux_arm64,macos_arm64}::float_impl;`
  — all clean. The regression is exclusive to the `linux_x86_64` impl.

## Diagnosis (Omega terms)

- `psi` commit `7b9dce26d7` ("case values require carrier-qualified names")
  makes an unqualified case value an error when the reference carries
  `authored_expression_exposure`.
- Exhaustive grep of the entire authored corpus (`source/` in this repo and the
  fetched `omega_language_std` tree) finds ZERO unqualified `Float` tokens —
  `Float` appears only as `Float::<machine>` paths, `case Float;` declarations
  (`std/calling.omg` `ValueClass`/`AbiValueClass`), and `Token::Float`.
- The failing source unit is therefore toolchain-synthesized text: a
  linux_x86_64-specific projection minted for the `FloatNativeProvider`
  `satisfies Float::*` / `via ForeignBinding::CompilerIntrinsic` leaf set
  (linux syscall/ABI projection), which emits the `Float` case of its
  value-class carrier unqualified. The other three targets' float intrinsic
  projections do not contain the offending sequence.
- Diagnostic attribution caveat is by design: `source-unit N` anonymizes the
  unit (diagnostic_output.rs) so the synthesized unit cannot be path-traced
  from the diagnostic alone.

Residual: no Squalr-side shim exists — the text is generated inside the
compiler; fixing it means qualifying `Float` in the linux_x86_64 float
intrinsic projection (or exempting synthesized units from the new rule).
The leg's witness (`tools/native_probe_driver.py` → `omega run --keep`) and
`omega update` both require the package-check path and are dead at this pin.
