
# 2026.11.27 IRV_Lab Seminar — 멀티에이전트, 어떻게 검증하는가

박천웅 · 발표 제한 20분 + 질의응답.
멀티에이전트 발표의 세 번째입니다. 10.30(멀티에이전트란 무엇인가, 이론)과 11.13(어떻게 만드는가, 실전)에 이어,
수업 팀 프로젝트의 마지막 실험(v10, v11)으로 **만든 시스템이 작동하는지 어떻게 아는가**를 다룹니다.

핵심 주제: **멀티에이전트는 말이 아니라 행동으로 검증해야 한다.**
'말'은 세 가지입니다. 에이전트의 말(회고, 관계 점수, 기억), 설계의 말(인수인계 규칙, 성격 설명문),
교재의 말(멀티에이전트의 강점). 셋 다 엔진에 남은 행동 기록과 맞대어 검증했습니다.

## 발표 구성

- 본편 **20장**, 부록 **6장**, 전체 **26장**. 본편 계획 **19:00** + 전환 여유 **1:00** = 제한 **20:00**.
  대본은 발표자가 별도로 작성합니다(`presentation_script.md`의 장별 메모는 초안).
- 1–2장: 표지, 목차.
- 3–5장 (00 세 번째 질문): 시리즈의 흐름, 실험 환경, 세 가지 '말'.
- 6–9장 (01 에이전트의 말): 관계 점수, 담화방, 거절 회고, 에이전트의 말을 재는 법.
- 10–15장 (02 설계의 말): 설계 문서의 인수인계, 42시간 멈춤, GM이 장애를 배우다, 보이는 비용, 성격 설명문 검사, 성격은 행동에서.
- 16–18장 (03 교재의 말): 왜 멀티에이전트였나, 교재가 약속한 강점, 아직 설명하지 못한 것.
- 19–20장 (04 검증의 설계): 다섯 가지 원칙, 정리(시리즈와 처음으로 돌아감).
- 부록 21–26장: 장애 실험 8판, 시나리오 1, 거절 회고 이행 세부, 실험 연표, 해석의 한계, 출처.

## 파일

| 파일 | 용도 |
|---|---|
| [index.html](index.html) | 1280×720 HTML 발표 화면, 발표자 노트, 20분 타이머 |
| [presentation_script.md](presentation_script.md) | 장별 시간표와 메모(대본 초안) |
| [SOURCES.md](SOURCES.md) | 교재 위치, 실험 기록, 수치의 정의와 한계 |
| [validation.json](validation.json) | 헤드리스 Edge로 확인한 레이아웃·상호작용 결과 |
| `assets/` | 슬라이드 목록(`slide_manifest.json`) |
| `.work/` | 수치 수집(`analyze.py` → `results.json`), 덱 빌드(`build_deck.py`, 본문 `content_main.py`, 부록 `content_appendix.py`), 검증(`validate_deck.py`), 스크린숏 |

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
