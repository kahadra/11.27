# Main-deck content for build_deck.py (exec'd there; uses its helpers and numbers).
# Theme (team technical report, 1.1-1.2): when a shared goal and a personal goal conflict, how do LLM agents
# disclose or withhold information, and where does cooperation continue or stop?
# Sections: 00 introduction · 01 design and method · 02 results (RQ1-RQ4, RQ3 at the centre) · 03 conclusion.
# Slide text: noun / ~함 / ~임 endings. Spoken notes: polite speech.

CF = R["conflict"]
CAP, FLOW, MIS = D["capacity"], D["flow"], D["missions"]
ACCV = D["accuse_v9b"]
ST = MET["settle"]
PAIRS = MET["pairs"]
EX, PR, GV, AC, DD = CF["exposure"], CF["proposals"], CF["trade_clues_given"], CF["accept"], CF["accusations"]


def per(n, d): return n / d if d else 0


p_open, p_sec = per(PR["open|late"], EX["open|late"]), per(PR["secured|late"], EX["secured|late"])
g_open, g_sec = per(GV["open|late"], EX["open|late"]), per(GV["secured|late"], EX["secured|late"])
p_open_all, p_sec_all = per(PR["open"], EX["open"]), per(PR["secured"], EX["secured"])
g_open_all, g_sec_all = per(GV["open"], EX["open"]), per(GV["secured"], EX["secured"])
ded_total = sum(DD.get(k, 0) for k in ("secured|right", "secured|wrong", "open|right", "open|wrong"))
ded_sec = DD["secured|right"] + DD["secured|wrong"]
ded_open = DD["open|right"] + DD["open|wrong"]
IA, ID = CF["imission_assigned"], CF["imission_achieved"]
dec_n = DEC["v11b-fault-30c-lean"][1] + DEC["v11b-s1-30c-lean"][1]
dec_bad = DEC["v11b-fault-30c-lean"][0] + DEC["v11b-s1-30c-lean"][0]
REL = MET["affinity"]["relationship_changes"]["reaction"]
hi_f, hi_t = ACC["high(>=60)|F"], ACC["high(>=60)|T"]
no_f, no_t = ACC["no_score|F"], ACC["no_score|T"]
c10, cs = FT10, FTS
AP = MET["approaches"]
T_, F_ = AX["TF|T"], AX["TF|F"]

add("공동 목표와 개인 목표 사이", "Title", 15, "",
    "멀티에이전트 발표 세 번째입니다. 오늘은 이 프로젝트가 처음부터 던진 질문, 공동 목표와 개인 목표가 부딪힐 때 에이전트가 어떻게 행동하는가에 최종 실험으로 답해 보겠습니다.",
    "수업 팀 프로젝트 · 팀 기술 보고서 · 발표자 박천웅")

add("목차", "Roadmap", 20,
    '<div class="toc-grid four">'
    '<button class="toc-item" data-jump="3"><span>00</span><div><h3>서론</h3><p>지난 발표 · 왜 게임인가 · 두 목표의 충돌 · 관련 연구 · 연구 질문</p></div><b>@@S3@@–@@E7@@</b></button>'
    '<button class="toc-item" data-jump="8"><span>01</span><div><h3>실험 설계와 검증법</h3><p>목표 구조 · 왜 멀티에이전트인가 · 행동 기록으로 재는 법 · 조작 점검</p></div><b>@@S8@@–@@E11@@</b></button>'
    '<button class="toc-item" data-jump="12"><span>02</span><div><h3>결과</h3><p>RQ1 공개 방식 · RQ2 자기 보고 · <b>RQ3 개인 목표와의 충돌</b> · RQ4 협력의 대가</p></div><b>@@S12@@–@@E16@@</b></button>'
    '<button class="toc-item" data-jump="17"><span>03</span><div><h3>결론</h3><p>한계 · 연구 질문에 대한 답 · 정리</p></div><b>@@S17@@–@@E19@@</b></button>'
    "</div>" + take("오늘의 질문: 공동 목표와 개인 목표가 부딪힐 때, 에이전트는 정보를 숨기는가?"),
    "서론에서 질문을 세우고, 실험 설계와 검증 방법을 본 뒤, 네 가지 연구 질문의 결과를 보고 결론으로 마무리합니다. 가장 길게 다룰 것은 세 번째, 개인 목표와의 충돌입니다.",
    "발표 구성")

