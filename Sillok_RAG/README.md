# From Searchable Archives to Askable Archives

**[▶ Open the presentation on GitHub Pages](https://littlekg87.github.io/DH2026/Sillok_RAG/)**

| Item | Details |
|---|---|
| Format | **Short Paper** |
| Date and time | **Jul 29, 2026 · 16:30–18:00** |
| Session | **S048** |
| Venue | **Room 106** |
| Title | *From Searchable Archives to Askable Archives: Designing a RAG-Based Research Interface for The Annals of the Joseon Dynasty* |
| Presenter | **Kunha Kim · Sogang University** |

*[한국어](#한국어) | [English](#english)*

---

## 한국어

### 연구 질문

조선왕조실록은 이미 디지털화되어 검색할 수 있지만, 연구자가 자연어 질문에서 출발해 관련 사료를 찾고 그 근거를 검증하는 과정까지 지원하지는 못한다. 이 연구는 “어떤 LLM이 가장 좋은가?”보다 먼저 물어야 할 질문을 제시한다.

> 역사 자료를 위한 RAG는 LLM을 덧붙이는 기능이 아니라, 사료의 구조와 역사학자의 판단을 연결하는 **연구 인터페이스**여야 한다.

### 핵심 설계

Ask Sillok은 세 층이 연결된 연구 아키텍처로 설계되었다.

1. **아카이브 구축**
   - 실록 XML에서 이미 정의된 기사 단위를 청크의 기본 경계로 사용한다.
   - 본문과 메타데이터를 분리해 저장하되, 출처와 증거의 연결은 유지한다.
   - 현대 한국어 질문·제목과 한문 본문이 공존하는 이중언어 구조를 반영하고, 이 자료에 맞게 임베딩 모델을 조정한다.

2. **검색 오케스트레이션**
   - 자연어 질문을 시대·인물·관직·주제 등의 검색 조건으로 해석하고 그 재구성 과정을 기록한다.
   - 의미 기반 벡터 검색과 메타데이터 기반 구조 검색을 병렬로 수행한다.
   - 두 후보군을 합친 뒤 역사적 조건을 반영해 재순위화하고, 근거 사료를 먼저 찾은 다음 답변을 생성한다.

3. **전문가 기반 검증**
   - 벡터 유사도와 역사적 관련성을 서로 다른 평가 대상으로 구분한다.
   - 연구자가 검색된 기록이 실제 증거로 유용한지 판단하고, 그 피드백이 검색·순위화·모델 설계를 다시 바꾸도록 한다.
   - 답변의 각 주장을 인용 구절, 전체 기사, 원문 페이지까지 거슬러 올라갈 수 있게 한다.

### 핵심 주장

- 검색 가능한 아카이브가 곧 질문 가능한 아카이브는 아니다.
- RAG의 품질은 생성 단계 이전의 자료 구조, 청킹, 임베딩, 검색, 재순위화에서 결정된다.
- 출처 표시는 장식이 아니라 사료 비판을 가능하게 하는 조건이다.
- 역사학자는 완성된 시스템의 최종 사용자가 아니라 **연구 환경의 설계자**다.

---

## English

### Research question

The Annals of the Joseon Dynasty are digitized and searchable, but conventional search does not carry a researcher from a natural-language question to historically relevant evidence and a verifiable answer. This study reframes historical RAG as a **research interface**, not an LLM attached to an archive.

### Core design

Ask Sillok connects three layers:

1. **Archive construction** uses the article boundaries already encoded in the XML, preserves the relationship between text, metadata, and provenance, and addresses the archive's Modern Korean–Classical Chinese structure.
2. **Retrieval orchestration** logs query reformulation, combines semantic and structured retrieval, merges candidate sets, and reranks them with historical conditions before generation.
3. **Expert-grounded validation** distinguishes vector similarity from historical relevance and feeds researchers' judgments back into the system.

### Main argument

An askable archive is not created by attaching an LLM. It requires source-aware segmentation, domain-aligned representation, transparent retrieval, historically meaningful ranking, and a return path from every claim to the original record. In this architecture, historians are not merely end users; they are designers of the research environment.
