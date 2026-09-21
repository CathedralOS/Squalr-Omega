#!/usr/bin/env python3
"""Drive the TARGETS-AND-THROUGHPUT native-read probe end to end.

Compiles tools/native_probe_subject.c with the platform C compiler, launches
it as a controlled child (the child announces "<pid> <page> <guard>" on its
stdout), hands those coordinates to squalr-tests through
/tmp/squalr-native-probe.control, runs `omega run --keep` on the app, and
asserts the "Squalr native-read: PASS" marker plus the timed-throughput line.

Python standard library only, per this app's tooling rule. POSIX hosts with a
C compiler and procfs are required for this leg (Linux is what the Omega
targets-native Linux impl covers; other hosts get a clear skip, not a fake
pass).
"""

import os
import platform
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUBJECT_SOURCE = os.path.join(ROOT, "tools", "native_probe_subject.c")
CONTROL_PATH = os.path.join(tempfile.gettempdir(), "squalr-native-probe.control")
PASS_MARKER = "Squalr native-read: PASS"


def find_omega(explicit):
    if explicit:
        return explicit
    candidate = os.path.join(ROOT, "..", "..", "..", "target", "release", "omega")
    if os.path.isfile(candidate):
        return os.path.abspath(candidate)
    found = shutil.which("omega")
    if found:
        return found
    sys.exit("no omega binary: pass --omega or build target/release/omega")


def find_cc():
    for name in ("cc", "gcc", "clang"):
        found = shutil.which(name)
        if found:
            return found
    sys.exit("no C compiler (cc/gcc/clang) on PATH")


def main():
    omega = find_omega(sys.argv[sys.argv.index("--omega") + 1]
                       if "--omega" in sys.argv else None)
    if platform.system() != "Linux":
        sys.exit("native probe requires Linux/procfs; skipped on this host")
    compiler = find_cc()

    if os.path.exists(CONTROL_PATH):
        os.remove(CONTROL_PATH)

    with tempfile.TemporaryDirectory() as work:
        subject = os.path.join(work, "native_probe_subject")
        build = subprocess.run(
            [compiler, "-O0", "-o", subject, SUBJECT_SOURCE],
            capture_output=True, text=True)
        if build.returncode != 0:
            sys.stderr.write(build.stderr)
            sys.exit("subject compile failed")

        child = subprocess.Popen(
            [subject], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, text=True)
        try:
            ready = child.stdout.readline().split()
            if len(ready) != 4 or ready[0] != "READY":
                sys.exit(f"child did not announce itself: {ready!r}")
            pid, page, guard = ready[1], ready[2], ready[3]
            print(f"child pid={pid} page={page} guard={guard}")

            with open(CONTROL_PATH, "w", encoding="ascii") as control:
                control.write(f"{pid} {page} {guard}\n")

            run = subprocess.run(
                [omega, "run", "--keep",
                 os.path.join(ROOT, "squalr-tests", "main.omg")],
                cwd=ROOT, capture_output=True, text=True, timeout=180)
            sys.stdout.write(run.stdout)
            sys.stderr.write(run.stderr)
            ok = (run.returncode == 0 and PASS_MARKER in run.stdout)
            if not ok:
                sys.exit(1)
            print("native probe driver: PASS")
        finally:
            if child.stdin:
                child.stdin.close()
            child.terminate()
            child.wait(timeout=10)
            if os.path.exists(CONTROL_PATH):
                os.remove(CONTROL_PATH)


if __name__ == "__main__":
    main()