# ---------------- 00 · Introduction -----------------------------------------------------------------
add("지난 두 발표와 오늘", "00 · Introduction", 40,
    '<div class="series">'
    '<div class="scard"><small>10.30 · 이론</small><h3>에이전트란 무엇인가</h3><p>스스로 결정하는 시스템<br>모델 + 도구 + 메모리 + 오케스트레이션<br><b>핵심은 시스템 설계</b></p></div>'
    '<div class="scard"><small>11.13 · 구현</small><h3>어떻게 만들었나</h3><p>LLM 에이전트 12명의 추리 게임<br>의도와 구현의 간극을 요소별로 수정<br><b>“경쟁은 돌아왔지만 정답보다 내 점수를 지키는 쪽, 협력의 규범은 남음”</b></p></div>'
    '<div class="scard now"><small>11.27 · 연구 질문</small><h3>두 목표가 부딪힐 때</h3><p>11.13의 관찰을 연구 질문으로 정리<br>최종 실험(v11b, 24판)으로 답함<br><b>정보를 숨기는가, 협력은 어디서 멈추는가</b></p></div></div>'
    + take("11.13에서 본 현상 → 팀 보고서의 연구 질문 → 최종 실험의 답"),
    "10월 30일에는 에이전트가 무엇인지, 11월 13일에는 직접 만든 과정을 말씀드렸습니다. 11.13의 결론은, 경쟁은 돌아왔지만 정답보다 내 점수를 지키는 쪽이었고 협력의 규범은 남았다는 것이었습니다. "
    "오늘은 이 관찰을 팀 보고서의 연구 질문으로 정리하고, 마지막 실험으로 답해 보겠습니다.",
    "2026.10.30 · 2026.11.13 세미나")

add("왜 게임인가", "00 · Introduction", 70,
    grid(box("규칙 기반 게임 = 실험 환경", "누가 언제 어떤 정보를 얻고 어떤 행동을 고를 수 있는지 <b>규칙으로 명시 가능</b> [2]<br><br>"
             "발언과 후속 행동을 함께 기록 → <b>무엇을 전달받은 뒤 무엇을 골랐는지</b> 확인 가능 (예: Codenames [3])", "teal"),
         table(["게임 유형", "정보", "판단의 근거"], [
             ["완전정보 (체스·바둑)", "모두가 같은 판을 봄", "판의 상태"],
             ["불완전정보 (포커)", "각자 비공개 정보", "관찰 + 상대의 행동 · <b>형식이 정해짐</b> [4]"],
             ["자연어 소셜 게임", "각자 비공개 정보", "상대의 <b>발언</b> · 의미가 대화와 상황에 따라 바뀜 [5]"]], "compact-table small-rows"),
         cls="wide-left")
    + take("연구 범위: 형식으로 정해진 정보로 고르는 문제 → <b>에이전트가 대화를 직접 해석해 다음 판단에 반영</b>하는 문제"),
    "왜 게임인가부터 보겠습니다. 게임은 누가 언제 어떤 정보를 얻고 어떤 행동을 할 수 있는지를 규칙으로 정할 수 있어서 좋은 실험 환경입니다. "
    "포커 같은 불완전정보 게임은 정보가 비대칭이지만 행동의 형식이 정해져 있습니다. 자연어로 소통하는 소셜 게임에서는 발언의 의미가 상황에 따라 바뀌기 때문에, 에이전트가 대화를 직접 해석해야 합니다.",
    "팀 기술 보고서 1.1 · [2] Hanabi · [3] Codenames · [4] PokerKit · [5] LLM과 게임 서베이")

add("두 목표가 부딪히는 자리", "00 · Introduction", 55,
    grid(box("텍스트 = 판단의 근거이자 조율 수단", "늑대인간: 이전 대화와 경험으로 신뢰와 대립 형성 [6]<br>Diplomacy (CICERO): 자연어 협상으로 공동 행동 조율 [7]", "teal"),
         box("여기에 두 목표가 함께 주어지면", "<b>공동 목표</b>: 사건 해결 — 단서를 공개할수록 유리<br><b>개인 목표</b>: 비밀 유지, 개인 점수 — 공개가 불리할 수 있음<br><br>"
             "→ <b>같은 공개 행동이 두 목표에 서로 다른 결과</b>", "amber"))
    + take("관찰할 것: 무엇을 누구에게 공개하고 누구와 협력하는가 — 특히 <b>두 목표가 충돌하는 지점</b>에서"),
    "늑대인간이나 Diplomacy 연구는 대화가 상대를 판단하는 근거이자 행동을 조율하는 수단이 된다는 것을 보여 줬습니다. "
    "여기에 공동 목표와 개인 목표가 함께 있으면, 같은 단서를 공개하는 행동이 한쪽에는 이득, 다른 쪽에는 손해가 될 수 있습니다. 이 충돌 지점에서 에이전트가 무엇을 하는지가 오늘의 관심입니다.",
    "팀 기술 보고서 1.1 · [6] Xu et al. Werewolf · [7] Meta FAIR CICERO")

