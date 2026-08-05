# From Searchable Archives to Askable Archives
## Bilingual Speaker Script — English / 한국어

## How to Use / 사용 방법

- Target delivery time: **8 minutes** at approximately 140 English words per minute.
- 목표 발화 시간은 영문 기준 분당 약 140단어로 **8분**입니다.
- The English and Korean texts are alternatives. **Deliver only one language**; do not read both.
- 영어와 한국어는 서로 대응하는 선택 대본입니다. 발표에서는 **한 언어만** 읽습니다.
- Each English paragraph is followed by its Korean version.
- 모든 영문 문단 바로 아래에 한국어 대응문을 배치했습니다.
- `[Action / 동작]` marks a click or visual demonstration. The action is included in the timing.
- `[Action / 동작]`은 클릭이나 화면 시연 시점을 뜻하며, 소요 시간은 전체 시간에 포함되어 있습니다.
- Slide numbers follow `DH2026_AskableArchives_presentation.html`.
- 슬라이드 번호는 `DH2026_AskableArchives_presentation.html`을 기준으로 합니다.

---

## 1. Title / 표지
**Time / 시간: 0:30 · Cumulative / 누적: 0:30**

**EN**  
Hello. I am Kunha Kim from the Institute for Digital History at Sogang
University. Before I begin, please scan this QR code and open Ask Sillok. An
English interface is available. Ask it anything about the Joseon period—an
event, person, institution, or everyday life. While it prepares an answer, keep
the page open and listen to the presentation. What happens between your question
and that answer is the subject of this talk.

**KO**  
안녕하세요. 서강대학교 디지털역사연구소의 김근하입니다. 시작하기 전에
화면의 QR 코드를 스캔해 Ask Sillok에 접속해 주세요. 영어 화면도 있습니다.
조선시대의 사건, 인물, 제도, 일상생활 등 무엇이든 질문해 보세요. 답변이
생성되는 동안 페이지를 그대로 열어 두고 제 발표를 들어주시기 바랍니다.
여러분의 질문과 그 답변 사이에서 무슨 일이 일어나는지가 오늘 발표의
주제입니다.

---

## 2. Searchable Is Not Askable / 검색 가능 ≠ 질문 가능
**Time / 시간: 0:20 · Cumulative / 누적: 0:50**

**EN**  
The Annals are already digitized and searchable. But conventional search assumes
that users already know the right person, office, event, or historical term.
An askable archive reverses that logic: it begins with a research question and
helps the historian discover the vocabulary and records not yet known.

**KO**  
실록은 이미 디지털화되어 검색할 수 있습니다. 그러나 기존 검색은 사용자가
정확한 인물, 관직, 사건, 시대어를 이미 알고 있다고 전제합니다. 질문 가능한
아카이브는 이 순서를 바꿉니다. 연구 질문에서 시작해, 아직 알지 못한 역사적
어휘와 기록을 발견하도록 돕습니다.

---

## 3. Quality Is a Pipeline Decision / RAG 품질은 파이프라인에서 결정된다
**Time / 시간: 0:25 · Cumulative / 누적: 1:15**

**EN**  
Many RAG projects become obsessed with better LLMs and whatever technology is
currently fashionable. But I think we need to change the question. RAG quality
is decided before generation: by source structure, evidence units, bilingual
encoding, retrieval, ranking, and provenance. The decisive issue is not one
trendy model, but the design between models and sources.

**KO**  
많은 RAG 프로젝트가 더 좋은 LLM과 최신 유행 기술을 적용하는 데 몰두합니다.
하지만 저는 질문부터 바꿔야 한다고 생각합니다. RAG의 품질은 생성 이전의
사료 구조, 증거 단위, 이중 언어 인코딩, 검색, 재순위, 출처 추적에서
결정됩니다. 핵심은 하나의 트렌디한 모델이 아니라 모델과 사료 사이의
설계입니다.

---

## 4. Three Layers of Ask Sillok / Ask Sillok의 세 계층
**Time / 시간: 0:45 · Cumulative / 누적: 2:00**

**EN**  
Ask Sillok connects three layers. First, we paired the Korean title and
Classical Chinese body of roughly 380,000 Annals articles, fine-tuned an
embedding model, and built a vector database specialized only for this archive.
Second, a carefully designed hybrid retrieval system and metadata-based
reranking select the evidence chunks. Most RAG projects stop there. We added a
third layer: ten scholars with PhDs in Joseon history conducted blind
human-in-the-loop tests, and their judgments guided the selection of the best
model. That is today’s
story. There is much more I would like to say, but this is a short paper.
Perhaps I should have submitted a long one.

