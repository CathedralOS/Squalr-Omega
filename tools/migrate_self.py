#!/usr/bin/env python3
"""Migrate retired `self` receivers to explicit named parameters.

- machine T::m(&self)/(&mut self)/(self)/(mut self) -> this: &T / this: &mut T / this: T / mut this: T
- state s(...) inside a machine: same receiver rewrite
- \\bself\\b inside the machine body -> this
- bare state calls n(...) inside the machine -> n(this, ...)
- T::m(...) calls inside T's own machines where m had a receiver -> T::m(this, ...)
"""
import re, pathlib, sys

MACHINE_SIG = re.compile(
    r'(?:pub\s+)?(?:boundary\s+)?(?:[a-z_0-9]+\s+)?machine\s+([A-Z][A-Za-z0-9_]*)\s*::\s*([A-Za-z0-9_]+)\s*(?:<[A-Za-z0-9_,\s\']*>)?\s*\('
)
STATE_SIG = re.compile(r'\bstate\s+([A-Za-z0-9_]+)\s*\(')
WORD = re.compile(r'\bself\b')
KWS = ('machine', 'record', 'struct', 'enum')


def _skip_noise(text, i):
    """Return index after a // comment or string literal starting at i, else i."""
    if text.startswith('//', i):
        j = text.find('\n', i)
        return len(text) if j < 0 else j
    if text[i] == '"':
        j = i + 1
        while j < len(text) and text[j] != '"':
            if text[j] == '\\':
                j += 1
            j += 1
        return j + 1
    return i


def match_parens(text, i):
    """i at '(' -> index just past matching ')'."""
    depth = 0
    while i < len(text):
        j = _skip_noise(text, i)
        if j != i:
            i = j
            continue
        c = text[i]
        if c == '(':
            depth += 1
        elif c == ')':
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return -1


def match_braces(text, i):
    depth = 0
    while i < len(text):
        j = _skip_noise(text, i)
        if j != i:
            i = j
            continue
        c = text[i]
        if c == '{':
            depth += 1
        elif c == '}':
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
    return [p for p in parts]


def receiver_for(tok, ty):
    t = re.sub(r'\s+', ' ', tok.strip())
    for old, new in (
        ('&mut self', f'this: &mut {ty}'),
        ('&self', f'this: &{ty}'),
        ('mut self', f'mut this: {ty}'),
        ('self', f'this: {ty}'),
    ):
        if t == old:
            return new
    return None


def fix_params(params, ty):
    """Return (new_params, had_receiver, already_this)."""
    parts, hit, has_this = split_top(params), False, False
    out = []
    for p in parts:
        r = receiver_for(p, ty)
        if r is not None:
            lead = p[: len(p) - len(p.lstrip())]
            out.append(lead + r)
            hit = True
        else:
            if re.match(r'^\s*this\s*:', p):
                has_this = True
            out.append(p)
    return ','.join(out), hit or has_this


def find_body_open(text, paren_end):
    """First '{' after paren_end unless a new decl keyword or '}' intervenes."""
    i = paren_end
    while i < len(text):
        c = text[i]
        if c == '{':
            return i
        if c == '}':
            return -1
        m = re.match(r'\s*(\w+)', text[i:])
        if m:
            if m.group(1) in KWS:
                return -1
            i += m.end()
            continue
        i += 1
    return -1


def rewrite_calls(body, state_names, ty, method_names):
    # bare state calls:  `name(`  where name in state_names and not preceded by . or ::
    for sname in state_names:
        pat = re.compile(r'(?<![:\.\w])' + sname + r'\s*\(')
        body = pat.sub(lambda m: m.group(0)[:-1].rstrip() + '(this, ' if _has_args(body, m) else m.group(0) + 'this)', body)
    return body


def _call_has_args(body, open_paren):
    """True if call at body[open_paren]=='(' has nonempty arg text."""
    end = match_parens(body, open_paren)
    return end > 0 and body[open_paren + 1 : end - 1].strip() != ''


def rewrite_state_calls(body, state_names):
    """name( / name(args) where name is a declared state -> name(this)/name(this, args)."""
    if not state_names:
        return body
    names = '|'.join(re.escape(s) for s in state_names)
    pat = re.compile(r'(?<![:\.\w])(?<!state )(' + names + r')\s*\(')

    def repl(m):
        open_paren = m.end() - 1
        head = m.group(0)
        end = match_parens(body, open_paren)
        if end > 0:
            first = body[open_paren + 1 : end - 1].split(',')[0].strip()
            if first in ('this', 'self'):
                return head
        if _call_has_args(body, open_paren):
            return head + 'this, '
        return head + 'this'

    return pat.sub(repl, body)