add("관련 연구와 이 연구의 위치", "00 · Introduction", 70,
    table(["연구", "환경", "보여 준 것", "남은 질문"], [
        ["Xu et al. [6]", "늑대인간", "대화·경험으로 다음 판단", "—"],
        ["CICERO [7]", "Diplomacy", "자연어 협상으로 공동 행동 조율", "—"],
        ["Hakimov et al. [3]", "Codenames", "단서 구성·해석 성과가 모델·조건마다 다름", "소통 능력 ≠ 목표 달성"],
        ["SOTOPIA [12]", "사회적 시나리오", "어려운 시나리오에서 GPT-4 목표 달성률 < 인간", "소통 능력 ≠ 목표 달성"],
        ["MuSR [13]", "사건 서술 추리", "<b>주어진</b> 단서를 종합해 범인 추론", "단서가 흩어져 있다면?"],
        ['<b class="hl">이 연구</b>', "머더 미스터리 TRPG", "단서가 12명에게 분산 · 공동 + 개인 목표", "<b>공개 결정 자체가 변수</b>"]], "compact-table small-rows")
    + take("MuSR은 단서가 주어진 추리 — 이 연구는 <b>누가 무엇을 공개하느냐에 따라 추리 재료가 달라지는</b> 환경"),
    "관련 연구를 한 표로 정리했습니다. Codenames와 SOTOPIA는 자연어로 소통하는 능력과 그 소통으로 목표를 이루는 능력이 다르다는 것을 보여 줍니다. "
    "MuSR은 주어진 단서로 범인을 추리하지만, 우리 환경에서는 단서가 열두 명에게 흩어져 있어서 누가 무엇을 공개하느냐가 곧 추리의 재료를 정합니다.",
    "팀 기술 보고서 1.2 · [3] [6] [7] [12] SOTOPIA · [13] MuSR")

add("연구 질문", "00 · Introduction", 45,
    '<div class="conclusion-list">'
    '<div><span>1</span><p><b>어떻게 공개하나</b> — 질문과 거래로 단서가 어떻게 오가는가</p></div>'
    '<div><span>2</span><p><b>무엇이 공개 결정을 좌우하나</b> — 에이전트의 자기 보고(친밀도 · 회고)가 실제 선택을 설명하는가</p></div>'
    '<div class="hl"><span>3</span><p><b>개인 목표와 부딪히면</b> — 개인 점수를 확보한 뒤 정보를 숨기는가, 협력은 어디서 멈추는가 <small>(오늘의 중심)</small></p></div>'
    '<div><span>4</span><p><b>협력의 대가</b> — 도운 쪽은 보답을 받는가</p></div></div>'
    + take("보고서 1.1: “개인 목표와 충돌하는 지점에서 그 협력이 어떻게 이어지거나 중단되는지”"),
    "연구 질문은 넷입니다. 어떻게 공개하는가, 무엇이 그 결정을 좌우하는가, 개인 목표와 부딪히면 어떻게 되는가, 협력하면 보답을 받는가. 오늘의 중심은 세 번째입니다.",
    "팀 기술 보고서 1.1 · 1쪽 제안서 (2026.10.05)")

# ---------------- 01 · Design and method ----------------------------------------------------------
add("실험 환경: 목표 구조", "01 · Design", 80,
    '<div class="arch">'
    '<div class="abox eng"><h3>엔진 = 심판</h3><p>판정 · 점수 · <b>모든 행동을 사실로 기록</b></p></div>'
    '<div class="abox gm"><h3>GM = 진행자</h3><p>단계 진행 · 행동 요구서</p></div>'
    '<div class="abox pl"><h3>플레이어 12명</h3><p>같은 모델, 각자의 정보 · 기억 · 성격 · 점수</p></div></div>'
    + note(f"사건 {CAP['combos']}가지 중 하나 · 30사이클 · 행동: 이동 → 탐색 · 질문 · 거래 → 추리 도전 · 최종 실험 v11b: 새 에이전트 16명, 장애 실험 8판 + 시나리오 1 16판 = 24판")
    + table(["목표", "내용", "충돌"], [
             ["<b>공동</b> · 사건 해결", f"혼자서는 못 풂: 개인 정보로 남는 조합 평균 {CAP['personal']}개, 팀 전체를 합치면 {CAP['team']}개", "단서를 공개할수록 유리"],
             ["<b>개인</b> · 서브 미션", f"1인 3개, 각 {MIS['points']}점 · 판마다 {MIS['share_obstruction']}에게 <b>방해형</b> (배신 · 정보 봉쇄 · 미션 방해 · 압박)", "공개가 불리할 수 있음"],
             ["<b>승자 독식</b>", "누가 맞히면 다른 생존자는 0점, <b>미션 점수도 사라짐</b>", "남이 푸는 것 = 내 손해"],
             ["판 뒤 나눔", "1위가 점수 일부를 원하는 상대에게 나눌 수 있음 (강제 없음)", "협력의 보상 통로"]], "compact-table small-rows")
    + take("공동 목표에는 공개가 필요하고, 개인 점수는 <b>남이 맞히는 순간 사라지는</b> 구조"),
    "구조는 엔진이 심판이자 기록자, GM이 진행자, 플레이어 열두 명이 각자 판단하는 형태입니다. 목표 구조가 중요합니다. 사건은 혼자서는 못 풀어서 공개가 필요합니다. "
    "반면 개인 미션이 있고, 일부에게는 배신이나 정보 봉쇄 같은 방해형 미션이 주어집니다. 그리고 승자 독식이라 남이 맞히면 내 미션 점수도 사라집니다. 두 목표가 점수에서 실제로 부딪히는 구조입니다.",
    "게임 기획서 v1.3 · 04 요소별 설계변화 §2, §3, §7 · competitive.py (점수 규칙)")

