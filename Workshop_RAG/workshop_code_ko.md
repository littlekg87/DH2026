# RAG 워크숍 실습 코드 — 한국어 완전판

> 원본 코드: https://github.com/littlekg87/DH2026/blob/main/Workshop_RAG/workshop_code.md
>
> **실습 방법:** 아래의 **19개 Python 코드 블록을 순서대로** Google Colab 코드 셀에 하나씩 복사하여 실행한다. 각 코드 블록은 원문과 동일한 번호(1-1~10-3)를 사용한다. 실행 전에 공유 Google Drive 폴더를 내 드라이브 바로가기로 추가하고 Colab 런타임을 **T4 GPU**로 설정한다.
>
> **언어 및 호환성:** 제목·설명·코드 주석을 한국어로 작성했다. SDG 보고서 본문과 기준 XML·청크가 영어이므로 **예시 질의와 LLM에 전달하는 프롬프트는 영어로 유지**한다. 파일 경로·변수·함수·모델 설정은 영문 원본의 실행 흐름을 유지한다.

## 1단계. 환경 설정 및 실습 자료 준비

실습에 필요한 Python 라이브러리를 설치하고 Google Drive를 연결한다. 모든 참여자가 같은 버전의 라이브러리를 사용하도록 의존성 버전을 고정한다. Qwen3 모델을 GPU에서 실행하므로 Colab 실행 환경을 **T4 GPU**로 선택해야 한다. Hugging Face의 오프라인 모드를 활성화하면 모델 로딩 단계에서 인터넷 접속을 시도하지 않도록 할 수 있다.

### 1-1. 라이브러리 설치

LangChain, sentence-transformers, FAISS, PDF 처리 패키지 등을 설치한다.

```python
!pip install -q \
    langchain-core==1.4.8 \
    langchain-community==0.4.2 \
    langchain-huggingface==1.2.2 \
    langchain-text-splitters==1.1.2 \
    "sentence-transformers>=4,<5" \
    faiss-cpu==1.14.3 \
    pypdf==5.9.0 \
    pymupdf==1.28.0 \
    "transformers>=4.51,<5"
```

### 1-2. Drive 및 GPU

GPU 존재 여부를 검사하고 Drive에 마운트한 뒤 임베딩 모델과 언어모델의 경로를 지정한다.

```python
import os, torch
from google.colab import drive

# 필요한 모델이 이미 로컬에 있으므로 Hugging Face Hub 접속 차단.
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

# Qwen3 실행을 위해 GPU가 필요하다. GPU가 없으면 중단한다.
assert torch.cuda.is_available(), (
    "GPU가 없습니다. 런타임 > 런타임 유형 변경 > GPU(T4)로 설정한 후 다시 실행하세요."
)
print("GPU:", torch.cuda.get_device_name(0))

drive.mount("/content/drive")

# 모델 경로 설정. 다른 파일 경로는 사용하는 단계에서 정의한다.
BASE        = "/content/drive/MyDrive/DH2026_Workshop"
ENCODER_DIR = f"{BASE}/Encoder"
LLM_DIR     = f"{BASE}/LLM"
```

### 1-3. 모델 파일 검사

모델 가중치와 설정 파일이 지정한 경로에 있는지 검사해 이후 오류를 예방한다.

```python
checks = {
    "Encoder weights": f"{ENCODER_DIR}/model.safetensors",
    "Encoder pooling": f"{ENCODER_DIR}/1_Pooling/config.json",
    "LLM weights":     f"{LLM_DIR}/model.safetensors",
    "LLM config":      f"{LLM_DIR}/config.json",
}

missing = [name for name, path in checks.items() if not os.path.exists(path)]

for name, path in checks.items():
    mark = "✗" if name in missing else "✓"
    print(f"  {mark}  {name:16s} {path}")

assert not missing, f"모델 파일 누락: {missing}"
print("\n모델 준비 완료. 이후 실습은 오프라인에서 실행할 수 있습니다.")
```


