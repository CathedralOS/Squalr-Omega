#!/usr/bin/env python3
"""Qualify unqualified `name(args)` calls to `Type::name(args)`.

Resolves the receiver (first arg) type from:
- enclosing machine/state params (incl. `mut x: T`)
- `let x: T` / `let mut x: T` bindings
- `let [mut] x = Type::ctor(...)` / `(Type::ctor(...))` — ctor return type
- `this.field[...]` / `x.field[...]` member chains via `data` decl fields
- transition-arm payloads: `U::Variant(payload)` on a union scrutinee

Only rewrites when the resolved type T has a `T::name` decl. Also inserts
`&mut`/`&` on the receiver arg when the callee's `this:` param demands it.
"""
import re, glob, sys

FILES = sorted(set(glob.glob('squalr-*/src/**/*.omg', recursive=True)))

MACHINE_SIG = re.compile(
    r'(?:pub\s+)?machine\s+([A-Z][A-Za-z0-9_]*)\s*::\s*([A-Za-z0-9_]+)\s*'
    r'(?:<[A-Za-z0-9_,\s\']*>)?\s*\(')
# free `machine name(` decls (no `Type::` prefix) — bare `name(...)` calls
# resolve to these, so they must never be qualified to `T::name(...)`.
FREE_MACHINE_SIG = re.compile(r'(?:pub\s+)?machine\s+([A-Za-z_]\w*)\s*\(')
STATE_SIG = re.compile(r'\bstate\s+([A-Za-z0-9_]+)\s*\(')
DATA_SIG = re.compile(r'(?:pub\s+)?data\s+([A-Z][A-Za-z0-9_]*)\s*\{')
UNION_SIG = re.compile(r'(?:pub\s+)?union\s+([A-Z][A-Za-z0-9_]*)\s*\{')

def skip_noise(t, i):
    if t.startswith('//', i):
        j = t.find('\n', i)
        return len(t) if j < 0 else j
    if t.startswith('/*', i):
        j = t.find('*/', i)
        return len(t) if j < 0 else j + 2
    if i < len(t) and t[i] == '"':
        j = i + 1
        while j < len(t) and t[j] != '"':
            if t[j] == '\\':
                j += 1
            j += 1
        return j + 1
    return i

def match_parens(t, i):
    d = 0
    while i < len(t):
        j = skip_noise(t, i)
        if j != i:
            i = j; continue
        c = t[i]
        if c == '(': d += 1
        elif c == ')':
            d -= 1
            if d == 0: return i + 1
        i += 1
    return -1

def match_braces(t, i):
    d = 0
    while i < len(t):
        j = skip_noise(t, i)
        if j != i:
            i = j; continue
        c = t[i]
        if c == '{': d += 1
        elif c == '}':
            d -= 1
            if d == 0: return i + 1
        i += 1
    return -1

def split_top(s, sep=','):
    out, d, st = [], 0, 0
    i = 0
    while i < len(s):
        j = skip_noise(s, i)
        if j != i:
            i = j; continue
        c = s[i]
        if c in '([{': d += 1
        elif c in ')]}': d -= 1
        elif c == sep and d == 0:
            out.append(s[st:i]); st = i + 1
        i += 1
    out.append(s[st:])
    return out

# ---------- global index ----------
fields = {}        # Type -> {field: Type}
variants = {}      # Union -> {Variant: payload Type}
machine_ret = {}   # (Type, name) -> return type
machine_this = {}  # (Type, name) -> this param mode: '&', '&mut', 'value', 'mut value'
all_machines = {}  # name -> set of Types
free_machines = set()  # names declared as free `machine name(`

for f in FILES:
    src = open(f).read()
    for m in DATA_SIG.finditer(src):
        ty = m.group(1)
        bo = src.find('{', m.end() - 1)
        be = match_braces(src, bo)
        if be < 0: continue
        fm = {}
        for fm_ in re.finditer(r'(\w+)\s*:\s*(\[[^\]\n]*\]|[^\n;]+?)\s*;', src[bo + 1:be - 1]):
            fm[fm_.group(1)] = fm_.group(2).strip()
        fields.setdefault(ty, {}).update(fm)
    for m in UNION_SIG.finditer(src):
        ty = m.group(1)
        bo = src.find('{', m.end() - 1)
        be = match_braces(src, bo)
        if be < 0: continue
        vm = {}
        for vm_ in re.finditer(r'(\w+)\s*:\s*([A-Za-z_][\w:<>]*)', src[bo + 1:be - 1]):
            vm[vm_.group(1)] = vm_.group(2).strip()
        variants.setdefault(ty, {}).update(vm)
    for m in MACHINE_SIG.finditer(src):
        ty, name = m.group(1), m.group(2)
        pe = match_parens(src, m.end() - 1)
        if pe < 0: continue
        params = split_top(src[m.end():pe - 1])
        this_mode = None
        if params and params[0].strip().startswith('this'):
            p0 = params[0].strip()
            this_mode = '&mut' if '&mut' in p0 else '&'
        tail = src[pe:pe + 400]
        rm = re.search(r'->\s*([A-Za-z_][\w:<>,\[\]\s\*&\']*?)[\s\{]', tail)
        machine_ret[(ty, name)] = rm.group(1).strip() if rm else '()'
        machine_this[(ty, name)] = this_mode
        all_machines.setdefault(name, set()).add(ty)
    for m in FREE_MACHINE_SIG.finditer(src):
        free_machines.add(m.group(1))