def rewrite_self_scope_calls(body, ty, method_names):
    """T::m( where m had a receiver, inside T's own machine -> T::m(this, ..."""
    if not method_names:
        return body
    names = '|'.join(re.escape(n) for n in method_names)
    pat = re.compile(r'\b' + re.escape(ty) + r'::(' + names + r')\s*\(')

    def repl(m):
        open_paren = m.end() - 1
        # already passing this/recv? skip if first arg is `this`
        end = match_parens(body, open_paren)
        if end < 0:
            return m.group(0)
        first = body[open_paren + 1 : end - 1].split(',')[0].strip()
        if first in ('this', 'self'):
            return m.group(0)
        if first == '':
            return m.group(0) + 'this'
        return m.group(0) + 'this, '

    return pat.sub(repl, body)


FREE_SIG = re.compile(
    r'(?:pub\s+)?(?:boundary\s+)?(?:[a-z_0-9]+\s+)?machine\s+([a-z_][A-Za-z0-9_]*)\s*\('
)


STATE_DECL = re.compile(r'\bstate\s+([A-Za-z_]\w*)\s*\(')

KWS_ID = {
    'transition','state','machine','record','struct','enum','data','let','mut',
    'true','false','pub','boundary','trait','satisfies','reaches','invokes',
    'crashes','requires','where','case','union','in','as','if','else','for',
    'while','return','fn','const','self','this','Optional','Wrapping','Saturating',
}
IDENT = re.compile(r'\b([a-z_]\w*)\b')
LETVAR = re.compile(r'\blet\s+(?:mut\s+)?([a-z_]\w*)')

def param_names(params):
    names = {}
    for part in split_top(params):
        m = re.match(r'\s*(?:mut\s+)?([a-z_]\w*)\s*:', part)
        if m:
            names[m.group(1)] = part.strip()
    return names

def thread_captured_params(text):
    """States that reference enclosing-machine params must declare them.
    Append missing machine params to the state signature and to all calls."""
    out, pos = [], 0
    for m in MACHINE_SIG.finditer(text):
        pe = match_parens(text, m.end() - 1)
        if pe < 0:
            continue
        params = text[m.end():pe - 1]
        bo = find_body_open(text, pe)
        if bo < 0:
            continue
        be = match_braces(text, bo)
        if be < 0:
            continue
        body = text[bo:be]
        mparams = param_names(params)
        if not mparams:
            continue
        # machine params excluding the receiver itself
        recv_names = set()
        for pname, decl in mparams.items():
            if re.match(r'^(this|mut this)\s*:', decl):
                recv_names.add(pname)
        scoped = {k: v for k, v in mparams.items() if k not in recv_names}
        if not scoped:
            continue
        # state decls with bodies
        s_edits = []
        call_edits = []
        for sm in STATE_DECL.finditer(body):
            sp = body.index('(', sm.end() - 1)
            se = match_parens(body, sp)
            if se < 0:
                continue
            sname = sm.group(1)
            sparams = body[sp + 1:se - 1]
            sdecl = param_names(sparams)
            # find state body start
            sb = find_body_open(body, se)
            if sb < 0:
                continue
            seb = match_braces(body, sb)
            if seb < 0:
                continue
            sbody = body[sb:seb]
            used = set(IDENT.findall(sbody)) - KWS_ID
            used -= set(LETVAR.findall(sbody))
            # drop field/call names that follow '.' or precede '(' where receiver is param
            captured = [k for k in scoped if k in used and k not in sdecl]
            if not captured:
                continue
            captured.sort(key=lambda k: list(scoped).index(k))
            addl = ''.join(', ' + scoped[k] for k in captured)
            s_edits.append((sp + 1, se - 1, sparams + addl))
            # every call to this state in the machine body appends the captured names
            argtail = ''.join(', ' + k for k in captured)
            for cm in re.finditer(r'(?<![\w.:])' + re.escape(sname) + r'\s*\(', body):
                head = body[max(0, cm.start() - 7):cm.start()]
                if head.rstrip().endswith('state'):
                    continue
                cp = body.index('(', cm.end() - 1)
                ce = match_parens(body, cp)
                if ce < 0:
                    continue
                inner = body[cp + 1:ce - 1].strip()
                rep = (inner + argtail) if inner else argtail.lstrip(', ')
                call_edits.append((cp + 1, ce - 1, rep))
        if not s_edits and not call_edits:
            continue
        newbody = body
        for a, b, rep in sorted(s_edits + call_edits, key=lambda e: -e[0]):
            newbody = newbody[:a] + rep + newbody[b:]
        out.append(text[pos:bo])
        out.append(newbody)
        pos = be
    out.append(text[pos:])
    return ''.join(out)

