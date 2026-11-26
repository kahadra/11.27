# Appendix slides (Q&A only, not in the 20-minute plan). exec'd by build_deck.py after the main deck.

TD, MEM, SIG, FA, ROLE, CALLS = (D[k] for k in ("talk_v9", "memory_v8", "signal_fix", "fault", "role", "calls"))


def app(title, body, notes, source):
    add(title, "Appendix · Q&A", 0, body, notes, source)


def _r(n, d): return f"{n / d:.2f}" if d else "–"


app("부록 · 미션 확보 분석 세부",
    table(["지표 (v11b 24판)", "구간", "미확보", "미션 확보 뒤"], [
        ["생존 사이클 수", "전체 · 초반 · 후반", f'{EX["open"]:,} · {EX["open|early"]:,} · {EX["open|late"]:,}', f'{EX["secured"]:,} · {EX["secured|early"]:,} · {EX["secured|late"]:,}'],
        ["거래 제안 / 생존 사이클", "전체 · 초반 · 후반", f'{_r(PR["open"], EX["open"])} · {_r(PR["open|early"], EX["open|early"])} · {_r(PR["open|late"], EX["open|late"])}',
         f'{_r(PR["secured"], EX["secured"])} · {_r(PR["secured|early"], EX["secured|early"])} · {_r(PR["secured|late"], EX["secured|late"])}'],
        ["거래로 넘긴 단서 / 생존 사이클", "전체 · 초반 · 후반", f'{_r(GV["open"], EX["open"])} · {_r(GV["open|early"], EX["open|early"])} · {_r(GV["open|late"], EX["open|late"])}',
         f'{_r(GV["secured"], EX["secured"])} · {_r(GV["secured|early"], EX["secured|early"])} · {_r(GV["secured|late"], EX["secured|late"])}'],
        ["받은 제안을 스스로 수락", "초반", pn(AC["open|early"]), pn(AC["secured|early"])],
        ["받은 제안을 스스로 수락", "후반", pn(AC["open|late"]), pn(AC["secured|late"])],
        ["추리 도전 (정답 / 오답)", "전체", f'{DD["open|right"]} / {DD["open|wrong"]}', f'{DD["secured|right"]} / {DD["secured|wrong"]}'],
        ["도전 이유에 미션·임무 언급", "전체", f'{DD["open|cites_mission"]}/{DD["open|with_reason"]}', f'{DD["secured|cites_mission"]}/{DD["secured|with_reason"]}']], "compact-table small-rows")
    + table(["방해형 미션", "I1 미션 방해", "I2 들키지 않은 배신", "I3 정보 봉쇄", "I4 압박과 신뢰"],
            [["달성 / 배정"] + [f'{ID.get(m, 0)}/{IA.get(m, 0)}' for m in ("I1", "I2", "I3", "I4")]], "compact-table small-rows center")
    + note(f"‘확보’ = 그 시점에 일반 서브 미션 1개 이상 달성 · 초반 1–{CF['late_from'] - 1}, 후반 {CF['late_from']}–30사이클 · 수락은 받은 쪽이 고른 결과만(기계적 거절 제외) · "
           f"도전 시점 중앙값 {CF['accusation_cycle_median']['secured']}사이클 · 이유 언급은 같은 사이클 추리 단계의 마지막 판단 글에서 ‘미션’·‘임무’ 단어 집계"),
    "미션 확보 분석의 세부 수치입니다.",
    "conflict_v11b.py · full-record.json · detail.jsonl")

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
RK = R["ranking_s1"]["rows"]


def _rank_rows(rows, start):
    return [[start + i, f'<b>{r["mbti"]}</b>' if start + i <= 4 else r["mbti"], f'{r["average"]:.1f}', r["total"],
             r["wins"], r["wrong"], r["missions"]] for i, r in enumerate(rows)]


