# Squalr Omega port

Read README.md, PORTING.md and TASKS.md before work. The north star is an
essentially 1:1 port of the pinned Rust Squalr, CLI/headless first. Source paths,
package responsibilities, command semantics and performance-relevant storage
relationships should remain recognizable.

- Use the exact upstream revision in upstream.json. Do not silently compare
  with a moving Rust checkout. Record intentional behavioral deviations.
- Every package owns its nested build.omg. Keep ordinary dependency edges;
  do not flatten source into one application to bypass package/compiler gaps.
- A build-only package is unported, not an implemented empty library. Do not
  add successful placeholder bodies, mocked scan outputs or unused framework.
- Use ordinary Omega data, ownership, machines and build mechanisms. Compiler
  bugs belong in Omega with a small regression and the unchanged application
  command as outer acceptance. Never teach the compiler a Squalr-specific shape.
- Port real vertical behavior. Supplied snapshots and fault-injected target
  readers are allowed testing adapters, not substitutes for the scan engine.
- Preserve result ranges, candidate stride versus byte coverage, reused
  snapshots and partition-owned output. Do not replace these with one object
  per result or a fixed-capacity demo simply to satisfy current compiler limits.
- A native milestone needs actual native execution and expected results.
  Source checking, host tests and interpreted execution are distinct evidence.
- Keep user edits. Work on a branch/worktree, run focused checks, checkpoint and
  push verified work. Never force-push shared history. When integrating with
  Omega, follow its AGENTS.md and landing reservation protocol for the parent pin.
- TASKS.md contains unfinished work only, not a landed-work diary. Record genuine
  language decisions in Omega's OWNER_QUESTIONS.md, not as silent app semantics.
- Host tooling uses Python standard library and supports Windows and macOS;
  scripts invoke the compiler, they do not implement an alternate compiler.
