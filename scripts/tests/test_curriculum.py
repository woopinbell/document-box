import json
import base64
import io
import re
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

import curriculum  # noqa: E402


class RegistryFixture:
    def __init__(self, root: Path) -> None:
        self.root = root
        (root / "tracks").mkdir()
        (root / "README.md").write_text(
            "# document-box\n\n## 학습 시작\n\n[학습 시작](tracks/README.md)\n",
            encoding="utf-8",
        )
        (root / "tracks/README.md").write_text(
            "# Curriculum\n\n"
            "[application overlay](frontend-fast-track.md#route-frontend-application-bridge)\n\n"
            '<a id="공식-수행-범위"></a>\n'
            "## 필수 학습 범위\n\n"
            "프로젝트마다 연습문제 한 개만 필수다.\n"
            "나머지 연습문제는 선택 심화다.\n"
            "문제가 만들어졌던 시점의 코드와 현재 완성본을 구분한다.\n"
            "Document Box의 이 규칙이 우선한다.\n",
            encoding="utf-8",
        )
        self.projects = []
        self.assessments = []
        self.completions = []
        track_ids = {
            "42": [
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
            ],
            "frontend": [
                "frontend-foundations-training",
                "frontend-delivery-training",
                "cloud-launch-training",
                "frontend-reliability-training",
                "portfolio-site",
            ],
            "backend": [
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
            ],
        }
        documents = {track: [] for track in track_ids}
        for track, ids in track_ids.items():
            for index, node_id in enumerate(ids):
                doc = f"tracks/{track}.md"
                anchor = f"stage-{node_id}"
                release = "codex-5.7" if track == "42" else "release-v1"
                learning = f"learning/{release}"
                practice = (
                    "docs/practice-codex-5.7/README.md"
                    if track == "42"
                    else "docs/practice/README.md"
                )
                answer = (
                    "docs/commits-codex-5.7/README.md"
                    if track == "42"
                    else "docs/commits/README.md"
                )
                if node_id in curriculum.MIGRATED_42_PROJECTS:
                    release = curriculum.CURRENT_42_RELEASE
                    learning = curriculum.CURRENT_42_LEARNING
                    practice = curriculum.CURRENT_42_PRACTICE
                    answer = curriculum.CURRENT_42_ANSWER
                if node_id == "sportsbook-risk-service":
                    release = "risk-v1.0.2"
                    learning = "learning/risk-v1.0.2"
                    practice = "docs/practice-risk-v1.0.2/README.md"
                    answer = "docs/commits-risk-v1.0.2/README.md"
                if node_id == "frontend-foundations-training":
                    release = "foundations-v1.0.1"
                    learning = "learning/current"
                    practice = "docs/practice/README.md"
                    answer = "docs/commits/README.md"
                if node_id == "frontend-delivery-training":
                    release = "delivery-v1.0.1"
                    learning = "learning/current"
                    practice = "docs/practice/README.md"
                    answer = "docs/commits/README.md"
                if node_id == "cloud-launch-training":
                    release = "cloud-launch-v1.0.1"
                    learning = "learning/current"
                    practice = "docs/practice/README.md"
                    answer = "docs/commits/README.md"
                if node_id == "frontend-reliability-training":
                    release = "reliability-v1.0.1"
                    learning = "learning/current"
                    practice = "docs/practice/README.md"
                    answer = "docs/commits/README.md"
                if node_id == "portfolio-site":
                    release = "portfolio-v3.0.1"
                    learning = "learning/portfolio-v3.0.1"
                    practice = "docs/practice-portfolio-v3.0.1/README.md"
                    answer = "docs/commits-portfolio-v3.0.1/README.md"
                _, next_ids = curriculum.CANONICAL_EDGES[node_id]
                next_links = "".join(
                    f'[next](#stage-{next_id})\n' for next_id in next_ids
                )
                prev_ids, _ = curriculum.CANONICAL_EDGES[node_id]
                prior_links = "".join(
                    (
                        f'[prior](42.md#stage-{prev_id})\n'
                        if prev_id == "42-incident" and track != "42"
                        else f'[prior](#stage-{prev_id})\n'
                    )
                    for prev_id in prev_ids
                )
                join_marker = (
                    "세 갈래를 모두 완료한다.\n" if len(prev_ids) > 1 else ""
                )
                odds_handoffs = (
                    "[Spring Kafka](https://github.com/woopinbell/"
                    "sportsbook-orchestration/blob/learning/orchestration-v1/"
                    "notes/spring-kafka.md)\n"
                    "[Avro](https://github.com/woopinbell/"
                    "sportsbook-orchestration/blob/learning/orchestration-v1/"
                    "notes/avro.md)\n"
                    "Kafka·Avro의 정본은 Sportsbook 원본 notes다.\n"
                    if node_id == "sportsbook-odds-feed-service"
                    else ""
                )
                documents[track].append(
                    f'<a id="{anchor}"></a>\n## {node_id}\n'
                    f'[repo](https://github.com/woopinbell/{node_id})\n'
                    f'release `{release}`, learning `{learning}`\n'
                    f'[practice](https://github.com/woopinbell/{node_id}/blob/'
                    f'{learning}/{practice})\n'
                    f'[answer](https://github.com/woopinbell/{node_id}/blob/'
                    f'{learning}/{answer})\n'
                    '[Central](https://github.com/woopinbell/central-notes/blob/main/'
                    f'TRACK_SEQUENCE.md#{anchor})\n'
                    '[scope](README.md#공식-수행-범위)\n'
                    '- **시작 조건:** 앞 과제를 완료한다.\n'
                    '- **먼저 읽을 것:** Central 안내를 읽는다.\n'
                    '- **저장소와 학습 자료:** 저장소와 문제·해설 링크를 사용한다.\n'
                    '- **직접 해볼 것:** 문제 한 개를 직접 구현한다.\n'
                    '- **현재 완성본 확인:** 별도 작업 공간에서 검사한다.\n'
                    '- **완료 조건:** 두 코드 시점을 구분해 설명한다.\n'
                    '- **다음 과제:** 표시된 링크로 이동한다.\n'
                    f'{odds_handoffs}'
                    f'{join_marker}{prior_links}{next_links}'
                )
                project = {
                    "id": node_id,
                    "track": track,
                    "repo": node_id,
                    "release": release,
                    "learning": learning,
                    "doc": doc,
                    "anchor": anchor,
                    "practice": practice,
                    "answer": answer,
                    "sourceWindow": {
                        "start": "2025-01-01",
                        "end": "2025-01-31",
                    },
                    "prev": None,
                    "next": None,
                }
                if node_id in curriculum.EXTENDED_SOURCE_WINDOWS:
                    project["extensionEnd"] = "2025-02-15"
                    project["main_paths"] = list(
                        curriculum.REQUIRED_MAIN_PATHS[node_id]
                    )
                if node_id in curriculum.UNCHANGED_NAVIGATION_RELEASES:
                    project["main_backlink"] = False
                if node_id == "portfolio-site":
                    project["template"] = "template-v3.0.1"
                self.projects.append(project)
            (root / f"tracks/{track}.md").write_text(
                "\n".join(documents[track]), encoding="utf-8"
            )

        frontend_path = root / "tracks/frontend.md"
        frontend_path.write_text(
            "[application overlay](frontend-fast-track.md#route-frontend-application-bridge)\n\n"
            + frontend_path.read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        by_id = {project["id"]: project for project in self.projects}
        ids_42 = track_ids["42"]
        ids_frontend = track_ids["frontend"]
        ids_backend = track_ids["backend"]
        for node_id, project in by_id.items():
            prev_ids, next_ids = curriculum.CANONICAL_EDGES[node_id]
            project["prev"] = list(prev_ids) if len(prev_ids) > 1 else (
                prev_ids[0] if prev_ids else None
            )
            project["next"] = list(next_ids) if len(next_ids) > 1 else (
                next_ids[0] if next_ids else None
            )

        prerequisite = self._local_node(
            "linux-foundation",
            "42",
            "tracks/42.md",
            None,
            list(curriculum.CANONICAL_EDGES["linux-foundation"][1]),
        )
        path_42 = root / "tracks/42.md"
        path_42.write_text(
            '<a id="stage-linux-foundation"></a>\n'
            "## Linux/Git Foundations\n"
            "[Central](https://github.com/woopinbell/central-notes/blob/main/"
            "TRACK_SEQUENCE.md#stage-linux-foundation)\n"
            "- **시작 조건:** 준비를 마친다.\n"
            "- **먼저 읽을 것:** Central 안내를 읽는다.\n"
            "- **저장소와 학습 자료:** Central 실습 자료를 사용한다.\n"
            "- **직접 해볼 것:** Git 실습을 한다.\n"
            "- **현재 완성본 확인:** 빠른 확인을 실행한다.\n"
            "- **완료 조건:** 결과를 설명한다.\n"
            "- **다음 과제:** 세 갈래 중 하나를 고른다.\n"
            '[next](#stage-c-foundation)\n'
            '[next](#stage-cpp-foundation)\n'
            '[next](#stage-container-stack)\n\n'
            + path_42.read_text(encoding="utf-8"),
            encoding="utf-8",
        )

        incident = self._local_node(
            "42-incident",
            "42",
            "tracks/42.md",
            "pong-pong",
            [ids_frontend[0], ids_backend[0]],
        )
        frontend_transfer = self._local_node(
            "frontend-transfer",
            "frontend",
            "tracks/frontend.md",
            ids_frontend[-2],
            ids_frontend[-1],
        )
        web_regression = self._local_node(
            "web-production-regression",
            "frontend",
            "tracks/frontend.md",
            ids_frontend[-1],
            "frontend-complete",
        )
        backend_assessment = self._local_node(
            "backend-incident",
            "backend",
            "tracks/backend.md",
            ids_backend[-1],
            "backend-complete",
        )
        self.assessments.extend(
            (incident, frontend_transfer, web_regression, backend_assessment)
        )
        self.completions.extend(
            (
                self._local_node(
                    "frontend-complete",
                    "frontend",
                    "tracks/frontend.md",
                    "web-production-regression",
                    None,
                ),
                self._local_node(
                    "backend-complete",
                    "backend",
                    "tracks/backend.md",
                    "backend-incident",
                    None,
                ),
            )
        )

        for node in self.assessments + self.completions:
            path = root / node["doc"]
            with path.open("a", encoding="utf-8") as stream:
                stream.write(f'\n<a id="{node["anchor"]}"></a>\n## {node["id"]}\n')
                if node["id"] not in {"frontend-complete", "backend-complete"}:
                    stream.write(
                        "- **시작 조건:** 앞 단계를 마친다.\n"
                        "- **먼저 읽을 것:** 평가 안내를 읽는다.\n"
                        "- **저장소와 학습 자료:** 평가 자료를 사용한다.\n"
                        "- **직접 해볼 것:** 평가를 수행한다.\n"
                        "- **현재 완성본 확인:** 결과를 확인한다.\n"
                        "- **완료 조건:** 검사를 통과한다.\n"
                        "- **다음 과제:** 다음 링크로 이동한다.\n"
                    )
                if node["id"] == "42-incident":
                    stream.write(
                        "[frontend](frontend.md#stage-frontend-foundations-training)\n"
                        "[backend](backend.md#stage-backend-foundations-training)\n"
                        "[application overlay](frontend-fast-track.md#route-frontend-application-bridge)\n"
                    )
                elif node["next"]:
                    stream.write(f'[next](#stage-{node["next"]})\n')

        selections = []
        selected_links = []
        for project_id, paths in curriculum.FRONTEND_APPLICATION_PRACTICES.items():
            project = by_id[project_id]
            selections.append(
                {
                    "project": project_id,
                    "learning": project["learning"],
                    "practice_paths": list(paths),
                }
            )
            selected_links.append(
                f"[answer](https://github.com/woopinbell/{project['repo']}/"
                f"blob/{project['learning']}/{project['answer']})"
            )
            for path in paths:
                selected_links.append(
                    f"[selected](https://github.com/woopinbell/{project['repo']}/"
                    f"blob/{project['learning']}/{path})"
                )
        self.overlay = {
            "id": curriculum.FRONTEND_APPLICATION_OVERLAY_ID,
            "track": "frontend",
            "doc": "tracks/frontend-fast-track.md",
            "anchor": "route-frontend-application-bridge",
            "entry_after": "42-incident",
            "required_prior": ["web-boundary-inspector", "42-incident"],
            "outcome": "frontend-application-readiness",
            "grants_mastery": False,
            "resume_at": "frontend-delivery-training",
            "preflight_projects": list(curriculum.FRONTEND_APPLICATION_PREFLIGHT),
            "selections": selections,
            "portfolio": dict(curriculum.FRONTEND_APPLICATION_PORTFOLIO),
        }
        route_42_links = []
        for stage in curriculum.DISPLAY_SEQUENCES["42"]:
            if stage == "42-incident":
                central = (
                    "https://github.com/woopinbell/central-notes/blob/main/"
                    "assessments/42-incident/README.md#assessment-42-incident"
                )
            else:
                central = (
                    "https://github.com/woopinbell/central-notes/blob/main/"
                    f"TRACK_SEQUENCE.md#stage-{stage}"
                )
            route_42_links.append(
                f"[central]({central}) [card](42.md#stage-{stage})"
            )
        (root / "tracks/frontend-fast-track.md").write_text(
            '<a id="route-frontend-application-bridge"></a>\n'
            "# Frontend application bridge\n\n"
            "`frontend-application-readiness`\n"
            "`grants_mastery=false`\n"
            "`make preflight ROUTE=frontend-application-bridge`\n"
            "[prior](42.md#stage-42-incident)\n"
            + "\n".join(route_42_links)
            + "\n"
            + "\n".join(selected_links)
            + "\n[portfolio](https://github.com/woopinbell/portfolio-site)\n"
            "`template-v3.0.1` `portfolio-v3.0.1` "
            "`learning/portfolio-v3.0.1`\n"
            "[resume](frontend.md#stage-frontend-delivery-training)\n",
            encoding="utf-8",
        )

        self.data = {
            "version": 4,
            "owner": "woopinbell",
            "entry": "linux-foundation",
            "practice_policy": dict(curriculum.PRACTICE_POLICY),
            "projects": self.projects,
            "prerequisites": [prerequisite],
            "assessments": self.assessments,
            "completions": self.completions,
            "overlays": [self.overlay],
            "branches": [
                {
                    "from": "linux-foundation",
                    "choices": [
                        "c-foundation",
                        "cpp-foundation",
                        "container-stack",
                    ],
                    "join": "web-boundary-inspector",
                    "requires": [
                        "stack-sort",
                        "irc-relay-server",
                        "container-stack",
                    ],
                },
                {
                    "from": "42-incident",
                    "choices": [
                        "frontend-foundations-training",
                        "backend-foundations-training",
                    ],
                    "join": None,
                    "requires": [],
                }
            ],
        }

    @staticmethod
    def _local_node(node_id, track, doc, prev, next_id):
        return {
            "id": node_id,
            "track": track,
            "doc": doc,
            "anchor": f"stage-{node_id}",
            "prev": prev,
            "next": next_id,
        }


class CurriculumValidationTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.fixture = RegistryFixture(self.root)

    def tearDown(self):
        self.temp.cleanup()

    def test_valid_three_track_branch_passes(self):
        self.assertEqual(
            curriculum.validate_registry(self.fixture.data, self.root), []
        )

    def test_registry_version_four_is_required(self):
        self.fixture.data["version"] = 1
        errors = curriculum.validate_registry(self.fixture.data, self.root)
        self.assertTrue(any("registry version must be 4" in error for error in errors))

    def test_application_overlay_stays_outside_the_canonical_graph(self):
        canonical_ids = {
            node_id
            for sequence in curriculum.DISPLAY_SEQUENCES.values()
            for node_id in sequence
        }
        self.assertNotIn(curriculum.FRONTEND_APPLICATION_OVERLAY_ID, canonical_ids)
        incident = next(
            node
            for node in self.fixture.data["assessments"]
            if node["id"] == "42-incident"
        )
        self.assertNotIn(
            curriculum.FRONTEND_APPLICATION_OVERLAY_ID,
            curriculum._ids(incident["next"]),
        )
        self.assertEqual(
            curriculum.validate_registry(self.fixture.data, self.root), []
        )

    def test_application_overlay_cannot_grant_mastery_or_join_next_edges(self):
        self.fixture.overlay["grants_mastery"] = True
        incident = next(
            node
            for node in self.fixture.data["assessments"]
            if node["id"] == "42-incident"
        )
        incident["next"].append(curriculum.FRONTEND_APPLICATION_OVERLAY_ID)
        errors = curriculum.validate_registry(self.fixture.data, self.root)
        self.assertTrue(any("grants_mastery=false" in error for error in errors))
        self.assertTrue(any("unknown next node" in error for error in errors))
        self.assertTrue(any("canonical next" in error for error in errors))

    def test_application_overlay_requires_reviewed_practices_and_delivery_resume(self):
        self.fixture.overlay["resume_at"] = "portfolio-site"
        self.fixture.overlay["outcome"] = "frontend-complete"
        self.fixture.overlay["selections"][0]["practice_paths"] = [
            "docs/practice/039.md"
        ]
        errors = curriculum.validate_registry(self.fixture.data, self.root)
        self.assertTrue(any("resume the canonical track" in error for error in errors))
        self.assertTrue(any("outcome must be" in error for error in errors))
        self.assertTrue(any("reviewed hands-on scope" in error for error in errors))

    def test_application_overlay_document_chain_and_markers_are_required(self):
        path = self.root / "tracks/frontend-fast-track.md"
        text = path.read_text(encoding="utf-8")
        text = text.replace("`grants_mastery=false`", "mastery maybe", 1)
        text = text.replace(
            "[resume](frontend.md#stage-frontend-delivery-training)",
            "resume later",
            1,
        )
        path.write_text(text, encoding="utf-8")
        errors = curriculum.validate_registry(self.fixture.data, self.root)
        self.assertTrue(any("grants_mastery=false" in error for error in errors))
        self.assertTrue(
            any("stage-frontend-delivery-training" in error for error in errors)
        )

    def test_empty_application_overlay_section_still_fails_markers(self):
        path = self.root / "tracks/frontend-fast-track.md"
        anchor = '<a id="route-frontend-application-bridge"></a>'
        path.write_text(anchor, encoding="utf-8")
        errors = curriculum.validate_registry(self.fixture.data, self.root)
        self.assertTrue(any("frontend-application-readiness" in error for error in errors))
        self.assertTrue(any("stage-frontend-delivery-training" in error for error in errors))

    def test_42_incident_card_must_offer_the_application_overlay(self):
        path = self.root / "tracks/42.md"
        text = path.read_text(encoding="utf-8").replace(
            "](frontend-fast-track.md#route-frontend-application-bridge)",
            "](frontend-fast-track.md#wrong-route)",
            1,
        )
        path.write_text(text, encoding="utf-8")
        errors = curriculum.validate_registry(self.fixture.data, self.root)
        self.assertTrue(any("tracks/42.md is missing" in error for error in errors))

    def test_repository_registry_and_current_cards_pass(self):
        repository_root = SCRIPT_DIR.parent
        data = json.loads(
            (repository_root / "tracks/curriculum.json").read_text(encoding="utf-8")
        )
        self.assertEqual(curriculum.validate_registry(data, repository_root), [])

    def test_registry_source_windows_match_the_approved_ledger(self):
        repository_root = SCRIPT_DIR.parent
        data = json.loads(
            (repository_root / "tracks/curriculum.json").read_text(encoding="utf-8")
        )
        ledger = (repository_root / "legacy-exceptions.md").read_text(
            encoding="utf-8"
        )
        rows = re.findall(
            r"^\| (42|Frontend|Backend) \| `([^`]+)` \| "
            r"(\d{4}-\d{2}-\d{2})–(\d{4}-\d{2}-\d{2}) \| "
            r"(—|\d{4}-\d{2}-\d{2}) \|$",
            ledger,
            re.MULTILINE,
        )
        expected = {
            project_id: {
                "track": track.lower(),
                "sourceWindow": {"start": start, "end": end},
                **({"extensionEnd": extension} if extension != "—" else {}),
            }
            for track, project_id, start, end, extension in rows
        }
        actual = {
            project["id"]: {
                "track": project["track"],
                "sourceWindow": project["sourceWindow"],
                **(
                    {"extensionEnd": project["extensionEnd"]}
                    if "extensionEnd" in project
                    else {}
                ),
            }
            for project in data["projects"]
        }
        self.assertEqual(len(rows), 30)
        self.assertEqual(len(expected), 30)
        self.assertEqual(actual, expected)

    def test_source_window_shape_order_and_extension_scope_are_enforced(self):
        project = self.fixture.data["projects"][0]
        project["sourceWindow"] = {"start": "2025-02-01", "end": "2025-01-01"}
        project["extensionEnd"] = "2024-12-31"
        ordinary = next(
            item
            for item in self.fixture.data["projects"]
            if item["id"] == "format-printer"
        )
        ordinary["extensionEnd"] = "2025-02-15"
        errors = curriculum.validate_registry(self.fixture.data, self.root)
        self.assertTrue(any("sourceWindow start must not exceed end" in e for e in errors))
        self.assertTrue(any("extensionEnd must be later" in e for e in errors))
        self.assertTrue(any("only allowed for the three new" in e for e in errors))

    def test_main_paths_are_safe_and_unique(self):
        project = self.fixture.data["projects"][0]
        project["main_paths"] = ["README.md", "README.md", "../DESIGN.md"]
        errors = curriculum.validate_registry(self.fixture.data, self.root)
        self.assertTrue(any("main_paths must not contain duplicates" in e for e in errors))
        self.assertTrue(any("must be a safe repository-relative path" in e for e in errors))
        self.assertTrue(any("main_paths must be exactly README.md, DESIGN.md" in e for e in errors))

    def test_unchanged_backlink_exception_is_explicit_and_scoped(self):
        by_id = {project["id"]: project for project in self.fixture.data["projects"]}
        del by_id["c-foundation"]["main_backlink"]
        by_id["cloud-launch-training"]["main_backlink"] = False
        errors = curriculum.validate_registry(self.fixture.data, self.root)
        self.assertTrue(
            any(
                "c-foundation: unchanged navigation release" in error
                for error in errors
            )
        )
        self.assertTrue(
            any(
                "cloud-launch-training: only an explicitly unchanged" in error
                for error in errors
            )
        )

    def test_github_slug_preserves_meaningful_hyphens(self):
        self.assertEqual(
            curriculum._github_slug("C 언어 (C99) 학습 가이드 - small-shell"),
            "c-언어-c99-학습-가이드---small-shell",
        )

    def test_duplicate_repository_and_wrong_count_are_rejected(self):
        self.fixture.data["projects"][1]["repo"] = self.fixture.data["projects"][0][
            "repo"
        ]
        self.fixture.data["projects"].pop()
        errors = curriculum.validate_registry(self.fixture.data, self.root)
        self.assertTrue(any("exactly 30" in error for error in errors))
        self.assertTrue(any("appears more than once" in error for error in errors))

    def test_asymmetric_edge_is_rejected(self):
        self.fixture.data["projects"][1]["prev"] = None
        errors = curriculum.validate_registry(self.fixture.data, self.root)
        self.assertTrue(any("reverse prev edge is missing" in error for error in errors))

    def test_symmetric_but_noncanonical_order_is_rejected(self):
        by_id = {node["id"]: node for node in self.fixture.data["projects"]}
        formatter = by_id["format-printer"]
        signal = by_id["signal-message-bus"]
        thread = by_id["thread-dining"]
        shell = by_id["small-shell"]
        formatter["next"] = "thread-dining"
        thread["prev"] = "format-printer"
        thread["next"] = "signal-message-bus"
        signal["prev"] = "thread-dining"
        signal["next"] = "small-shell"
        shell["prev"] = "signal-message-bus"
        errors = curriculum.validate_registry(self.fixture.data, self.root)
        self.assertTrue(any("canonical next" in error for error in errors))

    def test_missing_next_link_in_card_is_rejected(self):
        path = self.root / "tracks/42.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "[next](#stage-c-foundation)", "next: c-foundation", 1
            ),
            encoding="utf-8",
        )
        errors = curriculum.validate_registry(self.fixture.data, self.root)
        self.assertTrue(any("missing next link" in error for error in errors))

    def test_project_card_requires_exact_central_stage_handoff(self):
        path = self.root / "tracks/42.md"
        expected = (
            "https://github.com/woopinbell/central-notes/blob/main/"
            "TRACK_SEQUENCE.md#stage-format-printer"
        )
        path.write_text(
            path.read_text(encoding="utf-8").replace(expected, expected + "-wrong", 1),
            encoding="utf-8",
        )
        errors = curriculum.validate_registry(self.fixture.data, self.root)
        self.assertTrue(
            any("format-printer: current stage card is missing exact" in error for error in errors)
        )

    def test_project_card_rejects_repo_and_corpus_target_suffixes(self):
        path = self.root / "tracks/42.md"
        text = path.read_text(encoding="utf-8")
        text = text.replace(
            "https://github.com/woopinbell/format-printer)",
            "https://github.com/woopinbell/format-printer-wrong)",
            1,
        )
        text = text.replace(
            "docs/practice/README.md)",
            "docs/practice/README.md-wrong)",
            1,
        )
        text = text.replace(
            "docs/commits/README.md)",
            "docs/commits/README.md-wrong)",
            1,
        )
        path.write_text(text, encoding="utf-8")
        errors = curriculum.validate_registry(self.fixture.data, self.root)
        exact_target_errors = [error for error in errors if "missing exact target" in error]
        self.assertEqual(len(exact_target_errors), 3)

    def test_project_card_requires_exact_ref_tokens(self):
        path = self.root / "tracks/42.md"
        text = path.read_text(encoding="utf-8")
        text = text.replace("`v1.0.0`", "v1.0.0", 1)
        text = text.replace("`learning/current`", "learning/current", 1)
        path.write_text(text, encoding="utf-8")
        errors = curriculum.validate_registry(self.fixture.data, self.root)
        exact_ref_errors = [error for error in errors if "missing exact ref" in error]
        self.assertEqual(len(exact_ref_errors), 2)

    def test_practice_scope_policy_is_explicit(self):
        self.fixture.data["practice_policy"]["mastery"] = "all-provided"
        path = self.root / "tracks/README.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "프로젝트마다 연습문제 한 개만 필수다.",
                "프로젝트마다 모든 연습문제가 필수다.",
            ).replace(
                "문제가 만들어졌던 시점의 코드와 현재 완성본을 구분한다.",
                "한 시점의 코드만 확인한다.",
            ).replace(
                "Document Box의 이 규칙이 우선한다.",
                "프로젝트 문구가 우선한다.",
            ),
            encoding="utf-8",
        )
        errors = curriculum.validate_registry(self.fixture.data, self.root)
        self.assertTrue(any("practice_policy must require" in error for error in errors))
        self.assertGreaterEqual(
            sum("canonical practice scope marker" in error for error in errors),
            3,
        )

    def test_each_project_card_links_canonical_practice_scope(self):
        path = self.root / "tracks/42.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "](README.md#공식-수행-범위)",
                "](README.md#wrong-scope)",
                1,
            ),
            encoding="utf-8",
        )
        errors = curriculum.validate_registry(self.fixture.data, self.root)
        self.assertTrue(any("missing canonical practice scope" in error for error in errors))

    def test_each_project_card_has_beginner_action_sections(self):
        path = self.root / "tracks/42.md"
        text = path.read_text(encoding="utf-8")
        text = text.replace("**먼저 읽을 것:**", "**읽기:**", 1)
        text = text.replace("**직접 해볼 것:**", "**실습:**", 1)
        text = text.replace("**현재 완성본 확인:**", "**검사:**", 1)
        path.write_text(text, encoding="utf-8")
        errors = curriculum.validate_registry(self.fixture.data, self.root)
        self.assertEqual(
            sum("missing the learner action marker" in error for error in errors),
            3,
        )

    def test_linux_split_and_web_join_are_exact(self):
        by_id = {
            node["id"]: node
            for group in ("prerequisites", "projects", "assessments", "completions")
            for node in self.fixture.data[group]
        }
        self.assertEqual(
            curriculum._ids(by_id["linux-foundation"]["next"]),
            ["c-foundation", "cpp-foundation", "container-stack"],
        )
        self.assertEqual(
            curriculum._ids(by_id["web-boundary-inspector"]["prev"]),
            ["stack-sort", "irc-relay-server", "container-stack"],
        )

    def test_web_join_requires_all_three_prior_links_and_plain_marker(self):
        path = self.root / "tracks/42.md"
        text = path.read_text(encoding="utf-8")
        text = text.replace("세 갈래를 모두 완료한다.", "앞 과제를 완료한다.", 1)
        text = text.replace("[prior](#stage-irc-relay-server)", "irc 완료", 1)
        path.write_text(text, encoding="utf-8")
        errors = curriculum.validate_registry(self.fixture.data, self.root)
        self.assertTrue(any("every prior lane is required" in error for error in errors))
        self.assertTrue(any("missing required prior link" in error for error in errors))

    def test_linux_branch_contract_is_required(self):
        self.fixture.data["branches"] = self.fixture.data["branches"][1:]
        errors = curriculum.validate_registry(self.fixture.data, self.root)
        self.assertTrue(any("linux-foundation and 42-incident" in error for error in errors))

    def test_beginner_documents_reject_retired_jargon(self):
        path = self.root / "tracks/frontend.md"
        path.write_text(
            path.read_text(encoding="utf-8") + "\nClean release gate\n",
            encoding="utf-8",
        )
        errors = curriculum.validate_registry(self.fixture.data, self.root)
        self.assertTrue(any("uses learner-facing jargon" in error for error in errors))

    def test_odds_card_uses_original_kafka_and_avro_handoffs(self):
        path = self.root / "tracks/backend.md"
        text = path.read_text(encoding="utf-8")
        text = text.replace("[Spring Kafka]", "[Kafka]", 1)
        text = text.replace("[Avro]", "[Schema]", 1)
        text = text.replace(
            "Kafka·Avro의 정본은 Sportsbook 원본 notes다.",
            "Kafka 관련 index를 따른다.",
            1,
        )
        path.write_text(text, encoding="utf-8")
        errors = curriculum.validate_registry(self.fixture.data, self.root)
        self.assertEqual(
            sum("missing the original Sportsbook" in error for error in errors),
            2,
        )
        self.assertTrue(any("identify the original Sportsbook" in error for error in errors))

    def test_completion_cannot_form_a_cycle(self):
        frontend_assessment = next(
            node
            for node in self.fixture.data["assessments"]
            if node["id"] == "web-production-regression"
        )
        frontend_completion = next(
            node
            for node in self.fixture.data["completions"]
            if node["id"] == "frontend-complete"
        )
        frontend_assessment["prev"] = ["portfolio-site", "frontend-complete"]
        frontend_completion["next"] = "web-production-regression"
        errors = curriculum.validate_registry(self.fixture.data, self.root)
        self.assertTrue(any("completion must be a terminal" in error for error in errors))
        self.assertTrue(any("cycle detected" in error for error in errors))

    def test_extension_before_incident_is_rejected(self):
        first_frontend = next(
            project
            for project in self.fixture.data["projects"]
            if project["id"] == "frontend-foundations-training"
        )
        first_frontend["prev"] = "format-printer"
        first_42 = self.fixture.data["projects"][0]
        first_42["next"] = [first_42["next"], first_frontend["id"]]
        errors = curriculum.validate_registry(self.fixture.data, self.root)
        self.assertTrue(any("reachable before 42 incident" in error for error in errors))

    def test_single_learning_cta_is_required(self):
        (self.root / "README.md").write_text(
            "## 학습 시작\n\n[전체 지도](tracks/README.md)\n"
            "[학습 시작](tracks/README.md)\n",
            encoding="utf-8",
        )
        errors = curriculum.validate_registry(self.fixture.data, self.root)
        self.assertTrue(any("exactly one" in error for error in errors))

    def test_competing_learning_link_is_rejected(self):
        (self.root / "README.md").write_text(
            "## 학습 시작\n\n[전체 지도](tracks/README.md)\n"
            "[competing](tracks/42.md)\n",
            encoding="utf-8",
        )
        errors = curriculum.validate_registry(self.fixture.data, self.root)
        self.assertTrue(any("exactly one" in error for error in errors))

    def test_missing_document_anchor_is_rejected(self):
        self.fixture.data["projects"][0]["anchor"] = "stage-does-not-exist"
        errors = curriculum.validate_registry(self.fixture.data, self.root)
        self.assertTrue(any("anchor #stage-does-not-exist" in error for error in errors))

    def test_missing_required_assessment_is_rejected(self):
        self.fixture.data["assessments"] = [
            node
            for node in self.fixture.data["assessments"]
            if node["id"] != "frontend-transfer"
        ]
        errors = curriculum.validate_registry(self.fixture.data, self.root)
        self.assertTrue(any("assessment nodes must be exactly" in error for error in errors))

    def test_linux_foundation_prerequisite_is_required(self):
        self.fixture.data["prerequisites"] = []
        errors = curriculum.validate_registry(self.fixture.data, self.root)
        self.assertTrue(
            any("prerequisite nodes must contain exactly linux-foundation" in error for error in errors)
        )
        self.assertTrue(any("entry node does not exist" in error for error in errors))

    def test_current_42_and_risk_refs_are_pinned(self):
        by_id = {project["id"]: project for project in self.fixture.data["projects"]}
        by_id["format-printer"]["release"] = "codex-5.6.1"
        by_id["sportsbook-risk-service"]["learning"] = "learning/risk-v1.0.1"
        errors = curriculum.validate_registry(self.fixture.data, self.root)
        self.assertTrue(any("current 42 release must be v1.0.0" in error for error in errors))
        self.assertTrue(
            any(
                "sportsbook-risk-service: current learning must be learning/risk-v1.0.2"
                in error
                for error in errors
            )
        )

    def test_linux_foundation_rejects_retired_remote_link(self):
        path = self.root / "tracks/42.md"
        text = path.read_text(encoding="utf-8").replace(
            "## Linux/Git Foundations\n",
            "## Linux/Git Foundations\n"
            "[retired](https://github.com/woopinbell/linux-admin)\n",
            1,
        )
        path.write_text(text, encoding="utf-8")
        errors = curriculum.validate_registry(self.fixture.data, self.root)
        self.assertTrue(any("must not be an active remote link" in error for error in errors))

    def test_missing_local_markdown_link_is_rejected(self):
        (self.root / "README.md").write_text(
            "## 학습 시작\n\n[학습 시작](tracks/README.md)\n"
            "[missing](tracks/missing.md)\n",
            encoding="utf-8",
        )
        errors = curriculum.validate_registry(self.fixture.data, self.root)
        self.assertTrue(any("missing local link target" in error for error in errors))

    def test_absolute_local_link_escape_is_rejected(self):
        (self.root / "README.md").write_text(
            "## 학습 시작\n\n[학습 시작](tracks/README.md)\n"
            "[outside](/etc/hosts)\n",
            encoding="utf-8",
        )
        errors = curriculum.validate_registry(self.fixture.data, self.root)
        self.assertTrue(any("escapes repository" in error for error in errors))