_rh = ["순위", "MBTI", "평균", "총점", "정답", "오답 사망", "미션"]
app("부록 · 최종 실험 순위 (시나리오 1)",
    grid(table(_rh, _rank_rows(RK[:8], 1), "compact-table small-rows center"),
         table(_rh, _rank_rows(RK[8:], 9), "compact-table small-rows center"))
    + note(f"v11b 시나리오 1 · {R['ranking_s1']['games']}판 · 16명이 판마다 12명씩, 1명당 12판 · 평균 = 누적 점수(판 뒤 나눔 포함) ÷ 참가 판 · "
           "정답 = 1위로 맞힌 판(한 판에 여러 명 가능) · 미션 = 달성한 일반 서브 미션 수")
    + take(f"하위 넷은 모두 IS 유형으로 정답 0회 — 그러나 v9·v10 성격별 순위 상관 {D['rank_corr_v9_v10']['rho']} → 성격의 특성으로 읽지 않음"),
    "최종 실험인 시나리오 1의 최종 순위입니다. 상위권은 정답을 2–3번 낸 에이전트이고, 하위 넷은 모두 IS 유형으로 정답이 없었습니다. 다만 캠페인마다 성격별 순위가 크게 흔들려서 성격의 특성으로 해석하지는 않습니다.",
    "ranking_s1.py (standings_published · final_feedback) · 03 실험기록 §7.7")

app("부록 · 장애 실험 (제안서의 두 번째 질문)",
    grid(box("제안서 H3 · 작업 연속성", "“동료가 실패했을 때 어떻게 계속 진행할 수 있는가” — 팀 보고서 서론에서는 제외됨<br><br>"
             f"• 장애를 넣기 전 첫 판이 <b>{FA['stall_hours']}시간</b> 멈춤 (같은 사유의 요청을 두 번 받은 조정 버그, {' → '.join(str(x) for x in FA['funnel'])}건으로 좁힘)<br>"
             f"• 끊긴 플레이어를 GM이 ‘기다림’으로 둠 → 교훈·시간 비용을 넣은 뒤 {FA['t103'][0]} → {FA['t103'][1]}분<br>"
             f"• GM 부재 투표: 기다림 비용을 알리기 전 {VO['rounds']}라운드 → 알린 뒤 {VB['rounds']}번 모두 첫 라운드에 새 GM", "amber"),
         table(["판", "넣은 장애", "이전", "수정 후"], [[r[0], r[1], r[2], r[3]] for r in FAULT_ROWS], "compact-table small-rows"), cls="narrow-left"),
    "제안서의 두 번째 질문이었던 장애 대응 실험입니다. 같은 시드와 같은 장애 계획으로 두 번 돌렸습니다.",
    "v10-fault · v11-fault · v11b-fault · 03 실험기록 §7 · 변경 기록 B67, C28, C29, A63")

app("부록 · 교재가 말한 강점과 약점",
    table(["교재 II (2장 32–33쪽)", "행동으로 잰 것", "결과", "판정"], [
        ["<b>강점</b> · 협업과 전문화", "역할을 나눈 뒤 엉뚱한 행동 수", f'같은 칸에 없는 상대에게 질문 {ROLE["wrong_target"][0]} → {ROLE["wrong_target"][1]}, 해석 불가 {ROLE["unparsable"][0]} → {ROLE["unparsable"][1]}', verdict("확인")],
        ["<b>강점</b> · 병렬성", "30사이클 판의 시간", "1시간에 12–15사이클 → 30사이클 61–65분 (중앙값)", verdict("확인")],
        ["<b>강점</b> · 확장성", "인원을 바꿔 돌리기", "12명만 시험", verdict("미확인")],
        ["<b>강점</b> · 중복성과 복원력", "장애 주입 8판 × 2회", f'3번 판 {FA["t103"][0]} → {FA["t103"][1]}분, 8번 판 {FA["t108"][0]} → {FA["t108"][1]}분', verdict("확인")],
        ["<b>약점</b> · 조정과 소통", "규칙이 강요한 거절", f'{SIG["forced_refusal_before"]:.0%} → {SIG["forced_refusal_after"][0]:.0%}·{SIG["forced_refusal_after"][1]:.0%} · 그러나 {FA["stall_hours"]}시간 멈춤', verdict("부분")],
        ["<b>약점</b> · 낮은 효율", "효용 없는 통로", f'담화방을 끄자 판당 호출 −{100 - 100 * CALLS["per_game"][1] / CALLS["per_game"][0]:.0f}%', verdict("대응")]], "compact-table small-rows"),
    "교재가 말한 멀티에이전트의 강점과 약점을 행동으로 확인한 표입니다.",
    "교재 II Ch.2 pp.32–33 · 03 실험기록 §3, §6, §7")

