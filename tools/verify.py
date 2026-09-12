"""Invoke real Omega products; setup checks never stand in for compilation."""

import argparse
import json
import platform
from pathlib import Path
import subprocess
import sys
import time
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def check_layout(root, upstream=None):
    manifest = json.loads((root / "upstream.json").read_text(encoding="utf-8"))
    packages = manifest["packages"]
    paths = {package["path"] for package in packages}
    names = {package["name"] for package in packages}
    if len(paths) != len(packages) or len(names) != len(packages):
        raise ValueError("duplicate package path/name in reference map")
    if not (root / "build.omg").is_file():
        raise ValueError("missing root workspace build.omg")
    for package in packages:
        package_root = (root / package["path"]).resolve()
        if not package_root.is_relative_to(root.resolve()):
            raise ValueError("package escapes repository")
        if not (package_root / "build.omg").is_file():
            raise ValueError(f"missing build.omg for {package['name']}")
        for dependency in package["dependencies"]:
            destination = (package_root / dependency["path"]).resolve()
            if not destination.is_relative_to(root.resolve()):
                raise ValueError("dependency escapes repository")
            relative = destination.relative_to(root.resolve()).as_posix()
            if relative not in paths:
                raise ValueError(f"missing internal dependency: {relative}")
    if upstream:
        revision = subprocess.check_output(
            ["git", "-C", str(upstream), "rev-parse", "HEAD"], text=True
        ).strip()
        if revision != manifest["revision"]:
            raise ValueError(f"Rust reference revision differs: {revision}")
        dirty = subprocess.check_output(
            ["git", "-C", str(upstream), "status", "--porcelain"], text=True
        )
        if dirty.strip():
            raise ValueError("Rust reference has uncommitted changes")
        workspace = tomllib.loads((upstream / "Cargo.toml").read_text(encoding="utf-8"))
        expected = set(workspace["workspace"]["members"]) - set(manifest["excluded_frontends"])
        if paths != expected:
            raise ValueError("headless workspace member mapping differs from Rust")
        for package in packages:
            cargo = tomllib.loads((upstream / package["path"] / "Cargo.toml").read_text(encoding="utf-8"))
            dependencies = [
                {"name": name, "path": value["path"]}
                for name, value in cargo.get("dependencies", {}).items()
                if isinstance(value, dict) and "path" in value
            ]
            if cargo["package"]["name"] != package["name"] or dependencies != package["dependencies"]:
                raise ValueError(f"package mapping differs: {package['path']}")
    return len(packages), sum(len(package["dependencies"]) for package in packages)


def compiler_command(mode, executable, application, target, report):
    if mode == "audit":
        command = [executable, "audit", "packages", "--project", str(application), "--details"]
    elif mode == "check":
        command = [executable, "--check", "--build-dir", str(report / "compiler"), str(application / "main.omg")]
    else:
        command = [executable, "run", "--keep", str(application / "main.omg")]
    if target:
        command += ["--target", target]
    return command


def run_compiler(command, report, mode, timeout, application):
    report.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    try:
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True,
                                encoding="utf-8", errors="replace", timeout=timeout)
        status, stdout, stderr = result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired as error:
        status = 124
        stdout = error.stdout or b""
        stderr = error.stderr or b""
        if isinstance(stdout, bytes):
            stdout = stdout.decode("utf-8", errors="replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode("utf-8", errors="replace")
        stderr += "\nCompiler invocation timed out; no source verdict established.\n"
    except OSError as error:
        status, stdout, stderr = 127, "", str(error) + "\n"
    if mode == "native" and application == "squalr-tests" and status == 0:
        if "Squalr geometry: PASS" not in stdout:
            status = 1
            stderr += "\nNative execution did not produce the headless success marker.\n"
    (report / "stdout.txt").write_text(stdout, encoding="utf-8")
    (report / "stderr.txt").write_text(stderr, encoding="utf-8")
    record = {"command": command, "mode": mode, "exit_code": status,
              "seconds": time.monotonic() - started, "host": platform.platform()}
    (report / "result.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(stdout, end="")
    print(stderr, end="", file=sys.stderr)
    print(f"{mode}: exit {status}; evidence: {report}")
    return status


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["layout", "audit", "check", "native"])
    parser.add_argument("--omega", help="Path to the real Omega executable, or its PATH name")
    parser.add_argument("--upstream", type=Path, help="Optional clean, pinned Rust checkout for layout comparison")
    packages = json.loads((ROOT / "upstream.json").read_text(encoding="utf-8"))["packages"]
    parser.add_argument("--project", choices=[package["path"] for package in packages], default="squalr-tests")
    parser.add_argument("--target")
    parser.add_argument("--timeout", type=int, default=180)
    arguments = parser.parse_args()
    if arguments.timeout <= 0:
        parser.error("timeout must be positive")
    if arguments.mode == "layout":
        try:
            count, edges = check_layout(ROOT, arguments.upstream)
        except (OSError, ValueError, subprocess.CalledProcessError) as error:
            print(error, file=sys.stderr)
            return 1
        print(f"Setup: {count} package builds, {edges} internal reference edges. Not a compiler or parity verdict.")
        return 0
    if not arguments.omega:
        parser.error("--omega is required; no alternate evaluator is supplied")
    application = ROOT / arguments.project
    selected = next(package for package in packages if package["path"] == arguments.project)
    if arguments.mode == "native" and selected["role"] != "application":
        parser.error("native execution requires an application, not a library package")
    if arguments.mode != "audit" and not (application / "main.omg").is_file():
        print(f"Unported application entry: {application / 'main.omg'}", file=sys.stderr)
        return 2
    executable = arguments.omega
    if Path(executable).is_file():
        executable = str(Path(executable).resolve())
    report = ROOT / "build" / "verification" / arguments.project / arguments.mode
    command = compiler_command(arguments.mode, executable, application, arguments.target, report)
    return run_compiler(command, report, arguments.mode, arguments.timeout, arguments.project)


if __name__ == "__main__":
    sys.exit(main())