class RemoteContractTest(unittest.TestCase):
    @staticmethod
    def _response(payload=None, returncode=0, stderr=""):
        stdout = "" if payload is None else (
            payload if isinstance(payload, str) else json.dumps(payload)
        )
        return subprocess.CompletedProcess([], returncode, stdout, stderr)

    @staticmethod
    def _learning_fixture(
        with_notes=True,
        roles=None,
        release_sha=None,
        learning_sha=None,
        exact_current_paths=False,
    ):
        release = release_sha or "1" * 40
        learning = learning_sha or "4" * 40
        if roles is None:
            roles = ("notes", "commits", "practice") if with_notes else (
                "commits",
                "practice",
            )
        shas = [str(index + 2) * 40 for index in range(len(roles))]
        shas[-1] = learning
        paths = {
            "learning": "docs/README.md",
            "notes": "docs/README.md",
            "commits": (
                "docs/commits/README.md"
                if exact_current_paths
                else "docs/commits-release-v1/README.md"
            ),
            "practice": (
                "docs/practice/README.md"
                if exact_current_paths
                else "docs/practice-release-v1/README.md"
            ),
            "interview": "docs/interview/README.md",
        }
        compare = {
            "status": "ahead",
            "ahead_by": len(roles),
            "behind_by": 0,
            "total_commits": len(roles),
            "merge_base_commit": {"sha": release},
            "commits": [{"sha": sha} for sha in shas],
        }
        details = {}
        parent = release
        for role, sha in zip(roles, shas):
            files = [{"filename": paths[role]}]
            if role == "commits" and "notes" not in roles:
                files.append({"filename": "docs/README.md"})
            if role == "interview":
                files.append({"filename": "docs/README.md"})
            details[sha] = {
                "sha": sha,
                "parents": [{"sha": parent}],
                "commit": {"message": f"docs({role}): publish {role}\n"},
                "files": files,
            }
            parent = sha
        return release, learning, roles, compare, details

    def _project_dispatcher(
        self,
        project,
        *,
        lightweight=False,
        supplemental=False,
        backlink=True,
        missing_template=False,
        main_drift=False,
        tag_drift=False,
        learning_drift=False,
        extra_branch=False,
        extra_tag=False,
        missing_learning_index=False,
        missing_design=False,
    ):
        navigation_freeze = curriculum.UNCHANGED_NAVIGATION_RELEASES.get(
            project["id"]
        )
        frozen_learning = curriculum.FROZEN_MONOLITHIC_LEARNING.get(project["id"])
        release_basis = (
            navigation_freeze["main"] if navigation_freeze else "1" * 40
        )
        learning_tip = (
            frozen_learning["learning"] if frozen_learning else "4" * 40
        )
        if main_drift:
            release_basis = "9" * 40
        if learning_drift:
            learning_tip = "8" * 40
        fixture_roles = (
            ("learning",)
            if frozen_learning
            else curriculum._learning_roles(
                project["id"], release_basis, learning_tip
            )
        )
        release_sha, learning_sha, roles, compare, details = self._learning_fixture(
            project["id"] not in curriculum.NO_PROJECT_NOTES,
            fixture_roles,
            release_basis,
            learning_tip,
            exact_current_paths=(project["learning"] == "learning/current"),
        )
        tag_sha = navigation_freeze["tag"] if navigation_freeze else "a" * 40
        if tag_drift:
            tag_sha = "7" * 40
        refs = [
            f"{release_sha}\trefs/heads/main",
            f"{tag_sha if not lightweight else release_sha}\trefs/tags/{project['release']}",
        ]
        if not lightweight:
            refs.append(f"{release_sha}\trefs/tags/{project['release']}^{{}}")
        refs.append(f"{learning_sha}\trefs/heads/{project['learning']}")
        if supplemental:
            refs.append(
                f"{'b' * 40}\trefs/heads/{project['learning']}-supplemental"
            )
        if extra_branch:
            refs.append(f"{'c' * 40}\trefs/heads/dev")
        if extra_tag:
            refs.append(f"{'d' * 40}\trefs/tags/old-release")
        template = project.get("template")
        if template and not missing_template:
            refs.extend(
                (
                    f"{'c' * 40}\trefs/tags/{template}",
                    f"{'d' * 40}\trefs/tags/{template}^{{}}",
                )
            )
        refs_text = "\n".join(refs)
        expected_backlink = (
            "https://github.com/woopinbell/document-box/blob/main/"
            f"{project['doc']}#{project['anchor']}"
        )
        readme = expected_backlink if backlink else "# no curriculum backlink\n"

        def dispatch(command, timeout=20, cwd=None):
            if command[:3] == ["gh", "repo", "view"]:
                return self._response(
                    {
                        "url": f"https://github.com/woopinbell/{project['repo']}",
                        "visibility": "PRIVATE",
                        "defaultBranchRef": {"name": "main"},
                    }
                )
            if command[:2] == ["git", "ls-remote"]:
                return self._response(refs_text)
            if command[:2] == ["gh", "api"]:
                endpoint = command[-1]
                if missing_learning_index and "/contents/docs/README.md?ref=" in endpoint:
                    return self._response(returncode=1, stderr="not found")
                if missing_design and "/contents/DESIGN.md?ref=" in endpoint:
                    return self._response(returncode=1, stderr="not found")
                if "/compare/" in endpoint:
                    return self._response(compare)
                if template and endpoint.endswith(f"/commits/{release_sha}"):
                    return self._response({"parents": [{"sha": "d" * 40}]})
                for sha, detail in details.items():
                    if endpoint.endswith(f"/commits/{sha}"):
                        return self._response(detail)
                if "/contents/README.md?ref=" in endpoint and "--silent" not in command:
                    return self._response(
                        {
                            "encoding": "base64",
                            "content": base64.b64encode(readme.encode()).decode(),
                        }
                    )
                if "/contents/docs/README.md?ref=" in endpoint:
                    return self._response(
                        {
                            "encoding": "base64",
                            "content": base64.b64encode(b"# learning index\n").decode(),
                        }
                    )
                return self._response()
            raise AssertionError(f"unexpected command: {command}")

        return dispatch

    @staticmethod
    def _application_overlay_fixture():
        projects = {
            "frontend-foundations-training": {
                "id": "frontend-foundations-training",
                "repo": "frontend-foundations-training",
                "learning": "learning/current",
            },
            "frontend-reliability-training": {
                "id": "frontend-reliability-training",
                "repo": "frontend-reliability-training",
                "learning": "learning/current",
            },
            "portfolio-site": {
                "id": "portfolio-site",
                "repo": "portfolio-site",
                "template": "template-v3.0.1",
                "release": "portfolio-v3.0.1",
                "learning": "learning/portfolio-v3.0.1",
            },
        }
        selections = [
            {
                "project": project_id,
                "learning": projects[project_id]["learning"],
                "practice_paths": list(paths),
            }
            for project_id, paths in curriculum.FRONTEND_APPLICATION_PRACTICES.items()
        ]
        overlay = {
            "id": curriculum.FRONTEND_APPLICATION_OVERLAY_ID,
            "selections": selections,
            "portfolio": dict(curriculum.FRONTEND_APPLICATION_PORTFOLIO),
        }
        return overlay, projects

    def _overlay_dispatcher(
        self,
        *,
        missing_path=None,
        missing_mapping_id=None,
        mapping_format="legacy",
        missing_mapping_field=None,
        drift=False,
    ):
        branch_shas = {
            "frontend-foundations-training": "1" * 40,
            "frontend-reliability-training": "2" * 40,
        }
        calls = {repo: 0 for repo in branch_shas}
        portfolio_refs = "\n".join(
            (
                f"{'3' * 40}\trefs/heads/main",
                f"{'a' * 40}\trefs/tags/portfolio-v3.0.1",
                f"{'3' * 40}\trefs/tags/portfolio-v3.0.1^{{}}",
                f"{'4' * 40}\trefs/heads/learning/portfolio-v3.0.1",
                f"{'b' * 40}\trefs/tags/template-v3.0.1",
                f"{'5' * 40}\trefs/tags/template-v3.0.1^{{}}",
            )
        )
        mapping_rows = []
        for paths in curriculum.FRONTEND_APPLICATION_PRACTICES.values():
            for path in paths:
                stable_id = Path(path).stem
                if stable_id == missing_mapping_id:
                    continue
                mapping_id = (
                    stable_id
                    if mapping_format == "legacy"
                    else f"`{stable_id} / {stable_id}`"
                )
                commit = f"`{'c' * 8}`"
                parent = f"`{'d' * 8}`"
                if stable_id == "041":
                    if missing_mapping_field == "stable-id":
                        mapping_id = (
                            "" if mapping_format == "legacy" else f"` / {stable_id}`"
                        )
                    elif missing_mapping_field == "commit":
                        commit = ""
                    elif missing_mapping_field == "parent":
                        parent = ""
                mapping_rows.append(
                    f"| {mapping_id} | {commit} | {parent} | phase |"
                )
        mapping_rows = "\n".join(mapping_rows)
        mapping_payload = {
            "encoding": "base64",
            "content": base64.b64encode(mapping_rows.encode()).decode(),
        }

        def dispatch(command, timeout=20, cwd=None):
            if command[:2] == ["git", "ls-remote"]:
                repo = command[2].rstrip("/").rsplit("/", 1)[-1]
                if repo == "portfolio-site":
                    return self._response(portfolio_refs)
                calls[repo] += 1
                sha = branch_shas[repo]
                if drift and repo == "frontend-foundations-training" and calls[repo] > 1:
                    sha = "9" * 40
                learning = command[-1]
                return self._response(f"{sha}\t{learning}")
            if command[:2] == ["gh", "api"]:
                endpoint = command[-1]
                if missing_path and missing_path in endpoint:
                    return self._response(returncode=1, stderr="not found")
                if "docs/commits/README.md" in endpoint:
                    return self._response(mapping_payload)
                return self._response()
            raise AssertionError(f"unexpected command: {command}")

        return dispatch

    def test_migrated_project_release_learning_and_exact_topology_pass(self):
        project = {
            "id": "format-printer",
            "repo": "format-printer",
            "release": "v1.0.0",
            "learning": "learning/current",
            "main_backlink": False,
            "practice": "docs/practice/README.md",
            "answer": "docs/commits/README.md",
            "doc": "tracks/42.md",
            "anchor": "stage-format-printer",
        }
        with patch.object(
            curriculum, "_run", side_effect=self._project_dispatcher(project)
        ):
            self.assertEqual(
                curriculum._check_remote_project("woopinbell", project), []
            )

        cases = (
            ({"extra_branch": True}, "branches must be exactly"),
            ({"extra_tag": True}, "tags must be exactly"),
        )
        for options, marker in cases:
            with self.subTest(marker=marker), patch.object(
                curriculum,
                "_run",
                side_effect=self._project_dispatcher(project, **options),
            ):
                errors = curriculum._check_remote_project("woopinbell", project)
            self.assertTrue(any(marker in error for error in errors), errors)

    def test_new_project_exact_topology_index_and_source_docs_are_enforced(self):
        project = {
            "id": "c-foundation",
            "repo": "c-foundation",
            "release": "v1.0.0",
            "learning": "learning/current",
            "main_backlink": False,
            "practice": "docs/practice/README.md",
            "answer": "docs/commits/README.md",
            "main_paths": ["README.md", "DESIGN.md"],
            "doc": "tracks/42.md",
            "anchor": "stage-c-foundation",
        }
        with patch.object(
            curriculum, "_run", side_effect=self._project_dispatcher(project)
        ):
            self.assertEqual(
                curriculum._check_remote_project("woopinbell", project), []
            )

        cases = (
            ({"extra_branch": True}, "branches must be exactly"),
            ({"extra_tag": True}, "tags must be exactly"),
            ({"missing_learning_index": True}, "missing learning index"),
            ({"missing_design": True}, "missing required path DESIGN.md"),
        )
        for options, marker in cases:
            with self.subTest(marker=marker), patch.object(
                curriculum,
                "_run",
                side_effect=self._project_dispatcher(project, **options),
            ):
                errors = curriculum._check_remote_project("woopinbell", project)
            self.assertTrue(any(marker in error for error in errors), errors)

    def test_migrated_frontend_delivery_rejects_extra_refs(self):
        project = {
            "id": "frontend-delivery-training",
            "repo": "frontend-delivery-training",
            "release": "delivery-v1.0.1",
            "learning": "learning/current",
            "practice": "docs/practice/README.md",
            "answer": "docs/commits/README.md",
            "doc": "tracks/frontend.md",
            "anchor": "stage-frontend-delivery-training",
        }
        with patch.object(
            curriculum, "_run", side_effect=self._project_dispatcher(project)
        ):
            self.assertEqual(
                curriculum._check_remote_project("woopinbell", project), []
            )

        cases = (
            ({"extra_branch": True}, "branches must be exactly"),
            ({"extra_tag": True}, "tags must be exactly"),
        )
        for options, marker in cases:
            with self.subTest(marker=marker), patch.object(
                curriculum,
                "_run",
                side_effect=self._project_dispatcher(project, **options),
            ):
                errors = curriculum._check_remote_project("woopinbell", project)
            self.assertTrue(any(marker in error for error in errors), errors)

    def test_migrated_cloud_launch_rejects_extra_refs(self):
        project = {
            "id": "cloud-launch-training",
            "repo": "cloud-launch-training",
            "release": "cloud-launch-v1.0.1",
            "learning": "learning/current",
            "practice": "docs/practice/README.md",
            "answer": "docs/commits/README.md",
            "doc": "tracks/frontend.md",
            "anchor": "stage-cloud-launch-training",
        }
        with patch.object(
            curriculum, "_run", side_effect=self._project_dispatcher(project)
        ):
            self.assertEqual(
                curriculum._check_remote_project("woopinbell", project), []
            )

        cases = (
            ({"extra_branch": True}, "branches must be exactly"),
            ({"extra_tag": True}, "tags must be exactly"),
        )
        for options, marker in cases:
            with self.subTest(marker=marker), patch.object(
                curriculum,
                "_run",
                side_effect=self._project_dispatcher(project, **options),
            ):
                errors = curriculum._check_remote_project("woopinbell", project)
            self.assertTrue(any(marker in error for error in errors), errors)

    def test_migrated_frontend_reliability_rejects_extra_refs(self):
        project = {
            "id": "frontend-reliability-training",
            "repo": "frontend-reliability-training",
            "release": "reliability-v1.0.1",
            "learning": "learning/current",
            "practice": "docs/practice/README.md",
            "answer": "docs/commits/README.md",
            "doc": "tracks/frontend.md",
            "anchor": "stage-frontend-reliability-training",
        }
        with patch.object(
            curriculum, "_run", side_effect=self._project_dispatcher(project)
        ):
            self.assertEqual(
                curriculum._check_remote_project("woopinbell", project), []
            )

        cases = (
            ({"extra_branch": True}, "branches must be exactly"),
            ({"extra_tag": True}, "tags must be exactly"),
        )
        for options, marker in cases:
            with self.subTest(marker=marker), patch.object(
                curriculum,
                "_run",
                side_effect=self._project_dispatcher(project, **options),
            ):
                errors = curriculum._check_remote_project("woopinbell", project)
            self.assertTrue(any(marker in error for error in errors), errors)

    def test_application_overlay_remote_paths_and_portfolio_refs_pass(self):
        overlay, projects = self._application_overlay_fixture()
        with patch.object(
            curriculum, "_run", side_effect=self._overlay_dispatcher()
        ):
            self.assertEqual(
                curriculum._check_remote_overlay("woopinbell", overlay, projects),
                [],
            )

    def test_application_overlay_accepts_both_answer_mapping_row_formats(self):
        overlay, projects = self._application_overlay_fixture()
        for mapping_format in ("legacy", "stable-pair"):
            with self.subTest(mapping_format=mapping_format), patch.object(
                curriculum,
                "_run",
                side_effect=self._overlay_dispatcher(
                    mapping_format=mapping_format
                ),
            ):
                self.assertEqual(
                    curriculum._check_remote_overlay(
                        "woopinbell", overlay, projects
                    ),
                    [],
                )

    def test_application_overlay_whole_run_manifest_detects_ref_drift(self):
        overlay, projects = self._application_overlay_fixture()
        dispatcher = self._overlay_dispatcher(drift=True)
        with patch.object(curriculum, "_run", side_effect=dispatcher):
            start, start_errors = curriculum._overlay_ref_manifest(
                "woopinbell", [overlay], projects
            )
            final, final_errors = curriculum._overlay_ref_manifest(
                "woopinbell", [overlay], projects
            )
        self.assertEqual(start_errors, [])
        self.assertEqual(final_errors, [])
        self.assertNotEqual(start, final)

    def test_application_overlay_missing_practice_and_ref_drift_are_rejected(self):
        overlay, projects = self._application_overlay_fixture()
        with patch.object(
            curriculum,
            "_run",
            side_effect=self._overlay_dispatcher(
                missing_path="docs/practice/041.md",
                drift=True,
            ),
        ):
            errors = curriculum._check_remote_overlay(
                "woopinbell", overlay, projects
            )
        self.assertTrue(any("missing selected practice path" in error for error in errors))
        self.assertTrue(any("changed during overlay verification" in error for error in errors))

    def test_application_overlay_missing_answer_metadata_is_rejected(self):
        overlay, projects = self._application_overlay_fixture()
        for mapping_format in ("legacy", "stable-pair"):
            for missing_field in ("stable-id", "commit", "parent"):
                with self.subTest(
                    mapping_format=mapping_format,
                    missing_field=missing_field,
                ), patch.object(
                    curriculum,
                    "_run",
                    side_effect=self._overlay_dispatcher(
                        mapping_format=mapping_format,
                        missing_mapping_field=missing_field,
                    ),
                ):
                    errors = curriculum._check_remote_overlay(
                        "woopinbell", overlay, projects
                    )
                self.assertTrue(
                    any(
                        "lacks commit/parent metadata for 041" in error
                        for error in errors
                    )
                )

    def test_lightweight_supplemental_and_missing_backlink_are_rejected(self):
        project = {
            "id": "format-printer",
            "repo": "format-printer",
            "release": "v1.0.0",
            "learning": "learning/current",
            "practice": "docs/practice/README.md",
            "answer": "docs/commits/README.md",
            "doc": "tracks/42.md",
            "anchor": "stage-format-printer",
        }
        with patch.object(
            curriculum,
            "_run",
            side_effect=self._project_dispatcher(
                project, lightweight=True, supplemental=True, backlink=False
            ),
        ):
            errors = curriculum._check_remote_project("woopinbell", project)
        self.assertTrue(any("not an annotated tag" in error for error in errors))
        self.assertTrue(any("supplemental current-release" in error for error in errors))
        self.assertTrue(any("lacks exact card backlink" in error for error in errors))

    def test_frozen_monolithic_learning_tip_drift_is_rejected(self):
        project = {
            "id": "format-printer",
            "repo": "format-printer",
            "release": "v1.0.0",
            "learning": "learning/current",
            "main_backlink": False,
            "practice": "docs/practice/README.md",
            "answer": "docs/commits/README.md",
            "doc": "tracks/42.md",
            "anchor": "stage-format-printer",
        }
        with patch.object(
            curriculum,
            "_run",
            side_effect=self._project_dispatcher(project, learning_drift=True),
        ):
            errors = curriculum._check_remote_project("woopinbell", project)
        self.assertTrue(
            any(
                "monolithic learning exception requires the exact frozen" in e
                for e in errors
            )
        )

    def test_unchanged_navigation_object_drift_is_rejected(self):
        project = {
            "id": "signal-message-bus",
            "repo": "signal-message-bus",
            "release": "v1.0.0",
            "learning": "learning/current",
            "main_backlink": False,
            "practice": "docs/practice/README.md",
            "answer": "docs/commits/README.md",
            "doc": "tracks/42.md",
            "anchor": "stage-signal-message-bus",
        }
        for drift in ({"main_drift": True}, {"tag_drift": True}):
            with self.subTest(drift=drift), patch.object(
                curriculum,
                "_run",
                side_effect=self._project_dispatcher(project, **drift),
            ):
                errors = curriculum._check_remote_project("woopinbell", project)
            self.assertTrue(
                any("unchanged navigation exception requires exact" in e for e in errors)
            )

    def test_portfolio_template_must_be_annotated(self):
        project = {
            "id": "portfolio-site",
            "repo": "portfolio-site",
            "release": "portfolio-v3.0.1",
            "learning": "learning/portfolio-v3.0.1",
            "practice": "docs/practice-portfolio-v3.0.1/README.md",
            "answer": "docs/commits-portfolio-v3.0.1/README.md",
            "doc": "tracks/frontend.md",
            "anchor": "stage-portfolio-site",
            "template": "template-v3.0.1",
        }
        with patch.object(
            curriculum,
            "_run",
            side_effect=self._project_dispatcher(project, missing_template=True),
        ):
            errors = curriculum._check_remote_project("woopinbell", project)
        self.assertTrue(any("template tag template-v3.0.1 is missing" in e for e in errors))

    def test_portfolio_main_must_follow_neutral_template(self):
        project = {
            "id": "portfolio-site",
            "repo": "portfolio-site",
            "release": "portfolio-v3.0.1",
            "learning": "learning/portfolio-v3.0.1",
            "practice": "docs/practice-portfolio-v3.0.1/README.md",
            "answer": "docs/commits-portfolio-v3.0.1/README.md",
            "doc": "tracks/frontend.md",
            "anchor": "stage-portfolio-site",
            "template": "template-v3.0.1",
        }
        dispatch = self._project_dispatcher(project)

        def wrong_parent(command, timeout=20, cwd=None):
            if command[:2] == ["gh", "api"] and command[-1].endswith(
                f"/commits/{'1' * 40}"
            ):
                return self._response({"parents": [{"sha": "e" * 40}]})
            return dispatch(command, timeout=timeout, cwd=cwd)

        with patch.object(curriculum, "_run", side_effect=wrong_parent):
            errors = curriculum._check_remote_project("woopinbell", project)
        self.assertTrue(any("one publication commit after" in error for error in errors))

    def test_learning_wrong_subject_and_source_path_are_rejected(self):
        release, learning, roles, compare, details = self._learning_fixture()
        commits_sha = compare["commits"][1]["sha"]
        details[commits_sha]["commit"]["message"] = "docs(practice): wrong order"
        details[commits_sha]["files"] = [{"filename": "src/server.c"}]
        errors = curriculum._validate_learning_history(
            "repo", release, learning, roles, compare, details
        )
        self.assertTrue(any("subject must start with docs(commits)" in e for e in errors))
        self.assertTrue(any("forbidden path 'src/server.c'" in e for e in errors))

    def test_learning_accepts_one_source_grounded_interview_publication(self):
        release, learning, roles, compare, details = self._learning_fixture(
            roles=("notes", "commits", "practice", "interview"),
            learning_sha="9" * 40,
            exact_current_paths=True,
        )
        errors = curriculum._validate_learning_history(
            "repo",
            release,
            learning,
            roles[:-1],
            compare,
            details,
            exact_current_paths=True,
        )
        self.assertEqual(errors, [])

        interview_sha = compare["commits"][-1]["sha"]
        details[interview_sha]["files"] = [
            {"filename": "docs/interview/README.md"}
        ]
        errors = curriculum._validate_learning_history(
            "repo",
            release,
            learning,
            roles[:-1],
            compare,
            details,
            exact_current_paths=True,
        )
        self.assertTrue(
            any("interview publication must change docs/README.md exactly once" in e for e in errors)
        )

    def test_learning_rejects_unrecognized_extra_publication(self):
        release, learning, roles, compare, details = self._learning_fixture(
            roles=("notes", "commits", "practice", "interview"),
            learning_sha="9" * 40,
            exact_current_paths=True,
        )
        interview_sha = compare["commits"][-1]["sha"]
        details[interview_sha]["commit"]["message"] = "docs(review): publish review\n"
        errors = curriculum._validate_learning_history(
            "repo",
            release,
            learning,
            roles[:-1],
            compare,
            details,
            exact_current_paths=True,
        )
        self.assertTrue(any("exactly 3 publication commits" in e for e in errors))

    def test_learning_without_project_notes_publishes_index_with_answers(self):
        for project_id in (
            "c-foundation",
            "buffered-line-reader",
            "cpp-foundation",
        ):
            self.assertEqual(
                curriculum._learning_roles(project_id),
                ("commits", "practice"),
            )
        self.assertTrue(
            curriculum._learning_path_allowed(
                "commits", "docs/README.md", allow_commits_index=True
            )
        )
        self.assertFalse(
            curriculum._learning_path_allowed("commits", "docs/README.md")
        )
        self.assertFalse(
            curriculum._learning_path_allowed(
                "commits", "src/library.c", allow_commits_index=True
            )
        )

        release, learning, roles, compare, details = self._learning_fixture(
            False, exact_current_paths=True
        )
        self.assertEqual(
            curriculum._validate_learning_history(
                "repo",
                release,
                learning,
                roles,
                compare,
                details,
                exact_current_paths=True,
            ),
            [],
        )

        first_sha = compare["commits"][0]["sha"]
        details[first_sha]["files"] = [
            file_entry
            for file_entry in details[first_sha]["files"]
            if file_entry["filename"] != "docs/README.md"
        ]
        errors = curriculum._validate_learning_history(
            "repo",
            release,
            learning,
            roles,
            compare,
            details,
            exact_current_paths=True,
        )
        self.assertTrue(any("must change docs/README.md exactly once" in e for e in errors))

        release, learning, roles, compare, details = self._learning_fixture(
            False, exact_current_paths=True
        )
        first_sha = compare["commits"][0]["sha"]
        details[first_sha]["files"].append(
            {"filename": "docs/commits-v1/README.md"}
        )
        errors = curriculum._validate_learning_history(
            "repo",
            release,
            learning,
            roles,
            compare,
            details,
            exact_current_paths=True,
        )
        self.assertTrue(any("forbidden path 'docs/commits-v1/README.md'" in e for e in errors))

        release, learning, roles, compare, details = self._learning_fixture(True)
        commits_sha = compare["commits"][1]["sha"]
        details[commits_sha]["files"].append({"filename": "docs/README.md"})
        errors = curriculum._validate_learning_history(
            "repo", release, learning, roles, compare, details
        )
        self.assertTrue(any("forbidden path 'docs/README.md'" in e for e in errors))

    def test_format_printer_monolithic_learning_exception_is_path_scoped(self):
        frozen = curriculum.FROZEN_MONOLITHIC_LEARNING["format-printer"]
        self.assertEqual(
            curriculum._learning_roles(
                "format-printer", frozen["main"], frozen["learning"]
            ),
            ("learning",),
        )
        self.assertEqual(
            curriculum._learning_roles("format-printer"),
            ("notes", "commits", "practice"),
        )
        self.assertEqual(
            curriculum._learning_roles("thread-dining"),
            ("notes", "commits", "practice"),
        )
        for path in (
            "docs/README.md",
            "docs/commits/001.md",
            "docs/practice/001.md",
            "notes/ar.md",
        ):
            self.assertTrue(curriculum._learning_path_allowed("learning", path))
        for path in (
            "Makefile",
            "docs/commits-v1/001.md",
            "docs/notes/index.md",
            "include/format.h",
            "notes-index.md",
            "src/format.c",
            "tests/test.c",
        ):
            self.assertFalse(curriculum._learning_path_allowed("learning", path))

    def test_learning_merge_and_wrong_tip_are_rejected(self):
        release, learning, roles, compare, details = self._learning_fixture(False)
        first = compare["commits"][0]["sha"]
        details[first]["parents"].append({"sha": "f" * 40})
        compare["commits"][-1]["sha"] = "e" * 40
        errors = curriculum._validate_learning_history(
            "repo", release, learning, roles, compare, details
        )
        self.assertTrue(any("must be linear" in e for e in errors))
        self.assertTrue(any("not the learning branch tip" in e for e in errors))

    def test_central_link_anchor_is_checked(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "tracks").mkdir()
            (root / "tracks/42.md").write_text(
                "[note](https://github.com/woopinbell/central-notes/blob/main/"
                "cs-foundations/README.md#학습-순서)\n",
                encoding="utf-8",
            )
            payload = json.dumps(
                {
                    "encoding": "base64",
                    "content": base64.b64encode(
                        "# CS Foundations\n\n## 학습 순서\n".encode("utf-8")
                    ).decode("ascii"),
                }
            )
            response = subprocess.CompletedProcess([], 0, payload, "")
            with patch.object(curriculum, "_run", return_value=response):
                self.assertEqual(
                    curriculum._check_remote_central_links(
                        "woopinbell", root, "9" * 40
                    ),
                    [],
                )
                command = curriculum._run.call_args.args[0]
                self.assertIn(f"ref={'9' * 40}", command[-1])

    def test_public_repository_is_a_preflight_block(self):
        response = self._response({"visibility": "PUBLIC"})
        with patch.object(curriculum, "_run", return_value=response):
            result = curriculum._github_access("woopinbell", "format-printer")
        self.assertEqual(result.level, "BLOCK")
        self.assertIn("expected PRIVATE", result.detail)

    def test_preflight_runs_navigation_first(self):
        data = {"projects": [{"track": "42", "repo": "format-printer"}]}
        with patch.object(
            curriculum, "validate_registry", return_value=["broken chain"]
        ), patch.object(curriculum, "_github_track_access") as access:
            output = io.StringIO()
            with redirect_stdout(output):
                result = curriculum.preflight(data, "42", Path("."))
        self.assertEqual(result, 1)
        self.assertIn("BLOCK navigation", output.getvalue())
        access.assert_not_called()

    def test_frontend_application_route_without_track_preflights_only_overlay_projects(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RegistryFixture(Path(temporary))
            pass_result = curriculum.Result("PASS", "tool", "available")
            access_results = [pass_result] * len(
                curriculum.FRONTEND_APPLICATION_PREFLIGHT
            )
            with patch.object(
                curriculum,
                "_github_track_access",
                return_value=access_results,
            ) as access, patch.object(
                curriculum, "_tool_result", return_value=pass_result
            ), patch.object(
                curriculum, "_compose_result"
            ) as compose, patch.object(
                curriculum.shutil,
                "which",
                side_effect=lambda name: f"/bin/{name}",
            ), patch.object(curriculum, "_run") as run:
                output = io.StringIO()
                with redirect_stdout(output):
                    result = curriculum.preflight(
                        fixture.data,
                        None,
                        Path(temporary),
                        curriculum.FRONTEND_APPLICATION_OVERLAY_ID,
                    )
            self.assertEqual(result, 0)
            selected = access.call_args.args[1]
            self.assertEqual(
                [project["id"] for project in selected],
                list(curriculum.FRONTEND_APPLICATION_PREFLIGHT),
            )
            compose.assert_not_called()
            run.assert_not_called()
            self.assertIn("does not grant curriculum mastery", output.getvalue())
            self.assertNotIn("cloud-launch-training", output.getvalue())

    def test_frontend_application_route_rejects_the_wrong_track(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = RegistryFixture(Path(temporary))
            output = io.StringIO()
            with redirect_stdout(output):
                result = curriculum.preflight(
                    fixture.data,
                    "backend",
                    Path(temporary),
                    curriculum.FRONTEND_APPLICATION_OVERLAY_ID,
                )
        self.assertEqual(result, 2)
        self.assertIn("belongs to frontend, not backend", output.getvalue())

    def test_browser_cache_never_claims_three_engine_pass(self):
        project = {"track": "frontend", "repo": "frontend-foundations-training"}
        data = {"owner": "woopinbell", "projects": [project]}
        pass_result = curriculum.Result("PASS", "tool", "available")
        with patch.object(curriculum, "validate_registry", return_value=[]), patch.object(
            curriculum, "_github_track_access", return_value=[pass_result]
        ), patch.object(curriculum, "_tool_result", return_value=pass_result), patch.object(
            curriculum, "_compose_result", return_value=pass_result
        ), patch.object(
            curriculum,
            "_run",
            return_value=self._response("Server: ready"),
        ):
            output = io.StringIO()
            with redirect_stdout(output):
                result = curriculum.preflight(data, "frontend", Path("."))
        self.assertEqual(result, 0)
        self.assertIn("WARN  Playwright Chromium/Firefox/WebKit", output.getvalue())
        self.assertNotIn("browser cache found", output.getvalue())


if __name__ == "__main__":
    unittest.main()