## 2단계. PDF 텍스트 추출과 단순 청킹

PDF의 모든 페이지에서 텍스트를 추출하여 `raw_text.txt`로 저장한다. 이어서 `RecursiveCharacterTextSplitter`를 사용해 텍스트를 **500자 길이, 50자 중첩**으로 분할한다. 이 단계의 청크는 문서의 제목·소절·문단 구조를 고려하지 않는 **기본 비교 대상(naive baseline)**이다. 실제 RAG 검색에는 사용하지 않고, 후속 단계의 구조화된 청크와 비교한다.

### 2-1. PDF → 텍스트

`PdfReader`로 페이지별 텍스트를 추출한다.

```python
from pypdf import PdfReader

PDF_PATH = f"{BASE}/Source/The-Sustainable-Development-Goals-Report-2025.pdf"

reader   = PdfReader(PDF_PATH)
pages    = [(p.extract_text() or "") for p in reader.pages]
raw_text = "\n".join(pages)

with open("raw_text.txt", "w", encoding="utf-8") as f:
    f.write(raw_text)

print(f"{len(pages)} pages, {len(raw_text):,} chars → raw_text.txt")
```

### 2-2. 텍스트 → 청크

길이 기준 청킹을 실시하고 결과를 `naive_chunks.txt`에 저장한다.

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter     = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
naive_chunks = splitter.split_text(raw_text)

with open("naive_chunks.txt", "w", encoding="utf-8") as f:
    for i, c in enumerate(naive_chunks):
        f.write(f"{'='*70}\n[chunk {i}]  {len(c)} chars\n{'='*70}\n{c}\n\n")

print(f"{len(naive_chunks)} naive chunks → naive_chunks.txt")
```


## 3단계. PDF의 계층 구조를 XML로 변환

단순 텍스트 추출 과정에서는 문서의 계층 구조가 사라지고 표 조각이나 캡션 등 잡음이 포함될 수 있다. 원본 SDG 보고서는 소절 제목에 **GothamBold 11pt**, 본문에 **Whitney 9pt**를 사용한다. `build_xml.py`는 이 조판 정보를 바탕으로 목표(Goal), 소절(Subsection), 문단(Paragraph)의 계층을 XML로 재구성한다. 문장 의미에 의존하지 않고 서식과 구조 정보를 이용한다는 점이 핵심이다.

### 3-1. 구조화 스크립트 실행

`build_xml.py`에 입력 PDF와 출력 XML 파일 경로를 전달한다. 생성된 `sdg_report_2025.xml`은 로컬 실습 결과물이며, 다음 단계에서는 모든 참여자가 동일한 기준 XML 파일을 Drive에서 불러온다.

```python
BUILD_SCRIPT = f"{BASE}/Code/build_xml.py"

# build_xml.py 입력 인수: [입력 PDF] [출력 XML 경로]
!python "{BUILD_SCRIPT}" "{PDF_PATH}" sdg_report_2025.xml
```


## 4단계. XML을 청크와 LangChain Document로 변환

XML의 `<subsection>`을 기본 청킹 단위로 삼는다. 제목과 본문은 검색 대상으로 사용하고, 목표 번호·목표 이름·페이지·제목은 **메타데이터**에 보존한다. 임베딩 모델의 최대 입력 길이가 **256토큰**이므로 청크는 제목을 포함해 **172단어**를 넘지 않도록 문단 경계, 필요시 문장 경계에서 분할한다. 분할된 청크는 `part` 값을 기록하여 출처 추적을 가능하게 한다.

### 4-1. XML → JSONL

청크의 `text`와 `metadata`를 `sdg_chunks.jsonl`에 저장한다.

```python
import json, re, xml.etree.ElementTree as ET

XML_PATH  = f"{BASE}/Source/sdg_report_2025.xml"   # Drive의 기준 XML
MAX_WORDS = 172        # 제목 포함. 청크당 256토큰 제한을 고려한 단어 수.