**KO**  
Ask Sillok은 세 계층을 연결합니다. 먼저 조선왕조실록 약 38만 건의 한국어
제목과 한문 본문을 쌍으로 삼아 임베딩 모델을 파인튜닝하고, 오직 실록에
특화된 벡터 데이터베이스를 만들었습니다. 다음으로 정교한 하이브리드 검색과
메타데이터 기반 재순위로 증거 청크를 고릅니다. 대부분의 RAG는 여기서
끝납니다. 우리는 한 단계를 더 추가했습니다. 조선시대사 박사 열 명이
블라인드 방식의 Human in the Loop 평가를 진행했고, 그 판단으로 최고의
모델을 선택했습니다. 오늘은 이 이야기를 하겠습니다. 사실 하고 싶은
이야기가 많지만 숏 페이퍼 발표이니 짧게 하겠습니다. 롱 페이퍼로 낼 걸
그랬습니다.

---

## 5. Structure Before Vectors / 벡터보다 먼저 구조
**Time / 시간: 0:35 · Cumulative / 누적: 2:35**

**EN**  
The Annals are the official records of Joseon, the dynasty that ruled the Korean
peninsula from the fifteenth through the nineteenth centuries. Their significance
is recognized by UNESCO’s Memory of the World Register. Over many years, the
Korean government converted the records into XML and tagged key information.
As a result, each article already contains meaningful boundaries: a persistent
ID, dates, subjects, and typed entities. We preserve this structure rather than
flattening everything into text. The XML is the archive’s data model.

**KO**  
이 실록 데이터는 15세기부터 19세기까지 한반도를 지배한 조선 왕조의 공식
기록입니다. 유네스코 세계기록유산에 등재될 만큼 중요한 기록이기도 합니다.
한국 정부는 오랜 시간에 걸쳐 이 기록을 XML로 만들고 핵심 정보에 태그를
달았습니다. 덕분에 실록 XML의 각 기사는 영속적인 ID, 날짜, 주제, 유형화된
개체라는 의미 있는 구조를 이미 갖고 있습니다. 우리는 이를 평평한 텍스트로
만들지 않고 보존합니다. XML 자체가 실록의 데이터 모델입니다.

### [Sources / 근거 — 읽지 않음]

