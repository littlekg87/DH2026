# Workshop Code — Copy Cell by Cell

Copy each block below into a Colab cell and run it, **in order**. Blocks are
labelled to match the steps (e.g. `2-1`). Each block is one Colab cell.

> Prerequisite: you have added the shared Drive folder as a shortcut and set the
> runtime to **T4 GPU** (see the README).

---

## STEP 1 — Setup & Asset Preparation

Everything the workshop needs is prepared here, once. After this step the
pipeline runs even if the network drops.

**1-1. Install the pinned libraries.** Versions are fixed so every participant
runs the exact same environment.

```python
!pip install -q \
    langchain-core==1.4.8 \
    langchain-community==0.4.2 \
    langchain-huggingface==1.2.2 \
    langchain-text-splitters==1.1.2 \
    "sentence-transformers>=4,<5" \
    faiss-cpu==1.14.3 \
    pypdf==5.9.0 \
    "transformers>=4.51,<5"
```

**1-2. Mount Drive, verify the GPU, seal off the network, set paths.** Sealing
the Hugging Face Hub (`HF_HUB_OFFLINE`) guarantees no later cell silently
reaches out to the internet — everything is already local.

```python
import os, torch
from google.colab import drive

# Seal off the Hugging Face Hub: everything is already local.
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

# GPU is required for Qwen3. Stop now if it is missing.
assert torch.cuda.is_available(), (
    "No GPU detected. Set: Runtime > Change runtime type > GPU (T4), then re-run."
)
print("GPU:", torch.cuda.get_device_name(0))

drive.mount("/content/drive")

# Paths: models only (everything else is defined where it is used).
BASE        = "/content/drive/MyDrive/DH2026_Workshop"
ENCODER_DIR = f"{BASE}/Encoder"
LLM_DIR     = f"{BASE}/LLM"
```

**1-3. Confirm the models are in place** before we rely on them. Only the
pre-downloaded models are checked here; the PDF is used in STEP 2, and the XML
is produced in STEP 3.

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

assert not missing, f"Missing models: {missing}"
print("\nModels ready. The rest of the notebook runs offline.")
```

---

## STEP 2 — PDF → text → naive chunks

These naive chunks are **not** used for retrieval. They are the "before"
baseline: blind fixed-length cuts, with no structure and no provenance. We set
them aside now and contrast them with the structured chunks later.

Output files are written to local disk (`/content`) — they only need to live
for this session.

**2-1. PDF → text.**

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

**2-2. text → naive chunks.** Blind 500-character cuts with 50-character
overlap. No structure, no headings — this is the naive baseline.

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter     = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
naive_chunks = splitter.split_text(raw_text)

with open("naive_chunks.txt", "w", encoding="utf-8") as f:
    for i, c in enumerate(naive_chunks):
        f.write(f"{'='*70}\n[chunk {i}]  {len(c)} chars\n{'='*70}\n{c}\n\n")

print(f"{len(naive_chunks)} naive chunks → naive_chunks.txt")
```

---

## STEP 3 — Structure the PDF into hierarchical XML

A plain text dump loses the document's hierarchy (Goal > Subsection >
Paragraph) and mixes in noise (typesetting directives, broken table fragments).
`build_xml.py` rebuilds that hierarchy as XML.

The XML produced here is written to **local disk** — you watch the structuring
happen. The next step reads the canonical XML already prepared in Drive.

**3-1. Run the structuring script.** It takes an input PDF and an output XML
path.

```python
BUILD_SCRIPT = f"{BASE}/Code/build_xml.py"

# build_xml.py takes:  [input PDF]  [output XML]
!python "{BUILD_SCRIPT}" "{PDF_PATH}" sdg_report_2025.xml
```

---

## STEP 4 — XML → chunks → LangChain Documents

One `<subsection>` becomes one chunk. The heading and body become searchable
text; the Goal number, name, pages, and heading become **metadata** — the
provenance that rides along with every hit.

Input is the **canonical XML in Drive** (read-only), so every participant starts
from the exact same edition.

**4-1. XML → chunks.**