def split_long(text, limit):
    """긴 문단은 문장 경계에서 나눈다. 문장 중간은 분할하지 않는다."""
    parts, current, count = [], [], 0
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        words = len(sentence.split())
        if current and count + words > limit:
            parts.append(" ".join(current))
            current, count = [], 0
        current.append(sentence)
        count += words
    if current:
        parts.append(" ".join(current))
    return parts


root   = ET.parse(XML_PATH).getroot()
chunks = []

for goal in root.findall("goal"):
    g_num, g_name, g_pages = int(goal.get("number")), goal.get("name"), goal.get("pages")
    seq = 0

    for sub in goal.findall("subsection"):
        heading = sub.get("heading")
        budget  = max(MAX_WORDS - len(heading.split()), 40)

        # 1. 문단을 준비한다. 개별 문단이 길면 먼저 문장 단위로 분할한다.
        paragraphs = []
        for p in sub.findall("paragraph"):
            if not p.text:
                continue
            paragraphs += (split_long(p.text, budget)
                           if len(p.text.split()) > budget else [p.text])

        # 2. 단어 수 상한에 맞춰 문단을 청크로 묶는다.
        groups, current, count = [], [], 0
        for para in paragraphs:
            words = len(para.split())
            if current and count + words > budget:
                groups.append(current)
                current, count = [], 0
            current.append(para)
            count += words
        if current:
            groups.append(current)

        # 3. 묶음마다 청크를 만들고 동일한 출처 메타데이터를 부여한다.
        for i, group in enumerate(groups):
            seq += 1
            metadata = {                           # 출처 정보: 임베딩하지 않는다.
                "id":        f"G{g_num:02d}-S{seq:02d}",
                "goal":      g_num,
                "goal_name": g_name,
                "pages":     g_pages,
                "heading":   heading,
            }
            if len(groups) > 1:
                metadata["part"] = f"{i+1}/{len(groups)}"
            chunks.append({
                "metadata": metadata,
                "text": f"{heading}\n" + "\n".join(group),   # 이 텍스트만 임베딩한다.
            })

with open("sdg_chunks.jsonl", "w", encoding="utf-8") as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + "\n")

whole = sum(1 for c in chunks if "part" not in c["metadata"])
print(f"{len(chunks)} chunks → sdg_chunks.jsonl")
print(f"  {whole} subsections fit in one chunk; the rest were split")
```

### 4-2. LangChain Document

각 청크를 `Document(page_content=..., metadata=...)`로 변환한다. `page_content`만 임베딩하고 `metadata`는 근거 자료를 표시하는 데 활용한다.

```python
from langchain_core.documents import Document

docs = [Document(page_content=c["text"], metadata=c["metadata"]) for c in chunks]

print(docs[0].metadata)
```


## 5단계. 임베딩 모델 로드 및 벡터 생성

Drive에 저장된 임베딩 모델을 로컬 경로에서 불러와 GPU에서 실행한다. 기준 청크 파일을 읽고 각 청크의 텍스트를 **384차원 벡터**로 변환한다. 생성된 벡터는 텍스트 및 메타데이터와 함께 `sdg_embeddings.jsonl`에 저장한다. 이러한 임베딩 결과가 이후 벡터 인덱스 구축과 검색의 입력이 된다.

### 5-1. 임베딩 모델 로드

`HuggingFaceEmbeddings`를 사용하며 정규화 설정을 적용한다.

```python
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name=ENCODER_DIR,
    model_kwargs={"device": "cuda"},
    encode_kwargs={"normalize_embeddings": True},
)
print("Encoder loaded from:", ENCODER_DIR)
```

### 5-2. 문서 임베딩

`embed_documents()`로 모든 청크를 벡터화하고 개수·차원·값 일부를 확인한다.

```python
import json, time

CHUNKS_PATH = f"{BASE}/Source/sdg_chunks.jsonl"     # Drive에 저장된 기준 청크

chunks = [json.loads(line) for line in open(CHUNKS_PATH, encoding="utf-8")]

