# Squalr in Omega

An essentially 1:1 port of [Squalr](https://github.com/Squalr/Squalr) from Rust to
Omega, starting with CLI and headless use. This is an application and a compiler
customer, not a collection of compiler-shaped demos.

The workspace has 17 headless packages and 37 internal dependency edges, with
source for snapshots, scalar scanning, result encoding, command execution and
target access. The CLI entry and its read/dispatch/print loop are also present.
Source presence does not establish native acceptance or complete Rust parity.

The current published `squalr-tests` entry runs 12 geometry checks followed by
seeded snapshot/tombstone layout checks. Existing supplied-byte scan, exact-result
and repeated-scan checks are still outside its normal success path. The historical
12-check geometry application passed natively on macOS ARM64 with an older entry
and compiler; that evidence does not cover the current full application. Current
`Main::main` and its filesystem/time provider route target Linux x86_64. Full
application and CLI native acceptance remain unverified. See [TASKS.md](TASKS.md)
and [PORTING.md](PORTING.md) for the remaining work and acceptance contract.

## Build and test

Python 3.11+ runs the portable harness. Supply an Omega executable built from
the checkout you are testing; it must retain access to that checkout's bundled
library. Prefer `cargo build -p omega --release` (or `mbx build -p omega --release`)
for the complete package graph; an unoptimized compiler can spend several minutes
in package checking. The commands work in PowerShell and macOS/Linux shells:

```text
python tools/verify.py layout --upstream ../squalr_workspace
python tools/verify.py audit --omega /path/to/omega
python tools/verify.py check --timeout 600 --omega /path/to/omega
python tools/verify.py native --target linux_x86_64 --timeout 600 --omega /path/to/omega
```

On Windows use the path to `omega.exe`; on macOS use `python3` if necessary.
The default application is `squalr-tests`; `--project squalr-cli` selects the
CLI source entry. Run the native command above on Linux x86_64, the current full
application's authored target. The harness itself runs on Windows and macOS too;
other application targets still need matching entry/provider support and runtime
validation. Use `check --project squalr-engine-api` to isolate library checking
without dropping the application's dependency edges.

For `check` and `audit`, `--target` selects the compiler target. For `native`, it
asserts that the target matches the executing Python host; a mismatch is rejected
before invoking Omega. The harness then invokes `omega run --keep` without an
explicit target so Omega executes the host image. An explicit target on Omega's
own `run` command emits an image without executing it.

`layout` checks repository setup and the pinned Rust package mapping only.
`audit`, `check` and `native` invoke the actual Omega CLI. Failures stay failures;
the harness neither accepts package trust nor replaces native execution with
interpretation. It retains the command, host, output and exit status under
`build/verification/`. Ordinary package review/acceptance is a separate explicit
step; no generated approval file is checked in.

Before native execution, use the same compiler for ordinary package review:

```text
omega update --project squalr-tests --target linux_x86_64
omega update --resume --project squalr-tests
```

Inspect the first command's review and resolve its exact pending decisions before
resuming. The initial update selects the target; resume retains the proposal's
targets and does not accept a target override. The checked-in
`squalr-tests/omega.lock` records a reviewed Linux x86_64 baseline. Local package
identities include checkout paths, so another checkout needs ordinary
update/review for its local owners. A lock records package admission; native
acceptance still requires executing the application. A timeout is not a
successful check.

If a newer compiler rejects a historical lock policy version, preserve the old
lock under ignored `build/verification/lock-migration/` and retain its exact source
pins before starting fresh `omega update` review. Inspect and resolve the new
findings; do not edit version numbers or copy old decision rows into a new lock.
Git retains the previously committed lock as well.

The root `build.omg` is a workspace catalog. Each nested `build.omg` owns its
package or application and relative sibling dependencies. Applications select
std from an exact Omega Git revision by declared package name, not by a path
back into a particular embedding checkout. This deliberately exercises nested
workspaces, package-local aliases, dependency diamonds and independent roots.

## Port boundaries

| Packages | Responsibility |
| --- | --- |
| `squalr-engine-api` | Existing shared values, snapshots, filters, commands and results |
| `squalr-engine-scanning` | Scalar/SIMD scans, result encoding and parallel partitioning |
| `squalr-engine-targets`, `squalr-engine-targets-native` | Target contracts and operating-system access |
| `squalr-engine-session`, `squalr-engine`, `squalr-engine-projects` | Sessions, command execution and project data |
| `plugins/*` | Existing headless plugin package boundaries; implementation unported |
| `squalr-cli`, `squalr-tests` | CLI application and headless acceptance application |

Port behavior, package responsibilities and data structures faithfully. Translate
Rust idioms into ordinary Omega mechanisms; do not preserve Rust syntax at the
expense of semantics. Preserve the CLI command model rather than inventing a
new user interface for the port. GUI, TUI and installer work is out of scope.

Tests may supply captured bytes, deterministic allocation/target failures and
controlled child processes. They must still exercise the production scan engine.
The Rust implementation is a differential reference, not an infallible oracle;
small independent expected results and invalid-input cases remain necessary.

## Source and integration

[upstream.json](upstream.json) pins the reference revision and package map.
[PORTING.md](PORTING.md) defines parity and compiler handoff rules. The upstream
GPLv3 license is retained in [LICENSE](LICENSE); see [NOTICE](NOTICE).

Omega pins this repository as an optional submodule at `samples/apps/squalr`.
It also works as an independent checkout. Neither Squalr nor the original Rust
repository becomes a compiler dependency. Publish an application commit before
updating Omega's submodule pin.
