import json
import base64
import io
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
            "### 공식 수행 범위\n\n"
            "대표 practice 한 개와 카드 전체 gate를 수행한다.\n"
            "나머지 practice는 release 전체를 더 깊게 재구성하려는 선택 심화다.\n"
            "Historical practice tree와 Clean release tree를 구분한다.\n"
            "현행 필수 범위에는 이 Document Box 규칙이 우선한다.\n",
            encoding="utf-8",
        )
        self.projects = []
        self.assessments = []
        self.completions = []
        track_ids = {
            "42": [
                "format-printer",
                "signal-message-bus",
                "thread-dining",
                "small-shell",
                "stack-sort",
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
                if node_id == "sportsbook-risk-service":
                    release = "risk-v1.0.2"
                    learning = "learning/risk-v1.0.2"
                    practice = "docs/practice-risk-v1.0.2/README.md"
                    answer = "docs/commits-risk-v1.0.2/README.md"
                if node_id == "frontend-foundations-training":
                    release = "foundations-v1.0.1"
                    learning = "learning/foundations-v1.0.1"
                    practice = "docs/practice-foundations-v1.0.1/README.md"
                    answer = "docs/commits-foundations-v1.0.1/README.md"
                if node_id == "frontend-reliability-training":
                    release = "reliability-v1.0.1"
                    learning = "learning/reliability-v1.0.1"
                    practice = "docs/practice-reliability-v1.0.1/README.md"
                    answer = "docs/commits-reliability-v1.0.1/README.md"
                if node_id == "portfolio-site":
                    release = "portfolio-v3.0.1"
                    learning = "learning/portfolio-v3.0.1"
                    practice = "docs/practice-portfolio-v3.0.1/README.md"
                    answer = "docs/commits-portfolio-v3.0.1/README.md"
                if track == "42":
                    next_id = ids[index + 1] if index + 1 < len(ids) else "42-incident"
                elif track == "frontend":
                    if index < 3:
                        next_id = ids[index + 1]
                    elif index == 3:
                        next_id = "frontend-transfer"
                    else:
                        next_id = "web-production-regression"
                else:
                    next_id = (
                        ids[index + 1]
                        if index + 1 < len(ids)
                        else "backend-incident"
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
                    '- Clean release gate: annotated release의 별도 clean worktree에서 검증한다.\n'
                    '- Historical 무자료 gate: 현재 practice 파일이 명시한 시작 tree에서 검증한다.\n'
                    '- 연결 설명: 두 tree의 경계를 설명한다.\n'
                    f'{odds_handoffs}'
                    f'[next](#stage-{next_id})\n'
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
                    "prev": None,
                    "next": None,
                }
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
        for ids in (ids_42, ids_frontend, ids_backend):
            for left, right in zip(ids, ids[1:]):
                by_id[left]["next"] = right
                by_id[right]["prev"] = left

        prerequisite = self._local_node(
            "linux-foundation",
            "42",
            "tracks/42.md",
            None,
            ids_42[0],
        )
        by_id[ids_42[0]]["prev"] = "linux-foundation"
        path_42 = root / "tracks/42.md"
        path_42.write_text(
            '<a id="stage-linux-foundation"></a>\n'
            "## Linux/Git Foundations\n"
            "[Central](https://github.com/woopinbell/central-notes/blob/main/"
            "TRACK_SEQUENCE.md#stage-linux-foundation)\n"
            f'[next](#stage-{ids_42[0]})\n\n'
            + path_42.read_text(encoding="utf-8"),
            encoding="utf-8",
        )

        incident = self._local_node(
            "42-incident",
            "42",
            "tracks/42.md",
            ids_42[-1],
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
        by_id[ids_42[-1]]["next"] = "42-incident"
        by_id[ids_frontend[0]]["prev"] = "42-incident"
        by_id[ids_backend[0]]["prev"] = "42-incident"
        by_id[ids_frontend[-2]]["next"] = "frontend-transfer"
        by_id[ids_frontend[-1]]["prev"] = "frontend-transfer"
        by_id[ids_frontend[-1]]["next"] = "web-production-regression"
        by_id[ids_backend[-1]]["next"] = "backend-incident"

        for node in self.assessments + self.completions:
            path = root / node["doc"]
            with path.open("a", encoding="utf-8") as stream:
                stream.write(f'\n<a id="{node["anchor"]}"></a>\n## {node["id"]}\n')
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
        for stage in curriculum.CANONICAL_SEQUENCES["42"]:
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
            "version": 2,
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
                    "from": "42-incident",
                    "choices": [
                        "frontend-foundations-training",
                        "backend-foundations-training",
                    ],
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

    def test_registry_version_two_is_required(self):
        self.fixture.data["version"] = 1
        errors = curriculum.validate_registry(self.fixture.data, self.root)
        self.assertTrue(any("registry version must be 2" in error for error in errors))

    def test_application_overlay_stays_outside_the_canonical_graph(self):
        canonical_ids = {
            node_id
            for sequence in curriculum.CANONICAL_SEQUENCES.values()
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

    def test_unchanged_backlink_exception_is_explicit_and_scoped(self):
        by_id = {project["id"]: project for project in self.fixture.data["projects"]}
        del by_id["cloud-launch-training"]["main_backlink"]
        by_id["format-printer"]["main_backlink"] = False
        errors = curriculum.validate_registry(self.fixture.data, self.root)
        self.assertTrue(
            any(
                "cloud-launch-training: unchanged navigation release" in error
                for error in errors
            )
        )
        self.assertTrue(
            any("format-printer: only an explicitly unchanged" in error for error in errors)
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
        self.assertTrue(any("exactly 27" in error for error in errors))
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
                "[next](#stage-format-printer)", "next: format-printer", 1
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
            "docs/practice-codex-5.7/README.md)",
            "docs/practice-codex-5.7/README.md-wrong)",
            1,
        )
        text = text.replace(
            "docs/commits-codex-5.7/README.md)",
            "docs/commits-codex-5.7/README.md-wrong)",
            1,
        )
        path.write_text(text, encoding="utf-8")
        errors = curriculum.validate_registry(self.fixture.data, self.root)
        exact_target_errors = [error for error in errors if "missing exact target" in error]
        self.assertEqual(len(exact_target_errors), 3)

    def test_project_card_requires_exact_ref_tokens(self):
        path = self.root / "tracks/42.md"
        text = path.read_text(encoding="utf-8")
        text = text.replace("`codex-5.7`", "codex-5.7", 1)
        text = text.replace("`learning/codex-5.7`", "learning/codex-5.7", 1)
        path.write_text(text, encoding="utf-8")
        errors = curriculum.validate_registry(self.fixture.data, self.root)
        exact_ref_errors = [error for error in errors if "missing exact ref" in error]
        self.assertEqual(len(exact_ref_errors), 2)

    def test_practice_scope_policy_is_explicit(self):
        self.fixture.data["practice_policy"]["mastery"] = "all-provided"
        path = self.root / "tracks/README.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "대표 practice 한 개",
                "모든 practice",
            ).replace(
                "Historical practice tree와 Clean release tree를 구분한다.",
                "하나의 tree에서 모든 gate를 실행한다.",
            ).replace(
                "현행 필수 범위에는 이 Document Box 규칙이 우선한다.",
                "project wrapper가 우선한다.",
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

    def test_each_project_card_separates_historical_and_release_gates(self):
        path = self.root / "tracks/42.md"
        text = path.read_text(encoding="utf-8")
        text = text.replace("Clean release gate:", "통합 gate:", 1)
        text = text.replace("Historical 무자료 gate:", "무자료 gate:", 1)
        text = text.replace("연결 설명:", "설명:", 1)
        path.write_text(text, encoding="utf-8")
        errors = curriculum.validate_registry(self.fixture.data, self.root)
        self.assertEqual(
            sum("missing the two-tree gate marker" in error for error in errors),
            3,
        )

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
        self.assertTrue(any("current 42 release must be codex-5.7" in error for error in errors))
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
    def _learning_fixture(with_notes=True):
        release = "1" * 40
        learning = "4" * 40
        roles = ("notes", "commits", "practice") if with_notes else (
            "commits",
            "practice",
        )
        shas = [str(index + 2) * 40 for index in range(len(roles))]
        shas[-1] = learning
        paths = {
            "notes": "docs/README.md",
            "commits": "docs/commits-release-v1/README.md",
            "practice": "docs/practice-release-v1/README.md",
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
            details[sha] = {
                "sha": sha,
                "parents": [{"sha": parent}],
                "commit": {"message": f"docs({role}): publish {role}\n"},
                "files": [{"filename": paths[role]}],
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
    ):
        release_sha, learning_sha, roles, compare, details = self._learning_fixture(
            project["id"] not in curriculum.NO_PROJECT_NOTES
        )
        tag_sha = "a" * 40
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
                return self._response()
            raise AssertionError(f"unexpected command: {command}")

        return dispatch

    @staticmethod
    def _application_overlay_fixture():
        projects = {
            "frontend-foundations-training": {
                "id": "frontend-foundations-training",
                "repo": "frontend-foundations-training",
                "learning": "learning/foundations-v1.0.1",
            },
            "frontend-reliability-training": {
                "id": "frontend-reliability-training",
                "repo": "frontend-reliability-training",
                "learning": "learning/reliability-v1.0.1",
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
        self, *, missing_path=None, missing_mapping_id=None, drift=False
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
        mapping_rows = "\n".join(
            f"| {Path(path).stem} | `{'c' * 8}` | `{'d' * 8}` | phase |"
            for paths in curriculum.FRONTEND_APPLICATION_PRACTICES.values()
            for path in paths
            if Path(path).stem != missing_mapping_id
        )
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
                if "docs/commits-codex-5.6/README.md" in endpoint:
                    return self._response(mapping_payload)
                return self._response()
            raise AssertionError(f"unexpected command: {command}")

        return dispatch

    def test_annotated_release_linear_learning_and_sha_paths_pass(self):
        project = {
            "id": "format-printer",
            "repo": "format-printer",
            "release": "codex-5.7",
            "learning": "learning/codex-5.7",
            "practice": "docs/practice-codex-5.7/README.md",
            "answer": "docs/commits-codex-5.7/README.md",
            "doc": "tracks/42.md",
            "anchor": "stage-format-printer",
        }
        with patch.object(
            curriculum, "_run", side_effect=self._project_dispatcher(project)
        ):
            self.assertEqual(
                curriculum._check_remote_project("woopinbell", project), []
            )

    def test_application_overlay_remote_paths_and_portfolio_refs_pass(self):
        overlay, projects = self._application_overlay_fixture()
        with patch.object(
            curriculum, "_run", side_effect=self._overlay_dispatcher()
        ):
            self.assertEqual(
                curriculum._check_remote_overlay("woopinbell", overlay, projects),
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
        with patch.object(
            curriculum,
            "_run",
            side_effect=self._overlay_dispatcher(missing_mapping_id="041"),
        ):
            errors = curriculum._check_remote_overlay(
                "woopinbell", overlay, projects
            )
        self.assertTrue(any("lacks commit/parent metadata for 041" in error for error in errors))

    def test_lightweight_supplemental_and_missing_backlink_are_rejected(self):
        project = {
            "id": "format-printer",
            "repo": "format-printer",
            "release": "codex-5.7",
            "learning": "learning/codex-5.7",
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
