# Appendix slides (Q&A only, not in the 20-minute plan). exec'd by build_deck.py after the main deck.


def app(title, body, notes, source):
    add(title, "Appendix · Q&A", 0, body, notes, source)


# fault campaigns: same seeds, same fault plan (03 실험기록 §7.2, §7.6)
FAULT_ROWS = [
    ("101", "없음", "ISTP 정답 · 61분", "INFP 정답 · 60분"),
    ("102", "없음", "INFP 정답 · 54분", "정답 4명 · 63분"),
    ("103", "8사이클 플레이어 1명 끊김 (복귀 없음)", "ENTP 정답 · <b>139분</b>", "정답 3명 · <b>68분</b> (끊긴 자리 NPC)"),
    ("104", "8사이클 끊김 → 14사이클 복귀", "ENFJ 정답 · 67분", "INTJ 정답 · 61분 (복귀자는 집계 제외)"),
    ("105", "8사이클 GM 끊김 (복귀 없음)", "INTP 정답 · 57분", "마감 · 65분 (대기자가 GM 승계)"),
    ("106", "8사이클 GM 끊김 → 14사이클 복귀", "ENFP 정답 · 88분", "ENFP 정답 · 62분 (승계 후 반환)"),
    ("107", "플레이어 4명이 차례로 끊김", "마감 · 86분", "정답 3명 · 57분"),
    ("108", "GM이 다섯 번 끊김", "대기자 소진 무효 · <b>538분</b>", "대기자 소진 무효 · <b>39분</b>"),
]
app("부록 · 장애 실험 8판",
    table(["판", "넣은 장애", "이전 설명문 (결과 · 시간)", "수정 설명문 + 새 에이전트 (결과 · 시간)"], [list(r) for r in FAULT_ROWS], "compact-table small-rows")
    + note("두 회차 사이에 바뀐 것: GM 교훈과 시간 보상(3번 판 이후), 기다림 비용 고지, 성격 설명문 두 문장, 새 에이전트 16명. 판마다 한 번씩이라 시간 차이는 사례로 읽는다."),
    "같은 시드와 같은 장애 계획으로 두 번 돌린 장애 실험입니다.",
    "v11-fault-30c-lean · v11b-fault-30c-lean · 03 실험기록 §7.2, §7.6")

S1_ROWS = [("201", "ESTP", 24, 52), ("202", "ESFP", 30, 73), ("203", "INFP", 29, 72), ("204", "ESTJ", 30, 70), ("205", "ESFP, ENFJ", 30, 72),
           ("206", "ENFP", 24, 48), ("207", "ESTP, INFJ", 27, 56), ("208", "마감", 30, 69), ("209", "ENTJ", 19, 42), ("210", "ENTP", 30, 65),
           ("211", "INFJ, ESFP, ENFP", 30, 62), ("212", "INTJ", 28, 65), ("213", "ENFP, INFJ, INTP", 30, 68), ("214", "ESTP, INTJ, ESTJ, ENTJ", 30, 68),
           ("215", "ENFJ", 25, 55), ("216", "ESFJ", 26, 53)]
half = len(S1_ROWS) // 2
app("부록 · 시나리오 1 (16판)",
    grid(table(["판", "정답자", "사이클", "분"], [list(r) for r in S1_ROWS[:half]], "compact-table small-rows center"),
         table(["판", "정답자", "사이클", "분"], [list(r) for r in S1_ROWS[half:]], "compact-table small-rows center"))
    + note("에이전트 16명이 판마다 12명씩, 1명당 정확히 12판 · 평균 점수 상위 " + ", ".join(f"{m} {v}" for m, v in D["s1_rank"]["top"])
           + " · 하위 " + ", ".join(f"{m} {v}" for m, v in D["s1_rank"]["bottom"])),
    "새 에이전트 16명의 시나리오 1 판별 결과와 순위입니다.",
    "v11b-s1-30c-lean · 03 실험기록 §7.7")

