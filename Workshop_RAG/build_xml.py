"""SDG Report 2025 (PDF) → 계층 XML 변환.

설계 원칙 — 글자를 읽지 말고 조판을 읽는다
-------------------------------------------------
이 보고서는 구조를 이미 조판에 담고 있다. 편집자가 소제목을 GothamBold
11pt로, 본문을 Whitney 9pt로 지정해 두었다. 따라서 "이 줄이 소제목인가"를
문자열 규칙으로 추측할 필요가 없다. 지정된 서체를 그대로 읽으면 된다.

이전 판본은 텍스트만 보고 규칙으로 추론했다. 마침표가 없고 22단어 이하면
소제목으로 간주했는데, 그 결과 도표 축 라벨('Oceania*')·줄바꿈에서 잘린
캡션('Zealand')·조판 지시문이 모두 소제목으로 승격되어 143개 중 42개가
오분류였다. 규칙을 정교하게 다듬어도 12개가 남았고, 그 과정에서 본문
441단어짜리 진짜 소제목을 잃기도 했다. 텍스트만으로는 원리적으로
구별할 수 없는 경우가 있기 때문이다 — 줄바꿈에서 잘린 본문 문장과
소제목은 둘 다 마침표가 없고 길이도 비슷하다.

조판 정보를 쓰면 이 문제 자체가 사라진다.

조판 지도 (Goal 1~17 구간에서 실측)
-------------------------------------------------
    Gotham-Black   16pt   Goal 제목
    GothamBold     11pt   소제목            ← 우리가 찾는 것
    Whitney-Book    9pt   본문 문단          ← 우리가 찾는 것
    Whitney-Bold    9pt   본문 (강조 도입부)
    Whitney-*Italic 9pt   본문 (이탤릭)
    Whitney-Semibold 8.5pt 사진 캡션         ← 제외
    Whitney-Semibold 7.8~9.6pt 도표 제목     ← 제외
    Whitney-Medium/Book 5.2~7.5pt 도표 숫자·라벨 ← 제외
    Gotham-Black    8pt   머리말·쪽번호       ← 제외

사용법:  python build_xml.py <입력 PDF> <출력 XML>
"""

from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:  # pragma: no cover
    sys.exit("PyMuPDF가 필요합니다:  pip install pymupdf")


REPORT_TITLE = "The Sustainable Development Goals Report 2025"
REPORT_YEAR = "2025"

GOAL_NAMES: dict[int, str] = {
    1: "No poverty",
    2: "Zero hunger",
    3: "Good health and well-being",
    4: "Quality education",
    5: "Gender equality",
    6: "Clean water and sanitation",
    7: "Affordable and clean energy",
    8: "Decent work and economic growth",
    9: "Industry, innovation and infrastructure",
    10: "Reduced inequalities",
    11: "Sustainable cities and communities",
    12: "Responsible consumption and production",
    13: "Climate action",
    14: "Life below water",
    15: "Life on land",
    16: "Peace, justice and strong institutions",
    17: "Partnerships for the Goals",
}

# ── 조판 규격 ────────────────────────────────────────────────────────
GOAL_TITLE_FONT, GOAL_TITLE_SIZE = "Gotham-Black", (15.0, 17.0)
HEADING_FONT, HEADING_SIZE = "GothamBold", (10.5, 11.5)
BODY_SIZE = (8.8, 9.2)          # Whitney-Book / Bold / BookItalic
BODY_FONT_PREFIX = "Whitney-"

BULLET = "•"


@dataclass
class Subsection:
    heading: str
    paragraphs: list[str] = field(default_factory=list)


@dataclass
class GoalDocument:
    number: int
    name: str
    pages: str = ""
    keypoints: list[str] = field(default_factory=list)
    subsections: list[Subsection] = field(default_factory=list)


# ── 1단계: 줄 단위 추출 + 역할 분류 ──────────────────────────────────
def classify(spans: list[dict]) -> str:
    """줄의 조판 서체로 역할을 판정합니다."""
    visible = [s for s in spans if s["text"].strip()]
    if not visible:
        return "ignore"

    font = visible[0]["font"]
    size = round(visible[0]["size"], 1)

    if GOAL_TITLE_FONT in font and GOAL_TITLE_SIZE[0] <= size <= GOAL_TITLE_SIZE[1]:
        return "goal_title"

    # 소제목은 줄 전체가 GothamBold 11pt 로 조판된다.
    if all(
        HEADING_FONT in s["font"] and HEADING_SIZE[0] <= s["size"] <= HEADING_SIZE[1]
        for s in visible
    ):
        return "heading"

    if font.startswith(BODY_FONT_PREFIX) and BODY_SIZE[0] <= size <= BODY_SIZE[1]:
        return "body"

    # 캡션(Semibold 8.5pt)·도표 제목·축 숫자·머리말은 전부 여기로 떨어진다.
    return "ignore"


def read_lines(page: "fitz.Page") -> list[tuple[str, str, int]]:
    """(역할, 텍스트, 블록번호) 목록을 읽기 순서대로 돌려줍니다."""
    out: list[tuple[str, str, int]] = []
    data = page.get_text("dict")
    for bi, block in enumerate(data["blocks"]):
        for line in block.get("lines", []):
            spans = line["spans"]
            text = "".join(s["text"] for s in spans)
            if not text.strip():
                continue
            out.append((classify(spans), text.strip(), bi))
    return out


# ── 2단계: Goal 경계 찾기 ────────────────────────────────────────────
def normalize(text: str) -> str:
    return re.sub(r"[^a-z]", "", text.lower())


