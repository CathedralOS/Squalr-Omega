#!/usr/bin/env python3
"""Post-migration fixups for retired call forms.

- `this.m(args)` desugars to `m(this, args)` (receiver calls are receiverless;
  `this` must be passed explicitly).
- Machine calls in value positions the checker rejects — `(call)` tails,
  `-> (call)` arms, and calls inside `transition` conditions — are hoisted to
  typed `let` bindings before the enclosing statement.
"""
import re, glob

def scan_to_close(t, i, o, c):
    """index past the close delimiter; comment/string aware"""
    d, j = 0, i
    while j < len(t):
        if t[j:j+2] == '//':
            e = t.find('\n', j); j = len(t) if e < 0 else e; continue
        if t[j:j+2] == '/*':
            e = t.find('*/', j); j = len(t) if e < 0 else e + 2; continue
        if t[j] == '"':
            j += 1
            while j < len(t) and t[j] != '"':
                j += 1 + (t[j] == '\\')
            j += 1; continue
        if t[j] == o: d += 1
        elif t[j] == c:
            d -= 1
            if d == 0: return j
        j += 1
    return -1

def code_pos(t, i):
    """index i adjusted: returns i if it sits inside // or /* */ or a string"""
    j = 0
    while j < i:
        if t[j:j+2] == '//':
            e = t.find('\n', j); j = len(t) if e < 0 else e; continue
        if t[j:j+2] == '/*':
            e = t.find('*/', j); j = len(t) if e < 0 else e + 2; continue
        if t[j] == '"':
            j += 1
            while j < len(t) and t[j] != '"':
                j += 1 + (t[j] == '\\')
            j += 1; continue
        j += 1
    return j if j == i else -1

MACH = re.compile(r'(?:pub\s+)?(?:boundary\s+)?(?:[a-z_0-9]+\s+)?machine\s+(\w+)\s*(?:::)?\s*(\w*)?\s*(?:<[^>]*>)?\s*\(')
RET = re.compile(r'->\s*([\w<>\[\]&\'*:.,\s]+?)\s*(?:\{|satisfies|reaches|invokes|crashes|requires|where|$)', re.M)

scoped, free = {}, {}
files = glob.glob('**/*.omg', recursive=True)
for f in files:
    src = open(f).read()
    for m in MACH.finditer(src):
        if code_pos(src, m.start()) < 0:
            continue
        pe = scan_to_close(src, m.end()-1, '(', ')')
        if pe < 0: continue
        r = RET.search(src[pe:pe+300])
        if r:
            ty, nm = m.group(1), m.group(2)
            key = f'{ty}::{nm}' if nm else ty
            (scoped if nm else free)[key] = r.group(1).strip()

def resolve_rt(name, scope_ty):
    k = f'{scope_ty}::{name}'
    if k in scoped: return scoped[k]
    if name in free: return free[name]
    hits = [v for kk, v in scoped.items() if kk.endswith('::' + name)]
    if len(set(hits)) == 1: return hits[0]
    return 'u64' if 'u64' in hits else None