add("왜 멀티에이전트인가", "01 · Design", 55,
    table(["LLM 하나로 12명을 흉내 내면?", "잃는 것"], [
        ["사적 정보", "각자만 아는 단서가 한 맥락에 섞임 → 공개 · 보류라는 결정 자체가 사라짐"],
        ["각자의 기억", "같은 교훈으로 수렴 (v8: 16명이 같은 전술) ↔ 기억을 따로 두자 서로 같은 통찰 문장 0개"],
        ["각자의 점수", "개인 목표와 공동 목표의 충돌이 사라짐 — 이 연구가 보려는 바로 그것"]], "compact-table")
    + note("제안서 가설 H1(단일 LLM과 직접 비교)은 수행하지 않음 → 이 답은 구조적 논증임")
    + take("멀티에이전트 = <b>정보 · 기억 · 점수가 분리된</b> 행위자들 — 공개 결정이 존재하기 위한 전제"),
    "왜 멀티에이전트였는지도 짚겠습니다. LLM 하나가 열두 명을 흉내 내면 각자만 아는 정보가 한 맥락에 섞여서, 공개하거나 보류한다는 결정 자체가 사라집니다. 점수가 하나면 목표의 충돌도 없습니다. "
    "다만 단일 모델과 직접 비교한 실험은 하지 않았기 때문에, 이것은 구조적 논증입니다.",
    "1쪽 제안서 H1 · 11.13 세미나 · v8 보고서")

add("검증법: 말이 아니라 행동 기록으로", "01 · Design", 60,
    grid(ul("<b>엔진이 기록한 사실만 사용함</b> — 거래 이행(trade_judged), 단서 이동(disclosures), 미션 달성, 추리 도전. 의도를 코드가 판정하지 않음",
            "<b>당시 상태로 나눔</b> — 그 순간 개인 미션을 확보했는가(확보 / 미확보). 같은 시기끼리 비교(15사이클 이후)",
            "<b>기준선과 비교함</b> — 회고가 없던 버전의 같은 상황과 맞댐",
            "<b>자기 보고는 데이터로만 씀</b> — 친밀도 · 회고 · 추리 이유는 행동과 대조할 대상"),
         box("왜 필요한가 (11.13에서 본 사례)", f"에이전트는 얻은 단서를 <b>{D['memory_v8']['remembered']}개</b>로 기억했지만 실제로는 <b>{D['memory_v8']['actual']}개</b> (기억 저장 결함)<br><br>"
             "그 틀린 기억으로도 <b>성실하게 회고</b>함 → 에이전트의 글만 보면 오판함", "amber"), cls="wide-left")
    + take("에이전트의 말은 <b>데이터</b>, 증거는 <b>엔진에 남은 행동</b>"),
    "검증 방법입니다. 엔진이 사실로 기록한 것만 쓰고, 그 순간 에이전트가 개인 미션을 확보했는지로 상태를 나눠 같은 시기끼리 비교합니다. 친밀도나 회고 같은 자기 보고는 증거가 아니라 행동과 대조할 데이터로 씁니다. "
    "11.13에서 말씀드린 것처럼, 에이전트는 틀린 기억으로도 성실하게 회고했기 때문입니다.",
    "08 상호작용 지표 §1 · conflict_v11b.py · v8 캠페인 보고서")

