# Build a Working RAG in Half a Day
### UN Policy Reports with LangChain — DH2026 Workshop

*[English](#english) | [한국어](#한국어)*

---

<a name="english"></a>
# English

A **provenance-first** RAG pipeline: every answer is shown together with the
sources it rests on. We build it step by step — from a raw PDF to a grounded,
citable question-answering system — so that each stage is transparent, not a
black box.

The corpus is the UN *Sustainable Development Goals Report 2025*. By the end,
you will have a working retrieval-augmented chatbot that answers questions and
cites exactly which Goal, subsection, and pages each answer comes from.

---

## Before you start

Please complete these **two steps before the session begins.** They take about
a minute and prevent the most common hold-ups during the workshop.

### 1. Add the shared assets to your Drive

The models and data are prepared for you in a shared Google Drive folder. You do
**not** need to download them — you only add a shortcut so your Colab can read
them.

1. Open the shared folder: **[DH2026_Workshop (Google Drive)](https://drive.google.com/drive/folders/1nbFRzpxjPUYldNNV800QqhzENzbYR0eW?usp=sharing)**
2. Click **"Add shortcut to Drive"** (right-click the folder, or use the
   toolbar).
3. Place the shortcut in **My Drive** (the top level).

This adds no files to your storage — it is a pointer, not a copy. During the
workshop your notebook reads the models and the canonical data directly from
this shared folder.

### 2. Set your Colab runtime to GPU

The generation model (Qwen3) requires a GPU.

1. In Colab, open **Runtime → Change runtime type**.
2. Select **T4 GPU** and save.

The notebook stops at STEP 1 if no GPU is detected, so setting this first saves
you a restart.

---

## How to follow along

The code is split **cell by cell** in
**[workshop_code.md](workshop_code.md)**.

For each step:

1. Find the code block (e.g. `2-1`) in `workshop_code.md`.
2. Click the **copy** button on that block.
3. Paste it into a fresh Colab cell and run it.

Work through the steps **in order, STEP 1 to STEP 10.** Each block is meant to
be one Colab cell.

> A note on how the notebook is organized: STEP 1 prepares everything once
> (libraries, models, data), so that after it, the pipeline runs even if the
> network drops. If your runtime restarts, re-run STEP 1 and continue — the
> models and canonical data live in Drive, not in the temporary session.

---

## Slides

**[Build a Working RAG in Half a Day — slides](https://littlekg87.github.io/DH2026/Workshop_RAG/)**

Twenty pages covering the keynote and all ten steps. Bilingual (KO/EN) with a
dark/light toggle in the sidebar; your choice carries over to the explainers below.

---

## Supplementary material

Interactive explainers that accompany the workshop. Each one opens the step it
belongs to and links back to the slides.

| Step | Explainer |
|------|-----------|
| 2  | [What Is a Chunk — and how naive chunking fails](https://littlekg87.github.io/DH2026/Workshop_RAG/html/step02_chunk.html) |
| 3  | [Why XML — reading the typesetting, not the letters](https://littlekg87.github.io/DH2026/Workshop_RAG/html/step03_xml.html) |
| 4  | [How Provenance Rides Along](https://littlekg87.github.io/DH2026/Workshop_RAG/html/step04_metadata.html) |
| 5  | [Embeddings and Vectors](https://littlekg87.github.io/DH2026/Workshop_RAG/html/step05_vector.html) |
| 6  | [The Vector Store](https://littlekg87.github.io/DH2026/Workshop_RAG/html/step06_vectordb.html) |
| 7–8  | [Finding by Distance](https://littlekg87.github.io/DH2026/Workshop_RAG/html/step08_distance.html) |
| 9–10 | [From Retrieval to Answer](https://littlekg87.github.io/DH2026/Workshop_RAG/html/step10_answer.html) |

_(These render as live web pages via GitHub Pages.)_

---

## Pipeline overview

| Step | What it does |
|------|--------------|
| 1  | Setup & asset preparation |
| 2  | PDF → text → naive chunks (the "before" baseline) |
| 3  | Structure the PDF into hierarchical XML |
| 4  | XML → chunks → LangChain Documents |
| 5  | Load the encoder · embed every chunk |
| 6  | Build the vector store (FAISS) |
| 7  | A question becomes a vector too |
| 8  | Distance, by hand — NumPy instead of FAISS, to see what FAISS does |
| 9  | FAISS retrieval + provenance |
| 10 | Generation with provenance (Qwen3-0.6B) |

---

## Stack

- **Runtime:** Google Colab (GPU)
- **Framework:** LangChain
- **Encoder:** `all-MiniLM-L6-v2` (local, no API key)
- **Vector store:** FAISS
- **LLM:** Qwen3-0.6B (local, no API key)

All models are loaded locally from the shared Drive folder — no external API
keys, no Hugging Face Hub calls during the session.

---
---

<a name="한국어"></a>
# 한국어

**전거(provenance) 우선** RAG 파이프라인입니다. 모든 답변은 그 답변이 근거로
삼은 출처와 함께 제시됩니다. 원본 PDF에서 출발해 근거가 명시되고 인용 가능한
질의응답 시스템에 이르기까지 단계별로 구축하며, 각 단계가 블랙박스가 아니라
투명하게 드러나도록 합니다.

말뭉치는 UN *지속가능발전목표 보고서 2025(Sustainable Development Goals Report
2025)*입니다. 워크숍이 끝나면, 질문에 답하면서 그 답변이 어느 목표(Goal)·
하위 절(subsection)·페이지에서 나왔는지 정확히 인용하는 검색증강(RAG)
챗봇을 완성하게 됩니다.

---

## 시작하기 전에

아래 **두 단계를 세션 시작 전에** 완료해 주세요. 1분 정도면 되고, 워크숍 중
가장 흔한 지연을 예방합니다.

### 1. 공유 자산을 내 드라이브에 추가하기

모델과 데이터는 공유 Google Drive 폴더에 미리 준비되어 있습니다. 다운로드할
**필요는 없으며**, Colab이 읽을 수 있도록 바로가기만 추가하면 됩니다.

1. 공유 폴더 열기: **[DH2026_Workshop (Google Drive)](https://drive.google.com/drive/folders/1nbFRzpxjPUYldNNV800QqhzENzbYR0eW?usp=sharing)**
2. **"드라이브에 바로가기 추가"** 클릭 (폴더를 우클릭하거나 툴바 이용).
3. 바로가기를 **내 드라이브(My Drive)** 최상위에 놓기.

이 작업은 저장 공간에 파일을 추가하지 않습니다 — 복사본이 아니라 포인터입니다.
워크숍 중에는 노트북이 이 공유 폴더에서 모델과 정본(canonical) 데이터를 직접
읽습니다.

### 2. Colab 런타임을 GPU로 설정하기

생성 모델(Qwen3)은 GPU가 필요합니다.

1. Colab에서 **런타임 → 런타임 유형 변경** 열기.
2. **T4 GPU** 선택 후 저장.

GPU가 감지되지 않으면 노트북이 STEP 1에서 멈추므로, 먼저 설정해 두면 재시작을
피할 수 있습니다.

---

## 따라 하는 방법

코드는 **[workshop_code.md](workshop_code.md)**에 **셀 단위로** 나뉘어
있습니다.

각 단계마다:

1. `workshop_code.md`에서 해당 코드 블록(예: `2-1`)을 찾습니다.
2. 그 블록의 **복사(copy)** 버튼을 누릅니다.
3. Colab의 새 셀에 붙여넣고 실행합니다.

**STEP 1부터 STEP 10까지 순서대로** 진행하세요. 각 블록은 Colab 셀 하나에
해당합니다.

> 노트북 구성에 관한 참고: STEP 1은 모든 것(라이브러리·모델·데이터)을 한 번에
> 준비하므로, 이후에는 네트워크가 끊겨도 파이프라인이 동작합니다. 런타임이
> 재시작되면 STEP 1을 다시 실행하고 이어가면 됩니다 — 모델과 정본 데이터는
> 임시 세션이 아니라 드라이브에 있기 때문입니다.

---

## 발표자료

**[반나절 만에 만드는 작동하는 RAG — 발표자료](https://littlekg87.github.io/DH2026/Workshop_RAG/)**

기조강연과 STEP 1–10을 담은 20쪽입니다. 한/영 이중언어이며 사이드바에서
어두운 화면·밝은 화면을 고를 수 있습니다. 선택은 아래 보조 자료에도 이어집니다.

---

## 보조 자료

워크숍에 함께하는 인터랙티브 설명 자료입니다. 각 자료는 해당 단계를 펼쳐 보이고,
발표자료로 돌아오는 링크를 갖고 있습니다.

| 단계 | 설명 자료 |
|------|-----------|
| 2  | [청크란 무엇인가 — 그리고 나이브 청킹은 왜 실패하는가](https://littlekg87.github.io/DH2026/Workshop_RAG/html/step02_chunk.html) |
| 3  | [왜 XML인가 — 글자가 아니라 조판을 읽는다](https://littlekg87.github.io/DH2026/Workshop_RAG/html/step03_xml.html) |
| 4  | [전거가 청크에 실리는 법](https://littlekg87.github.io/DH2026/Workshop_RAG/html/step04_metadata.html) |
| 5  | [임베딩과 벡터](https://littlekg87.github.io/DH2026/Workshop_RAG/html/step05_vector.html) |
| 6  | [벡터 데이터베이스](https://littlekg87.github.io/DH2026/Workshop_RAG/html/step06_vectordb.html) |
| 7–8  | [거리로 찾는다](https://littlekg87.github.io/DH2026/Workshop_RAG/html/step08_distance.html) |
| 9–10 | [검색 결과가 답변이 되기까지](https://littlekg87.github.io/DH2026/Workshop_RAG/html/step10_answer.html) |

_(이 자료들은 GitHub Pages를 통해 실제 웹 페이지로 렌더링됩니다.)_

---

## 파이프라인 개요

| 단계 | 하는 일 |
|------|--------------|
| 1  | 환경 설정 및 자산 준비 |
| 2  | PDF → 텍스트 → 나이브 청크 ("이전" 기준선) |
| 3  | PDF를 계층적 XML로 구조화 |
| 4  | XML → 청크 → LangChain Document |
| 5  | 인코더 로드 · 모든 청크 임베딩 |
| 6  | 벡터 저장소(FAISS) 구축 |
| 7  | 질문도 벡터가 된다 |
| 8  | 거리를 손으로 계산 — FAISS 없이 넘파이로, FAISS가 하는 일을 눈으로 |
| 9  | FAISS 검색 + 전거 |
| 10 | 전거와 함께 생성 (Qwen3-0.6B) |

---

## 스택

- **런타임:** Google Colab (GPU)
- **프레임워크:** LangChain
- **인코더:** `all-MiniLM-L6-v2` (로컬, API 키 불필요)
- **벡터 저장소:** FAISS
- **LLM:** Qwen3-0.6B (로컬, API 키 불필요)

모든 모델은 공유 드라이브 폴더에서 로컬로 로드됩니다 — 세션 중 외부 API 키나
Hugging Face Hub 호출이 없습니다.
