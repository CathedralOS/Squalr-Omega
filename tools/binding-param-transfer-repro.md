# Binding-member `parameter transfer` interference repro

`binding-param-transfer-repro/` is a minimal application package (entry +
`Cli` data holding `engine` + `console: Binding<Console>`) whose
`Engine::dispatch_parsed_list` unwraps `CommandLineParse -> CommandLineCommand
-> PrivilegedCommand` through case-bound successors.

With the `console: Binding<Console>` member present, `--check` fails:

    selected ProgramEntry establishment rejoins 0 Terminal attachment
    identities; ... omitted at local construction at
    `state graph: terminator: conditional successors: parameter transfer`
    (state 0, statement 1)

Deleting the member (nothing else changes) compiles clean. Boundary-binding
members are the only access path to `pub boundary trait Console` (std
`console.omg`), so the shape is not respellable from the application side.
Every egress position for a case-bound field is poisoned while a Binding
member exists anywhere in the application package's data graph: state-successor
args (`parameter transfer`), `(expr)` call args (`parameter path`), bare call
arms (`call count agreement`/`target state`), nested call args
(`source symbol`), and bound-field borrow results (`result ownership`).
Reproduced on omega@9838f76f804b and omega@8a9485804ea (bundled release).
Same interference family as the leg-22 `caller structural result` report.
