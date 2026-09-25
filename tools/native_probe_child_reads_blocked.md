> SUPERSEDED (2026-09-23): the fs fused-provider deadlock below was cleared on
> Omega main (z4's fused FsHost binding + `ad39f401ed` ambient borrowed-self
> receivers + `122222e07e` crash-declaring callee custody, all ≤ `5d5e5f371c`).
> The lane is now blocked by a NEW toolchain regression — see
> `tools/native_probe_toolchain_float_regression.md`.

# LEAF native-probe-child-reads — blocked at toolchain rev 24d256130eba1eef860cbed64b6f9e109715aeb7

Branch `leaf/native-probe-child-reads`, zergling z6 (2026-09-22). Omega built
fresh from `CathedralOS/Omega` main at `24d256130eba1eef860cbed64b6f9e109715aeb7`
(`cargo build --release -p omega`) — one commit past the replay fix
`d756f86e21` / dep requirement `2a8edec522`. `squalr-tests/main.omg` is the
verbatim restore of `tools/native_probe_main.omg.parked` (minus no lines).

## The wall, exactly

`omega update --project squalr-tests --target linux_x86_64` (fresh binary):

```
error: selected ProgramEntry Service field `Main::raw_fs` requires a selected
Fused provider for boundary `FilesystemHost`
```

`omega run --keep main.omg` cannot be attempted: the lock's dependency
projection differs until a review publishes, and no review can publish while
the entry carries `Service<FilesystemHost>`.

## Why the entry cannot attach — the binding bootstrap deadlock

`Service<FilesystemHost>` attachment needs `fused_service_erasure` bound for
the requirement, which only the toolchain-minted plan supplies
(`build-evaluation/src/provider_settlement/canonical_filesystem_host.rs`),
and the mint only runs when the package's inputs carry an *accepted*
`FilesystemHostService` semantic binding:

`accepted_semantic_binding(AcceptedSemanticBindingRole::FilesystemHostService)`

That binding is consumer-scoped and can only be *nominated* by the consumer's
own review: `candidate_service_bindings` (`manager/src/review/candidate/
semantic_bindings.rs:314`) scans the package's review projection for fs
service references, then `candidate_semantic_binding_inputs` wraps it as
`ConsumerScopedSemanticBindingReviewInput(review.key(), ...)`. The
preliminary `compile_pass` (`TargetEntryDiscovery::Dependencies`) therefore
must emit the root's review before the binding exists — but the root's check
runs `derive_fused_program_entry_establishments`
(`build/selected-dispatch/src/service_custody/root.rs:109`) inside
`execution_settlement` *unconditionally* for `selected_program_entry`, and it
rejects the `Service<FilesystemHost>` field before the review can nominate
the binding that would erase it. The requirement is the binding and the
binding is the requirement: no `omega` CLI path can attach an fs service to a
`ProgramEntry`.

The same check rejects `Service<TimeHost>` identically — and `TimeHost` has
no settlement at all at this rev (no `TimeHostService` role, no
`time_impl.omg` in any std target dir, no minted plan), so the probe's
throughput leg is doubly fenced.

Second wall reached when `raw_fs`/`time` are removed but
`providers: EngineOsProviders` stays: the attached-data walk recurses into
nested `host: Service<FilesystemHost>` fields inside the providers and fails
`attached data shape` — the same missing erasure, one level down. Provider
data carrying host services cannot attach to an entry at this rev either.

## Every native-I/O lane tried, each proven dead at 24d25613

Minimal repro (`fsapp`: dep package `ctl` + root `main.omg`, `Source::Path`
deps to the local std + dep — all commands `omega update --project . --target
linux_x86_64`, then review-accept + `--resume`, then `omega run`):

1. `Service<ProbeCtl>` + `machine` impls + `select_provider` — attaches and
   publishes (the fused-erasure mechanism works for squalr-owned boundary
   traits), but the dispatch needs a boundary target, and
   `boundary machine` satisfies impls are the only things that register one.