app("부록 · 담화방 (v9, 끈 이유)",
    table(["확인한 것", "결과"], [
        ["모델 호출 중 담화", f'{100 * TD["call_share"][0] / TD["call_share"][1]:.0f}%'],
        ["판 끝 친밀도", f'{TD["affinity_final"]} (240쌍 중 {TD["affinity_at_100"][0]}쌍이 100)'],
        ["담화를 들은 양 4분위별 승리율", " / ".join(f"{x}%" for x in TD["win_by_quartile"]) + " → 관계 없음"],
        ["같은 칸 짝 전체의 거래 제안 (담화방 전 → 후)", f'{TD["propose_all_before"]}% → {TD["propose_all_after"]}%: 총량은 그대로, 상대만 옮겨 감']], "compact-table small-rows")
    + note(f"v10에서 끔 → 판당 호출 {CALLS['per_game'][0]:,} → {CALLS['per_game'][1]:,}회 · 이후 자연어는 질문·답변·거래에 붙은 말로만 오감"),
    "자유 담화방을 끈 이유입니다.",
    "요소별 영향 분석 v8–v9 §5 · 03 실험기록 §6.2")

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
    grid(box("시기와 생존의 교란", "미션 확보는 후반에 몰리고, 오답으로 죽은 에이전트는 이후 기록에서 빠짐. 후반끼리 비교했지만 사이클 단위 정합은 아님", "amber"),
         box("판 수와 조건", "v11b 24판 · 장애 판에는 장애가, 버전 사이에는 여러 요소가 함께 바뀜 → 한 요소의 효과로 돌리지 않음", "amber"),
         box("모델 하나", "모든 단계를 한 모델로 돌렸다. 기만 0이나 친밀도 천장이 모델 성향일 가능성을 배제하지 못한다", "amber"),
         box("단일 LLM 비교 없음", "멀티에이전트를 고른 이유는 구조적 논증임. 단일 모델과 직접 비교하지 않음", "amber"), cols=2),
    "수치를 읽을 때의 한계입니다.",
    "SOURCES.md")

app("부록 · 출처",
    table(["구분", "내용"], [
        ["팀 기술 보고서", "이재형 · 박천웅 · 황규한, 서론 1.1–1.2 및 참고문헌 [1]–[13] (Hanabi, Codenames, PokerKit, LLM·게임 서베이, Werewolf, CICERO, SOTOPIA, MuSR 등)"],
        ["팀 문서", "1쪽 제안서 (2026.10.05, H1–H3) · 게임 기획서 v1.3 · 미션 개편 v10 · 엔진 competitive.py 점수 규칙"],
        ["교재 I", "M. Wooldridge, <i>An Introduction to MultiAgent Systems</i>, 2nd ed. — §1.2, §1.3 (FAQ)"],
        ["교재 II", "M. Albada, <i>Building Applications with AI Agents</i>, O’Reilly — Ch.2 pp.32–33, Ch.7, Ch.8, Ch.9, Ch.10, Ch.12"],
        ["성격 검사", "IPIP Big-Five 50문항 · McCrae &amp; Costa (1989) MBTI ↔ Big-Five 대응"],
        ["실험 기록", "v9-main2, v10-main, v10-fault, v11-fault, v11b-fault, v11b-s1 (batch.json, full-record.json, detail.jsonl)"],
        ["분석", "analyze.py → results.json · conflict_v11b.py (미션 확보 분석) · b68_followthrough.py · 상호작용 지표 · 요소별 영향 분석 v8–v9"]], "compact-table"),
    "출처입니다.", "SOURCES.md")