add("조작 점검: 성격 설명문", "01 · Design", 50,
    grid(box("확인할 것", "같은 모델 16명에게 MBTI 16유형의 성격 설명문을 줌 → <b>의도대로 읽히는가?</b><br><br>"
             "표준 성격 문항(IPIP Big-Five 50문항)으로 검사 · MBTI ↔ Big-Five 대응 McCrae &amp; Costa (1989)", "violet"),
         table(["지표 (MBTI 글자를 뺀 설명문)", "1차", "수정 후"], [
             ["T/F가 중앙값 기준으로 갈리는 비율", pct(P1["tf_split"]), pct(P2["tf_split"])],
             ["E가 우호성(배려)에 섞이는 정도 d", f'{P1["e_on_agree"]:.2f}', f'{P2["e_on_agree"]:.2f}'],
             ["ENTJ가 일반적인 모습과 닮은 정도", f'{D["probe_entj"]["p1"]}', f'{D["probe_entj"]["p2"]}']], "compact-table small-rows center"),
         cls="narrow-left")
    + note("1차에서 S 문장은 ‘상상력 없음’, E 문장은 ‘배려’로 읽힘 → 두 문장만 고친 뒤 새 에이전트로 최종 실험")
    + take("성격 조건을 게임 전에 <b>따로 검사</b>한 뒤 실험에 투입함"),
    "실험 전에 조작 점검도 했습니다. 성격 설명문이 의도대로 읽히는지 표준 성격 문항으로 검사했더니, S 문장은 상상력이 없다로, E 문장은 배려로 읽히고 있었습니다. 두 문장을 고친 뒤 T와 F가 100퍼센트 갈렸고, 그다음에 최종 실험을 돌렸습니다.",
    "personality-probe-1 · -2 summary.json · 성격검사 설계 · 변경 기록 B70")

# ---------------- 02 · Results ---------------------------------------------------------------------
add("RQ1 · 어떻게 공개하나", "02 · Results", 65,
    tiles([(f'{pf([ST["settled"], ST["proposals"]])}', f'거래 성사 ({ST["settled"]:,}/{ST["proposals"]:,})'),
           (f'{pf([ST["settled_after_counter"], ST["countered"]])}', f'역제안 뒤 성사 ({ST["settled_after_counter"]}/{ST["countered"]})'),
           (f'{dec_bad}/{dec_n}', "기만 (약속과 다른 단서)"),
           (f'{FLOW["via_question"]:,} · {FLOW["via_trade"]:,}', "단서 이동: 질문 · 거래")])
    + grid(table(["질문 방식", "사용", "단서가 넘어온 비율"], [
        ["일반 질문", f'{AP["question"]["n"]:,}', pct(AP["question"]["transfer_rate"])],
        ["설득", f'{AP["persuade"]["n"]}', pct(AP["persuade"]["transfer_rate"])],
        ["심문", f'{AP["interrogate"]["n"]}', pct(AP["interrogate"]["transfer_rate"])],
        ["협박", f'{AP["threaten"]["n"]}', pct(AP["threaten"]["transfer_rate"])]], "compact-table center"),
        table(["성향 (판당)", "T", "F"], [
            ["질문", f'{float(T_["questions_per_game"]):.1f}', f'{float(F_["questions_per_game"]):.1f}'],
            ["거래 제안", f'{float(T_["trade_proposals_per_game"]):.1f}', f'{float(F_["trade_proposals_per_game"]):.1f}'],
            ["질문 중 심문·협박", f'<b>{100 * float(T_["hostile_share"]):.1f}%</b>', f'<b>{100 * float(F_["hostile_share"]):.1f}%</b>']], "compact-table center"))
    + take("거절보다 <b>조건 조정</b>(역제안)으로 흥정함 · 속일 수 있어도 속이지 않음 · 성향은 양이 아니라 <b>방식</b>에서 드러남"),
    "첫 번째 질문, 어떻게 공개하는가입니다. 거래는 60퍼센트가 성사됐고, 역제안은 거절이 아니라 조건 조정으로 쓰여 86퍼센트가 성사로 끝났습니다. 속일 수 있게 설계했지만 기만은 한 건도 없었습니다. "
    "성향은 양이 아니라 방식에서 드러났습니다. T는 질문의 4분의 1이 심문이나 협박이었고, F는 1퍼센트도 안 됐습니다.",
    "08 상호작용 지표 §3 A–E · metrics.json D, E · per_axis.csv · 엔진 trade_judged")