- [National Institute of Korean History record](https://sillok.history.go.kr/id/kaa_10201006_001)
- [Sillok XML structure reference](https://wikidocs.net/239521)
- [UNESCO Memory of the World: The Annals of the Choson Dynasty](https://www.unesco.org/en/memory-world/annals-choson-dynasty)

---

## 6. Metadata and Text / 메타데이터와 텍스트
**Time / 시간: 0:25 · Cumulative / 누적: 3:00**

**EN**  
I place special importance on metadata. The philosophy of RAG is to answer from
evidence, so preserving information about that evidence is essential. We store
text and metadata separately for different operations, but a persistent record
ID keeps them as one evidence object. They can then be reunited for filtering,
ranking, citation, and return to the original source.

**KO**  
저는 메타데이터를 매우 중요하게 생각합니다. RAG의 철학은 근거를 바탕으로
답변하는 것입니다. 따라서 RAG를 설계할 때는 근거에 관한 정보, 즉
메타데이터를 보존해야 합니다. 텍스트와 메타데이터는 서로 다른 연산을 위해
분리해 저장하지만, 영속적인 ID로 하나의 증거 객체로 유지합니다. 그래서
필터링, 재순위, 인용, 원문 복귀 단계에서 다시 정확히 결합할 수 있습니다.

---

## 7. A Bilingual Archive / 이중 언어 아카이브
**Time / 시간: 0:15 · Cumulative / 누적: 3:15**

**EN**  
The next challenge is linguistic. Historians ask in modern Korean, while the
original record is in Classical Chinese. The system must bridge the two without
replacing the historical source with a modern paraphrase.

**KO**  
다음 과제는 언어입니다. 역사학자는 현대 한국어로 질문하지만 실록 원문은
한문입니다. 역사적 원문을 현대어 의역으로 대체하지 않으면서 두 언어를
연결해야 합니다.

---

## 8. Two Languages in One XML Record / 하나의 XML 속 두 언어
**Time / 시간: 0:20 · Cumulative / 누적: 3:35**

**EN**  
This bilingual relation exists inside each article. A Korean title and its
Classical Chinese body share one ID: the title names the event for a modern
reader, and the body preserves the historical statement. This pair becomes a
direct training signal.

**KO**  
이 이중 언어 관계는 각 기사 안에 존재합니다. 하나의 ID 아래 한국어 제목은
현대어로 사건을 명명하고, 한문 본문은 역사적 진술을 보존합니다. 이 쌍이
직접적인 학습 신호가 됩니다.

### [Sources / 근거 — 읽지 않음]

- [National Institute of Korean History record](https://sillok.history.go.kr/id/kaa_10201006_001)
- [Sillok XML structure reference](https://wikidocs.net/239521)

---

## 9. Domain-Adapted Embeddings / 도메인 적응 임베딩
**Time / 시간: 0:25 · Cumulative / 누적: 4:00**

**EN**  
We fine-tuned roughly 380,000 articles directly, pairing each Korean title with
its Classical Chinese body. This produced an encoder specialized for the
bilingual structure of the Annals.

**KO**  
우리는 약 38만 건의 기사에서 한국어 제목과 한문 본문을 직접 쌍으로 삼아
파인튜닝했습니다. 이를 통해 조선왕조실록의 이중 언어 구조에 특화된 인코더
모델을 만들었습니다.

**[Action / 동작]** Click **Fine-tuned / 파인튜닝 모델**.

**EN**  
We plan to release both this model and the vector data produced with it on
Hugging Face, possibly as early as the beginning of September. This diagram is
conceptual; unpublished evaluation figures remain reserved.

**KO**  
이 모델과 이 모델로 생성한 벡터 데이터는 빠르면 9월 초에 Hugging Face에
공개할 예정입니다. 화면은 개념도이며 미발표 평가 수치는 공개하지 않습니다.

---

## 10. From Question to Evidence / 질문에서 증거까지
**Time / 시간: 0:40 · Cumulative / 누적: 4:40**

**EN**  
A good vector database alone does not make a good RAG system. Vector similarity
search ranks chunks that are close to the question in embedding space. P@1 and
nDCG@10 do not create that ranking; they evaluate the returned order against
relevance labels. Yet neither closeness nor standard relevance tells us whether
a chunk can serve as historical evidence. Our goal is therefore not one
“correct” chunk, but evidentially useful chunks near the top. Ranking metrics
remain diagnostic tools; experts define useful evidence. Each question then
passes through four decisions: reformulation, dual retrieval, historical
weighting, and evidence with provenance.

**KO**  
좋은 벡터 데이터베이스만으로는 좋은 RAG를 만들 수 없습니다. 벡터 유사도
검색은 벡터 공간에서 질문과 가까운 청크를 상위에 올립니다. P@1과
nDCG@10은 그 순위를 만드는 방식이 아니라, 결과 순위가 관련성 라벨과
얼마나 잘 맞는지 평가하는 지표입니다. 그러나 벡터 거리가 가깝거나
일반적으로 관련 있다는 사실만으로는 그 청크가 역사학적 답변의 근거로
적합한지 알 수 없습니다. 우리의 목표는 하나의 ‘정답 청크’가 아니라,
증거로 쓸 수 있는 청크를 상위에 올리는 것입니다. 순위 지표는 진단
도구이고, 유용한 증거의 기준은 전문가가 정의합니다. 질문은 이를 위해 질의
재정의, 이중 검색, 역사적 가중치, 출처가 연결된 증거라는 네 번의 판단을
거칩니다.

### [Sources / 근거 — 읽지 않음]

- [EACL 2026: classical IR relevance does not fully capture RAG utility](https://aclanthology.org/2026.eacl-long.391/)
- [ACL 2026: distinguishing relevance from utility in RAG](https://aclanthology.org/2026.findings-acl.1579/)

---

## 11. Query Reformulation / 질의 재정의
**Time / 시간: 0:10 · Cumulative / 누적: 4:50**

**EN**  
A natural question may hide several search conditions. We identify people,
periods, events, and terminology before retrieval, and log the reformulation so
the transformation remains reviewable.

**KO**  
자연어 질문에는 여러 검색 조건이 숨어 있습니다. 검색 전에 인물, 시기,
사건, 용어를 식별하고, 변환 과정을 검토할 수 있도록 재정의된 질의를
기록합니다.

---

## 12. Dual Retrieval / 이중 검색
**Time / 시간: 0:20 · Cumulative / 누적: 5:10**

**EN**  
The reformulated question travels through two routes at once.

**KO**  
재정의된 질문은 동시에 두 경로를 통과합니다.

**[Action / 동작]** Click **Replay flow / 흐름 다시 보기** and follow the two paths.

**EN**  
Semantic retrieval finds conceptually related records across the two languages.
Structured retrieval uses people, periods, and metadata. The two paths fail in
different ways, so we merge and rerank their candidates.

**KO**  
의미 검색은 두 언어를 가로질러 개념적으로 관련된 기록을 찾습니다. 구조
검색은 인물, 시기, 메타데이터를 사용합니다. 두 경로는 서로 다르게 실패할
수 있으므로 후보를 합쳐 다시 순위를 정합니다.

---

## 13. Historically Informed Weighting / 역사적 가중치
**Time / 시간: 0:25 · Cumulative / 누적: 5:35**

**EN**  
Vector distance proposes candidates, but historical metadata changes their
order. If a question explicitly names King Sejong, the system finds Sejong in
the metadata and gives matching chunks a bonus, moving them upward. The screen
shows the same logic with a reign, office, and year range.

**KO**  
벡터 거리는 후보를 제안하지만 역사적 메타데이터는 그 순서를 바꿉니다.
예를 들어 질문에 ‘세종’이라는 키워드가 명시되어 있다면, 메타데이터에서
세종을 찾아 일치하는 청크에 가산점을 주고 상위로 끌어올립니다. 화면에서는
같은 원리를 왕대, 관직명, 연도 범위에 적용합니다.

**[Action / 동작]** Click **Office name / 관직명**, **Reign match / 왕대 일치**, and
**Year range / 연도 범위** while speaking.

**EN**  
The same logic applies to an office, reign, year, subject, or person. This is a
transparent ranking function, not an evaluation result.

**KO**  
같은 방식으로 관직명, 왕대, 연도, 주제, 인물에 가산점을 줄 수 있습니다.
이것은 평가 결과가 아니라 투명하게 확인할 수 있는 순위 함수입니다.

---

## 14. Provenance First / 출처를 먼저
**Time / 시간: 0:20 · Cumulative / 누적: 5:55**

**EN**  
The system does not generate an answer and search for a source afterward. It
retrieves the original entry, preserves the full record and metadata, identifies
the cited passage, and only then supports a claim. Provenance is the result of
source structure surviving the pipeline.

**KO**  
이 시스템은 답변을 먼저 만든 뒤 출처를 찾지 않습니다. 실록 원문 기사를
검색하고, 전체 기록과 메타데이터를 보존하며, 인용 구절을 확인한 뒤에야
주장을 만듭니다. 출처 추적은 사료 구조가 파이프라인 끝까지 살아남은
결과입니다.

---

## 15. Similarity Is Not Relevance / 유사도 ≠ 역사적 관련성
**Time / 시간: 0:20 · Cumulative / 누적: 6:15**

**EN**  
This leads to two different meanings of quality. Machine evaluation asks whether
the vectors are close and the expected correspondence was retrieved. Historical
evaluation asks a different question: can a researcher actually use this record
as evidence? A high similarity score cannot answer that alone.

**KO**  
여기서 품질은 두 가지 의미로 나뉩니다. 기계 평가는 벡터가 가까운지,
설계된 대응 관계를 검색했는지 묻습니다. 역사학적 평가는 다른 질문을
합니다. 연구자가 이 기록을 실제 증거로 사용할 수 있는가입니다. 높은
유사도 점수만으로는 여기에 답할 수 없습니다.

---

## 16. Human in the Loop / Human in the Loop
**Time / 시간: 0:25 · Cumulative / 누적: 6:40**

**EN**  
We therefore built an additional evaluation system, and this is a distinctive
part of our research. Instead of relying only on mechanical performance metrics,
ten domain experts judged whether correct and useful chunks were retrieved,
without knowing which model produced them. Human in the Loop means that the
perspective of actual users determines retrieval quality and feeds back into
model selection and redesign.

**KO**  
그래서 우리는 평가 시스템을 하나 더 만들었습니다. 이것이 우리 연구의
특별한 점입니다. 기계적 성능 지표에만 의존하지 않고, 전문가 열 명이 어떤
모델인지 모르는 상태에서 제대로 된 유용한 청크가 검색되었는지
판단했습니다. Human in the Loop은 실제 사용자의 관점이 검색 품질을
결정하고, 그 판단이 모델 선택과 재설계로 돌아간다는 뜻입니다.

---

## 17. Ask Sillok as a Whole / Ask Sillok 전체 구조
**Time / 시간: 0:20 · Cumulative / 누적: 7:00**

**EN**  
The complete architecture operates on three time scales. We build the
archive-native index once. We orchestrate retrieval for every question. And we
continually revise the system through expert judgment and error analysis. These
are not separate modules, but one return path from source to evidence and back
to design.

**KO**  
전체 아키텍처는 세 가지 시간 규모로 작동합니다. 아카이브 고유의 인덱스는
한 번 구축하고, 검색 파이프라인은 모든 질문마다 실행하며, 전문가 판단과
오류 분석을 통해 시스템을 지속적으로 수정합니다. 이들은 분리된 모듈이
아니라 사료에서 증거로, 다시 설계로 돌아오는 하나의 환류 경로입니다.

---

## 18. Live Technology Stack / 실제 운영 기술 스택
**Time / 시간: 0:25 · Cumulative / 누적: 7:25**

**EN**  
Digital humanists sometimes overlook the physical infrastructure that makes
philosophy and design actually work. My team and I did not stop at design; we
used NPU and AWS to build an operating RAG system. So, if AWS has a bad day,
Ask Sillok takes the day off too. I built it with Byungjun Kim, Jeong-hui Park,
Donghyun Woo, and Si-heon Lee. Ask Sillok is a team effort.

**KO**  
디지털인문학자들은 철학과 설계를 실제로 작동하게 하는 물리적 기반을 종종
간과합니다. 저와 우리 팀은 설계에 그치지 않고, NPU와 AWS를 활용해 실제로
작동하는 RAG 시스템을 만들었습니다. 그래서 AWS가 갑자기 망하면 Ask
Sillok도 함께 하루 쉬게 됩니다. 이 시스템은 김병준, 박정희, 우동현,
이시헌 선생님과 함께 만들었습니다. Ask Sillok은 팀의 결과입니다.

---

## 19. Closing / 마무리
**Time / 시간: 0:35 · Cumulative / 누적: 8:00**

**EN**  
RAG essentially shares a philosophy with the humanities, especially history.
What are we trained to do every day? Find evidence and answer from it. That is
why I believe RAG has a central place in the future of digital humanities. If
this work interests you, I would welcome international collaboration; please
contact me anytime. The paper and patent application are currently under review,
so I have had to withhold some key figures and process details today. I
appreciate your understanding. Thank you.

**KO**  
RAG는 본질적으로 인문학, 특히 역사학과 같은 철학을 공유합니다. 우리
인문학자들이 지독하게 잘하고 매일 훈련받는 일, 바로 근거를 찾고 그 근거를
바탕으로 답하는 것입니다. 그래서 저는 디지털인문학의 미래에 RAG가 있다고
믿습니다. 제 발표가 마음에 드셨다면 국제적인 연구 협력을 기대하겠습니다.
언제든 편하게 연락해 주십시오. 이 연구는 현재 논문과 특허 심사 중이어서
핵심 수치와 일부 프로세스를 공개하지 못한 점을 양해 부탁드립니다.
감사합니다.

---

## Timing Summary / 시간 요약

| Section / 구간 | Slides / 슬라이드 | Time / 시간 |
|---|---:|---:|
| Opening and reframing / 도입과 관점 전환 | 1–4 | 2:00 |
| Archive construction / 아카이브 구축 | 5–9 | 2:00 |
| Retrieval orchestration / 검색 파이프라인 | 10–14 | 1:55 |
| Validation, system, and closing / 검증·시스템·마무리 | 15–19 | 2:05 |
| **Total / 합계** | **1–19** | **8:00** |

### Emergency Cut / 비상 단축

If the chair signals that time is short, advance through slide 8 without its
spoken paragraph, omit the live clicks on slide 13, and shorten slide 17 to its
first two sentences. This saves approximately 30–35 seconds while preserving
the new claims, team introduction, and closing.

좌장이 시간 부족 신호를 보내면 8번 슬라이드는 설명 없이 넘기고, 13번
슬라이드의 클릭 시연을 건너뛴 뒤, 17번 슬라이드는 첫 두 문장만 말합니다.
새로 추가한 주장과 팀 소개, 결론은 유지하면서 약 30–35초를 줄일 수
있습니다.