```python
import json, xml.etree.ElementTree as ET

XML_PATH = f"{BASE}/Source/sdg_report_2025.xml"   # canonical edition in Drive

root = ET.parse(XML_PATH).getroot()

chunks = []
for goal in root.findall("goal"):
    g_num, g_name, g_pages = int(goal.get("number")), goal.get("name"), goal.get("pages")

    for i, sub in enumerate(goal.findall("subsection")):
        heading = sub.get("heading")
        body    = "\n".join(p.text for p in sub.findall("paragraph") if p.text)

        chunks.append({
            "metadata": {                          # provenance. never embedded.
                "id":        f"G{g_num:02d}-S{i+1:02d}",
                "goal":      g_num,
                "goal_name": g_name,
                "pages":     g_pages,
                "heading":   heading,
            },
            "text": f"{heading}\n{body}",          # body. only this is embedded.
        })

with open("sdg_chunks.jsonl", "w", encoding="utf-8") as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + "\n")

print(f"{len(chunks)} chunks → sdg_chunks.jsonl")
```

**4-2. chunks → LangChain Documents.** Same content, re-cast into the shape
LangChain expects: `page_content` gets embedded (the search target); `metadata`
is not embedded (used to cite provenance).

```python
from langchain_core.documents import Document

docs = [Document(page_content=c["text"], metadata=c["metadata"]) for c in chunks]

print(docs[0].metadata)
```

---

## STEP 5 — Load the encoder · embed every chunk

The encoder is loaded from Drive (local path), not the Hub — the network is
already sealed off. Embeddings are regenerated live here: the vectors this
encoder produces in **this** environment become the canonical set.

**5-1. Load the encoder** (from Drive, local, on GPU).

```python
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name=ENCODER_DIR,
    model_kwargs={"device": "cuda"},
    encode_kwargs={"normalize_embeddings": True},
)
print("Encoder loaded from:", ENCODER_DIR)
```

**5-2. Load the canonical chunks, then embed them.** Input is the canonical
chunks in Drive. Each sentence becomes 384 numbers. On GPU this takes about a
second.

```python
import json, time

CHUNKS_PATH = f"{BASE}/Source/sdg_chunks.jsonl"     # canonical chunks in Drive

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

---

## STEP 6 — Build the vector store (FAISS)

The vectors from STEP 5 go straight in — nothing is recomputed. Vectors and
source text live separately; an index number joins them.

**6-1. Build FAISS from the existing vectors.**

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

---

## STEP 7 — A question becomes a vector too

The same encoder that embedded the chunks now embeds the query. The only
difference: a query carries no metadata.

**7-1. Embed a query and inspect it.**

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

**7-2. Try it yourself.** Re-run this cell as often as you like — it affects
nothing downstream.

```python
import numpy as np

my_query = input("Enter your question (English): ")
mv = np.array(embeddings.embed_query(my_query))

print(f"\n{my_query}")
print(f"→ {len(mv)}-dim vector\n")

for r in range(0, 384, 8):
    print(f"  [{r:3d}] " + "  ".join(f"{x:+.4f}" for x in mv[r:r+8]))
```

---

## STEP 8 — Distance between the query vector and the index

Search is nothing more than measuring distances and sorting. Here we do it **by
hand** — no FAISS — to see what FAISS does for us.

**8-1. Measure the distance to every chunk, then sort.**

```python
import numpy as np

query = "How many people still live in extreme poverty?"
qv    = embeddings.embed_query(query)                  # the query as a vector

V = store.index.reconstruct_n(0, store.index.ntotal)   # all chunk vectors
Q = np.array(qv)                                        # the one query vector

print(f"chunk vectors : {len(V)}, each {len(V[0])} numbers")
print(f"query vector  : 1, {len(Q)} numbers\n")

# measure the distance to each chunk
#   (square the differences, sum all 384, take the square root)
distances = []
for v in V:
    diff = v - Q                        # 384 differences
    dist = np.sqrt((diff ** 2).sum())   # square → sum → square root
    distances.append(dist)

print(f"measured {len(distances)} distances, one per chunk.\n")

# sort nearest first
order = np.argsort(distances)

hand_top3 = [store.index_to_docstore_id[int(i)] for i in order[:3]]

for rank, i in enumerate(order[:3], 1):
    print(f"#{rank}  distance {distances[i]:.4f}   {store.index_to_docstore_id[int(i)]}")
```

---

## STEP 9 — FAISS retrieval + provenance

What we computed by hand in STEP 8, FAISS does in one line. We confirm the
results match, then attach the source (which Goal, which subsection) to every
hit.

**9-1. Ask FAISS, and compare with the hand-computed result.**

```python
query = "How many people still live in extreme poverty?"

