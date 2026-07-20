#!/usr/bin/env python3
"""Validate and preflight the three-track curriculum navigation contract.

The registry is data, not generated learning material.  This program never installs
or upgrades tools and never checks out a learner's working tree.
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import re
import shutil
import subprocess
import sys
import unicodedata
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import quote, unquote


TRACK_COUNTS = {"42": 13, "frontend": 5, "backend": 12}
VALID_TRACKS = frozenset(TRACK_COUNTS)
REGISTRY_VERSION = 4
DISPLAY_SEQUENCES = {
    "42": (
        "linux-foundation",
        "c-foundation",
        "format-printer",
        "buffered-line-reader",
        "signal-message-bus",
        "thread-dining",
        "small-shell",
        "stack-sort",
        "cpp-foundation",
        "stl-container",
        "irc-relay-server",
        "container-stack",
        "web-boundary-inspector",
        "pong-pong",
        "42-incident",
    ),
    "frontend": (
        "frontend-foundations-training",
        "frontend-delivery-training",
        "cloud-launch-training",
        "frontend-reliability-training",
        "frontend-transfer",
        "portfolio-site",
        "web-production-regression",
        "frontend-complete",
    ),
    "backend": (
        "backend-foundations-training",
        "backend-delivery-training",
        "backend-reliability-training",
        "sportsbook-shared-protocol",
        "sportsbook-wallet-service",
        "sportsbook-risk-service",
        "sportsbook-odds-feed-service",
        "sportsbook-betting-service",
        "sportsbook-settlement-service",
        "sportsbook-gateway",
        "sportsbook-admin-api",
        "sportsbook-orchestration",
        "backend-incident",
        "backend-complete",
    ),
}


def _linear_edges(
    sequence: tuple[str, ...], first_prev: tuple[str, ...]
) -> dict[str, tuple[tuple[str, ...], tuple[str, ...]]]:
    edges: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {}
    for index, node_id in enumerate(sequence):
        prev_ids = first_prev if index == 0 else (sequence[index - 1],)
        next_ids = () if index == len(sequence) - 1 else (sequence[index + 1],)
        edges[node_id] = (prev_ids, next_ids)
    return edges


CANONICAL_EDGES = {
    "linux-foundation": (
        (),
        ("c-foundation", "cpp-foundation", "container-stack"),
    ),
    "c-foundation": (("linux-foundation",), ("format-printer",)),
    "format-printer": (("c-foundation",), ("buffered-line-reader",)),
    "buffered-line-reader": (("format-printer",), ("signal-message-bus",)),
    "signal-message-bus": (("buffered-line-reader",), ("thread-dining",)),
    "thread-dining": (("signal-message-bus",), ("small-shell",)),
    "small-shell": (("thread-dining",), ("stack-sort",)),
    "stack-sort": (("small-shell",), ("web-boundary-inspector",)),
    "cpp-foundation": (("linux-foundation",), ("stl-container",)),
    "stl-container": (("cpp-foundation",), ("irc-relay-server",)),
    "irc-relay-server": (("stl-container",), ("web-boundary-inspector",)),
    "container-stack": (("linux-foundation",), ("web-boundary-inspector",)),
    "web-boundary-inspector": (
        ("stack-sort", "irc-relay-server", "container-stack"),
        ("pong-pong",),
    ),
    "pong-pong": (("web-boundary-inspector",), ("42-incident",)),
    "42-incident": (
        ("pong-pong",),
        ("frontend-foundations-training", "backend-foundations-training"),
    ),
}
CANONICAL_EDGES.update(
    _linear_edges(
        DISPLAY_SEQUENCES["frontend"],
        ("42-incident",),
    )
)
CANONICAL_EDGES.update(
    _linear_edges(
        DISPLAY_SEQUENCES["backend"],
        ("42-incident",),
    )
)
NO_PROJECT_NOTES = {
    "c-foundation",
    "buffered-line-reader",
    "cpp-foundation",
    "web-boundary-inspector",
    "portfolio-site",
    "sportsbook-shared-protocol",
}
EXTENDED_SOURCE_WINDOWS = frozenset(
    {"c-foundation", "buffered-line-reader", "cpp-foundation"}
)
REQUIRED_MAIN_PATHS = {
    project_id: ("README.md", "DESIGN.md")
    for project_id in EXTENDED_SOURCE_WINDOWS
}
UNCHANGED_NAVIGATION_RELEASES = {
    "c-foundation": {
        "release": "v1.0.0",
        "main": "6ae8f96e9f2617501a4e260a10025a401aee7e41",
        "tag": "bbb88a11dd7051720be6a5503c40486ac409c3dc",
    },
    "format-printer": {
        "release": "v1.0.0",
        "main": "be4966f3c1d176453a34b609036ef4998fa8b022",
        "tag": "fe7a0d79cb9733f4f6871e5164a305907cd7b78e",
    },
    "signal-message-bus": {
        "release": "v1.0.0",
        "main": "ed859ce08c0d84154c21be6ffd6cdb1ea1c353c3",
        "tag": "7563b6325e6c1a31bc63dbf22b935bb155e0e434",
    },
    "thread-dining": {
        "release": "v1.0.0",
        "main": "94ccaa4085af3decfd6d7bba2ff0b879954947e5",
        "tag": "983bb1f4ce52ce33feb68955d9c0788670b12fb4",
    },
    "small-shell": {
        "release": "v1.0.0",
        "main": "0fb1f6bf4825890f7b657ce5de918aed52a8318d",
        "tag": "3e7164817b3883783c80c6a1ced90531faf85efe",
    },
    "buffered-line-reader": {
        "release": "v1.0.0",
        "main": "7ec26185957209a0bd2216cd179dc630e1c3297f",
        "tag": "3924afef984ca0d7424721a2835264577efcc2e0",
    },
    "stack-sort": {
        "release": "v1.0.0",
        "main": "51325493a5e0e10f72dcfc04079d3b4f2c96488e",
        "tag": "dc08a9be3ec27a5096be753ef7f7126ce8b713e9",
    },
    "cpp-foundation": {
        "release": "v1.0.0",
        "main": "13e353061f5c4a95b4a2d89b69fc62ef7c405e47",
        "tag": "062f666f25a07a5d264d00590c15fbe5b657e669",
    },
    "stl-container": {
        "release": "v1.0.0",
        "main": "6f875e0677674d86145188d8558e3cf56b61c9cb",
        "tag": "d6ff0b12322c9221d47f308097dc4b4980f3b483",
    },
    "irc-relay-server": {
        "release": "v1.0.0",
        "main": "b69347797e81c803397ced1ba23042216caa74fd",
        "tag": "7c8fe460cd8e4e01ac5c82a5e6e987be7cce58fb",
    },
    "container-stack": {
        "release": "v1.0.0",
        "main": "bd498c17f255681cbc57e598e09a876abb2c0a2e",
        "tag": "dd878d65945e32c9a499b175643a1ae39880cb3a",
    },
    "web-boundary-inspector": {
        "release": "v1.0.0",
        "main": "cf57ffeb652288548c351209a278d4907f0b2f95",
        "tag": "5ee7967b12c27a259d1a64f4c72de67f524c46c7",
    },
    "pong-pong": {
        "release": "v1.0.0",
        "main": "091a9326c7efe94f59b7e6db4dd841eb2bb228cd",
        "tag": "22f9d6e3b646b6e76cfa545497c9f14e5f0bfebd",
    },
    "cloud-launch-training": {
        "release": "cloud-launch-v1.0.1",
        "main": "480e18b5b47cccf5fe0f38e6c5811fde567bdfe4",
        "tag": "20857ee56df971d3a1b5eb7a8cf181377dd971ef",
    },
    "sportsbook-orchestration": {
        "release": "orchestration-v1",
        "main": "564a83a57bd834870303688adb96450639c13bd2",
        "tag": "51f8698a2123e9b5ce8052edad42a17405e8b3bb",
    },
}
PROJECT_FIELDS = (
    "id",
    "track",
    "repo",
    "release",
    "learning",
    "doc",
    "anchor",
    "practice",
    "answer",
    "sourceWindow",
    "prev",
    "next",
)
PRACTICE_POLICY = {
    "mastery": "one-representative-plus-card-gate",
    "remaining": "optional-deepening",
    "historical_gate": "selected-practice-parent",
    "release_gate": "clean-release-tree",
    "wrapper_scope": "document-box-canonical",
}
LOCAL_NODE_FIELDS = ("id", "track", "doc", "anchor", "prev", "next")
OVERLAY_FIELDS = (
    "id",
    "track",
    "doc",
    "anchor",
    "entry_after",
    "required_prior",
    "outcome",
    "grants_mastery",
    "resume_at",
    "preflight_projects",
    "selections",
    "portfolio",
)
FRONTEND_APPLICATION_OVERLAY_ID = "frontend-application-bridge"
FRONTEND_APPLICATION_PREFLIGHT = (
    "web-boundary-inspector",
    "frontend-foundations-training",
    "frontend-reliability-training",
    "portfolio-site",
)
FRONTEND_APPLICATION_PRACTICES = {
    "frontend-foundations-training": (
        "docs/practice/041.md",
    ),
    "frontend-reliability-training": (
        "docs/practice/010.md",
        "docs/practice/011.md",
        "docs/practice/013.md",
        "docs/practice/036.md",
        "docs/practice/037.md",
        "docs/practice/039.md",
        "docs/practice/043.md",
        "docs/practice/044.md",
        "docs/practice/046.md",
        "docs/practice/047.md",
        "docs/practice/108.md",
        "docs/practice/109.md",
        "docs/practice/110.md",
        "docs/practice/112.md",
    ),
}
FRONTEND_APPLICATION_ANSWER_MAPPINGS = {
    "frontend-foundations-training": "docs/commits/README.md",
    "frontend-reliability-training": "docs/commits-codex-5.6/README.md",
}
FRONTEND_APPLICATION_PORTFOLIO = {
    "project": "portfolio-site",
    "template": "template-v3.0.1",
    "release": "portfolio-v3.0.1",
    "learning": "learning/portfolio-v3.0.1",
}
MIGRATED_42_PROJECTS = frozenset(
    {
        "c-foundation",
        "format-printer",
        "buffered-line-reader",
        "signal-message-bus",
        "thread-dining",
        "small-shell",
        "stack-sort",
        "cpp-foundation",
        "stl-container",
        "irc-relay-server",
        "container-stack",
        "web-boundary-inspector",
        "pong-pong",
    }
)
MIGRATED_FRONTEND_PROJECTS = frozenset(
    {"frontend-foundations-training", "frontend-delivery-training"}
)
STRICT_TOPOLOGY_PROJECTS = (
    EXTENDED_SOURCE_WINDOWS | MIGRATED_42_PROJECTS | MIGRATED_FRONTEND_PROJECTS
)
FROZEN_MONOLITHIC_LEARNING = {
    "format-printer": {
        "release": "v1.0.0",
        "main": "be4966f3c1d176453a34b609036ef4998fa8b022",
        "tag": "fe7a0d79cb9733f4f6871e5164a305907cd7b78e",
        "learning_ref": "learning/current",
        "learning": "7a271026d6afbec22e8e32c6cfeaf7ac5ae1d777",
    }
}
CURRENT_42_RELEASE = "v1.0.0"
CURRENT_42_LEARNING = "learning/current"
CURRENT_42_PRACTICE = "docs/practice/README.md"
CURRENT_42_ANSWER = "docs/commits/README.md"
LEGACY_42_RELEASE = "codex-5.7"
LEGACY_42_LEARNING = "learning/codex-5.7"
LEGACY_42_PRACTICE = "docs/practice-codex-5.7/README.md"
LEGACY_42_ANSWER = "docs/commits-codex-5.7/README.md"
PROJECT_SETUP = {
    "c-foundation": "make check",
    "format-printer": "make && make test",
    "buffered-line-reader": "make check",
    "signal-message-bus": "make && make test (repeat; include long/abandoned sender cases)",
    "thread-dining": "make && make test (repeat the timing scenarios)",
    "small-shell": "make && make test",
    "stack-sort": "make && make test",
    "cpp-foundation": "make check",
    "stl-container": "make && make test (also run the strict C++98 compile gate)",
    "irc-relay-server": "make && make test && make smoke",
    "container-stack": "make test && make ENV_FILE=.env.example config; then prepare secret files and run make ENV_FILE=.env.example up && make smoke && make ENV_FILE=.env.example down",
    "web-boundary-inspector": "pnpm --dir browser-platform install --frozen-lockfile; pnpm --dir browser-platform exec playwright install chromium firefox webkit; make check",
    "pong-pong": "pnpm install --frozen-lockfile; make typecheck && make test && make build && make e2e",
    "frontend-foundations-training": "pnpm install --frozen-lockfile; pnpm exec playwright install chromium; make check-repo && make build && make test-e2e",
    "frontend-delivery-training": "pnpm install --frozen-lockfile; pnpm exec playwright install chromium; make check",
    "cloud-launch-training": "npm ci; npx playwright install; make check",
    "frontend-reliability-training": "pnpm install --frozen-lockfile; pnpm exec playwright install chromium; make lint && make typecheck && make test && make build && make test-e2e",
    "portfolio-site": "npm ci; npx playwright install; npm test && npm run lint && npm run typecheck && npm run build && npm run test:e2e",
    "backend-foundations-training": "make check",
    "backend-delivery-training": "make test && make build-spring && make build-go && make check-docs",
    "backend-reliability-training": "make check",
    "sportsbook-shared-protocol": "./mvnw verify",
    "sportsbook-wallet-service": "./mvnw verify",
    "sportsbook-risk-service": "./mvnw verify (correctness only; the 1,000 RPS qualification remains RED)",
    "sportsbook-odds-feed-service": "./mvnw verify",
    "sportsbook-betting-service": "./mvnw verify",
    "sportsbook-settlement-service": "./mvnw verify",
    "sportsbook-gateway": "./mvnw verify",
    "sportsbook-admin-api": "./mvnw verify",
    "sportsbook-orchestration": "scripts/validate-release-manifest.sh; scripts/build-all.sh; e2e/run-e2e.sh",
}


class CurriculumError(RuntimeError):
    """Raised for a malformed or disconnected curriculum."""


@dataclass(frozen=True)
class Result:
    level: str
    name: str
    detail: str


def _run(
    command: list[str], timeout: int = 20, cwd: Path | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )


def _ids(value: Any) -> list[str]:
    if value is None or value == "":
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return value
    raise CurriculumError("prev/next must be a string, a string list, or null")


def _paths(value: Any, field: str) -> list[str]:
    values = [value] if isinstance(value, str) else value
    if not isinstance(values, list) or not values or not all(
        isinstance(item, str) and item for item in values
    ):
        raise CurriculumError(f"{field} must be a path or a non-empty path list")
    return values


def load_registry(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise CurriculumError(f"registry not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise CurriculumError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise CurriculumError("registry root must be an object")
    return data


def _all_nodes(data: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    groups = (
        ("project", data.get("projects", [])),
        ("prerequisite", data.get("prerequisites", [])),
        ("assessment", data.get("assessments", [])),
        ("completion", data.get("completions", [])),
    )
    nodes: list[tuple[str, dict[str, Any]]] = []
    for kind, values in groups:
        if not isinstance(values, list):
            raise CurriculumError(f"{kind}s must be a list")
        for value in values:
            if not isinstance(value, dict):
                raise CurriculumError(f"every {kind} must be an object")
            nodes.append((kind, value))
    return nodes


def _safe_relative_path(value: str, field: str) -> None:
    path = Path(value)
    if (
        not value
        or path.is_absolute()
        or ".." in path.parts
        or value.startswith(("http://", "https://"))
    ):
        raise CurriculumError(f"{field} must be a safe repository-relative path: {value}")


def _github_slug(heading: str) -> str:
    value = html.unescape(heading.strip().rstrip("#").rstrip())
    value = re.sub(r"!\[([^]]*)\]\([^)]*\)", r"\1", value)
    value = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", value)
    value = value.replace("`", "").replace("*", "").lower()
    output: list[str] = []
    for character in value:
        category = unicodedata.category(character)
        if character in {"-", "_"} or character.isspace():
            output.append(character)
        elif not category.startswith(("P", "S", "C")):
            output.append(character)
    return "".join(output).strip().replace(" ", "-")


def _document_anchor_count(text: str, anchor: str) -> int:
    html_anchor = re.compile(
        rf"<(?:a|span)\s+[^>]*\bid=[\"']{re.escape(anchor)}[\"'][^>]*>",
        re.IGNORECASE,
    )
    count = len(html_anchor.findall(text))
    for line in text.splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if match and _github_slug(match.group(1)) == anchor:
            count += 1
    return count


def _anchor_section(text: str, anchor: str) -> str:
    marker = re.search(
        rf"<(?:a|span)\s+[^>]*\bid=[\"']{re.escape(anchor)}[\"'][^>]*>",
        text,
        re.IGNORECASE,
    )
    if not marker:
        return ""
    next_marker = re.search(
        r"<(?:a|span)\s+[^>]*\bid=[\"']stage-[^\"']+[\"'][^>]*>",
        text[marker.end() :],
        re.IGNORECASE,
    )
    end = marker.end() + next_marker.start() if next_marker else len(text)
    return text[marker.end() : end]


def _local_markdown_link_errors(root: Path) -> list[str]:
    errors: list[str] = []
    root = root.resolve()
    root_resolved = root
    link_pattern = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
    for document in sorted(root.rglob("*.md")):
        if ".git" in document.parts:
            continue
        text = document.read_text(encoding="utf-8")
        for raw_target in link_pattern.findall(text):
            target = raw_target.strip()
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            else:
                target = target.split(maxsplit=1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            path_part, separator, fragment = target.partition("#")
            unresolved = document if not path_part else document.parent / unquote(path_part)
            resolved = unresolved.resolve()
            try:
                resolved.relative_to(root_resolved)
            except ValueError:
                errors.append(
                    f"{document.relative_to(root)}: local link escapes repository {target}"
                )
                continue
            if resolved.is_dir():
                resolved = resolved / "README.md"
            if not resolved.is_file():
                errors.append(
                    f"{document.relative_to(root)}: missing local link target {target}"
                )
                continue
            if separator and fragment:
                anchor_count = _document_anchor_count(
                    resolved.read_text(encoding="utf-8"), unquote(fragment)
                )
                if anchor_count != 1:
                    errors.append(
                        f"{document.relative_to(root)}: anchor #{fragment} must appear "
                        f"exactly once in {resolved.relative_to(root)}, found {anchor_count}"
                    )
    return errors


def _validate_overlays(
    data: dict[str, Any],
    root: Path,
    node_by_id: dict[str, dict[str, Any]],
) -> list[str]:
    """Validate optional learning routes without adding them to the mastery graph."""

    errors: list[str] = []
    overlays = data.get("overlays")
    if not isinstance(overlays, list):
        return ["overlays must be a list"]
    if len(overlays) != 1:
        errors.append(f"overlays must contain exactly one entry, found {len(overlays)}")
        return errors
    overlay = overlays[0]
    if not isinstance(overlay, dict):
        return ["every overlay must be an object"]

    missing = [field for field in OVERLAY_FIELDS if field not in overlay]
    extra = sorted(set(overlay) - set(OVERLAY_FIELDS))
    if missing:
        errors.append("frontend application overlay missing: " + ", ".join(missing))
    if extra:
        errors.append("frontend application overlay has unknown fields: " + ", ".join(extra))
    if missing:
        return errors

    overlay_id = overlay.get("id")
    if overlay_id != FRONTEND_APPLICATION_OVERLAY_ID:
        errors.append(
            "overlay id must be " + FRONTEND_APPLICATION_OVERLAY_ID
        )
    if overlay_id in node_by_id:
        errors.append(f"overlay id collides with canonical node: {overlay_id}")
    if overlay.get("track") != "frontend":
        errors.append("frontend application overlay track must be frontend")
    if overlay.get("entry_after") != "42-incident":
        errors.append("frontend application overlay must enter after 42-incident")
    if overlay.get("required_prior") != [
        "web-boundary-inspector",
        "42-incident",
    ]:
        errors.append(
            "frontend application overlay must require the current web boundary gate "
            "and 42 incident"
        )
    if overlay.get("outcome") != "frontend-application-readiness":
        errors.append(
            "frontend application overlay outcome must be "
            "frontend-application-readiness"
        )
    if overlay.get("grants_mastery") is not False:
        errors.append("frontend application overlay must set grants_mastery=false")
    if overlay.get("resume_at") != "frontend-delivery-training":
        errors.append(
            "frontend application overlay must resume the canonical track at "
            "frontend-delivery-training"
        )
    preflight_projects = overlay.get("preflight_projects")
    if not isinstance(preflight_projects, list) or not all(
        isinstance(project_id, str) for project_id in preflight_projects
    ):
        errors.append(
            "frontend application overlay preflight_projects must be a string list"
        )
        preflight_projects = []
    if preflight_projects != list(FRONTEND_APPLICATION_PREFLIGHT):
        errors.append(
            "frontend application overlay preflight_projects must be the current "
            "Web Boundary, Foundations, Reliability and Portfolio projects"
        )
    for project_id in preflight_projects:
        if project_id not in node_by_id or "repo" not in node_by_id[project_id]:
            errors.append(
                f"frontend application overlay references unknown project {project_id}"
            )

    selections = overlay.get("selections")
    if not isinstance(selections, list):
        errors.append("frontend application overlay selections must be a list")
        selections = []
    selection_by_project: dict[str, dict[str, Any]] = {}
    for selection in selections:
        if not isinstance(selection, dict):
            errors.append("every frontend application selection must be an object")
            continue
        if set(selection) != {"project", "learning", "practice_paths"}:
            errors.append(
                "frontend application selections must contain exactly project, "
                "learning and practice_paths"
            )
            continue
        project_id = selection.get("project")
        if not isinstance(project_id, str):
            errors.append("frontend application selection project must be a string")
            continue
        if project_id in selection_by_project:
            errors.append(
                f"frontend application selection repeats project {project_id}"
            )
            continue
        selection_by_project[project_id] = selection
        project = node_by_id.get(project_id)
        if not project or "repo" not in project:
            errors.append(
                f"frontend application selection references unknown project {project_id}"
            )
            continue
        if selection.get("learning") != project.get("learning"):
            errors.append(
                f"frontend application selection {project_id} must use current learning "
                f"ref {project.get('learning')}"
            )
        paths = selection.get("practice_paths")
        if not isinstance(paths, list) or not paths or not all(
            isinstance(path, str) and path for path in paths
        ):
            errors.append(
                f"frontend application selection {project_id} practice_paths must be "
                "a non-empty string list"
            )
            continue
        if len(paths) != len(set(paths)):
            errors.append(
                f"frontend application selection {project_id} repeats a practice path"
            )
        for path in paths:
            try:
                _safe_relative_path(path, f"overlay.{project_id}.practice_paths")
            except CurriculumError as exc:
                errors.append(str(exc))
            if not path.startswith("docs/practice/") or not path.endswith(".md"):
                errors.append(
                    f"frontend application selection {project_id} must use exact "
                    f"docs/practice/*.md paths: {path}"
                )

    if set(selection_by_project) != set(FRONTEND_APPLICATION_PRACTICES):
        errors.append(
            "frontend application selections must contain exactly Foundations and "
            "Reliability"
        )
    for project_id, expected_paths in FRONTEND_APPLICATION_PRACTICES.items():
        selection = selection_by_project.get(project_id)
        if selection and selection.get("practice_paths") != list(expected_paths):
            errors.append(
                f"frontend application selection {project_id} practice paths do not "
                "match the reviewed hands-on scope"
            )

    portfolio = overlay.get("portfolio")
    if portfolio != FRONTEND_APPLICATION_PORTFOLIO:
        errors.append(
            "frontend application overlay portfolio must pin portfolio-site "
            "template-v3.0.1, portfolio-v3.0.1 and learning/portfolio-v3.0.1"
        )
    portfolio_project = node_by_id.get("portfolio-site")
    if portfolio_project:
        for field in ("template", "release", "learning"):
            if FRONTEND_APPLICATION_PORTFOLIO[field] != portfolio_project.get(field):
                errors.append(
                    f"frontend application portfolio {field} must match the registered "
                    "portfolio-site project"
                )

    doc = overlay.get("doc")
    anchor = overlay.get("anchor")
    section: str | None = None
    if not isinstance(doc, str):
        errors.append("frontend application overlay doc must be a path")
    else:
        try:
            _safe_relative_path(doc, "overlay.doc")
            doc_path = root / doc
            if not doc_path.is_file():
                errors.append(f"frontend application overlay document not found: {doc}")
            elif not isinstance(anchor, str) or not anchor:
                errors.append("frontend application overlay anchor must be non-empty")
            else:
                text = doc_path.read_text(encoding="utf-8")
                count = _document_anchor_count(text, anchor)
                if count != 1:
                    errors.append(
                        f"frontend application overlay anchor #{anchor} must appear "
                        f"exactly once in {doc}, found {count}"
                    )
                section = _anchor_section(text, anchor)
        except CurriculumError as exc:
            errors.append(str(exc))

    owner = str(data.get("owner", "woopinbell"))
    if section is not None:
        required_markers = (
            "`frontend-application-readiness`",
            "`grants_mastery=false`",
            "make preflight ROUTE=frontend-application-bridge",
            "](42.md#stage-42-incident)",
            "](frontend.md#stage-frontend-delivery-training)",
        )
        for marker in required_markers:
            if marker not in section:
                errors.append(
                    "frontend application overlay document is missing marker " + marker
                )
        for stage in DISPLAY_SEQUENCES["42"]:
            card_marker = f"](42.md#stage-{stage})"
            if card_marker not in section:
                errors.append(
                    f"frontend application overlay document is missing 42 stage {stage}"
                )
            if stage == "42-incident":
                central_marker = (
                    f"https://github.com/{owner}/central-notes/blob/main/"
                    "assessments/42-incident/README.md#assessment-42-incident"
                )
            else:
                central_marker = (
                    f"https://github.com/{owner}/central-notes/blob/main/"
                    f"TRACK_SEQUENCE.md#stage-{stage}"
                )
            if f"]({central_marker})" not in section:
                errors.append(
                    f"frontend application overlay document is missing Central handoff "
                    f"for 42 stage {stage}"
                )
        for project_id, expected_paths in FRONTEND_APPLICATION_PRACTICES.items():
            project = node_by_id.get(project_id, {})
            learning = project.get("learning", "")
            repo = project.get("repo", project_id)
            answer = project.get("answer", "")
            answer_target = (
                f"https://github.com/{owner}/{repo}/blob/{learning}/{answer}"
            )
            if f"]({answer_target})" not in section:
                errors.append(
                    f"frontend application overlay document is missing current "
                    f"answer ledger {project_id}:{answer}"
                )
            for path in expected_paths:
                target = (
                    f"https://github.com/{owner}/{repo}/blob/{learning}/{path}"
                )
                if f"]({target})" not in section:
                    errors.append(
                        f"frontend application overlay document is missing selected "
                        f"practice {project_id}:{path}"
                    )
        portfolio_url = f"https://github.com/{owner}/portfolio-site"
        if f"]({portfolio_url})" not in section:
            errors.append(
                "frontend application overlay document is missing portfolio-site link"
            )
        for token in (
            "template-v3.0.1",
            "portfolio-v3.0.1",
            "learning/portfolio-v3.0.1",
        ):
            if f"`{token}`" not in section:
                errors.append(
                    f"frontend application overlay document is missing portfolio ref `{token}`"
                )

    overlay_link = "](frontend-fast-track.md#route-frontend-application-bridge)"
    for source in (
        root / "tracks/README.md",
        root / "tracks/42.md",
        root / "tracks/frontend.md",
    ):
        if not source.is_file():
            continue
        source_text = source.read_text(encoding="utf-8")
        if source.name == "42.md":
            source_text = _anchor_section(source_text, "stage-42-incident")
        if overlay_link not in source_text:
            errors.append(
                f"{source.relative_to(root)} is missing the frontend application overlay link"
            )
    return errors


def validate_registry(data: dict[str, Any], root: Path) -> list[str]:
    errors: list[str] = _local_markdown_link_errors(root)

    if data.get("version") != REGISTRY_VERSION:
        errors.append(f"registry version must be {REGISTRY_VERSION}")

    def record(action: Any) -> None:
        try:
            action()
        except CurriculumError as exc:
            errors.append(str(exc))

    projects = data.get("projects", [])
    if not isinstance(projects, list):
        return ["projects must be a list"]
    if len(projects) != 30:
        errors.append(f"projects must contain exactly 30 entries, found {len(projects)}")

    nodes_with_kind: list[tuple[str, dict[str, Any]]] = []
    try:
        nodes_with_kind = _all_nodes(data)
    except CurriculumError as exc:
        errors.append(str(exc))
        return errors

    node_by_id: dict[str, dict[str, Any]] = {}
    kind_by_id: dict[str, str] = {}
    for kind, node in nodes_with_kind:
        required = PROJECT_FIELDS if kind == "project" else LOCAL_NODE_FIELDS
        missing = [field for field in required if field not in node]
        if missing:
            errors.append(
                f"{kind} {node.get('id', '<unknown>')} missing: {', '.join(missing)}"
            )
            continue
        node_id = node["id"]
        if not isinstance(node_id, str) or not node_id:
            errors.append(f"{kind} id must be a non-empty string")
            continue
        if node_id in node_by_id:
            errors.append(f"duplicate curriculum id: {node_id}")
            continue
        node_by_id[node_id] = node
        kind_by_id[node_id] = kind
        if node.get("track") not in VALID_TRACKS:
            errors.append(f"{node_id}: invalid track {node.get('track')!r}")

        for edge in ("prev", "next"):
            record(lambda node=node, edge=edge: _ids(node[edge]))

        doc = node.get("doc")
        if not isinstance(doc, str):
            errors.append(f"{node_id}: doc must be a path")
        else:
            try:
                _safe_relative_path(doc, f"{node_id}.doc")
                doc_path = root / doc
                if not doc_path.is_file():
                    errors.append(f"{node_id}: document not found: {doc}")
                else:
                    anchor = node.get("anchor")
                    if not isinstance(anchor, str) or not anchor:
                        errors.append(f"{node_id}: anchor must be non-empty")
                    else:
                        doc_text = doc_path.read_text(encoding="utf-8")
                        anchor_count = _document_anchor_count(doc_text, anchor)
                        if anchor_count != 1:
                            errors.append(
                                f"{node_id}: anchor #{anchor} must appear exactly once "
                                f"in {doc}, found {anchor_count}"
                            )
                        elif kind != "completion":
                            section = _anchor_section(doc_text, anchor)
                            card_markers = (
                                "**시작 조건:**",
                                "**먼저 읽을 것:**",
                                "**저장소와 학습 자료:**",
                                "**직접 해볼 것:**",
                                "**현재 완성본 확인:**",
                                "**완료 조건:**",
                                "**다음 과제:**",
                            )
                            for marker in card_markers:
                                if marker not in section:
                                    errors.append(
                                        f"{node_id}: current stage card is missing the "
                                        f"learner action marker {marker}"
                                    )
            except CurriculumError as exc:
                errors.append(str(exc))

        if kind == "project":
            repo = node.get("repo")
            release = node.get("release")
            learning = node.get("learning")
            if not isinstance(repo, str) or not re.fullmatch(r"[A-Za-z0-9_.-]+", repo):
                errors.append(f"{node_id}: invalid repository name")
            if not isinstance(release, str) or not release:
                errors.append(f"{node_id}: release must be non-empty")
            if not isinstance(learning, str) or not learning.startswith("learning/"):
                errors.append(f"{node_id}: learning must start with learning/")
            backlink_required = node.get("main_backlink", True)
            if not isinstance(backlink_required, bool):
                errors.append(f"{node_id}: main_backlink must be a boolean")
            elif node_id in UNCHANGED_NAVIGATION_RELEASES:
                if backlink_required:
                    errors.append(
                        f"{node_id}: unchanged navigation release must record "
                        "main_backlink=false"
                    )
            elif not backlink_required:
                errors.append(
                    f"{node_id}: only an explicitly unchanged navigation release may "
                    "omit the exact main README backlink"
                )
            for field in ("practice", "answer"):
                try:
                    for value in _paths(node.get(field), f"{node_id}.{field}"):
                        _safe_relative_path(value, f"{node_id}.{field}")
                except CurriculumError as exc:
                    errors.append(str(exc))
            try:
                main_paths = _paths(
                    node.get("main_paths", ["README.md"]),
                    f"{node_id}.main_paths",
                )
                if len(main_paths) != len(set(main_paths)):
                    errors.append(f"{node_id}: main_paths must not contain duplicates")
                required_main_paths = REQUIRED_MAIN_PATHS.get(node_id)
                if required_main_paths and tuple(main_paths) != required_main_paths:
                    errors.append(
                        f"{node_id}: main_paths must be exactly "
                        f"{', '.join(required_main_paths)}"
                    )
                for value in main_paths:
                    _safe_relative_path(value, f"{node_id}.main_paths")
            except CurriculumError as exc:
                errors.append(str(exc))

            window = node.get("sourceWindow")
            window_dates: dict[str, date] = {}
            if not isinstance(window, dict) or set(window) != {"start", "end"}:
                errors.append(
                    f"{node_id}: sourceWindow must contain exactly start and end"
                )
            else:
                for boundary in ("start", "end"):
                    value = window.get(boundary)
                    try:
                        if not isinstance(value, str) or not re.fullmatch(
                            r"\d{4}-\d{2}-\d{2}", value
                        ):
                            raise ValueError
                        window_dates[boundary] = date.fromisoformat(value)
                    except ValueError:
                        errors.append(
                            f"{node_id}: sourceWindow.{boundary} must be an ISO date"
                        )
                if set(window_dates) == {"start", "end"} and (
                    window_dates["start"] > window_dates["end"]
                ):
                    errors.append(f"{node_id}: sourceWindow start must not exceed end")

            extension = node.get("extensionEnd")
            if node_id in EXTENDED_SOURCE_WINDOWS:
                try:
                    if not isinstance(extension, str) or not re.fullmatch(
                        r"\d{4}-\d{2}-\d{2}", extension
                    ):
                        raise ValueError
                    extension_date = date.fromisoformat(extension)
                    if "end" in window_dates and extension_date <= window_dates["end"]:
                        errors.append(
                            f"{node_id}: extensionEnd must be later than sourceWindow.end"
                        )
                except ValueError:
                    errors.append(f"{node_id}: extensionEnd must be an ISO date")
            elif extension is not None:
                errors.append(
                    f"{node_id}: extensionEnd is only allowed for the three new projects"
                )
            if node.get("track") == "42":
                if node_id in MIGRATED_42_PROJECTS:
                    expected_42 = {
                        "release": CURRENT_42_RELEASE,
                        "learning": CURRENT_42_LEARNING,
                        "practice": CURRENT_42_PRACTICE,
                        "answer": CURRENT_42_ANSWER,
                    }
                else:
                    expected_42 = {
                        "release": LEGACY_42_RELEASE,
                        "learning": LEGACY_42_LEARNING,
                        "practice": LEGACY_42_PRACTICE,
                        "answer": LEGACY_42_ANSWER,
                    }
                for field, expected in expected_42.items():
                    if node.get(field) != expected:
                        errors.append(
                            f"{node_id}: current 42 {field} must be {expected}"
                        )
            if node_id == "sportsbook-risk-service":
                expected_risk = {
                    "release": "risk-v1.0.2",
                    "learning": "learning/risk-v1.0.2",
                    "practice": "docs/practice-risk-v1.0.2/README.md",
                    "answer": "docs/commits-risk-v1.0.2/README.md",
                }
                for field, expected in expected_risk.items():
                    if node.get(field) != expected:
                        errors.append(
                            f"sportsbook-risk-service: current {field} must be {expected}"
                        )
            if isinstance(doc, str) and (root / doc).is_file() and isinstance(
                node.get("anchor"), str
            ):
                section = _anchor_section(
                    (root / doc).read_text(encoding="utf-8"), node["anchor"]
                )
                owner = data.get("owner", "woopinbell")
                central_handoff = (
                    f"https://github.com/{owner}/central-notes/blob/main/"
                    f"TRACK_SEQUENCE.md#{node.get('anchor')}"
                )
                exact_targets = (
                    f"https://github.com/{owner}/{repo}",
                    f"https://github.com/{owner}/{repo}/blob/{learning}/{node.get('practice')}",
                    f"https://github.com/{owner}/{repo}/blob/{learning}/{node.get('answer')}",
                )
                for target in exact_targets:
                    if f"]({target})" not in section:
                        errors.append(
                            f"{node_id}: current stage card is missing exact target {target}"
                        )
                for token in (str(release), str(learning)):
                    if f"`{token}`" not in section:
                        errors.append(
                            f"{node_id}: current stage card is missing exact ref `{token}`"
                        )
                if f"]({central_handoff})" not in section:
                    errors.append(
                        f"{node_id}: current stage card is missing exact Central "
                        f"handoff {central_handoff}"
                    )
                scope_handoff = "](README.md#공식-수행-범위)"
                if scope_handoff not in section:
                    errors.append(
                        f"{node_id}: current stage card is missing canonical "
                        "practice scope handoff"
                    )
                if node_id == "sportsbook-odds-feed-service":
                    if "Spring/Kafka 관련 index" in section:
                        errors.append(
                            "sportsbook-odds-feed-service: generic persistence index "
                            "must not be labeled as Kafka"
                        )
                    note_links = (
                        (
                            "Spring Kafka",
                            "https://github.com/woopinbell/sportsbook-orchestration/"
                            "blob/learning/orchestration-v1/notes/spring-kafka.md",
                        ),
                        (
                            "Avro",
                            "https://github.com/woopinbell/sportsbook-orchestration/"
                            "blob/learning/orchestration-v1/notes/avro.md",
                        ),
                    )
                    for label, note_url in note_links:
                        if f"[{label}]({note_url})" not in section:
                            errors.append(
                                "sportsbook-odds-feed-service: current stage card is "
                                f"missing the original Sportsbook {label} handoff"
                            )
                    ownership = "Kafka·Avro의 정본은 Sportsbook 원본 notes다"
                    if ownership not in section:
                        errors.append(
                            "sportsbook-odds-feed-service: current stage card must "
                            "identify the original Sportsbook notes as canonical"
                        )

    errors.extend(_validate_overlays(data, root, node_by_id))

    counts = {track: 0 for track in VALID_TRACKS}
    repos: set[str] = set()
    for project in projects:
        if not isinstance(project, dict):
            continue
        track = project.get("track")
        if track in counts:
            counts[track] += 1
        repo = project.get("repo")
        if isinstance(repo, str):
            if repo in repos:
                errors.append(f"repository appears more than once: {repo}")
            repos.add(repo)
    for track, expected in TRACK_COUNTS.items():
        if counts[track] != expected:
            errors.append(
                f"{track} must contain exactly {expected} projects, found {counts[track]}"
            )

    for track, sequence in DISPLAY_SEQUENCES.items():
        expected_projects = [
            node_id for node_id in sequence if kind_by_id.get(node_id) == "project"
        ]
        actual_projects = [
            project.get("id")
            for project in projects
            if isinstance(project, dict) and project.get("track") == track
        ]
        if actual_projects != expected_projects:
            errors.append(
                f"{track}: project order must be " + " -> ".join(expected_projects)
            )

    entry = data.get("entry")
    if entry != "linux-foundation":
        errors.append("entry must be linux-foundation")
    if entry not in node_by_id:
        errors.append(f"entry node does not exist: {entry}")
    if data.get("practice_policy") != PRACTICE_POLICY:
        errors.append(
            "practice_policy must require one representative practice plus the card "
            "gate and classify remaining practices as optional deepening"
        )

    for node_id, node in node_by_id.items():
        try:
            prev_ids = _ids(node.get("prev"))
            next_ids = _ids(node.get("next"))
        except CurriculumError:
            continue
        if node_id in prev_ids or node_id in next_ids:
            errors.append(f"{node_id}: self edge is forbidden")
        for next_id in next_ids:
            target = node_by_id.get(next_id)
            if target is None:
                errors.append(f"{node_id}: unknown next node {next_id}")
            elif node_id not in _ids(target.get("prev")):
                errors.append(f"{node_id} -> {next_id}: reverse prev edge is missing")
        for prev_id in prev_ids:
            source = node_by_id.get(prev_id)
            if source is None:
                errors.append(f"{node_id}: unknown prev node {prev_id}")
            elif node_id not in _ids(source.get("next")):
                errors.append(f"{prev_id} -> {node_id}: reverse next edge is missing")
        if not next_ids and kind_by_id.get(node_id) != "completion":
            errors.append(f"{node_id}: non-completion dead end")
        if next_ids and kind_by_id.get(node_id) == "completion":
            errors.append(f"{node_id}: completion must be a terminal node")

    for track, sequence in DISPLAY_SEQUENCES.items():
        for node_id in sequence:
            node = node_by_id.get(node_id)
            if node is None:
                continue
            expected_prev_raw, expected_next_raw = CANONICAL_EDGES[node_id]
            expected_prev = list(expected_prev_raw)
            expected_next = list(expected_next_raw)
            if _ids(node.get("prev")) != expected_prev:
                errors.append(
                    f"{node_id}: canonical prev must be {expected_prev or 'empty'}"
                )
            if _ids(node.get("next")) != expected_next:
                errors.append(
                    f"{node_id}: canonical next must be {expected_next or 'empty'}"
                )
            if expected_next:
                doc_path = root / str(node.get("doc"))
                section = (
                    _anchor_section(
                        doc_path.read_text(encoding="utf-8"), str(node.get("anchor"))
                    )
                    if doc_path.is_file()
                    else ""
                )
                for next_id in expected_next:
                    target = node_by_id.get(next_id)
                    if target is None:
                        continue
                    if target.get("doc") == node.get("doc"):
                        target_link = f"](#{target.get('anchor')})"
                    else:
                        target_link = (
                            f"]({Path(str(target.get('doc'))).name}#"
                            f"{target.get('anchor')})"
                        )
                    if target_link not in section:
                        errors.append(
                            f"{node_id}: stage card is missing next link {target_link[2:-1]}"
                        )
            if len(expected_prev) > 1:
                doc_path = root / str(node.get("doc"))
                section = (
                    _anchor_section(
                        doc_path.read_text(encoding="utf-8"), str(node.get("anchor"))
                    )
                    if doc_path.is_file()
                    else ""
                )
                if "세 갈래를 모두 완료" not in section:
                    errors.append(
                        f"{node_id}: join card must explain that every prior lane is required"
                    )
                for prev_id in expected_prev:
                    source = node_by_id.get(prev_id)
                    if source is None:
                        continue
                    if source.get("doc") == node.get("doc"):
                        source_link = f"](#{source.get('anchor')})"
                    else:
                        source_link = (
                            f"]({Path(str(source.get('doc'))).name}#"
                            f"{source.get('anchor')})"
                        )
                    if source_link not in section:
                        errors.append(
                            f"{node_id}: join card is missing required prior link "
                            f"{source_link[2:-1]}"
                        )

    if entry in node_by_id:
        visited: set[str] = set()
        active: set[str] = set()

        def visit(node_id: str) -> None:
            if node_id in active:
                errors.append(f"cycle detected at {node_id}")
                return
            if node_id in visited:
                return
            active.add(node_id)
            for child in _ids(node_by_id[node_id].get("next")):
                if child in node_by_id:
                    visit(child)
            active.remove(node_id)
            visited.add(node_id)

        visit(entry)
        reachable = set(visited)
        unreachable = sorted(set(node_by_id) - reachable)
        if unreachable:
            errors.append(f"unreachable curriculum nodes: {', '.join(unreachable)}")
        for node_id in node_by_id:
            visit(node_id)

    expected_completions = {"frontend-complete", "backend-complete"}
    actual_completions = {
        node_id for node_id, kind in kind_by_id.items() if kind == "completion"
    }
    if actual_completions != expected_completions:
        errors.append(
            "completion nodes must be exactly frontend-complete and backend-complete"
        )

    expected_assessments = {
        "42-incident",
        "frontend-transfer",
        "web-production-regression",
        "backend-incident",
    }
    actual_assessments = {
        node_id for node_id, kind in kind_by_id.items() if kind == "assessment"
    }
    if actual_assessments != expected_assessments:
        errors.append(
            "assessment nodes must be exactly 42-incident, frontend-transfer, "
            "web-production-regression, and backend-incident"
        )

    actual_prerequisites = {
        node_id for node_id, kind in kind_by_id.items() if kind == "prerequisite"
    }
    if actual_prerequisites != {"linux-foundation"}:
        errors.append("prerequisite nodes must contain exactly linux-foundation")
    foundation = node_by_id.get("linux-foundation")
    if foundation:
        foundation_path = root / str(foundation.get("doc"))
        section = (
            _anchor_section(
                foundation_path.read_text(encoding="utf-8"),
                str(foundation.get("anchor")),
            )
            if foundation_path.is_file()
            else ""
        )
        central_target = (
            "https://github.com/woopinbell/central-notes/blob/main/"
            "TRACK_SEQUENCE.md#stage-linux-foundation"
        )
        if f"]({central_target})" not in section:
            errors.append(
                "linux-foundation: stage card is missing the exact Central handoff"
            )
        if "https://github.com/woopinbell/linux-admin" in section:
            errors.append(
                "linux-foundation: retired linux-admin must not be an active remote link"
            )

    branches = data.get("branches", [])
    expected_branches = {
        "linux-foundation": {
            "choices": {"c-foundation", "cpp-foundation", "container-stack"},
            "join": "web-boundary-inspector",
            "requires": {"stack-sort", "irc-relay-server", "container-stack"},
        },
        "42-incident": {
            "choices": {
                "frontend-foundations-training",
                "backend-foundations-training",
            },
            "join": None,
            "requires": set(),
        },
    }
    if not isinstance(branches, list):
        errors.append("branches must be a list")
    else:
        actual_from = [
            item.get("from") for item in branches if isinstance(item, dict)
        ]
        if set(actual_from) != set(expected_branches) or len(actual_from) != 2:
            errors.append(
                "branches must define linux-foundation and 42-incident exactly once"
            )
        for source_id, expected in expected_branches.items():
            matches = [
                item
                for item in branches
                if isinstance(item, dict) and item.get("from") == source_id
            ]
            if len(matches) != 1:
                continue
            branch = matches[0]
            choices = set(_ids(branch.get("choices")))
            if choices != expected["choices"]:
                errors.append(
                    f"{source_id}: branch choices must be {sorted(expected['choices'])}"
                )
            source = node_by_id.get(source_id)
            if source and choices != set(_ids(source.get("next"))):
                errors.append(f"{source_id}: branch choices must equal its next edges")
            if branch.get("join") != expected["join"]:
                errors.append(
                    f"{source_id}: branch join must be {expected['join']!r}"
                )
            requires = set(_ids(branch.get("requires")))
            if requires != expected["requires"]:
                errors.append(
                    f"{source_id}: branch requirements must be "
                    f"{sorted(expected['requires'])}"
                )
            join_id = expected["join"]
            join = node_by_id.get(str(join_id)) if join_id else None
            if join and requires != set(_ids(join.get("prev"))):
                errors.append(
                    f"{source_id}: branch requirements must equal {join_id}.prev"
                )

    incident_id = "42-incident"
    if entry in node_by_id and incident_id in node_by_id:
        reachable_without_incident: set[str] = set()
        stack = [entry]
        while stack:
            current = stack.pop()
            if current == incident_id or current in reachable_without_incident:
                continue
            reachable_without_incident.add(current)
            stack.extend(_ids(node_by_id[current].get("next")))
        leaked = sorted(
            node_id
            for node_id in reachable_without_incident
            if node_by_id[node_id].get("track") in {"frontend", "backend"}
        )
        if leaked:
            errors.append(
                "extension track is reachable before 42 incident: " + ", ".join(leaked)
            )

    root_readme = root / "README.md"
    if not root_readme.is_file():
        errors.append("root README.md is missing")
    else:
        root_text = root_readme.read_text(encoding="utf-8")
        sections = re.findall(
            r"(?ms)^## 학습 시작\s*$\n(.*?)(?=^##\s|\Z)", root_text
        )
        ctas = (
            re.findall(
                r"\[[^\]]+\]\((?:\./)?tracks/README\.md(?:#[^)]+)?\)",
                sections[0],
            )
            if len(sections) == 1
            else []
        )
        section_links = (
            re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", sections[0])
            if len(sections) == 1
            else []
        )
        if len(sections) != 1 or len(ctas) != 1 or len(section_links) != 1:
            errors.append(
                "root README's single '학습 시작' section must contain exactly one "
                "Markdown link, the tracks/README.md CTA"
            )

    track_readme = root / "tracks/README.md"
    if track_readme.is_file():
        track_text = track_readme.read_text(encoding="utf-8")
        scope_markers = (
            '<a id="공식-수행-범위"></a>',
            "프로젝트마다 연습문제 한 개만 필수",
            "나머지 연습문제는 선택 심화",
            "문제가 만들어졌던 시점의 코드",
            "현재 완성본",
            "Document Box의 이 규칙이 우선",
        )
        for marker in scope_markers:
            if marker not in track_text:
                errors.append(
                    "tracks/README.md is missing the canonical practice scope "
                    f"marker: {marker}"
                )

    simple_learning_docs = (
        root / "tracks/README.md",
        root / "tracks/42.md",
        root / "tracks/frontend.md",
        root / "tracks/backend.md",
        root / "tracks/frontend-fast-track.md",
        root / "tracks/PROGRESS_TEMPLATE.md",
    )
    forbidden_jargon = (
        "current learning index",
        "practice ledger",
        "answer ledger",
        "Clean release gate",
        "Historical 무자료 gate",
        "full `부모 commit`",
        "연결 설명:",
    )
    for learning_doc in simple_learning_docs:
        if not learning_doc.is_file():
            continue
        learning_text = learning_doc.read_text(encoding="utf-8")
        for phrase in forbidden_jargon:
            if phrase in learning_text:
                errors.append(
                    f"{learning_doc.relative_to(root)} uses learner-facing jargon: "
                    f"{phrase}"
                )

    return errors


def _tool_result(name: str, required: bool, hint: str = "") -> Result:
    path = shutil.which(name)
    if path:
        return Result("PASS", name, path)
    level = "BLOCK" if required else "WARN"
    return Result(level, name, hint or f"install {name} before the affected project")


def _github_access(owner: str, repo: str) -> Result:
    """Check one repository after the caller has authenticated once."""

    view = _run(
        ["gh", "repo", "view", f"{owner}/{repo}", "--json", "visibility"],
        timeout=15,
    )
    if view.returncode != 0:
        return Result(
            "BLOCK",
            "GitHub private access",
            f"cannot read {owner}/{repo}: {view.stderr.strip()}",
        )
    try:
        visibility = json.loads(view.stdout).get("visibility")
    except json.JSONDecodeError:
        return Result(
            "BLOCK",
            f"GitHub {repo}",
            "repository metadata was not valid JSON",
        )
    if visibility != "PRIVATE":
        return Result(
            "BLOCK",
            f"GitHub {repo}",
            f"expected PRIVATE visibility, found {visibility or 'UNKNOWN'}",
        )
    return Result("PASS", f"GitHub {repo}", "authenticated PRIVATE access")


def _github_track_access(owner: str, projects: list[dict[str, Any]]) -> list[Result]:
    """Authenticate once, then prove access and PRIVATE visibility for every repo."""

    if not shutil.which("gh"):
        return [Result("BLOCK", "GitHub private access", "gh is not installed")]
    auth = _run(["gh", "auth", "status"], timeout=15)
    if auth.returncode != 0:
        return [
            Result(
                "BLOCK",
                "GitHub private access",
                "run `gh auth login` with access to private repositories",
            )
        ]
    with ThreadPoolExecutor(max_workers=min(6, len(projects) or 1)) as executor:
        futures = {
            executor.submit(_github_access, owner, project["repo"]): project["repo"]
            for project in projects
        }
        by_repo: dict[str, Result] = {}
        for future in as_completed(futures):
            repo = futures[future]
            try:
                by_repo[repo] = future.result()
            except subprocess.TimeoutExpired:
                by_repo[repo] = Result(
                    "BLOCK", f"GitHub {repo}", "repository access check timed out"
                )
    return [by_repo[project["repo"]] for project in projects]


def _compose_result() -> Result:
    if not shutil.which("docker"):
        return Result("BLOCK", "Docker Compose", "install Docker Desktop")
    compose = _run(["docker", "compose", "version"], timeout=12)
    if compose.returncode != 0:
        return Result(
            "BLOCK",
            "Docker Compose",
            "install the Docker Compose plugin supplied with Docker Desktop",
        )
    return Result("PASS", "Docker Compose", compose.stdout.strip().splitlines()[0])


def preflight(
    data: dict[str, Any],
    track: str | None,
    root: Path | None = None,
    route: str | None = None,
) -> int:
    selected_track = track.strip() if isinstance(track, str) else ""
    selected_overlay: dict[str, Any] | None = None
    if route:
        overlays = [
            item
            for item in data.get("overlays", [])
            if isinstance(item, dict) and item.get("id") == route
        ]
        if len(overlays) != 1:
            print(f"BLOCK route: unknown curriculum overlay {route}")
            return 2
        selected_overlay = overlays[0]
        overlay_track = selected_overlay.get("track")
        if selected_track and overlay_track != selected_track:
            print(
                f"BLOCK route: {route} belongs to {overlay_track}, not {selected_track}"
            )
            return 2
        selected_track = str(overlay_track)

    track = selected_track
    if track not in VALID_TRACKS:
        print("BLOCK TRACK: choose exactly one of 42, frontend, backend")
        print(
            "usage: make preflight TRACK=42|frontend|backend or "
            "make preflight ROUTE=frontend-application-bridge"
        )
        return 2
    if root is not None:
        navigation_errors = validate_registry(data, root.resolve())
        if navigation_errors:
            for error in navigation_errors:
                print(f"BLOCK navigation: {error}")
            return 1
        print("PASS  local navigation: registry, cards, links and sequence")
    all_projects = data.get("projects", [])
    projects = [item for item in all_projects if item.get("track") == track]
    if selected_overlay is not None:
        overlay = selected_overlay
        project_by_id = {
            item.get("id"): item
            for item in all_projects
            if isinstance(item, dict) and isinstance(item.get("id"), str)
        }
        projects = [
            project_by_id[project_id]
            for project_id in overlay.get("preflight_projects", [])
            if project_id in project_by_id
        ]
        print(
            f"PASS  route: {route} ({overlay.get('outcome')}; "
            "does not grant curriculum mastery)"
        )
    if not projects:
        print(f"BLOCK registry: no projects found for {track}")
        return 1
    owner = data.get("owner", "woopinbell")
    results = [
        _tool_result("git", True),
        _tool_result("gh", True, "install GitHub CLI, then run `gh auth login`"),
    ]
    results.extend(_github_track_access(owner, projects))
    if track == "42":
        results.extend(
            (
                _tool_result("make", True),
                _tool_result("cc", True, "install the platform C compiler"),
                _tool_result("c++", True, "install the platform C++ compiler"),
                _tool_result("python3", True),
                _tool_result("node", True, "install the Node version requested by each release"),
                _tool_result("npm", True),
                _tool_result("npx", True),
                _tool_result("pnpm", False, "run `corepack enable` before pong-pong"),
                _tool_result("docker", True, "install Docker Desktop and start the daemon"),
                _compose_result(),
            )
        )
    elif track == "frontend" and route == FRONTEND_APPLICATION_OVERLAY_ID:
        results.extend(
            (
                _tool_result("make", True),
                _tool_result("node", True, "install the Node version requested by each release"),
                _tool_result("npm", True),
                _tool_result(
                    "pnpm",
                    True,
                    "run `corepack enable` before the selected Foundations/Reliability gates",
                ),
                _tool_result("npx", True),
            )
        )
    elif track == "frontend":
        results.extend(
            (
                _tool_result("make", True),
                _tool_result("node", True, "install the Node version requested by each release"),
                _tool_result("npm", True),
                _tool_result("pnpm", False, "run `corepack enable`, if the project requests pnpm"),
                _tool_result("npx", True),
                _tool_result("java", True, "install the JDK required by the Firestore emulator"),
                _tool_result("docker", True, "install Docker Desktop and start the daemon"),
                _compose_result(),
            )
        )
    else:
        results.extend(
            (
                _tool_result("make", True),
                _tool_result("java", True, "install the JDK version requested by each release"),
                _tool_result("mvn", True, "install Maven; prefer a repository's ./mvnw when present"),
                _tool_result("python3", True),
                _tool_result("jq", True, "install jq for release and evidence checks"),
                _tool_result("curl", True),
                _tool_result("docker", True, "install Docker Desktop and start the daemon"),
                _compose_result(),
                _tool_result(
                    "go",
                    False,
                    "install the release-pinned Go toolchain before backend-delivery-training",
                ),
            )
        )

    route_needs_docker = not (
        track == "frontend" and route == FRONTEND_APPLICATION_OVERLAY_ID
    )
    if route_needs_docker and shutil.which("docker"):
        docker = _run(["docker", "info"], timeout=12)
        results.append(
            Result(
                "PASS" if docker.returncode == 0 else "WARN",
                "Docker daemon",
                "available"
                if docker.returncode == 0
                else "start Docker Desktop before a Docker-backed gate",
            )
        )
    if track in {"42", "frontend"}:
        results.append(
            Result(
                "WARN",
                "Playwright Chromium/Firefox/WebKit",
                "a cache directory is not proof of three engines; run each release's "
                "pinned `npx playwright install chromium firefox webkit` command",
            )
        )

    for result in results:
        print(f"{result.level:5} {result.name}: {result.detail}")
    print("\nProject setup is never automatic. Follow each release README in this order:")
    for project in projects:
        setup = project.get(
            "setup",
            PROJECT_SETUP.get(
                project["repo"],
                "read README.md, install the pinned dependencies, run baseline",
            ),
        )
        if isinstance(setup, list):
            setup = "; ".join(str(item) for item in setup)
        print(f"- {project['repo']}: {setup}")
    return 1 if any(result.level == "BLOCK" for result in results) else 0


def _parse_ls_remote(stdout: str) -> dict[str, str]:
    refs: dict[str, str] = {}
    for line in stdout.splitlines():
        parts = line.split("\t", 1)
        if len(parts) == 2 and re.fullmatch(r"[0-9a-f]{40}", parts[0]):
            refs[parts[1]] = parts[0]
    return refs


def _json_payload(result: subprocess.CompletedProcess[str]) -> Any | None:
    if result.returncode != 0:
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return None


def _learning_roles(
    project_id: str,
    release_sha: str | None = None,
    learning_sha: str | None = None,
) -> tuple[str, ...]:
    frozen = FROZEN_MONOLITHIC_LEARNING.get(project_id)
    if frozen and (
        release_sha == frozen["main"] and learning_sha == frozen["learning"]
    ):
        return ("learning",)
    if project_id in NO_PROJECT_NOTES:
        return ("commits", "practice")
    return ("notes", "commits", "practice")


def _learning_path_allowed(
    role: str,
    path: str,
    *,
    allow_commits_index: bool = False,
    exact_current_paths: bool = False,
) -> bool:
    if role == "learning":
        return (
            path == "docs/README.md"
            or path.startswith("notes/")
            or path.startswith("docs/commits/")
            or path.startswith("docs/practice/")
        )
    if role == "notes":
        return (
            path == "docs/README.md"
            or path.startswith("docs/notes/")
            or path.startswith("docs/reflection/")
            or path.startswith("notes/")
            or path.startswith("notes-")
        )
    if role == "commits":
        commits_path = (
            path.startswith("docs/commits/")
            if exact_current_paths
            else re.match(r"^docs/commits(?:-[^/]+)?/", path) is not None
        )
        return (allow_commits_index and path == "docs/README.md") or commits_path
    if role == "practice":
        return (
            path.startswith("docs/practice/")
            if exact_current_paths
            else re.match(r"^docs/practice(?:-[^/]+)?/", path) is not None
        )
    return False


def _validate_learning_history(
    label: str,
    release_sha: str,
    learning_sha: str,
    roles: tuple[str, ...],
    compare: dict[str, Any],
    details: dict[str, dict[str, Any]],
    *,
    exact_current_paths: bool = False,
) -> list[str]:
    """Validate the immutable release-to-learning publication as a pure contract."""

    errors: list[str] = []
    expected_count = len(roles)
    merge_base = compare.get("merge_base_commit") or {}
    commits = compare.get("commits")
    if compare.get("status") != "ahead":
        errors.append(f"{label}: learning status must be ahead of release")
    if compare.get("behind_by") != 0:
        errors.append(f"{label}: learning must not be behind release")
    if compare.get("ahead_by") != expected_count:
        errors.append(
            f"{label}: learning must add exactly {expected_count} publication commits"
        )
    if compare.get("total_commits") != expected_count:
        errors.append(
            f"{label}: compare must expose exactly {expected_count} publication commits"
        )
    if merge_base.get("sha") != release_sha:
        errors.append(f"{label}: release must be the exact learning merge base")
    if not isinstance(commits, list) or len(commits) != expected_count:
        errors.append(
            f"{label}: learning commit list must contain exactly {expected_count} commits"
        )
        return errors

    expected_parent = release_sha
    index_owner = (
        "learning"
        if roles == ("learning",)
        else "notes"
        if "notes" in roles
        else "commits"
    )
    index_change_count = 0
    for index, (role, summary) in enumerate(zip(roles, commits)):
        sha = summary.get("sha") if isinstance(summary, dict) else None
        if not isinstance(sha, str):
            errors.append(f"{label}: learning commit {index + 1} has no SHA")
            continue
        detail = details.get(sha)
        if not isinstance(detail, dict):
            errors.append(f"{label}: cannot inspect learning commit {sha}")
            expected_parent = sha
            continue
        parents = detail.get("parents")
        parent_shas = (
            [parent.get("sha") for parent in parents if isinstance(parent, dict)]
            if isinstance(parents, list)
            else []
        )
        if parent_shas != [expected_parent]:
            errors.append(
                f"{label}: {role} commit {sha} must be linear from {expected_parent}"
            )
        commit = detail.get("commit") or {}
        message = commit.get("message") if isinstance(commit, dict) else None
        subject = message.splitlines()[0] if isinstance(message, str) else ""
        if not re.match(rf"^docs\({re.escape(role)}\):\s+\S", subject):
            errors.append(
                f"{label}: publication {index + 1} subject must start with "
                f"docs({role}):"
            )
        files = detail.get("files")
        if not isinstance(files, list) or not files:
            errors.append(f"{label}: {role} publication must change learning files")
        else:
            for file_entry in files:
                if not isinstance(file_entry, dict):
                    errors.append(f"{label}: {role} publication has unreadable file data")
                    continue
                paths = [file_entry.get("filename")]
                if file_entry.get("previous_filename"):
                    paths.append(file_entry.get("previous_filename"))
                if role == index_owner and "docs/README.md" in paths:
                    index_change_count += 1
                for path in paths:
                    if not isinstance(path, str) or not _learning_path_allowed(
                        role,
                        path,
                        allow_commits_index=(role == "commits" and "notes" not in roles),
                        exact_current_paths=exact_current_paths,
                    ):
                        errors.append(
                            f"{label}: {role} publication changes forbidden path {path!r}"
                        )
        expected_parent = sha
    if index_change_count != 1:
        errors.append(
            f"{label}: {index_owner} publication must change docs/README.md exactly once"
        )
    final_sha = commits[-1].get("sha") if isinstance(commits[-1], dict) else None
    if final_sha != learning_sha:
        errors.append(f"{label}: final publication commit is not the learning branch tip")
    return errors


def _remote_text(
    owner: str, repo: str, path: str, sha: str
) -> tuple[str | None, str | None]:
    endpoint = (
        f"repos/{owner}/{repo}/contents/{quote(path, safe='/')}"
        f"?ref={quote(sha, safe='')}"
    )
    result = _run(["gh", "api", endpoint], timeout=20)
    payload = _json_payload(result)
    if not isinstance(payload, dict):
        return None, result.stderr.strip() or "unreadable GitHub contents response"
    try:
        return base64.b64decode(payload["content"]).decode("utf-8"), None
    except (KeyError, ValueError, UnicodeDecodeError):
        return None, "content is not valid base64 UTF-8"


def _check_remote_project(owner: str, project: dict[str, Any]) -> list[str]:
    project_id = str(project["id"])
    repo = project["repo"]
    release = project["release"]
    learning = project["learning"]
    label = f"{owner}/{repo}"
    errors: list[str] = []
    view = _run(
        [
            "gh",
            "repo",
            "view",
            label,
            "--json",
            "url,visibility,defaultBranchRef",
        ],
        timeout=20,
    )
    if view.returncode != 0:
        return [f"{label}: private repository access failed: {view.stderr.strip()}"]
    try:
        metadata = json.loads(view.stdout)
    except json.JSONDecodeError:
        return [f"{label}: gh returned invalid repository metadata"]
    if metadata.get("visibility") != "PRIVATE":
        errors.append(f"{label}: expected PRIVATE visibility")
    default = (metadata.get("defaultBranchRef") or {}).get("name")
    if default != "main":
        errors.append(f"{label}: default branch is {default!r}, expected main")
    url = metadata.get("url") or f"https://github.com/{label}"
    patterns = [
        "refs/heads/main",
        f"refs/tags/{release}",
        f"refs/tags/{release}^{{}}",
        f"refs/heads/{learning}*",
    ]
    if project_id in STRICT_TOPOLOGY_PROJECTS:
        patterns.extend(("refs/heads/*", "refs/tags/*"))
    template = project.get("template")
    if template:
        patterns.extend((f"refs/tags/{template}", f"refs/tags/{template}^{{}}"))
    command = ["git", "ls-remote", url, *patterns]
    remote = _run(command, timeout=30)
    if remote.returncode != 0:
        errors.append(f"{label}: git ls-remote failed: {remote.stderr.strip()}")
        return errors
    refs = _parse_ls_remote(remote.stdout)
    main_sha = refs.get("refs/heads/main")
    tag_sha = refs.get(f"refs/tags/{release}")
    peeled_sha = refs.get(f"refs/tags/{release}^{{}}")
    learning_sha = refs.get(f"refs/heads/{learning}")
    if not main_sha:
        errors.append(f"{label}: main is missing")
    if not tag_sha:
        errors.append(f"{label}: release tag {release} is missing")
    if not peeled_sha or peeled_sha == tag_sha:
        errors.append(f"{label}: {release} is not an annotated tag")
    if main_sha and peeled_sha and main_sha != peeled_sha:
        errors.append(f"{label}: {release} does not peel to main")
    if not learning_sha:
        errors.append(f"{label}: learning branch {learning} is missing")

    if project_id in STRICT_TOPOLOGY_PROJECTS:
        actual_heads = {
            ref.removeprefix("refs/heads/")
            for ref in refs
            if ref.startswith("refs/heads/")
        }
        expected_heads = {"main", learning}
        if actual_heads != expected_heads:
            errors.append(
                f"{label}: branches must be exactly {sorted(expected_heads)}, "
                f"found {sorted(actual_heads)}"
            )
        actual_tags = {
            ref.removeprefix("refs/tags/")
            for ref in refs
            if ref.startswith("refs/tags/") and not ref.endswith("^{}")
        }
        if actual_tags != {release}:
            errors.append(
                f"{label}: tags must be exactly {[release]}, found {sorted(actual_tags)}"
            )

    expected_learning_ref = f"refs/heads/{learning}"
    supplemental = sorted(
        ref
        for ref in refs
        if ref != expected_learning_ref
        and (
            ref.startswith(expected_learning_ref + "/")
            or ref.startswith(expected_learning_ref + "-")
            or ref.startswith(expected_learning_ref + ".")
        )
    )
    for ref in supplemental:
        errors.append(f"{label}: supplemental current-release branch is forbidden: {ref}")

    navigation_freeze = UNCHANGED_NAVIGATION_RELEASES.get(project_id)
    if navigation_freeze and not project.get("main_backlink", True):
        actual_navigation = {
            "release": release,
            "main": main_sha,
            "tag": tag_sha,
        }
        if actual_navigation != navigation_freeze:
            errors.append(
                f"{label}: unchanged navigation exception requires exact "
                "release, main, and annotated tag objects"
            )

    frozen_learning = FROZEN_MONOLITHIC_LEARNING.get(project_id)
    if frozen_learning:
        actual_learning = {
            "release": release,
            "main": peeled_sha,
            "tag": tag_sha,
            "learning_ref": learning,
            "learning": learning_sha,
        }
        if actual_learning != frozen_learning:
            errors.append(
                f"{label}: monolithic learning exception requires the exact frozen "
                "release and learning objects"
            )

    if template:
        template_tag = refs.get(f"refs/tags/{template}")
        template_peeled = refs.get(f"refs/tags/{template}^{{}}")
        if not template_tag:
            errors.append(f"{label}: template tag {template} is missing")
        if not template_peeled or template_peeled == template_tag:
            errors.append(f"{label}: {template} is not an annotated tag")
        if main_sha and template_peeled:
            publication_result = _run(
                ["gh", "api", f"repos/{owner}/{repo}/commits/{main_sha}"],
                timeout=30,
            )
            publication = _json_payload(publication_result)
            parents = publication.get("parents") if isinstance(publication, dict) else None
            parent_shas = (
                [parent.get("sha") for parent in parents if isinstance(parent, dict)]
                if isinstance(parents, list)
                else []
            )
            if parent_shas != [template_peeled]:
                errors.append(
                    f"{label}: deployable main must be one publication commit after "
                    f"{template}"
                )

    if peeled_sha and learning_sha:
        compare_endpoint = (
            f"repos/{owner}/{repo}/compare/{peeled_sha}...{learning_sha}"
        )
        compare_result = _run(["gh", "api", compare_endpoint], timeout=30)
        compare = _json_payload(compare_result)
        if not isinstance(compare, dict):
            errors.append(f"{label}: cannot compare release and learning snapshots")
        else:
            details: dict[str, dict[str, Any]] = {}
            compare_commits = compare.get("commits")
            if isinstance(compare_commits, list):
                for summary in compare_commits:
                    sha = summary.get("sha") if isinstance(summary, dict) else None
                    if not isinstance(sha, str):
                        continue
                    detail_result = _run(
                        ["gh", "api", f"repos/{owner}/{repo}/commits/{sha}"],
                        timeout=30,
                    )
                    detail = _json_payload(detail_result)
                    if isinstance(detail, dict):
                        details[sha] = detail
            errors.extend(
                _validate_learning_history(
                    label,
                    peeled_sha,
                    learning_sha,
                    _learning_roles(project_id, peeled_sha, learning_sha),
                    compare,
                    details,
                    exact_current_paths=(learning == "learning/current"),
                )
            )

    if learning_sha:
        _, index_error = _remote_text(owner, repo, "docs/README.md", learning_sha)
        if index_error:
            errors.append(
                f"{label}@{learning_sha}: missing learning index docs/README.md: "
                f"{index_error}"
            )

    for field in ("practice", "answer"):
        for path in _paths(project[field], f"{project['id']}.{field}"):
            endpoint = (
                f"repos/{owner}/{repo}/contents/{quote(path, safe='/')}"
                f"?ref={quote(learning_sha or '', safe='')}"
            )
            check = _run(["gh", "api", "--silent", endpoint], timeout=20)
            if check.returncode != 0:
                errors.append(
                    f"{label}@{learning_sha or learning}: missing {field} path {path}"
                )
    for path in _paths(project.get("main_paths", ["README.md"]), "main_paths"):
        endpoint = (
            f"repos/{owner}/{repo}/contents/{quote(path, safe='/')}"
            f"?ref={quote(main_sha or '', safe='')}"
        )
        check = _run(["gh", "api", "--silent", endpoint], timeout=20)
        if check.returncode != 0:
            errors.append(f"{label}@{main_sha or 'main'}: missing required path {path}")

    if main_sha and project.get("main_backlink", True):
        readme, readme_error = _remote_text(owner, repo, "README.md", main_sha)
        if readme_error:
            errors.append(f"{label}@{main_sha}: unreadable README.md: {readme_error}")
        else:
            backlink = (
                f"https://github.com/{owner}/document-box/blob/main/"
                f"{project['doc']}#{project['anchor']}"
            )
            if backlink not in (readme or ""):
                errors.append(f"{label}@{main_sha}: README lacks exact card backlink {backlink}")

    final_remote = _run(command, timeout=30)
    if final_remote.returncode != 0:
        errors.append(f"{label}: final ref drift check failed")
    elif _parse_ls_remote(final_remote.stdout) != refs:
        errors.append(f"{label}: refs changed during remote verification")
    return errors


def _overlay_ref_manifest(
    owner: str,
    overlays: list[dict[str, Any]],
    project_by_id: dict[str, dict[str, Any]],
) -> tuple[dict[str, dict[str, str]], list[str]]:
    """Freeze every ref consumed by an overlay for whole-run drift detection."""

    commands: dict[str, list[str]] = {}
    errors: list[str] = []
    for overlay in overlays:
        for selection in overlay.get("selections", []):
            if not isinstance(selection, dict):
                continue
            project = project_by_id.get(str(selection.get("project")))
            if not project:
                continue
            learning = str(selection.get("learning", ""))
            label = f"{owner}/{project['repo']}:{learning}"
            commands[label] = [
                "git",
                "ls-remote",
                f"https://github.com/{owner}/{project['repo']}",
                f"refs/heads/{learning}",
            ]
        portfolio = overlay.get("portfolio")
        if not isinstance(portfolio, dict):
            continue
        project = project_by_id.get(str(portfolio.get("project", "")))
        if not project:
            continue
        release = str(portfolio.get("release", ""))
        learning = str(portfolio.get("learning", ""))
        template = str(portfolio.get("template", ""))
        label = f"{owner}/{project['repo']}:portfolio-overlay"
        commands[label] = [
            "git",
            "ls-remote",
            f"https://github.com/{owner}/{project['repo']}",
            "refs/heads/main",
            f"refs/tags/{release}",
            f"refs/tags/{release}^{{}}",
            f"refs/heads/{learning}",
            f"refs/tags/{template}",
            f"refs/tags/{template}^{{}}",
        ]

    manifest: dict[str, dict[str, str]] = {}
    for label, command in commands.items():
        result = _run(command, timeout=30)
        refs = _parse_ls_remote(result.stdout)
        if result.returncode != 0 or not refs:
            errors.append(f"cannot freeze overlay refs for {label}")
            continue
        manifest[label] = refs
    return manifest, errors


def _check_remote_overlay(
    owner: str,
    overlay: dict[str, Any],
    project_by_id: dict[str, dict[str, Any]],
) -> list[str]:
    """Verify overlay-only practice paths and Portfolio refs at frozen SHAs."""

    errors: list[str] = []
    overlay_id = str(overlay.get("id", "<unknown>"))
    for selection in overlay.get("selections", []):
        if not isinstance(selection, dict):
            continue
        project_id = selection.get("project")
        project = project_by_id.get(str(project_id))
        if not project:
            errors.append(f"{overlay_id}: unknown selected project {project_id}")
            continue
        repo = project["repo"]
        learning = selection.get("learning")
        label = f"{owner}/{repo}"
        command = [
            "git",
            "ls-remote",
            f"https://github.com/{label}",
            f"refs/heads/{learning}",
        ]
        remote = _run(command, timeout=30)
        refs = _parse_ls_remote(remote.stdout)
        learning_ref = f"refs/heads/{learning}"
        learning_sha = refs.get(learning_ref)
        if remote.returncode != 0 or not learning_sha:
            errors.append(
                f"{overlay_id}: cannot freeze {label} {learning_ref}"
            )
            continue
        mapping_path = FRONTEND_APPLICATION_ANSWER_MAPPINGS.get(str(project_id))
        mapping_text: str | None = None
        if mapping_path:
            mapping_text, mapping_error = _remote_text(
                owner, repo, mapping_path, learning_sha
            )
            if mapping_error:
                errors.append(
                    f"{overlay_id}: {label}@{learning_sha} has unreadable answer "
                    f"mapping {mapping_path}: {mapping_error}"
                )
        for path in selection.get("practice_paths", []):
            endpoint = (
                f"repos/{owner}/{repo}/contents/{quote(path, safe='/')}"
                f"?ref={quote(learning_sha, safe='')}"
            )
            result = _run(["gh", "api", "--silent", endpoint], timeout=20)
            if result.returncode != 0:
                errors.append(
                    f"{overlay_id}: {label}@{learning_sha} is missing selected "
                    f"practice path {path}"
                )
            stable_id = Path(path).stem
            mapping_row = re.compile(
                rf"^\|\s*(?:{re.escape(stable_id)}|"
                rf"`{re.escape(stable_id)} / {re.escape(stable_id)}`)\s*\|\s*"
                r"`[0-9a-f]{8,40}`\s*\|\s*`[0-9a-f]{8,40}`\s*\|",
                re.MULTILINE,
            )
            if mapping_text is not None and not mapping_row.search(mapping_text):
                errors.append(
                    f"{overlay_id}: {label}@{learning_sha} answer mapping "
                    f"{mapping_path} lacks commit/parent metadata for {stable_id}"
                )
        final = _run(command, timeout=30)
        if final.returncode != 0 or _parse_ls_remote(final.stdout) != refs:
            errors.append(
                f"{overlay_id}: {label} learning ref changed during overlay verification"
            )

    portfolio = overlay.get("portfolio")
    if isinstance(portfolio, dict):
        project_id = str(portfolio.get("project", ""))
        project = project_by_id.get(project_id)
        if not project:
            errors.append(f"{overlay_id}: unknown Portfolio project {project_id}")
            return errors
        repo = project["repo"]
        label = f"{owner}/{repo}"
        release = str(portfolio.get("release", ""))
        learning = str(portfolio.get("learning", ""))
        template = str(portfolio.get("template", ""))
        patterns = (
            "refs/heads/main",
            f"refs/tags/{release}",
            f"refs/tags/{release}^{{}}",
            f"refs/heads/{learning}",
            f"refs/tags/{template}",
            f"refs/tags/{template}^{{}}",
        )
        command = ["git", "ls-remote", f"https://github.com/{label}", *patterns]
        remote = _run(command, timeout=30)
        refs = _parse_ls_remote(remote.stdout)
        if remote.returncode != 0:
            errors.append(f"{overlay_id}: cannot read Portfolio refs from {label}")
        else:
            main_sha = refs.get("refs/heads/main")
            release_tag = refs.get(f"refs/tags/{release}")
            release_sha = refs.get(f"refs/tags/{release}^{{}}")
            learning_sha = refs.get(f"refs/heads/{learning}")
            template_tag = refs.get(f"refs/tags/{template}")
            template_sha = refs.get(f"refs/tags/{template}^{{}}")
            if not main_sha:
                errors.append(f"{overlay_id}: {label} main is missing")
            if not release_tag or not release_sha or release_tag == release_sha:
                errors.append(
                    f"{overlay_id}: {label} release {release} must be annotated"
                )
            if main_sha and release_sha and main_sha != release_sha:
                errors.append(
                    f"{overlay_id}: {label} release {release} does not peel to main"
                )
            if not learning_sha:
                errors.append(
                    f"{overlay_id}: {label} learning branch {learning} is missing"
                )
            if not template_tag or not template_sha or template_tag == template_sha:
                errors.append(
                    f"{overlay_id}: {label} template {template} must be annotated"
                )
        final = _run(command, timeout=30)
        if final.returncode != 0 or _parse_ls_remote(final.stdout) != refs:
            errors.append(
                f"{overlay_id}: {label} refs changed during overlay verification"
            )
    return errors


def _central_link_targets(root: Path, owner: str) -> dict[str, set[str]]:
    pattern = re.compile(
        rf"https://github\.com/{re.escape(owner)}/central-notes/blob/main/"
        r"([^\s)#]+)(?:#([^\s)]+))?"
    )
    targets: dict[str, set[str]] = {}
    documents = [root / "README.md", *sorted((root / "tracks").glob("*.md"))]
    for document in documents:
        if not document.is_file():
            continue
        for path, fragment in pattern.findall(document.read_text(encoding="utf-8")):
            targets.setdefault(unquote(path), set())
            if fragment:
                targets[unquote(path)].add(unquote(fragment))
    return targets


def _check_remote_central_links(owner: str, root: Path, main_sha: str) -> list[str]:
    errors: list[str] = []
    for path, fragments in sorted(_central_link_targets(root, owner).items()):
        endpoint = (
            f"repos/{owner}/central-notes/contents/{quote(path, safe='/')}"
            f"?ref={quote(main_sha, safe='')}"
        )
        result = _run(["gh", "api", endpoint], timeout=20)
        if result.returncode != 0:
            errors.append(f"central-notes@{main_sha}: missing linked path {path}")
            continue
        try:
            payload = json.loads(result.stdout)
            content = base64.b64decode(payload["content"]).decode("utf-8")
        except (KeyError, ValueError, UnicodeDecodeError, json.JSONDecodeError):
            errors.append(f"central-notes@{main_sha}: unreadable linked path {path}")
            continue
        for fragment in sorted(fragments):
            anchor_count = _document_anchor_count(content, fragment)
            if anchor_count != 1:
                errors.append(
                    f"central-notes@{main_sha}: anchor #{fragment} in {path} must "
                    f"appear exactly once, found {anchor_count}"
                )
    return errors


def check_remote(data: dict[str, Any], root: Path) -> int:
    local_errors = validate_registry(data, root)
    if local_errors:
        for error in local_errors:
            print(f"ERROR local navigation: {error}", file=sys.stderr)
        print("remote navigation: BLOCKED by local navigation", file=sys.stderr)
        return 1
    if not shutil.which("gh") or not shutil.which("git"):
        print("BLOCK check-remote-navigation requires gh and git", file=sys.stderr)
        return 2
    auth = _run(["gh", "auth", "status"], timeout=15)
    if auth.returncode != 0:
        print("BLOCK authenticate with `gh auth login` for private access", file=sys.stderr)
        return 2
    owner = data.get("owner", "woopinbell")
    projects = data.get("projects", [])
    errors: list[str] = []
    project_by_id = {
        project["id"]: project
        for project in projects
        if isinstance(project, dict) and isinstance(project.get("id"), str)
    }
    overlays = [
        overlay
        for overlay in data.get("overlays", [])
        if isinstance(overlay, dict)
    ]
    overlay_start, overlay_start_errors = _overlay_ref_manifest(
        owner, overlays, project_by_id
    )
    errors.extend(overlay_start_errors)
    central_url = f"https://github.com/{owner}/central-notes"
    central_command = ["git", "ls-remote", central_url, "refs/heads/main"]
    central_remote = _run(central_command, timeout=30)
    central_refs = _parse_ls_remote(central_remote.stdout)
    central_main = central_refs.get("refs/heads/main")
    if central_remote.returncode != 0 or not central_main:
        print("BLOCK cannot freeze central-notes main SHA", file=sys.stderr)
        return 2
    with ThreadPoolExecutor(max_workers=min(6, len(projects) or 1)) as executor:
        futures = {
            executor.submit(_check_remote_project, owner, project): project
            for project in projects
        }
        for future in as_completed(futures):
            project = futures[future]
            try:
                project_errors = future.result()
            except (CurriculumError, subprocess.TimeoutExpired) as exc:
                project_errors = [f"{project.get('repo')}: remote check failed: {exc}"]
            if project_errors:
                errors.extend(project_errors)
                print(f"FAIL  {project.get('repo')}")
            else:
                print(f"PASS  {project.get('repo')}")
    for overlay in overlays:
        overlay_errors = _check_remote_overlay(owner, overlay, project_by_id)
        if overlay_errors:
            errors.extend(overlay_errors)
            print(f"FAIL  overlay {overlay.get('id')}")
        else:
            print(f"PASS  overlay {overlay.get('id')}")
    overlay_final, overlay_final_errors = _overlay_ref_manifest(
        owner, overlays, project_by_id
    )
    errors.extend(overlay_final_errors)
    if overlay_start != overlay_final:
        errors.append("overlay refs changed during the full remote verification run")
        print("FAIL  overlay ref snapshot")
    elif not overlay_start_errors and not overlay_final_errors:
        print("PASS  overlay ref snapshot")
    central_errors = _check_remote_central_links(owner, root, central_main)
    central_final = _run(central_command, timeout=30)
    if (
        central_final.returncode != 0
        or _parse_ls_remote(central_final.stdout) != central_refs
    ):
        central_errors.append("central-notes: main changed during remote verification")
    if central_errors:
        errors.extend(central_errors)
        print("FAIL  central-notes links")
    else:
        print("PASS  central-notes links")
    if errors:
        for error in sorted(errors):
            print(f"ERROR {error}", file=sys.stderr)
        print(f"remote navigation: FAIL ({len(errors)} errors)", file=sys.stderr)
        return 1
    print(f"remote navigation: PASS ({len(projects)} projects)")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    preflight_parser = subparsers.add_parser("preflight")
    preflight_parser.add_argument("--registry", type=Path, required=True)
    preflight_parser.add_argument("--track")
    preflight_parser.add_argument("--route")
    check_parser = subparsers.add_parser("check")
    check_parser.add_argument("--registry", type=Path, required=True)
    check_parser.add_argument("--root", type=Path, required=True)
    remote_parser = subparsers.add_parser("check-remote")
    remote_parser.add_argument("--registry", type=Path, required=True)
    remote_parser.add_argument("--root", type=Path, required=True)
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        data = load_registry(args.registry)
        if args.command == "preflight":
            return preflight(
                data,
                args.track,
                args.registry.resolve().parent.parent,
                args.route,
            )
        if args.command == "check-remote":
            return check_remote(data, args.root.resolve())
        errors = validate_registry(data, args.root.resolve())
    except CurriculumError as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        print(f"navigation: FAIL ({len(errors)} errors)", file=sys.stderr)
        return 1
    print(
        "navigation: PASS "
        f"({len(data['projects'])} projects, "
        f"{len(data.get('prerequisites', []))} prerequisites, "
        f"{len(data.get('assessments', []))} assessments, "
        f"{len(data.get('overlays', []))} overlays)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