def drop_unused_state_self(body, filelabel):
    """state x(&self, ...) inside a free machine: drop the receiver if self is unused."""
    edits = []
    for sm in STATE_SIG.finditer(body):
        sp = match_parens(body, sm.end() - 1)
        if sp < 0:
            continue
        params = body[sm.end() : sp - 1]
        parts = split_top(params)
        idx = [i for i, p in enumerate(parts) if receiver_for(p, 'T') is not None]
        if not idx:
            continue
        # find this state's body extent
        brace = find_body_open(body, sp)
        if brace < 0:
            sbody = ''
        else:
            be = match_braces(body, brace)
            sbody = body[brace:be] if be > 0 else ''
        if WORD.search(sbody):
            print(f'  MANUAL: {filelabel}: state {sm.group(1)} uses self in a free machine')
            continue
        parts = [p for i, p in enumerate(parts) if i not in idx]
        edits.append((sm.end(), sp - 1, ','.join(parts)))
    for a, b, rep in reversed(edits):
        body = body[:a] + rep + body[b:]
    return body


def migrate(text):
    out, pos, changed = [], 0, 0
    for m in MACHINE_SIG.finditer(text):
        if m.start() < pos:
            continue
        ty = m.group(1)
        paren_open = m.end() - 1
        paren_end = match_parens(text, paren_open)
        if paren_end < 0:
            continue
        new_params, is_recv = fix_params(text[paren_open + 1 : paren_end - 1], ty)
        if not is_recv:
            continue
        brace = find_body_open(text, paren_end)
        if brace < 0:
            # boundary/decl machine: signature only
            out.append(text[pos:paren_open + 1] + new_params + ')')
            pos = paren_end
            continue
        brace_end = match_braces(text, brace)
        if brace_end < 0:
            continue
        body = text[paren_end:brace_end]
        # collect declared state names + rename their receivers first
        state_names = []
        s_edits = []
        for sm in STATE_SIG.finditer(body):
            sp = match_parens(body, sm.end() - 1)
            if sp < 0:
                continue
            inner, hit = fix_params(body[sm.end() : sp - 1], ty)
            if hit:
                state_names.append(sm.group(1))
                s_edits.append((sm.end(), sp - 1, inner))
        for a, b, rep in reversed(s_edits):
            body = body[:a] + rep + body[b:]
        # T::m( calls inside this machine: only m's that had a self receiver
        methods = set()
        for mm in MACHINE_SIG.finditer(text):
            if mm.group(1) != ty:
                continue
            pe = match_parens(text, mm.end() - 1)
            if pe < 0:
                continue
            if any(
                receiver_for(p, ty) is not None
                for p in split_top(text[mm.end() : pe - 1])
            ) or re.search(r'\bthis\s*:', text[mm.end() : pe - 1]):
                methods.add(mm.group(2))
        body = rewrite_state_calls(body, set(state_names))
        body = rewrite_self_scope_calls(body, ty, methods)
        body_new = WORD.sub('this', body)
        changed += len(WORD.findall(body))
        out.append(text[pos : paren_open + 1] + new_params + ')' + body_new)
        pos = brace_end
    if pos == 0:
        pass
    else:
        out.append(text[pos:])
    migrated = ''.join(out) if pos else text
    return migrated, changed


def migrate_free(text, filelabel):
    """Free machines: drop unused &self receivers in their state decls."""
    out, pos = [], 0
    for m in FREE_SIG.finditer(text):
        if m.start() < pos:
            continue
        pe = match_parens(text, m.end() - 1)
        if pe < 0:
            continue
        brace = find_body_open(text, pe)
        if brace < 0:
            continue
        be = match_braces(text, brace)
        if be < 0:
            continue
        body = text[pe:be]
        new_body = drop_unused_state_self(body, filelabel)
        out.append(text[pos:pe])
        out.append(new_body)
        pos = be
    if pos == 0:
        return text
    out.append(text[pos:])
    return ''.join(out)


def main():
    total_f, total_s = 0, 0
    for p in sorted(pathlib.Path('.').rglob('*.omg')):
        if any(x in p.parts for x in ('.git', 'target')):
            continue
        src = p.read_text()
        new, cnt = migrate(src)
        new = migrate_free(new, str(p))
        new = thread_captured_params(new)
        if new != src:
            p.write_text(new)
            total_f += 1
            total_s += cnt
    print(f'== {total_f} files migrated, {total_s} self refs renamed')


if __name__ == '__main__':
    main()
