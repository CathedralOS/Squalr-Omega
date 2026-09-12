# Port contract

## Parity means

The target is Squalr's existing headless application, not a redesigned scanner.
Preserve command/request/response behavior, scan comparisons and numeric edge
cases, address/stride geometry, snapshots, repeated scans, result ordering,
pagination, cancellations and partial target-read failures. Preserve performance
architecture: RLE filters, independently produced result batches, shared snapshot
storage, scalar/SIMD dispatch and region-level parallel work.

Rust-specific async, trait-object, closure and allocation spellings may translate
to Omega's ordinary mechanisms. Such translation is not permission to weaken a
contract, serially flatten output or delete a supported mode. Unavailable library
or compiler facilities are named blockers, not successful placeholder methods.

The workspace includes the internal dependency closure of the CLI, including
its existing built-in plugin aggregator. Only build declarations are initially
present for most of that graph. Third-party Rust dependencies are not silently
implemented, vendored as foreign runtime code or replaced with empty services.
Their functionality must be routed to ordinary Omega packages or explicitly
ported when the consuming behavior is reached.

## Executable progression

1. Preserve primitive region/filter geometry and cross-package headless tests.
2. Port the supplied-byte scalar scan through snapshots, comparison dispatch,
   RLE output and querying. Exercise repeated scans over the same snapshot.
3. Connect existing CLI commands and file/captured-input test adapters to that
   engine. Keep test-only commands out of the public CLI grammar.
4. Read a controlled child process through the existing target boundary;
   exercise short/failed reads and disappearing pages without inventing valid bytes.
5. Restore SIMD and parallel paths, cancellation and deterministic publication;
   compare exact results and measure allocation volume and throughput.

This orders work; it does not reduce the eventual parity target. A supported
scalar path is a useful milestone, not permission to abandon optimized paths.

## Evidence and compiler pressure

For each increment, retain the exact Rust source mapping, ordinary Omega command,
input and expected result. Use Rust differential checks plus small independent
fixtures. Include empty input, no/all matches, overlapping candidates, tails,
address overflow, repeat filtering and failure cases as each behavior is ported.

Compiler work must keep the authored application intact and fix the owning
general representation/operation. Do not lower to a test-only route, flatten
packages, switch to interpretation as the completion bar, or constrain input
to hide a missing feature. Record the earliest current blocker with the actual
diagnostic and owner; do not guess downstream failures from it.

The root is a workspace, not a synthetic combined executable. Per-package build
evaluation, std's named Git member, source closure and independent application
acceptance are part of the customer. A second application's approval must not be
borrowed from the first. Shared workspace lock limitations remain compiler work.

## Reference updates

upstream.json records a clean Rust commit. Before updating it, inspect upstream
behavior changes and compare the internal package edges. Preserve attribution
and the upstream license. Implementation mappings belong beside source or in
the active task; do not copy an ever-growing historical ledger into this file.