t0 = time.time()
vectors = embeddings.embed_documents([c["text"] for c in chunks])
print(f"{len(vectors)} embeddings done · {time.time()-t0:.1f}s\n")

print(f"dimensions: {len(vectors[0])}")
print(f"first chunk, first 10 values: {[round(x, 4) for x in vectors[0][:10]]}\n")

with open("sdg_embeddings.jsonl", "w", encoding="utf-8") as f:
    for c, v in zip(chunks, vectors):
        f.write(json.dumps({**c, "vector": v}, ensure_ascii=False) + "\n")

print("→ sdg_embeddings.jsonl")
```


## 6단계. FAISS 벡터 저장소 구축

5단계에서 계산한 임베딩 벡터를 재계산하지 않고 FAISS에 그대로 등록한다. 벡터 인덱스와 원문 텍스트는 서로 구분하여 관리하고, 문서 ID를 통해 연결한다. 검색 시에는 가까운 벡터를 찾은 후 해당 ID의 원문과 메타데이터를 불러올 수 있다.

### 6-1. FAISS 인덱스 구축

`FAISS.from_embeddings()`에 텍스트-벡터 쌍, 메타데이터, 문서 ID를 전달한다. 인덱스 차원과 벡터 수를 확인한 후 첫 문서의 벡터·ID·제목을 출력한다.

```python
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from langchain_community.vectorstores import FAISS

store = FAISS.from_embeddings(
    text_embeddings=list(zip([c["text"] for c in chunks], vectors)),
    embedding=embeddings,
    metadatas=[c["metadata"] for c in chunks],
    ids=[c["metadata"]["id"] for c in chunks],
)

print(f"{store.index.ntotal} × {store.index.d} dims · {type(store.index).__name__}\n")

i = 0
print("vector store :", store.index.reconstruct(i)[:4].round(4), "...")
print("id table     :", i, "→", store.index_to_docstore_id[i])
print("text store   :", store.docstore.search(store.index_to_docstore_id[i]).metadata["heading"][:50])
```


## 7단계. 검색 질문을 벡터로 변환

문서 청크를 임베딩한 것과 동일한 모델로 사용자 질문을 벡터화한다. 검색 질문에는 문서처럼 출처 메타데이터가 부착되지 않는다. 실습에서는 극빈 상태의 인구를 묻는 영어 질문을 사용해 질문 벡터가 384차원으로 변환되는 과정을 직접 관찰한다.

### 7-1. 질의 임베딩

`embed_query()`를 사용해 질문 벡터를 만들고 차원별 값을 출력한다.

```python
query = "How many people still live in extreme poverty?"

qv = embeddings.embed_query(query)

print(f"query : {query}")
print(f"vector: {len(qv)} dims\n")

print("  dim       value")
print("  ────────────────")
for i in range(10):
    print(f"  {i:3d}   {qv[i]:+.4f}")
print("   ⋮        ⋮")
for i in range(374, 384):
    print(f"  {i:3d}   {qv[i]:+.4f}")
```

### 7-2. 직접 입력

참여자가 영어 질문을 입력해 벡터값을 확인한다. 다른 영어 질문을 입력해 반복해도 후속 결과에는 영향을 주지 않는다.

```python
import numpy as np

my_query = input("영어로 질문을 입력하세요: ")
mv = np.array(embeddings.embed_query(my_query))

print(f"\n{my_query}")
print(f"→ {len(mv)}-dim vector\n")

for r in range(0, 384, 8):
    print(f"  [{r:3d}] " + "  ".join(f"{x:+.4f}" for x in mv[r:r+8]))
