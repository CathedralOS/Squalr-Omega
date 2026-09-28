# Binding-member interference: the dodge

`tools/binding-param-transfer-repro` (this directory's sibling) fails on
omega-8a94858 with `result ownership` / `parameter transfer` /
`edge cleanup: no state plan` diagnostics that only appear when a data type
reachable from the program entry carries a `Binding<T>` member — for ANY
boundary trait T (reproduced with `Binding<FilesystemHost>`).

This package is the same program with the member removed and the boundary
reached through trait-level calls + `invokes` ceilings instead:

- `Console::write_line("x")`, `Console::exit_process(0)`,
  `block Console::read_line(&mut buf)` — no `Binding<Console>` member.
- Machines that (transitively) call the boundary publish `invokes Console;`
  (and `blocks;` + `crashes Trap` where the callee warrants it); callers
  of a `blocks;` machine must use the `block` envelope.

It compiles clean on omega-8a94858 — proof the poison is the member
declaration, not boundary invocation. `ConsoleNativeProvider::*` is private
to std's console module and cannot be called directly; trait-level dispatch
is the poison-free route.
