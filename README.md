
# 2026.11.27 IRV_Lab Seminar — 공동 목표와 개인 목표 사이

박천웅 · 발표 제한 20분 + 질의응답.
이 프로젝트로 하는 세 번째 발표입니다. 10.30(에이전트란 무엇인가, 이론)과 11.13(어떻게 만들었나, 구현)에 이어,
팀 기술 보고서(서론 1.1–1.2)의 연구 질문에 마지막 실험(v11b, 24판)으로 답합니다.

핵심 질문: **공동 목표와 개인 목표가 부딪힐 때, 에이전트는 정보를 숨기는가? 협력은 어디서 멈추는가?**
답: 개인 점수(서브 미션)를 확보한 뒤에도 정보를 숨기지 않았습니다. 대신 '손해 없는 추리 도전'으로 판에서 빠졌습니다
(도전 152건 중 140건이 미션 확보 뒤, 정답률 21%). 측정은 에이전트의 말이 아니라 엔진에 남은 행동으로 했습니다.

## 발표 구성

- 본편 **19장**, 부록 **10장**, 전체 **29장**. 본편 계획 **19:00** + 전환 여유 **1:00** = 제한 **20:00**.
  대본은 발표자가 별도로 작성합니다(`presentation_script.md`의 장별 메모는 초안).
- 1–2장: 표지, 목차.
- 3–7장 (00 서론): 지난 두 발표와 오늘, 왜 게임인가, 두 목표가 부딪히는 자리, 관련 연구와 이 연구의 위치, 연구 질문.
- 8–11장 (01 실험 설계와 검증법): 목표 구조, 왜 멀티에이전트인가, 행동 기록으로 재는 법, 조작 점검(성격 설명문).
- 12–16장 (02 결과): RQ1 공개 방식, RQ2 자기 보고, RQ3 개인 점수를 확보한 뒤 · 충돌은 추리 도전에서, RQ4 협력의 대가.
- 17–19장 (03 결론): 한계와 남은 질문, 연구 질문에 대한 답, 정리.
- 부록 20–29장: 미션 확보 분석 세부, 최종 실험 순위(시나리오 1), 장애 실험(제안서의 두 번째 질문), 교재가 말한 강점과 약점, 담화방, 시나리오 1, 거절 회고 이행 세부, 실험 연표, 해석의 한계, 출처.

## 파일

| 파일 | 용도 |
|---|---|
| `technicalreport.docx` | 팀 기술 보고서(서론). 팀원 문서라 저장소에는 올리지 않음 |
| [index.html](index.html) | 1280×720 HTML 발표 화면, 발표자 노트, 20분 타이머 |
| [presentation_script.md](presentation_script.md) | 장별 시간표와 메모(대본 초안) |
| [SOURCES.md](SOURCES.md) | 교재 위치, 실험 기록, 수치의 정의와 한계 |
| [validation.json](validation.json) | 헤드리스 Edge로 확인한 레이아웃·상호작용 결과 |
| `assets/` | 슬라이드 목록(`slide_manifest.json`) |
| `.work/` | 수치 수집(`analyze.py` → `results.json`, 미션 확보 분석 `conflict_v11b.py`), 덱 빌드(`build_deck.py`, 본문 `content_main.py`, 부록 `content_appendix.py`), 검증(`validate_deck.py`), 스크린숏 |

## 실행

`index.html`을 Edge 또는 Chrome에서 엽니다. 다른 컴퓨터로 옮길 때는 폴더 전체를 복사합니다.
글꼴은 CDN에서 불러오므로 인터넷 연결이 없으면 대체 글꼴로 표시됩니다.

- 좌우 화살표, PageUp/PageDown: 이동. `Home`: 첫 장. `End`: 마지막 장.
- `M`: 슬라이드 목록과 번호 이동. `N`: 현재 장의 발표자 노트. `F`: 전체 화면.
- `T` 또는 하단 **시작**: 타이머 시작·일시정지. 하단 되돌림 버튼: 초기화.
- 본편 마지막 장 뒤에는 다음 버튼으로 부록에 들어가지 않습니다. 부록은 목록에서 선택합니다.

## 다시 만들기

실험 기록(`F:\multi_agent_AI_Game\`)이 있는 컴퓨터에서 실행합니다. 거절 회고 이행 분석은 먼저
`F:\multi_agent_AI_Game\발표_후속_v11\analysis\b68_followthrough.py`를 돌려 `b68_followthrough.json`을 만듭니다.

```powershell
$env:PYTHONUTF8 = "1"
python -B F:\multi_agent_AI_Game\발표_후속_v11\analysis\b68_followthrough.py
python -B .work\analyze.py        # 실험 기록 · 지표 표 → .work\results.json
python -B .work\build_deck.py     # → index.html, presentation_script.md, assets\slide_manifest.json
python -B .work\validate_deck.py  # → validation.json, .work\screenshots\, .work\contact_sheet.png
```
