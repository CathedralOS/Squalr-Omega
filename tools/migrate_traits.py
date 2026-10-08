#!/usr/bin/env python3
"""Genericize squalr traits whose member machines carried the retired self receiver.

trait X { machine m(&mut self, ...); } -> trait X<Provider> { machine m(provider: &mut Provider, ...); }
satisfies X::m on `machine T::m(` impls -> satisfies X<T>::m
"""
import re, pathlib

TRAIT = re.compile(r'(?:pub\s+)?(?:boundary\s+)?trait\s+([A-Z][A-Za-z0-9_]*)(\s*<[^>{]*>)?\s*\{')
MEMBER = re.compile(r'\bmachine\s+([A-Za-z0-9_]+)\s*(<[A-Za-z0-9_,\s\']*>)?\s*\(')
SATISFIES = re.compile(r'satisfies\s+([A-Z][A-Za-z0-9_]*)\s*::\s*([A-Za-z0-9_]+)')
MACHINE_T = re.compile(
    r'(?:pub\s+)?(?:boundary\s+)?(?:\w+\s+)?machine\s+([A-Z][A-Za-z0-9_]*)\s*::\s*([A-Za-z0-9_]+)\s*\('
)
SELF_TOK = re.compile(r'^\s*(&mut\s+self|&\s*self|mut\s+self|self)\s*$')
SELF_WORD = re.compile(r'\bself\b')


def match_delim(text, i, op, cl):
    depth = 0
    while i < len(text):
        if text[i] == op:
            depth += 1
        elif text[i] == cl:
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return -1


def split_top(params):
    parts, depth, cur = [], 0, []
    for ch in params:
        if ch in '<([{':
            depth += 1
        elif ch in '>)]}':
            depth -= 1
        if ch == ',' and depth == 0:
            parts.append(''.join(cur))
            cur = []
        else:
            cur.append(ch)
    parts.append(''.join(cur))
    return parts


def recv_form(tok):
    t = re.sub(r'\s+', ' ', tok.strip())
    return {
        '&mut self': 'provider: &mut Provider',
        '&self': 'provider: &Provider',
        'mut self': 'mut provider: Provider',
        'self': 'provider: Provider',
    }.get(t)


def migrate_traits(text):
    """Returns (text, set_of_genericized_trait_names)."""
    out, pos, traits = [], 0, set()
    for m in TRAIT.finditer(text):
        name = m.group(1)
        brace = m.end() - 1
        end = match_delim(text, brace, '{', '}')
        if end < 0:
            continue
        block = text[brace:end]
        edits, hit = [], False
        for mm in MEMBER.finditer(block):
            pe = match_delim(block, mm.end() - 1, '(', ')')
            if pe < 0:
                continue
            params = block[mm.end() : pe - 1]
            np, changed = [], False
            for p in split_top(params):
                r = recv_form(p)
                if r is not None:
                    np.append(p[: len(p) - len(p.lstrip())] + r)
                    changed = True
                else:
                    np.append(p)
            if changed:
                hit = True
                edits.append((mm.end(), pe - 1, ','.join(np)))
        already_generic = m.group(2) is not None
        has_provider = re.search(r'\bprovider\s*:', block) is not None
        if not hit:
            if already_generic:
                traits.add(name)
                if has_provider:
                    nb = re.sub(r'\bSelf\b', 'Provider', block)
                    if nb != block:
                        out.append(text[pos:m.end() - 1])
                        out.append(nb)
                        pos = end
            continue
        new_block = block
        for a, b, rep in reversed(edits):
            new_block = new_block[:a] + rep + new_block[b:]
        new_block = re.sub(r'\bSelf\b', 'Provider', new_block)
        traits.add(name)
        head = text[pos : m.end() - 1].rstrip()
        if '<' not in text[m.start() : m.end() - 1]:
            head += '<Provider>'
        out.append(head)
        out.append(' ')
        out.append(new_block)
        pos = end
    if pos == 0:
        return text, traits
    out.append(text[pos:])
    return ''.join(out), traits


def migrate_satisfies(text, trait_names):
    """satisfies X::m -> satisfies X<T>::m using the machine's own record type."""
    # map: each machine T::m's byte span -> T (for satisfies inside its header)
    impls = []  # (pos, ty)
    for mm in MACHINE_T.finditer(text):
        impls.append((mm.start(), mm.group(1)))

    def ty_at(pos):
        # nearest preceding machine decl
        t = None
        for p, ty in impls:
            if p <= pos:
                t = ty
            else:
                break
        return t

    def repl(m):
        tname, member = m.group(1), m.group(2)
        if tname not in trait_names:
            return m.group(0)
        ty = ty_at(m.start())
        if ty is None:
            return m.group(0)
        return f'satisfies {tname}<{ty}>::{member}'

    text = SATISFIES.sub(repl, text)
    # named impl blocks: `X: T satisfies Trait` -> `X: T satisfies Trait<T>`
    named = re.compile(r'([A-Z][A-Za-z0-9_]*)\s+satisfies\s+([A-Z][A-Za-z0-9_]*)(?!\s*::|\s*<)')

    def repl2(m):
        ty, tname = m.group(1), m.group(2)
        if tname not in trait_names:
            return m.group(0)
        return f'{ty} satisfies {tname}<{ty}>'

    return named.sub(repl2, text)


def main():
    generic_traits = set()
    files = [
        p
        for p in sorted(pathlib.Path('.').rglob('*.omg'))
        if not any(x in p.parts for x in ('.git', 'target'))
    ]
    # pass 1: genericize trait decls, collect names
    for p in files:
        src = p.read_text()
        new, names = migrate_traits(src)
        if names:
            generic_traits |= names
            p.write_text(new)
            print(f'{p}: trait(s) {sorted(names)} genericized')
    print(f'== generic traits: {sorted(generic_traits)}')
    # pass 2: satisfies sites
    for p in files:
        src = p.read_text()
        new = migrate_satisfies(src, generic_traits)
        if new != src:
            p.write_text(new)
            print(f'{p}: satisfies updated')


if __name__ == '__main__':
    main()
