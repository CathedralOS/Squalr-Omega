# Decline census — Sep 24 refresh (omega @9317f0ec96, Squalr-Omega @cc44b661)

Method: `tools/verify.py check --omega <swarm-binary>` per package, then
`omega inspect-terminal --machine <fq> <pkg>/build.omg` per declared machine for
the packages that pass check. Packages gated at package-check record one probe
per package; all their machines carry the same DEPCHECK/hang verdict.
This is a map leg — nothing here was fixed.

## Coverage

| package | machines | check | per-machine verdicts |
|---|---|---|---|
| squalr-engine-api | 695 | PASS (exit 0, ~70s) | swept: 296 VERIFIES + 400 declines + 17 enum artifacts |
| squalr-engine-targets | 18 | PASS (exit 0, ~194s) | swept together with api (shared build closure) |
| squalr-engine-scanning | 88 | HANG | `--check` exceeds 900s twice (400s + 900s/600s pure-CPU, zero output on idle box); every machine gated |
| squalr-engine-targets-native | 162 | FAIL | `failed to resolve …/source/library/core/service.omg` |
| squalr-engine-session | 53 | FAIL | same wall (via dependency on targets-native) |
| squalr-tests | 9 | FAIL | package identity `squalr-tests` invalid (snake_case migration unapplied) + stale hyphenated omega.lock |
| squalr-cli (not assigned, observed) | — | FAIL | same stale-lock wall; also carries 2 stale `core::service` imports |

Net: 296 of 696 reachable api+targets machines (42.5%) lower to verified terminal
today. 400 real declines across ~45 distinct diagnostic strings. 312 machines in
scanning/targets-native/session/tests never reach machine level — they sit
behind four package-level walls.

Sweep enumeration note: 17 `MachineNotFound` rows are enumeration artifacts —
trait-block `machine name(&self, …)` signatures captured as machines, not
concrete callable units. They are excluded from the decline counts.

## Package-level walls (gate whole packages before any machine)

| family | machines | example | bottom-out | claim status | suggested next worker |
|---|---|---|---|---|---|
| stale `use omega::language::core::service;` | 215 (native 162 + session 53) + squalr-cli | `LinuxMemoryQueryer::open_virtual_pages` | package resolution — `core/service.omg` was deleted upstream when `Service<R>` became an intrinsic closed identity (carrier now in `core::binding`); all 13 imports across native/session/tests/cli are unused leftovers | unclaimed — Squalr-side | any z-worker: delete ~13 unused import lines; no Omega change |
| invalid package identity + stale lock | 9 (tests) | `CommandDriver::init` | `application("squalr-tests")` in `squalr-tests/build.omg` uses pre-migration hyphenated name; omega.lock also holds hyphenated package names — `omega update` refuses until identity is valid | unclaimed — Squalr-side | any z-worker: `application("squalr_tests")` + delete lock + `omega update`; then expect the service.omg wall (tests carries 2 stale imports) |
| stale lock (hyphenated names) | squalr-cli | — | `cannot prepare accepted omega.lock: invalid text package name` | unclaimed — Squalr-side | same worker as tests: rebuild lock after identity fix; then service.omg wall |
| squalr-engine-scanning check hang | 88 | `PointerScanRangeSearchKernel::is_empty` | package check spins >600s pure userspace CPU on an idle box, zero output; strace tail shows repeated library re-reads — likely a resolution/lowering loop, stage not yet localized | unclaimed | bisect: prune scanning sources until --check terminates; likely a single looping construct |

## Machine-level decline families (api + targets, 400 declines)

Counted at the `inspect-terminal` verdict. `InvalidUnitMachinePlan` rows are
reported by their inner omission — the t2c local-construction phase that
stopped admitting the body.