def strip_ref(t):
    return t.lstrip('&').replace('mut ', '').strip()

def base_type(t):
    t = strip_ref(t)
    m = re.match(r'([A-Z][A-Za-z0-9_]*)', t)
    return m.group(1) if m else None

def resolve_member(ty, chain):
    """resolve field accesses on ty following chain of .field / [i]."""
    cur = ty
    for part in chain:
        if part.startswith('['):
            m = re.match(r'\[([A-Za-z_][\w:<>]*)', cur)
            cur = m.group(1) if m else cur
            continue
        key = part.lstrip('.')
        fm = fields.get(cur, {})
        nxt = strip_ref(fm.get(key, ''))
        if not nxt:
            return None
        cur = nxt
    return cur

def env_for_params(params):
    env = {}
    for p in split_top(params):
        p = p.strip()
        m = re.match(r'(?:mut\s+)?(\w+)\s*:\s*(.+)', p)
        if m:
            env[m.group(1)] = base_type(m.group(2)) or m.group(2)
    return env

def qualify_body(body, ty, params):
    total = 0
    base_env = env_for_params(params)
    # split into segments: prologue (before first state) + per-state spans,
    # each state contributes its own params to the env
    spans = []
    prev = 0
    for sm in STATE_SIG.finditer(body):
        pe = match_parens(body, sm.end() - 1)
        if pe < 0:
            continue
        spans.append((prev, sm.start(), base_env))
        env = dict(base_env)
        env.update(env_for_params(body[sm.end():pe - 1]))
        bo = body.find('{', pe)
        if bo >= 0 and bo < pe + 400:
            be = match_braces(body, bo)
            if be > 0:
                spans.append((bo + 1, be - 1, env))
                prev = be - 1
                continue
        prev = pe
    if not spans:
        spans = [(0, len(body), base_env)]
    for ss, se, env in sorted(spans, reverse=True):
        nb, n = _qualify_span(body[ss:se], ty, env)
        if n:
            body = body[:ss] + nb + body[se:]
            total += n
    return body, total