THIS_CALL = re.compile(r'\bthis\.([a-z_]\w*)\s*\(')
total_this = total_tail = total_cond = 0
for f in files:
    src = open(f).read()
    # ---- pass 1: recv.m(args) -> m(recv, args), fixpoint over nesting ----
    for _round in range(40):
        edits = []
        claimed = []
        for m in re.finditer(r'\.([a-z_]\w*)\s*\(', src):
            if code_pos(src, m.start()) < 0:
                continue
            if any(a <= m.start() < b for a, b in claimed):
                continue
            j = m.start()
            while j > 0 and (src[j-1].isalnum() or src[j-1] in '._[]'):
                j -= 1
            recv = src[j:m.start()]
            first_seg = re.match(r'(this|[a-z_]\w*)', recv)
            if not first_seg or not first_seg.group(1) or first_seg.group(1)[0].isupper():
                continue
            if recv.split('.')[0] in ('in','as','if','let','mut','true','false','state','machine','transition','case','data','trait','use','pub','return','transition','requires','reaches','where') or recv.endswith('::'):
                continue
            name = m.group(1)
            p = src.index('(', m.end()-1)
            q = scan_to_close(src, p, '(', ')')
            if q < 0: continue
            inner = src[p+1:q].strip()
            rep = f'{name}({recv}, {inner})' if inner else f'{name}({recv})'
            edits.append((j, q+1, rep))
            claimed.append((j, q+1))
        if not edits:
            break
        for a, b, rep in sorted(edits, key=lambda e: -e[0]):
            src = src[:a] + rep + src[b:]
        total_this += len(edits)

    # ---- machine body spans (for scope + transition search) ----
    machs = []  # (body_open, body_close, scope_ty)
    for m in MACH.finditer(src):
        if code_pos(src, m.start()) < 0: continue
        pe = scan_to_close(src, m.end()-1, '(', ')')
        if pe < 0: continue
        be = src.find('{', pe)
        if be < 0: continue
        ee = scan_to_close(src, be, '{', '}')
        if ee < 0: continue
        machs.append((be, ee, m.group(1)))

    # ---- decls (machines + states) with return types, for tail fallback ----
    decls = []  # (start, rt)
    for m in MACH.finditer(src):
        if code_pos(src, m.start()) < 0: continue
        pe = scan_to_close(src, m.end()-1, '(', ')')
        if pe < 0: continue
        r = RET.search(src[pe:pe+300])
        if r:
            ty, nm = m.group(1), m.group(2)
            decls.append((m.start(), scoped.get(f'{ty}::{nm}') or r.group(1).strip()))
    bodies = [b for b, e, ty in machs]
    for m in re.finditer(r'\bstate\s+(\w+)\s*\(', src):
        if code_pos(src, m.start()) < 0: continue
        pe = scan_to_close(src, m.end()-1, '(', ')')
        if pe < 0: continue
        r = RET.search(src[pe:pe+300])
        if r:
            decls.append((m.start(), r.group(1).strip()))
        be2 = src.find('{', pe)
        if be2 >= 0:
            bodies.append(be2)
    decls.sort()
    bodies.sort()

    # ---- transition statements: keyword + cond + arm brace ----
    transitions = []  # (kw_start, cond_start, cond_end, brace_end)
    for m in re.finditer(r'\btransition\b', src):
        if code_pos(src, m.start()) < 0:
            continue
        i = m.end()
        # condition scan, comment aware: find `{` at depth 0
        d = 0
        j = i
        cond_start = i
        while j < len(src):
            if src[j:j+2] == '//':
                e = src.find('\n', j); j = len(src) if e < 0 else e; continue
            if src[j:j+2] == '/*':
                e = src.find('*/', j); j = len(src) if e < 0 else e + 2; continue
            if src[j] == '"':
                j += 1
                while j < len(src) and src[j] != '"':
                    j += 1 + (src[j] == '\\')
                j += 1; continue
            if src[j] == '(':
                j = scan_to_close(src, j, '(', ')')
                if j < 0: break
                continue
            if src[j] == '{':
                break
            if src[j] in '};' :
                j = -2; break
            j += 1
        if j < 0 or j >= len(src) or src[j] != '{':
            continue
        be = j
        ee = scan_to_close(src, be, '{', '}')
        if ee < 0: continue
        transitions.append((m.start(), cond_start, be, ee))

    edits = []
    n = 0
    # ---- pass 2a: machine calls inside transition conditions ----
    for kw, cs, ce, be_ in transitions:
        cond = src[cs:ce]
        scope = next((ty for b, e, ty in reversed(machs) if b < kw < e), '')
        inner_edits = []
        # paren-depth map so only top-level calls hoist
        depths = []
        d = 0
        for ch in cond:
            depths.append(d)
            if ch == '(': d += 1
            elif ch == ')': d -= 1
        for cm in re.finditer(r'([A-Za-z_]\w*(?:::[A-Za-z_]\w*)*)\s*\(', cond):
            if depths[cm.start()] != 0:
                continue
            call_name = cm.group(1)
            name = call_name.rsplit('::', 1)[-1]
            if name in ('if','as','in','in_array','tuple','cast','mut'):
                continue
            # skip a qualifier that is itself a call: `x.y(` receivers stay
            if '::' in call_name and cm.start() > 0 and cond[cm.start()-1] in '.)':
                continue
            rt_ = resolve_rt(name, scope)
            if rt_ is None:
                continue
            p = cond.index('(', cm.end()-1)
            q = scan_to_close(cond, p, '(', ')')
            if q < 0: continue
            args = cond[p+1:q]
            n += 1
            var = f'hoist{n}'
            ls = src.rfind('\n', 0, kw) + 1
            ind = re.match(r'[ \t]*', src[ls:]).group(0)
            edits.append((ls, ls, f'{ind}let {var}: {rt_} = {call_name}({args});\n'))
            inner_edits.append((cs + cm.start(), cs + q + 1, var))
            total_cond += 1
        edits.extend(inner_edits)

    # ---- pass 2b: `(name(args))` tails and `-> (name(args))` arms ----
    claimed = []
    for m in re.finditer(r'\(\s*([a-z_]\w*)\s*\(', src):
        if code_pos(src, m.start()) < 0:
            continue
        if any(a <= m.start() < b for a, b in claimed):
            continue
        name = m.group(1)
        scope = next((ty for b, e, ty in reversed(machs) if b < m.start() < e), '')
        rt_ = resolve_rt(name, scope)
        if rt_ is None: continue
        p = src.index('(', m.end()-1)
        q = scan_to_close(src, p, '(', ')')
        if q < 0: continue
        k = q + 1
        while k < len(src) and src[k] in ' \t\n': k += 1
        if k >= len(src) or src[k] != ')': continue
        args = src[p+1:q]
        n += 1
        var = f'hoist{n}'
        # find enclosing `{` via backward depth scan (comment-aware enough: we
        # only track braces, comments rarely hold them)
        j = m.start(); depth = 0
        brace = -1
        while j > 0:
            j -= 1
            if src[j] == '}': depth += 1
            elif src[j] == '{':
                if depth == 0:
                    brace = j; break
                depth -= 1
        # enclosing transition that opens that brace?
        kw_pos = -1
        if brace >= 0:
            for kw, cs, ce, be_ in transitions:
                if ce == brace:
                    kw_pos = kw; break
        if kw_pos >= 0:
            ls = src.rfind('\n', 0, kw_pos) + 1
        else:
            ls = src.rfind('\n', 0, m.start()) + 1
        ind = re.match(r'[ \t]*', src[ls:]).group(0)
        edits.append((ls, ls, f'{ind}let {var}: {rt_} = {name}({args});\n'))
        edits.append((m.start(), k+1, f'({var})'))
        claimed.append((m.start(), k+1))
        total_tail += 1

    # ---- pass 2c: bare `name(args)` machine-call tails (no parens, no ;) ----
    for m in re.finditer(r'(^[ \t]*)([a-z_]\w*)\s*\(', src, re.M):
        if code_pos(src, m.start(2)) < 0:
            continue
        if any(a <= m.start() < b for a, b in claimed):
            continue
        name = m.group(2)
        p = src.index('(', m.end()-1)
        q = scan_to_close(src, p, '(', ')')
        if q < 0: continue
        k = q + 1
        if not re.match(r'[ \t]*(\n|$)', src[k:]):
            continue
        scope = next((ty for b, e, ty in reversed(machs) if b < m.start() < e), '')
        rt_ = resolve_rt(name, scope)
        if rt_ is None:
            rt_ = next((r for s_, r in reversed(decls) if s_ < m.start()), None)
        if rt_ is None: continue
        args = src[p+1:q]
        n += 1
        var = f'hoist{n}'
        ind = m.group(1)
        edits.append((m.start(), k, f'{ind}let {var}: {rt_} = {name}({args});\n{ind}({var})'))
        total_tail += 1
    # ---- pass 2d: machine calls as record-literal field values ----
    for m in re.finditer(r':\s*([a-z_]\w*)\s*\(', src):
        if code_pos(src, m.start(1)) < 0:
            continue
        if any(a <= m.start(1) < b for a, b in claimed):
            continue
        if src[m.start():m.start()+2] == '::' or src[m.start()-1] == ':':
            continue
        name = m.group(1)
        scope = next((ty for b, e, ty in reversed(machs) if b < m.start() < e), '')
        rt_ = resolve_rt(name, scope)
        if rt_ is None:
            rt_ = next((r for s_, r in reversed(decls) if s_ < m.start()), None)
        if rt_ is None: continue
        p = src.index('(', m.end()-1)
        q = scan_to_close(src, p, '(', ')')
        if q < 0: continue
        args = src[p+1:q]
        n += 1
        var = f'hoist{n}'
        ls = src.rfind('\n', 0, m.start()) + 1
        ind = re.match(r'[ \t]*', src[ls:]).group(0)
        kw_pos = next((kw for kw, cs, ce, ee2 in reversed(transitions) if kw < m.start() < ee2), -1)
        if kw_pos >= 0:
            ls = src.rfind('\n', 0, kw_pos) + 1
        else:
            bb = next((b for b in reversed(bodies) if b < m.start()), -1)
            ls = src.rfind('\n', 0, m.start()) + 1
            if bb >= 0:
                eob = next((e for b, e, ty in machs if b == bb), -1)
                # confirm match is inside that body (avoid a later sibling body's top)
                st_close = scan_to_close(src, bb, '{', '}')
                if st_close > m.start():
                    ls = src.find('\n', bb) + 1
        ind = re.match(r'[ \t]*', src[ls:]).group(0)
        edits.append((ls, ls, f'{ind}let {var}: {rt_} = {name}({args});\n'))
        edits.append((m.start(1), q+1, var))
        claimed.append((m.start(1), q+1))
        total_tail += 1
    if edits:
        for a, b, rep in sorted(edits, key=lambda e: -e[0]):
            src = src[:a] + rep + src[b:]
    if total_this + total_tail + total_cond:
        open(f, 'w').write(src)

print('== this-calls', total_this, '| tails/arms', total_tail, '| conditions', total_cond)