```


## 8단계. 벡터 사이의 거리를 직접 계산

검색은 질문 벡터와 저장된 문서 벡터 사이의 거리를 측정하고 가까운 문서부터 정렬하는 과정으로 이해할 수 있다. 이 단계에서는 FAISS 검색 함수를 호출하지 않고, 두 벡터의 각 차원 값의 차이를 구한다. 차이를 제곱해 모두 더하고 제곱근을 구하는 **유클리드 거리**를 사용한다. 상위 3개 문서의 ID와 거리를 출력한다.

### 8-1. 수동 검색

모든 청크 벡터와 질문 벡터 사이의 거리를 계산한 뒤 `numpy.argsort()`로 정렬한다. 그 결과를 다음 단계의 FAISS 검색 결과와 비교한다.

```python
import numpy as np

query = "How many people still live in extreme poverty?"
qv    = embeddings.embed_query(query)                  # 질문 벡터

V = store.index.reconstruct_n(0, store.index.ntotal)   # 전체 청크 벡터
Q = np.array(qv)                                        # 질문 벡터 하나

print(f"chunk vectors : {len(V)}, each {len(V[0])} numbers")
print(f"query vector  : 1, {len(Q)} numbers\n")

# 청크별 거리 계산: 384차원에서 차이의 제곱합의 제곱근을 구한다.
distances = []
for v in V:
    diff = v - Q                        # 각 차원에서의 차이
    dist = np.sqrt((diff ** 2).sum())   # 제곱 → 합계 → 제곱근
    distances.append(dist)

print(f"measured {len(distances)} distances, one per chunk.\n")

# 가장 가까운 문서부터 정렬한다.
order = np.argsort(distances)

hand_top3 = [store.index_to_docstore_id[int(i)] for i in order[:3]]

for rank, i in enumerate(order[:3], 1):
    print(f"#{rank}  distance {distances[i]:.4f}   {store.index_to_docstore_id[int(i)]}")
```


## 9단계. FAISS 검색 결과와 출처 메타데이터

FAISS는 앞 단계의 거리 계산과 유사한 작업을 간단한 검색 함수로 처리한다. 같은 질문을 사용하여 수동으로 계산한 상위 문서 ID와 FAISS가 반환한 상위 문서 ID가 같은지 검사한다. 이어서 검색된 텍스트와 함께 목표 번호, 목표명, 페이지, 소절 제목을 표시한다. 메타데이터는 검색 대상이 아니라 **근거 자료의 출처를 추적하기 위한 정보**다.

### 9-1. 결과 비교

`similarity_search_with_score()`를 실행하고 8단계의 `hand_top3`와 비교한다.

```python
query = "How many people still live in extreme poverty?"

results    = store.similarity_search_with_score(query, k=3)
faiss_top3 = [doc.metadata["id"] for doc, _ in results]

print(f"query: {query}\n")
print("STEP 8 (by hand) :", hand_top3)
print("STEP 9 (FAISS)   :", faiss_top3)
print("match            :", hand_top3 == faiss_top3)
```

### 9-2. 출처 부착

문서별 `metadata`에서 ID·목표·페이지·제목을 읽어 본문과 함께 출력한다.

```python
def search_with_sources(q, k=3):
    for rank, (doc, dist) in enumerate(store.similarity_search_with_score(q, k=k), 1):
        m = doc.metadata
        part = f" · part {m['part']}" if "part" in m else ""
        print(f"[{rank}]  distance {dist:.4f}")
        print(f"     {m['id']} · Goal {m['goal']} {m['goal_name']} · pp. {m['pages']}{part}")
        print(f"     {m['heading']}")
        print()
        print(doc.page_content)
        print("─" * 70)