add("RQ2 · 자기 보고는 선택을 설명하나", "02 · Results", 85,
    grid(box("① 친밀도 (에이전트가 상대마다 스스로 매긴 점수)",
             f"올린 반응 {REL['up']:,} · 내린 반응 {REL['down']:,} → 거의 위로만 움직임<br><br>"
             f"받는 쪽이 매긴 친밀도별 수락률<br>60점 이상: F {pf(hi_f)} · T {pf(hi_t)}<br>아직 점수 없음: F {pf(no_f)} · T {pf(no_t)}<br>"
             "→ <b>‘좋다’고 보고한 상대의 제안을 더 받아 주지 않음</b>", "teal"),
         box("② 거절 회고 (거절되면 ‘왜 · 무엇을 바꿀지’를 씀)",
             f"상대가 고른 거절 {cs['refusals']}건 → 모두 회고 작성<br><br>회고 없던 v10과 같은 상황 비교<br>"
             f"다시 제안 때 조건 변경 {pf(c10['changed'])} → <b>{pf(cs['changed'])}</b><br>"
             f"‘먼저 확인하겠다’({cs['plans']['ask']['n']}건) 뒤 실제 질문 {pf(cs['plans']['ask']['asked_2c'])} (기준선 {pf(c10['asked_2c'])})<br>"
             f"다시 제안한 거래 성사 {pf(c10['again_settled'])} → <b>{pf(cs['again_settled'])}</b>", "violet"))
    + note("회고와 다음 행동은 같은 모델 호출에서 나옴 → 글과 행동의 일치는 학습의 증거가 아님 · 친밀도는 대부분 60점 이상(천장 효과)")
    + take("보고한 관계와 다짐은 <b>공개 결정을 거의 설명하지 못함</b> — 행동 기록이 필요한 이유"),
    "두 번째 질문, 에이전트의 자기 보고가 실제 선택을 설명하는가입니다. 친밀도는 거의 위로만 올렸는데, 60점 넘게 준 상대의 제안을 오히려 덜 받아 줬습니다. "
    "거절 회고는 221건 모두 성실히 썼고, 조건을 바꾸는 행동은 늘었습니다. 하지만 가장 많이 쓴 ‘먼저 확인하겠다’는 기준선 수준이었고, 성사율은 그대로였습니다. 말로는 공개 결정을 설명할 수 없었습니다.",
    "상호작용 지표 F3 · b68_followthrough.py · v10-main · v11b-s1")

add("RQ3 · 개인 점수를 확보한 뒤", "02 · Results", 100,
    grid(bars([f"거래 제안\n(생존 사이클당 · {CF['late_from']}사이클 이후)", f"거래로 넘긴 단서\n(생존 사이클당 · {CF['late_from']}사이클 이후)"],
              [("미확보", GREY, [p_open, g_open]), ("미션 확보 뒤", BLUE, [p_sec, g_sec])], w=520, h=250, fmt=lambda v: f"{v:.2f}"),
         table(["지표", "미확보", "미션 확보 뒤"], [
             ["거래 제안 / 사이클 (전체)", f"{p_open_all:.2f}", f"{p_sec_all:.2f}"],
             [f"거래 제안 / 사이클 ({CF['late_from']}사이클 이후)", f"{p_open:.2f}", f"<b>{p_sec:.2f}</b>"],
             [f"넘긴 단서 / 사이클 ({CF['late_from']}사이클 이후)", f"{g_open:.2f}", f"<b>{g_sec:.2f}</b>"],
             [f"받은 제안 수락 ({CF['late_from']}사이클 이후)", pn(AC["open|late"]), pn(AC["secured|late"])]], "compact-table small-rows center")
         + table(["방해형 미션", "배정", "달성"], [
             ["I2 들키지 않은 배신", IA.get("I2", 0), f'<b>{ID.get("I2", 0)}</b>'],
             ["I3 정보 봉쇄", IA.get("I3", 0), ID.get("I3", 0)]], "compact-table small-rows center"),
         cls="wide-left")
    + note(f"‘미션 확보’ = 그 시점에 서브 미션을 1개 이상 달성한 상태 (v11b 24판, 생존 사이클 {EX['open'] + EX['secured']:,}개). 확보는 주로 후반에 일어나 {CF['late_from']}사이클 이후끼리도 비교함")
    + take("남이 맞히면 잃을 점수가 생겨도 <b>정보를 숨기지 않음</b> — 오히려 더 제안하고 더 넘김 · 배신 미션은 0회 달성"),
    "이제 오늘의 중심입니다. 개인 미션을 확보하면, 남이 사건을 풀 때 그 점수를 잃습니다. 그러니 확보한 뒤에는 단서를 숨길 거라고 예상할 수 있습니다. 결과는 반대였습니다. "
    "같은 후반끼리 비교해도 확보한 에이전트가 거래를 더 제안하고 단서도 더 넘겼습니다. 받은 제안을 수락하는 비율만 조금 낮았습니다. 들키지 않게 배신하라는 미션은 열한 명이 받았지만 한 명도 달성하지 않았습니다.",
    "conflict_v11b.py (엔진 mission_achieved · trade_* · disclosures) · 미션_개편_v10.md")

