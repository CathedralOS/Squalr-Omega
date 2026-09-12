# Squalr in Omega

An essentially 1:1 port of [Squalr](https://github.com/Squalr/Squalr) from Rust to
Omega, starting with CLI and headless use. This is an application and a compiler
customer, not a collection of compiler-shaped demos.

**Setup stage, not a working scanner yet.** The workspace declares the 17
headless packages and their 37 internal dependency edges. Most packages have
only their build declaration. The source seed ports memory alignment, the
region operations needed by `SnapshotRegionFilter`, and filter geometry, with
12 authored headless checks. Package checking completes, but native Terminal
production still rejects the geometry entry's missing checked Unit body plan.
There is no supplied-byte scanner or CLI entry yet. The remaining work is
listed in [TASKS.md](TASKS.md); passing repository checks is not port completion.

## Build and test

Python 3.11+ runs the portable harness. Supply an Omega executable built from
the checkout you are testing; it must retain access to that checkout's bundled
library. The commands work in PowerShell and macOS/Linux shells:

```text
python tools/verify.py layout --upstream ../squalr_workspace
python tools/verify.py audit --omega /path/to/omega
python tools/verify.py check --timeout 600 --omega /path/to/omega
python tools/verify.py native --timeout 600 --omega /path/to/omega
```

On Windows use the path to `omega.exe`; on macOS use `python3` if necessary.
The default application is `squalr-tests`. `--project squalr-cli` selects
the real CLI lane, whose entry remains unported. No entry is silently generated.
`--target windows_x86_64` (or another supported target) makes selection explicit.
Use `check --project squalr-engine-api` to isolate library checking without
dropping the application's dependency edges.

`layout` checks repository setup and the pinned Rust package mapping only.
`audit`, `check` and `native` invoke the actual Omega CLI. Failures stay failures;
the harness neither accepts package trust nor replaces native execution with
interpretation. It retains the command, host, output and exit status under
`build/verification/`. Ordinary package review/acceptance is a separate explicit
step; no generated approval file is checked in.

Before native execution, use `omega update --project squalr-tests --target <target>`
with the same compiler (`macos_arm64` on macOS or `windows_x86_64` on Windows).
Inspect the reported review, resolve its exact pending decisions, then run
`omega update --resume --project squalr-tests`. The checked-in `omega.lock`
records the reviewed macOS baseline. Local package identities include checkout
paths, so another checkout needs ordinary update/review for its local owners;
Windows acceptance and runtime validation remain open. The longer harness timeout
accommodates the measured roughly 210-second package passes of the tested debug
compiler; it does not turn a timeout into a successful check.

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