query = "How many people still live in extreme poverty?"
search_with_sources(query)
```


## 10단계. Qwen3-0.6B를 이용한 답변 생성

검색기는 관련 근거를 찾고 언어모델은 이를 활용해 답변을 작성한다. Qwen3는 인과적 언어모델이므로 `AutoModelForCausalLM`을 사용하고, 대화형 입력은 chat template로 구성한다. 출력에서 입력 프롬프트에 대응하는 토큰을 제외해야 생성된 답변만 얻을 수 있다. 검색 근거 없이 생성한 답변과 검색 결과를 제공한 뒤 생성한 답변을 비교한다.

### 10-1. 모델 로드 및 연결

로컬 Qwen3 모델을 불러오고 LangChain의 `LLM` 인터페이스에 맞춘 래퍼를 만든다.

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.utils import logging as hf_logging
from langchain_core.language_models.llms import LLM
from typing import Optional, List, Any

hf_logging.set_verbosity_error()          # 생성 관련 안내 메시지 숨김

tokenizer = AutoTokenizer.from_pretrained(LLM_DIR)
model = AutoModelForCausalLM.from_pretrained(
    LLM_DIR,
    dtype="auto",
    device_map="cuda",
)
print("Loaded:", model.config.model_type,
      f"· {sum(p.numel() for p in model.parameters())/1e6:.0f}M params")


class Qwen3LLM(LLM):
    """Qwen3의 LangChain LLM 래퍼. llm.invoke(prompt)로 호출한다."""
    max_new_tokens: int = 512

    @property
    def _llm_type(self) -> str:
        return "qwen3-local"

    def _call(self, prompt: str, stop: Optional[List[str]] = None,
              run_manager: Any = None, **kwargs) -> str:
        messages = [{"role": "user", "content": prompt}]
        text = tokenizer.apply_chat_template(
            messages, tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False,          # <think> 블록 없이 답변만 생성
        )
        inputs = tokenizer(text, return_tensors="pt").to(model.device)
        prompt_len = inputs.input_ids.shape[1]
        with torch.no_grad():
            out = model.generate(
                **inputs,
                max_new_tokens=self.max_new_tokens,
                do_sample=False,            # 그리디 디코딩: 결정적 출력
                pad_token_id=tokenizer.eos_token_id,
            )
        answer_ids = out[0][prompt_len:]    # 출력에서 입력 프롬프트 제외
        return tokenizer.decode(answer_ids, skip_special_tokens=True).strip()


llm = Qwen3LLM()
print("준비 완료.")
```

### 10-2. BEFORE

관련 문서 없이 질문을 전달해 모델의 내부 지식에 의존한 답변을 얻는다.

```python
import textwrap

query = "How many people still live in extreme poverty?"

answer = llm.invoke(query)
print(textwrap.fill(answer, width=80))
```

### 10-3. AFTER

관련 청크를 검색해 프롬프트에 포함하고 모델에 해당 근거만 사용하도록 지시한 뒤, 답변과 출처를 함께 출력한다.

```python
import textwrap

def ask_with_sources(q, k=3):
    # 1. 근거 자료 검색
    results = store.similarity_search_with_score(q, k=k)

    # 2. 검색된 청크로 문맥 구성
    context = "\n\n".join(doc.page_content for doc, _ in results)
    prompt = (
        "Use only the following sources to answer the question. "
        "If the answer is not in the sources, say you cannot find it.\n\n"
        f"{context}\n\n"
        f"Question: {q}"
    )

    # 3. 언어모델로 답변 생성
    answer = llm.invoke(prompt)

    # 4. 답변과 근거 문서의 출처 출력
    print(textwrap.fill(answer, width=80))
    print("\n출처")
    for doc, _ in results:
        m = doc.metadata
        part = f" · part {m['part']}" if "part" in m else ""
        print(f"  [{m['id']}] Goal {m['goal']} {m['goal_name']} · pp. {m['pages']}{part}")

query = "How many people still live in extreme poverty?"
ask_with_sources(query)
```


---

## 실습 결과의 핵심 비교

**10-2와 10-3은 같은 질문을 사용한다.** 차이는 모델에 검증 가능한 근거 자료를 제공했는지 여부다. 근거 자료 없이 생성한 답변은 그럴듯하더라도 정확성이나 출처를 평가하기 어렵다. 검색 결과를 기반으로 생성한 답변은 보고서의 해당 부분과 직접 대조해 검증할 수 있다. 이러한 **검색–생성–출처 확인**의 연결이 RAG 시스템의 핵심이다.