add("RQ3 · 충돌은 추리 도전에서 드러남", "02 · Results", 95,
    tiles([(f"{ded_total}건", "추리 도전 (v11b 24판)"), (f"{ded_sec}건 ({pf([ded_sec, ded_total])})", "미션 확보 뒤의 도전"),
           (pf([DD['secured|right'], ded_sec]), f"그 정답률 ({DD['secured|right']}/{ded_sec})"),
           (f"{DD['secured|cites_mission']}/{DD['secured|with_reason']}", "도전 이유에 미션 점수를 언급")])
    + grid(table(["미션을 1개 이상 확보한 상태에서", "결과"], [
        ["도전 → 정답", "1위 100점"],
        ["도전 → 오답", "사망 −20점 + <b>미션 점수 유지</b> (1개면 0점, 2개면 +20점)"],
        ["보류 → 남이 맞힘", "0점 · <b>미션 점수 사라짐</b>"],
        ["보류 → 아무도 못 맞힘", "−10점 · 미션 점수 사라짐"]], "compact-table small-rows"),
        box("에이전트가 쓴 이유 (시드 201)", "“가설의 신뢰도는 낮지만, <b>달성한 미션 덕분에 오답이어도 20점을 지킨다</b>”<br><br>"
            "“보류하면 다른 승자가 나와 달성한 임무 점수도 잃을 수 있으므로 <b>계획보다 일찍 고발해 점수를 확보</b>하겠다”", "amber"),
        cls="wide-left")
    + note(f"미확보 상태의 도전은 {ded_open}건뿐임 · 11.13(v9): 손해 없는 상황의 도전 {ACCV['no_loss']}/{ACCV['total']} → 최종 실험에서도 같은 양상 · 이유 언급은 마지막 추리 판단 글의 단어 집계")
    + take("협력은 정보를 숨기는 데서 멈추지 않음 — 개인 점수를 지키는 <b>‘손해 없는 도전’으로 이탈</b>함"),
    "그럼 충돌은 어디서 드러났을까요. 추리 도전입니다. 152건 중 140건이 미션을 확보한 뒤에 나왔고, 그 정답률은 21퍼센트였습니다. 점수 구조를 보면 이유가 보입니다. "
    "미션을 확보한 상태에서 틀리면 죽지만 미션 점수는 남고, 기다리다 남이 맞히면 그 점수가 사라집니다. 에이전트들도 이유에 그렇게 썼습니다. 11.13에서 본 현상이 최종 실험에서도 그대로였습니다.",
    "conflict_v11b.py (deduction_submission · detail.jsonl) · competitive.py 점수 규칙 · 게임보고서 seed-201 · 요소별 영향 분석 §4.1")

add("RQ4 · 협력의 대가", "02 · Results", 65,
    tiles([(f'{SH["to_helper"]}/{SH["events"]}', "판 뒤 나눔 중 1위에게 단서를 준 상대에게 간 것"),
           (f'{SH["points"]}점', f'나눈 점수 합 ({SH["events"]}건)'),
           (f'{PAIRS["pairs_in_3plus_games"]}쌍', f'3판 이상 다시 거래한 짝 (성사 짝 {PAIRS["pairs_with_settled_trade"]}쌍 중)')])
    + grid(box("나눔은 보답이었음", "나눔은 강제되지 않는 선택 · 약속을 어겨도 벌칙 없음<br>그래도 거의 전부가 <b>그 판에서 도와준 상대</b>에게 감", "teal"),
           box("반복이 신뢰를 지탱함", "같은 16명이 판을 넘어 다시 만남 (교재 I의 ‘미래의 그림자’)<br>"
               "가장 오래간 짝: INFJ–INFP (시나리오 1에서 7판)", "teal"))
    + take("협력은 <b>보답과 반복</b>으로 유지됨 — 강제 장치 없이"),
    "네 번째, 협력의 대가입니다. 1위가 점수를 나눌지는 자유인데, 48건 중 46건이 그 판에서 단서를 준 상대에게 갔습니다. 거래가 성사된 짝 중 55쌍은 세 판 이상 다시 거래했습니다. 강제 없이도 협력은 보답과 반복으로 유지됐습니다.",
    "상호작용 지표 G3_score_sharing.csv · B3_information_flow.csv · H1_partnerships.csv")