2. `boundary machine CtlNative::ctl_open(...) satisfies ProbeCtl::control_open;`
   — check passes, dispatch resolves — then realization fails:
   `bodyless boundary symbol ctl_open has no executable realization; use it
   only in contracts, or satisfy a boundary requirement via an admitted
   provider`. The admitted set is the hosted catalog only
   (`inferred_hosted_catalog_leaf`: `ConsoleNativeProvider::{read_byte,
   write_byte}`, `ConsoleNativeProvider`/`ProcessExitNativeProvider`
   `exit_process`). Foreign boundary ops have no realization path.
3. `machine ... satisfies T::m via Binding::Syscall(2);` (bodiless external
   leaf, corpus `external_leaf_syscall_compile` shape) — check passes,
   `external_supply`/`callable`/`syscall` rows mint into the lock — but the
   leaf mints no machine plan: direct calls fail `missing a checked
   transitive machine plan`, and as the requirement's only impl the service
   call fails `missing boundary target`. Uncallable from checked code at
   this rev.
4. `boundary machine ... via Binding::Syscall(n)` — rejected at check:
   `carries a via binding but is not an external leaf` (via requires a
   bodiless non-boundary machine).
5. `machine` impl + `boundary machine` impl for the same requirement —
   `binds X 2 times; one row per method`. Checked impl + leaf for the same
   requirement — same collision.
6. `ctl: CtlNative` plain provider-data field + `self.ctl.control_open()` —
   the leaf call binds but again `missing a checked transitive machine plan`
   at realization. Data-attached providers cannot reach syscalls either.
7. Scalar-result provider impls hit `Lowering(Unsupported("scalar-result
   provider candidates have no admitted terminal route"))`
   (`checked-trees-to-lowered-psi/unit/attached_unit/providers.rs:206`) —
   the terminal route for `-> i32` provider methods is not admitted; the
   console catalog works precisely because `write_byte`/`exit_process` are
   unit and `read_byte` returns the structural `ByteRead`.
8. `Service<Console>` field + `block self.console.read_byte()` +
   `self.console.write_byte(65)` — realizes and compiles (`compiled for
   target linux_x86_64 OK`). This is the *only* lane that produces a working
   native binary, and it carries no path to file or process syscalls.

## Omega-side regression statement (for the board)

`tests/omega/pass/filesystem/*` and every other corpus entry carrying
`Service<FilesystemHost>` on a `ProgramEntry` compile only through the
test-harness `SemanticBindingReview::Explicit` path. Under the CLI
(`omega update`/`omega run`/`omega install`) the consumer-scoped binding can
never be discovered because the consumer's own preliminary check dies on the
field at `derive_fused_program_entry_establishments` — before
`candidate_service_bindings` can nominate `FilesystemHostService` and before
`mint_canonical_filesystem_host_plan` can run. Either the preliminary pass
must tolerate unattached `Service` fields on the discovered-entry (deferring
erasure to the bound recompile) or the fs binding needs a second nomination
channel that does not depend on the consumer's own preliminary success —
matching how `candidate_target_entry_binding` lets a *dependency* propose the
consumer's entry-contract binding.

Secondary, for the non-std lane: `via Binding::Syscall` external leaves mint
review rows but no machine plans — they are satisfies rows that nothing can
call — and scalar-result provider candidates have no admitted terminal route.
Both are toolchain-owned; neither can be shimmed in Squalr (AGENTS.md).

## What the branch carries

- `squalr-tests/main.omg` — verbatim restore of
  `tools/native_probe_main.omg.parked` (probe chain gated on
  `/tmp/squalr-native-probe.control`, geometry canary on the false edge).
  Red at this rev by the walls above — kept as the honest attempted shape,
  not flattened or stubbed.
- `tools/native_probe_subject.c`, `tools/native_probe_driver.py` — already on
  main; untouched.
- This note.

## Gate

- `cargo build --release -p omega` at `24d256130eba` — built OK.
- `omega update --project squalr-tests --target linux_x86_64` — FAILS at
  candidate checking with the diagnostic above (identical error for the
  minimal `data Main { console: Service<Console>; host:
  Service<FilesystemHost>; }` repro).
- `python3 tools/native_probe_driver.py` — unattemptable: `omega run` cannot
  produce a binary while the entry carries unattached services.