def _qualify_span(body, ty, env):
    env = dict(env)
    env['this'] = ty
    edits = []

    # let bindings first (needed before call rewrite)
    for m in re.finditer(r'\blet\s+(?:mut\s+)?(\w+)\s*:\s*([A-Za-z_][\w:<>,\[\]\s\*&\']*?)\s*=', body):
        env[m.group(1)] = base_type(m.group(2)) or m.group(2)
    for m in re.finditer(r'\blet\s+(?:mut\s+)?(\w+)\s*=\s*\(?\s*([A-Z][\w]*)::(\w+)\s*\(', body):
        rt = machine_ret.get((m.group(2), m.group(3)))
        if rt:
            env[m.group(1)] = base_type(rt) or rt
    # arm payloads: `U::Variant(p1, p2) ->` on transitions; payload type from union
    for m in re.finditer(r'([A-Z][\w]*)::(\w+)\s*\(\s*([^()]*)\)\s*->', body):
        un, var = m.group(1), m.group(2)
        pld = variants.get(un, {}).get(var)
        if pld:
            names = [x.strip() for x in m.group(3).split(',') if x.strip()]
            ptypes = [x.strip() for x in pld.split(',') if x.strip()]
            if len(ptypes) == len(names):
                for n, t in zip(names, ptypes):
                    env[n] = base_type(t) or t

    def arg0_type(a0, start):
        a0 = a0.strip()
        if not a0 or a0.startswith('&'):
            a0 = a0.lstrip('&').replace('mut ', '').strip()
        if a0 in env:
            return env[a0]
        if a0.startswith('this.'):
            parts = re.split(r'(\.\w+|\[[^\]]*\])', a0[5:])
            chain = [p for p in parts if p]
            mem = re.split(r'(\[[^\]]*\])', a0[5:])
            segs = [s for s in mem if s and not s.startswith('[')]
            chain = []
            for s in mem:
                if not s: continue
                if s.startswith('['): chain.append(s)
                else:
                    chain.extend('.' + p for p in s.split('.') if p)
            return resolve_member(ty, chain)
        mm = re.match(r'(\w+)\.', a0)
        if mm and mm.group(1) in env:
            rest = a0[len(mm.group(1)):]
            chain = []
            for s in re.split(r'(\[[^\]]*\])', rest):
                if not s: continue
                if s.startswith('['): chain.append(s)
                else: chain.extend('.' + p for p in s.split('.') if p)
            return resolve_member(env[mm.group(1)], chain)
        return None

    state_names = set(re.findall(r'\bstate\s+([A-Za-z0-9_]+)\s*\(', body))
    for m in re.finditer(r'(?<![:\w.])([a-z_]\w*)\s*\(', body):
        name = m.group(1)
        if name not in all_machines or name in free_machines:
            continue
        # bare `-> name(...)` tail = state destination, not a value call
        pre = body[max(0, m.start() - 8):m.start()]
        if re.search(r'->\s*$', pre):
            continue
        # a same-name state in this machine: ambiguous — skip
        if name in state_names:
            continue
        pe = match_parens(body, m.end() - 1)
        if pe < 0: continue
        args = body[m.end():pe - 1]
        first = split_top(args)[0].strip() if args.strip() else ''
        if not first:
            continue
        t0 = arg0_type(first, m.start())
        if not t0 or (t0, name) not in machine_ret:
            # fallback: if name declared on exactly one type, use it
            types = all_machines[name]
            if len(types) == 1:
                t0 = next(iter(types))
            else:
                continue
        this_mode = machine_this.get((t0, name))
        recv = first
        if this_mode == '&mut' and not first.startswith('&mut'):
            recv = '&mut ' + first.lstrip('&').replace('mut ', '', 1).strip() if first.startswith('&') else '&mut ' + first
        elif this_mode == '&' and not first.startswith('&'):
            recv = '&' + first
        rest = args[len(first):]
        newcall = f'{t0}::{name}({recv}{rest})'
        edits.append((m.start(), pe, newcall))

    # repair pass: X::name(arg0,...) where arg0's type T != X and T::name exists
    for m in re.finditer(r'(?<![:\w])([A-Z]\w*)::(\w+)\s*\(', body):
        xty, name = m.group(1), m.group(2)
        # factories/plain fns have no `this` receiver — arg0 isn't the receiver
        if machine_this.get((xty, name)) is None:
            continue
        pe = match_parens(body, m.end() - 1)
        if pe < 0:
            continue
        args = body[m.end():pe - 1]
        first = split_top(args)[0].strip() if args.strip() else ''
        if not first:
            continue
        t0 = arg0_type(first, m.start())
        if not t0 or t0 == xty or (t0, name) not in machine_ret:
            continue
        this_mode = machine_this.get((t0, name))
        recv = first
        if this_mode == '&mut' and not first.startswith('&mut'):
            recv = '&mut ' + (first.lstrip('&').replace('mut ', '', 1).strip() if first.startswith('&') else first)
        elif this_mode == '&' and not first.startswith('&'):
            recv = '&' + first
        rest = args[len(first):]
        edits.append((m.start(), pe, f'{t0}::{name}({recv}{rest})'))

    for st, en, rep in reversed(edits):
        body = body[:st] + rep + body[en:]
    return body, len(edits)

total = 0
for f in FILES:
    src = open(f).read()
    out = src
    # process each machine body
    pieces = []
    pos = 0
    for m in MACHINE_SIG.finditer(src):
        ty = m.group(1)
        pe = match_parens(src, m.end() - 1)
        if pe < 0: continue
        bo = src.find('{', pe)
        if bo < 0 or bo > pe + 600: continue
        be = match_braces(src, bo)
        if be < 0: continue
        pieces.append((m.start(), bo + 1, be - 1, ty, src[m.end():pe - 1]))
    for st, bs, be, ty, params in sorted(pieces, reverse=True):
        body = out[bs:be]
        nb, n = qualify_body(body, ty, params)
        if n:
            out = out[:bs] + nb + out[be:]
            total += n
    if out != src:
        open(f, 'w').write(out)
        print(f)
print('qualified', total)
