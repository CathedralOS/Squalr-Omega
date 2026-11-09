#!/usr/bin/env python3
"""Drop clause-ending semicolons from machine headers.

Omega's `machine-clause-delimiters` decision (wiki/spec/language/
state_contracts.md#machine-header-delimiters) says a header clause is ended by
the next clause keyword or by the body, never by `;`. Only a bodyless
declaration keeps one final `;`. The port wrote `requires ...;` directly
before a body, which a current compiler reads as a bodyless declaration
followed by a stray block.

For every `machine` header this removes a depth-0 `;` whose next significant
token is `{` or another clause keyword. Comments, strings and every other
byte are preserved. Run with `--check` to list the edits without writing.
"""
import pathlib
import sys

CLAUSES = {"requires", "ensures", "reaches", "invokes", "suspends", "blocks",
           "crashes", "terminates", "satisfies"}


def tokens(text):
    """Yield (kind, start, end) for significant tokens; skip comments/space."""
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if c.isspace():
            i += 1
        elif text.startswith("//", i):
            j = text.find("\n", i)
            i = n if j < 0 else j
        elif c == '"':
            j = i + 1
            while j < n and text[j] != '"':
                j += 2 if text[j] == "\\" else 1
            yield ("string", i, min(j + 1, n))
            i = j + 1
        elif c.isalpha() or c == "_":
            j = i + 1
            while j < n and (text[j].isalnum() or text[j] == "_"):
                j += 1
            yield ("word", i, j)
            i = j
        else:
            yield ("punct", i, i + 1)
            i += 1


def migrate(text):
    stream = list(tokens(text))
    remove = []
    position = 0
    while position < len(stream):
        kind, start, end = stream[position]
        position += 1
        if kind != "word" or text[start:end] != "machine":
            continue
        depth = 0
        while position < len(stream):
            kind, start, end = stream[position]
            spelling = text[start:end]
            if kind == "punct" and spelling in "([":
                depth += 1
            elif kind == "punct" and spelling in ")]":
                depth -= 1
            elif depth == 0 and kind == "punct" and spelling in "{}":
                break
            elif depth == 0 and kind == "punct" and spelling == ";":
                following = stream[position + 1] if position + 1 < len(stream) else None
                next_spelling = text[following[1]:following[2]] if following else ""
                if next_spelling == "{" or (following and following[0] == "word"
                                            and next_spelling in CLAUSES):
                    remove.append(start)
                    position += 1
                    if next_spelling == "{":
                        break
                    continue
                position += 1
                break
            position += 1
    if not remove:
        return text, 0
    pieces, last = [], 0
    for offset in remove:
        pieces.append(text[last:offset])
        last = offset + 1
    pieces.append(text[last:])
    return "".join(pieces), len(remove)


def main():
    arguments = sys.argv[1:]
    check = "--check" in arguments
    roots = [argument for argument in arguments if argument != "--check"]
    if not roots:
        print(__doc__)
        return 2
    files = edits = 0
    for root in roots:
        root = pathlib.Path(root)
        paths = [root] if root.is_file() else sorted(root.rglob("*.omg"))
        for path in paths:
            if "build" in path.parts and "verification" in path.parts:
                continue
            original = path.read_bytes().decode("utf-8")
            migrated, count = migrate(original)
            if count:
                files += 1
                edits += count
                if check:
                    print(f"{path}: {count}")
                else:
                    path.write_bytes(migrated.encode("utf-8"))
    print(f"{'would edit' if check else 'edited'} {edits} header terminators in {files} files")
    return 1 if check and edits else 0


if __name__ == "__main__":
    sys.exit(main())