results    = store.similarity_search_with_score(query, k=3)
faiss_top3 = [doc.metadata["id"] for doc, _ in results]

print(f"query: {query}\n")
print("STEP 8 (by hand) :", hand_top3)
print("STEP 9 (FAISS)   :", faiss_top3)
print("match            :", hand_top3 == faiss_top3)
```

**9-2. Attach provenance to the search results.** Metadata is never searched —
it rides along with the hit.

```python
def search_with_sources(q, k=3):
    for rank, (doc, dist) in enumerate(store.similarity_search_with_score(q, k=k), 1):
        m = doc.metadata
        print(f"[{rank}]  distance {dist:.4f}")
        print(f"     {m['id']} · Goal {m['goal']} {m['goal_name']} · pp. {m['pages']}")
        print(f"     {m['heading']}")
        print()
        print(doc.page_content)
        print("─" * 70)

query = "How many people still live in extreme poverty?"
search_with_sources(query)
```

---

## STEP 10 — Generation with provenance (Qwen3-0.6B)

The retriever finds evidence; the LLM turns it into an answer. Every answer is
shown together with the sources it rests on.

Qwen3 differs from Flan-T5 in three ways: it is causal, not seq2seq
(`AutoModelForCausalLM`); it is a chat model (input is wrapped in the chat
template); and it echoes the prompt (we slice the answer back out).

**10-1. Load Qwen3 and wrap it as a LangChain LLM.**

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.utils import logging as hf_logging
from langchain_core.language_models.llms import LLM
from typing import Optional, List, Any

hf_logging.set_verbosity_error()          # hide generation-flag notices

tokenizer = AutoTokenizer.from_pretrained(LLM_DIR)
model = AutoModelForCausalLM.from_pretrained(
    LLM_DIR,
    dtype="auto",
    device_map="cuda",
)
print("Loaded:", model.config.model_type,
      f"· {sum(p.numel() for p in model.parameters())/1e6:.0f}M params")


class Qwen3LLM(LLM):
    """Qwen3 behind LangChain's LLM interface: call it with llm.invoke(prompt)."""
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
            enable_thinking=False,          # no <think> block, answer only
        )
        inputs = tokenizer(text, return_tensors="pt").to(model.device)
        prompt_len = inputs.input_ids.shape[1]
        with torch.no_grad():
            out = model.generate(
                **inputs,
                max_new_tokens=self.max_new_tokens,
                do_sample=False,            # greedy: same answer every time
                pad_token_id=tokenizer.eos_token_id,
            )
        answer_ids = out[0][prompt_len:]    # drop the echoed prompt
        return tokenizer.decode(answer_ids, skip_special_tokens=True).strip()


llm = Qwen3LLM()
print("Ready.")
```

**10-2. BEFORE — ask without any context.** No retrieval, no evidence. The model
answers from memory alone: possibly outdated, possibly wrong, with no source to
check.

```python
import textwrap

query = "How many people still live in extreme poverty?"

answer = llm.invoke(query)
print(textwrap.fill(answer, width=80))
```

**10-3. AFTER — answer grounded in retrieved sources.** Retrieve evidence, feed
it to the LLM, and show the answer **with** its sources. Now the answer rests on
the report, and every claim is traceable.

```python
import textwrap

def ask_with_sources(q, k=3):
    # 1. retrieve
    results = store.similarity_search_with_score(q, k=k)

    # 2. build the context from retrieved chunks
    context = "\n\n".join(doc.page_content for doc, _ in results)
    prompt = (
        "Use only the following sources to answer the question. "
        "If the answer is not in the sources, say you cannot find it.\n\n"
        f"{context}\n\n"
        f"Question: {q}"
    )

    # 3. generate
    answer = llm.invoke(prompt)

    # 4. show the answer, then the sources it rests on
    print(textwrap.fill(answer, width=80))
    print("\nSources")
    for doc, _ in results:
        m = doc.metadata
        print(f"  [{m['id']}] Goal {m['goal']} {m['goal_name']} · pp. {m['pages']}")

query = "How many people still live in extreme poverty?"
ask_with_sources(query)
```

---

Compare **10-2** and **10-3**: the same question, answered from the model's
memory versus grounded in the report. The first sounds confident but cannot be
checked; the second rests on named sources you can open and verify. That
contrast is the whole point of provenance-first RAG.
