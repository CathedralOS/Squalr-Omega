# Resolver text regression

Run `omega run --both main.omg` after ordinary dependency review. Both engines
must exit zero. The program uses the real engine API package: parse `abc` into
a relative symbol path and display it back into a buffer, retaining all three
bytes and leaving the next byte untouched. It also checks a dotted path with a
hexadecimal offset (`abc.def+0x10`) and the empty path, with nonzero canaries
beyond the output to expose accidental writes.

The pinned upstream `symbolic_resolver_definition.rs` preserves the parsed
field name in `SymbolicResolverRelativeSymbolPath::parse_segment` and displays
that name. The Omega port's old window copier wrote the bytes but returned its
initial destination offset on normal completion, dropping the name's length.
Literal and window copies now share the running-position implementation.