# ---------------- 03 · Conclusion -------------------------------------------------------------------
add("한계와 남은 질문", "03 · Conclusion", 60,
    grid(box("기만 0의 원인", f"성사된 거래 {dec_n}건 모두 이행 · 배신 미션 0회<br>가설 ① 늘 들키고 같은 짝을 다시 만남<br>가설 ② 모델 자체의 정직한 성향<br><b>둘을 가르는 실험은 하지 않음</b>", "amber"),
         box("비교의 조건", f"미션 확보는 후반에 몰림 → {CF['late_from']}사이클 이후끼리 비교했지만 사이클 단위 정합은 아님<br>오답으로 죽은 에이전트는 이후 기록에서 빠짐", "amber"),
         box("모델 하나, 단일 LLM 비교 없음", "모든 실험이 같은 모델 · 제안서 H1(단일 LLM 비교) 미수행", "amber"),
         box("점수 규칙이 만든 행동", "‘손해 없는 도전’은 규칙이 허용한 합리적 선택 → 규칙을 바꾸면 달라질 수 있음 (후속 실험)", "amber"), cols=2)
    + take("관찰 · 가설 · 검증 실험을 구분해 둠"),
    "한계도 분명합니다. 기만이 없는 이유가 늘 들키기 때문인지 모델의 성향인지는 가르지 못했습니다. 미션 확보가 후반에 몰려 있어 시기를 맞춰 비교했지만 완전하지 않고, 모델도 하나뿐입니다. "
    "손해 없는 도전은 규칙이 허용한 선택이기 때문에, 규칙을 바꿔 보는 것이 다음 실험입니다.",
    "엔진 trade_judged · conflict_v11b.py · 1쪽 제안서 H1")

add("결론: 연구 질문에 대한 답", "03 · Conclusion", 70,
    '<div class="conclusion-list">'
    f'<div><span>1</span><p><b>공개</b> — 거절보다 조건 조정으로 흥정하고, 속일 수 있어도 속이지 않음 (기만 {dec_bad}/{dec_n})</p></div>'
    '<div><span>2</span><p><b>자기 보고</b> — 친밀도와 회고는 실제 공개 결정을 거의 설명하지 못함 → 행동 기록으로 재야 함</p></div>'
    f'<div class="hl"><span>3</span><p><b>개인 목표와의 충돌</b> — 점수를 확보한 뒤에도 정보를 숨기지 않음. 대신 <b>손해 없는 도전으로 이탈</b> (도전 {ded_sec}/{ded_total}건이 확보 뒤, 정답률 {pf([DD["secured|right"], ded_sec])})</p></div>'
    f'<div><span>4</span><p><b>협력의 대가</b> — 판 뒤 나눔 {SH["to_helper"]}/{SH["events"]}건이 도와준 상대에게 감 → 보답과 반복으로 유지</p></div></div>'
    + take("이 에이전트들에게 두 목표의 충돌은 <b>‘무엇을 숨기나’가 아니라 ‘언제 판에서 빠지나’</b>의 문제였음"),
    "정리하면, 에이전트들은 조건을 조정하며 흥정했고 속이지 않았습니다. 자기 보고는 선택을 설명하지 못해서 행동 기록으로 재야 했습니다. 개인 목표와 부딪혀도 정보를 숨기지 않았고, 대신 손해 없는 도전으로 판에서 빠졌습니다. "
    "협력은 보답과 반복으로 유지됐습니다. 이 에이전트들에게 충돌은 무엇을 숨기느냐가 아니라 언제 빠지느냐의 문제였습니다.",
    "발표 요약 · results.json")

add("정리", "03 · Conclusion", 40,
    '<div class="series">'
    '<div class="scard"><small>10.30</small><h3>무엇인가</h3><p>모델이 아니라 <b>시스템</b></p></div>'
    '<div class="scard"><small>11.13</small><h3>어떻게 만들었나</h3><p>의도와 구현의 간극을 <b>요소별로</b> 메움</p></div>'
    '<div class="scard now"><small>11.27</small><h3>두 목표가 부딪힐 때</h3><p>숨기지 않고 <b>빠져나감</b><br>— 행동 기록으로 확인</p></div></div>'
    + take("공동 목표와 개인 목표 사이에서, 에이전트는 <b>정보가 아니라 타이밍</b>으로 자기 몫을 지킴"),
    "세 번의 발표를 정리하겠습니다. 에이전트는 모델이 아니라 시스템이었고, 만드는 일은 의도와 구현의 간극을 메우는 일이었습니다. 그리고 두 목표가 부딪힐 때 에이전트는 정보를 숨기지 않고, 타이밍으로 자기 몫을 지켰습니다. 감사합니다.",
    "발표 요약")