pl = FTS["plans"]
app("부록 · 거절 회고 이행 세부",
    table(["상대가 고른 거절 뒤", "v10 (회고 없음)", "v11b 장애 8판", "v11b 시나리오 1"], [
        ["거절 수 (회고와 연결)", f'{FT10["refusals"]}', f'{FTF["refusals"]} ({FTF["reviewed"]})', f'{FTS["refusals"]} ({FTS["reviewed"]})'],
        ["2사이클 안에 그 상대에게 질문", pn(FT10["asked_2c"]), pn(FTF["asked_2c"]), pn(FTS["asked_2c"])],
        ["그 뒤 같은 상대에게 다시 제안", pn(FT10["again"]), pn(FTF["again"]), pn(FTS["again"])],
        ["다시 제안 전에 그 상대에게 질문", pn(FT10["asked_before_again"]), pn(FTF["asked_before_again"]), pn(FTS["asked_before_again"])],
        ["다시 제안할 때 조건 변경", pn(FT10["changed"]), pn(FTF["changed"]), pn(FTS["changed"])],
        ["다시 제안한 거래 성사", pn(FT10["again_settled"]), pn(FTF["again_settled"]), pn(FTS["again_settled"])]], "compact-table small-rows")
    + table(["회고에 쓴 것 (시나리오 1)", "건수", "2사이클 안에 그 상대에게 질문", "같은 상대에게 다시 제안", "다시 제안 때 조건 변경"], [
        ["먼저 확인 · 질문", pl["ask"]["n"], pn(pl["ask"]["asked_2c"]), pn(pl["ask"]["again"]), pn(pl["ask"]["changed"])],
        ["조건 · 유형 변경", pl["terms"]["n"], pn(pl["terms"]["asked_2c"]), pn(pl["terms"]["again"]), pn(pl["terms"]["changed"])],
        ["다른 상대", pl["other"]["n"], pn(pl["other"]["asked_2c"]), pn(pl["other"]["again"]), pn(pl["other"]["changed"])]], "compact-table small-rows")
    + note("회고 문장 분류는 정규식으로 센 근사치(한 회고가 여러 항목에 들 수 있음). 조건 = 주는 유형과 원하는 유형. 회고와 다음 행동은 같은 모델 호출에서 나온다."),
    "거절 회고를 실제로 이행했는지의 세부 수치입니다.",
    "b68_followthrough.py · detail.jsonl · full-record.json")

app("부록 · 실험 연표와 조건",
    table(["단계", "기간", "규모", "바뀐 것", "결과"], [
        ["v9 (11.13 발표까지)", "11/9–12", "16판", "기억 체계, 모델 교체, 승자 독식, 담화방", "정답자 나온 판 10/16"],
        ["v10", "11/12–14", "16판", "자동 판정 제거, 거래 순서 처리, 담화방 끔, 미션 개편", "13/16"],
        ["v10 장애", "11/14–16", "1판에서 멈춤", "—", "42시간 멈춤 → 원인 규명"],
        ["v11 장애", "11/16–18", "8판", "요청 번호, 거절 회고, GM이 장애를 배움", "6/8"],
        ["성격 검사", "11/18", "2회", "설명문 S·E 문장 수정", "T/F 구분 83% → 100%"],
        ["v11b 장애 · 시나리오 1", "11/19–22", "8판 + 16판", "새 에이전트 16명, 기다림 비용 고지", "6/8 · 15/16"]], "compact-table small-rows")
    + note("모델: gpt-6.1-terra via Codex CLI (reasoning medium) · 30사이클 · 판마다 12명 · 공유 계정이라 하루 사용량을 나눠 씀"),
    "실험 연표와 조건입니다.",
    "batch.json · 03 실험기록 · 변경 기록")

app("부록 · 해석의 한계",
    grid(box("동시에 바뀐 것", "v9→v10, 이전 설명문→v11b 모두 여러 요소가 함께 바뀌었다. 한 요소의 효과로 돌리지 않는다", "amber"),
         box("판 수", "장애 시나리오는 시나리오마다 1판, 캠페인은 8–16판. 판별 결과는 사건 난이도와 운의 영향이 크다", "amber"),
         box("모델 하나", "모든 단계를 한 모델로 돌렸다. 기만 0이나 친밀도 천장이 모델 성향일 가능성을 배제하지 못한다", "amber"),
         box("단일 LLM 비교 없음", "멀티에이전트를 고른 이유는 구조적 논증이다. 단일 모델과 직접 비교하지 않았다", "amber"), cols=2),
    "수치를 읽을 때의 한계입니다.",
    "SOURCES.md")

app("부록 · 출처",
    table(["구분", "내용"], [
        ["교재 I", "M. Wooldridge, <i>An Introduction to MultiAgent Systems</i>, 2nd ed. — §1.2, §1.3 (FAQ)"],
        ["교재 II", "M. Albada, <i>Building Applications with AI Agents</i>, O’Reilly — Ch.2 pp.32–33, Ch.7, Ch.8, Ch.9, Ch.10, Ch.12"],
        ["성격 검사", "IPIP Big-Five 50문항 · McCrae &amp; Costa (1989) MBTI ↔ Big-Five 대응"],
        ["실험 기록", "v9-main2, v10-main, v10-fault, v11-fault, v11b-fault, v11b-s1 (batch.json, full-record.json, detail.jsonl)"],
        ["분석", "analyze.py → results.json · b68_followthrough.py · 상호작용 지표 · 요소별 영향 분석 v8–v9"]], "compact-table"),
    "출처입니다.", "SOURCES.md")