def detect_goal_pages(doc: "fitz.Document") -> dict[int, tuple[int, int]]:
    """Goal 제목(Gotham-Black 16pt)이 놓인 쪽으로 Goal 구간을 잡습니다."""
    starts: dict[int, int] = {}
    for pno in range(doc.page_count):
        titles = [t for role, t, _ in read_lines(doc[pno]) if role == "goal_title"]
        if not titles:
            continue
        joined = normalize(" ".join(titles))
        for num, name in GOAL_NAMES.items():
            if num in starts:
                continue
            if normalize(name) and normalize(name) in joined:
                starts[num] = pno
                break

    ranges: dict[int, tuple[int, int]] = {}
    ordered = sorted(starts.items())
    for idx, (num, start) in enumerate(ordered):
        end = ordered[idx + 1][1] - 1 if idx + 1 < len(ordered) else start + 1
        ranges[num] = (start, end)
    return ranges


# ── 3단계: 본문 조립 ─────────────────────────────────────────────────
def is_noise_paragraph(text: str) -> bool:
    """9pt 본문으로 조판됐지만 서술 문단이 아닌 것을 걸러냅니다."""
    stripped = text.strip()
    if len(stripped.split()) < 6:
        return True
    if not re.search(r"[.!?]", stripped):
        return True
    # 숫자·기호만 남은 조각
    if not re.search(r"[A-Za-z]{4,}", stripped):
        return True
    return False


def parse_goal(doc: "fitz.Document", number: int, start: int, end: int) -> GoalDocument:
    goal = GoalDocument(
        number=number,
        name=GOAL_NAMES[number],
        pages=f"{start + 1}-{end + 1}",
    )

    current: Subsection | None = None
    heading_parts: list[str] = []
    heading_block: int | None = None
    para_parts: list[str] = []
    para_block: int | None = None

    def flush_heading() -> None:
        nonlocal current, heading_parts, heading_block
        if not heading_parts:
            return
        text = re.sub(r"\s+", " ", " ".join(heading_parts)).strip()
        current = Subsection(heading=text)
        goal.subsections.append(current)
        heading_parts = []
        heading_block = None

    def flush_paragraph() -> None:
        nonlocal para_parts, para_block
        if not para_parts:
            return
        text = re.sub(r"\s+", " ", " ".join(para_parts)).strip()
        text = re.sub(r"(\w)-\s(\w)", r"\1\2", text)      # 줄끝 하이픈 복원
        para_parts = []
        para_block = None
        if text.startswith(BULLET):
            point = text.lstrip(BULLET).strip()
            if point:
                goal.keypoints.append(point)
            return
        if is_noise_paragraph(text) or current is None:
            return
        current.paragraphs.append(text)

    for pno in range(start, end + 1):
        for role, text, block in read_lines(doc[pno]):
            if role == "goal_title":
                continue

            if role == "heading":
                flush_paragraph()
                # 소제목이 여러 줄로 감기는 것과, 다른 단의 소제목이 곧바로
                # 이어지는 것을 구별한다. 감긴 줄은 같은 블록에 있고,
                # 별개의 소제목은 블록이 다르다.
                if heading_parts and block != heading_block:
                    flush_heading()
                heading_parts.append(text)
                heading_block = block
                continue

            # 소제목이 끝났으면 확정한다.
            if heading_parts:
                flush_heading()

            if role == "body":
                # 블록이 바뀌거나 새 불릿이 시작되면 문단을 끊는다.
                if para_parts and (block != para_block or text.startswith(BULLET)):
                    flush_paragraph()
                para_parts.append(text)
                para_block = block
                continue

            # ignore — 도표·캡션·머리말이 끼어들면 문단도 거기서 끊는다.
            flush_paragraph()

        flush_paragraph()

    flush_heading()
    flush_paragraph()
    return goal


# ── 4단계: XML 작성 ──────────────────────────────────────────────────
def build_xml(goals: list[GoalDocument]) -> ET.Element:
    report = ET.Element("report", {"title": REPORT_TITLE, "year": REPORT_YEAR})
    for goal in goals:
        goal_el = ET.SubElement(
            report,
            "goal",
            {"number": str(goal.number), "name": goal.name, "pages": goal.pages},
        )
        if goal.keypoints:
            kp_el = ET.SubElement(goal_el, "keypoints")
            for point in goal.keypoints:
                ET.SubElement(kp_el, "point").text = point
        for sub in goal.subsections:
            if not sub.paragraphs:
                continue
            sub_el = ET.SubElement(goal_el, "subsection", {"heading": sub.heading})
            for para in sub.paragraphs:
                ET.SubElement(sub_el, "paragraph").text = para
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="SDG Report 2025 PDF → 계층 XML")
    parser.add_argument("pdf", type=Path)
    parser.add_argument("xml", type=Path)
    args = parser.parse_args()

    doc = fitz.open(args.pdf)
    ranges = detect_goal_pages(doc)
    print(f"PDF → XML 변환: {args.pdf}  ({doc.page_count}쪽)")
    print("Goal 구간:", ", ".join(f"G{n}={s + 1}-{e + 1}" for n, (s, e) in sorted(ranges.items())))
    print()

    goals = [parse_goal(doc, n, *ranges[n]) for n in sorted(ranges)]
    for g in goals:
        print(
            f"  Goal {g.number:>2} {g.name:<40} | kp={len(g.keypoints):>2} "
            f"sub={len(g.subsections):>2} para={sum(len(s.paragraphs) for s in g.subsections):>3}"
        )

    root = build_xml(goals)
    ET.indent(root, space="  ")
    ET.ElementTree(root).write(args.xml, encoding="utf-8", xml_declaration=True)

    subs = sum(len(g.subsections) for g in goals)
    paras = sum(len(s.paragraphs) for g in goals for s in g.subsections)
    print(f"\n소제목 {subs} · 문단 {paras}")
    print(f"저장 완료: {args.xml}")


if __name__ == "__main__":
    main()