| family | count | example machine | bottom-out crate | claim status | suggested next worker |
|---|---|---|---|---|---|
| state graph: result signature | 69 | `ScanConstraintSet::push` | typed-trees-to-checked-trees `execution/terminal_unit/state_graph/mod.rs` | unclaimed | z-worker: widest single wall — result-signature admission on the unit state graph |
| statement sequence: unsupported statement kind | 60 | `PrivilegedCommandResponse::get_result_address` | typed-trees-to-checked-trees `execution/terminal_unit/control/{checked_machine,statement_sequence}` | unclaimed | z-worker: name the statement kinds still unadmitted (not eliminated by earlier legs) |
| machine has no source-independent checked scalar control plan | 47 | `command_line_parser::find_equals` | checked-trees-to-lowered-psi `machine_lowering/machine_dispatch.rs` | unclaimed | z-worker: machines with no scalar control plan — admit or route through the unit-effect path |
| statement sequence: call: call operation | 40 | `ScanResultPage::get` | typed-trees-to-checked-trees `execution/terminal_unit/calls` | **FENCED** — Claude `STATE-LOCAL-VALUE-FRONTIER` (calls/) until ~10:23Z | already claimed; verify fence expiry covers it |
| indexed reads require a whole view/byte-view parameter | 42 (40+2) | `StorageSizeText::get_byte` | checked-trees-to-lowered-psi `expression_preparation/prepare_expression.rs` | unclaimed | z-worker (z3's view chain is adjacent) |
| state graph: terminator cluster | 41 | `AnonymousValueStringFormat::from_str_window` (guard expression 19; jump/guarded parameter transfer 19; edge cleanup 2; roster 2) | typed-trees-to-checked-trees `execution/terminal_unit/state_graph/mod.rs` | unclaimed | same z-worker as result signature — same file, same admission family |
| OperationProofUnavailable | 21 | `StorageSizeText::put_digits_reversed` | checked-trees-to-lowered-psi `proofs/operation_proofs.rs` + `control_cycle_proofs.rs` | unclaimed | z-worker: obligation→proof miss in operation/cycle proof lookup |
| t2c outer calls | 16 | `StorageSizeConversions::value_to_text_consistent` | typed-trees-to-checked-trees `execution/terminal_unit/control/call_occurrences.rs` | unclaimed | z-worker: ordered statement calls + unconsumed nested calls |
| t2c structural field store | 11 | `AnonymousValueString::clone_from` | typed-trees-to-checked-trees `execution/terminal_unit/structural_scalar_store` | unclaimed | z-worker: case/scalar field store + destination-parameter arms |
| c2l misc Unsupported singlets | ~28 | `NormalizedModule::get_module_name` (ordered structural destination ×4, scalar computation ×5, direct scalar call sig ×3, composed Unit attachment ×2, acyclic ×2, operand-value ×2, misc ×10) | checked-trees-to-lowered-psi `expression_preparation`, `scalar_call_closure`, `graph_*`, `composed_control/*` | `composed_control/*` (≈6) FENCED z4 until ~08:05Z; rest unclaimed | defer to after fences drop or pick unclaimed sub-files |
| retained-receiver reconciliation drops | 5 | `PageElement::clone` | checked-trees-to-lowered-psi source-custody/value_correspondence | unclaimed | z-worker |
| InvalidTerminalModule cluster | 5 | `ContainerType::from_pointer_size` (StructuralResultMustBeOwned ×2, InvalidStructuralArgumentPath ×2, InvalidByteSequenceLengthSource ×1) | terminal-verifier validation | **FENCED** — z4 `CASE-PAYLOAD-TERMINAL-CHANNEL` covers terminal-verifier until ~08:05Z | after fence drops |
| call neither registered target nor ordinary body | 2 | `PointerScanResults::uses_multi_target_terminal_materialization` | checked-trees-to-lowered-psi `unit/plan_omissions.rs` | unclaimed | z-worker |

## Delta vs the previous sweep (omega @906f03f41b)

- squalr-engine-api previously declined in checked compilation for the whole
  package set; now 296/696 swept machines verify and `--check` exits 0 in ~70s.
- `DEPCHECK:targets-native-check` was 56 diagnostics (`host.*` unresolved +
  `Service` generic unknown) — now a single `service.omg` resolution error:
  the stale import itself, not the type machinery. The fix is delete-the-import.
- The `unsupported statement kind` and `result signature` local-construction
  families are still the top walls (129 combined) — earlier chain legs covered
  specific statement kinds; these are the remainder.
- `omega-language-std @13433c1a` dep-block family is gone — the git pin advances
  resolved under the new toolchain (std snapshot loads fine).

## Verdict shapes observed

- `verified=true` — machine lowers + verifies terminal.
- `cannot lower terminal machine … InvalidUnitMachinePlan … has no admitted body
  (local construction stopped at <phase> …)` — t2c local construction stopped;
  the `<phase>` string is the family key above.
- `cannot lower terminal machine … Unsupported("<reason>")` — c2l admission
  declined; the `<reason>` string is the family key.
- `cannot lower terminal machine … OperationProofUnavailable(ObligationId(N))` —
  c2l proof lookup miss.
- `cannot lower terminal machine … InvalidTerminalModule(<reason>)` —
  terminal-verifier validation decline.
- `cannot check inspection project: checked compilation failed for package
  <pkg>` — package wall, recorded per-package above.
