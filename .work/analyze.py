"""Collect every number used in the 2026-11-27 deck into results.json.

Two kinds of numbers:
  computed   - recomputed here from run records / metric tables (engine facts only)
  documented - taken from an earlier analysis document; each carries its source path
Run on the machine that holds F:\\multi_agent_AI_Game.
"""
import csv
import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
P = Path(r"F:\multi_agent_AI_Game")
DATA = P / "발표인계_1130" / "data"
IM = DATA / "상호작용_지표"
FT_JSON = P / "발표_후속_v11" / "analysis" / "b68_followthrough.json"


def rows(path):
    return list(csv.DictReader(open(path, encoding="utf-8-sig")))


def frac(xs, k):
    return [sum(1 for x in xs if x[k]), len(xs)]


# ---------- 1. trade-refusal review: did they do what they wrote? ----------
ft = json.load(open(FT_JSON, encoding="utf-8"))
FT = {}
for camp, rs in ft.items():
    nx = [r for r in rs if r["has_next"]]
    ag = [r for r in rs if r["again"]]
    d = dict(refusals=len(rs), reviewed=sum(r["reviewed"] for r in rs),
             asked_2c=frac(rs, "asked_2c"), again=frac(nx, "again"), asked_before_again=frac(ag, "asked_before_again"),
             changed=frac(ag, "changed"), again_settled=frac(ag, "again_settled"))
    plans = {}
    for k in ("ask", "terms", "other"):
        sub = [r for r in rs if r["plan"][k]]
        plans[k] = dict(n=len(sub), asked_2c=frac(sub, "asked_2c"), again=frac([r for r in sub if r["has_next"]], "again"),
                        changed=frac([r for r in sub if r["again"]], "changed"))
    d["plans"] = plans
    FT[camp] = d

# ---------- 2. deception (engine trade_judged) ----------
DEC = {}
for root, camp in [("unified-packages-v9/runs", "v9-main2-30c-lean"), ("unified-packages-v10/runs", "v10-main-30c-lean"),
                   ("unified-packages-v11/runs", "v11b-fault-30c-lean"), ("unified-packages-v11/runs", "v11b-s1-30c-lean")]:
    b = json.load(open(P / root / camp / "batch.json", encoding="utf-8"))
    judged = bad = 0
    for a in b["attempts"]:
        if a.get("status") != "completed" or not a.get("game_id"):
            continue
        rec = json.load(open(P / root / a["game_id"] / "full-record.json", encoding="utf-8"))
        for e in rec["events"]:
            if e.get("type") == "trade_judged":
                judged += 1
                bad += not all((e.get("payload") or {}).get("honest", {}).values())
    DEC[camp] = [bad, judged]

# ---------- 3. GM-absence votes ----------
VOTE = {}
for tag, folder in [("old", "interaction-v11-oldtext"), ("b70", "interaction-v11b")]:
    rr = rows(IM / folder / "G2_gm_absent_rounds.csv")
    vv = rows(IM / folder / "G2_gm_absent_votes.csv")
    per_seed = Counter(r["seed"] for r in rr)
    first_round = [r["result"] for r in rr if r["round"] == "1"]
    VOTE[tag] = dict(rounds_by_seed=dict(per_seed), rounds=len(rr), votes=len(vv), wait_votes=sum(v["choice"] == "wait" for v in vv),
                     appoint_votes=sum(v["choice"] == "appoint" for v in vv), first_round=dict(Counter(first_round)))

# ---------- 4. score sharing vs who helped the winner ----------
B3 = rows(IM / "interaction-v11b" / "B3_information_flow.csv")
G3 = rows(IM / "interaction-v11b" / "G3_score_sharing.csv")
helped, helped_trade = defaultdict(set), defaultdict(set)
for b in B3:
    key = (b["campaign"], b["seed"], b["receiver"])
    helped[key].add(b["giver"])
    if b["via"] == "trade":
        helped_trade[key].add(b["giver"])
SHARE = dict(events=len(G3), to_helper=sum(g["to"] in helped[(g["campaign"], g["seed"], g["giver"])] for g in G3),
             to_trade_helper=sum(g["to"] in helped_trade[(g["campaign"], g["seed"], g["giver"])] for g in G3),
             points=sum(int(float(g["points"])) for g in G3))

# ---------- 5. affinity vs acceptance, interaction metrics ----------
F3 = {(r["recipient_affinity_bucket"], r["recipient_tf"]): [int(r["settled"]), int(r["proposals"])] for r in rows(IM / "interaction-v11b" / "F3_accept_by_affinity.csv")}
M = json.load(open(IM / "interaction-v11b" / "metrics.json", encoding="utf-8"))
AX = {(r["axis"], r["letter"]): r for r in rows(IM / "interaction-v11b" / "per_axis.csv")}

# ---------- 6. personality probe ----------
PROBE = {}
for tag, folder in [("p1", "personality-probe-1"), ("p2", "personality-probe-2")]:
    c = json.load(open(DATA / "성격검사" / folder / "summary.json", encoding="utf-8"))["conditions"]
    a = c["masked"]["axes"]
    PROBE[tag] = dict(tf_split=a["TF"]["median_split_hit"], e_on_agree=a["EI"]["d_on_other_factors"]["agreeableness"],
                      s_intellect=a["SN"]["S"], n_intellect=a["SN"]["N"],
                      label_s_intellect=c.get("label", {}).get("axes", {}).get("SN", {}).get("S"))

# ---------- 7. documented numbers (earlier analyses) ----------
DOC = {
    "talk_v9": dict(src="unified-packages-v11/docs/요소별_영향_분석_v8_v9.md §5", call_share=[10490, 27507], heard_from_room=0.88,
                    affinity_final=98.4, affinity_at_100=[211, 240], win_by_quartile=[4.2, 6.2, 8.3, 4.2],
                    pair_propose_talk=13.0, pair_propose_notalk=6.6, propose_all_before=11.1, propose_all_after=10.2),
    "memory_v8": dict(src="unified-packages-fixed/docs/v8_캠페인_보고서.md (03 실험기록 §4)", questions=2536, remembered=0, actual=833),
    "accuse_v9b": dict(src="요소별_영향_분석_v8_v9.md §4.1", no_loss=92, total=115, cite_mission=78, correct_in_no_loss=10),
    "signal_fix": dict(src="03 실험기록 §6.1, b68_effect.py", forced_refusal_before=0.78, forced_refusal_after=[0.14, 0.08],
                       settle_v9b=[427, 1054], settle_v10=[539, 915]),
    "fault": dict(src="03 실험기록 §7.2, §7.6, 01 여정 §8", stall_hours=42, funnel=[332, 23, 2, 1],
                  t103=[139, 68], t108=[538, 39], quota108=11),
    "role": dict(src="03 실험기록 §3 (v7 → v8)", wrong_target=[34, 0], unparsable=[14, 0]),
    "calls": dict(src="03 실험기록 §6.2", per_game=[1719, 1144], tokens_m=[35.1, 25.7]),
    "rank_corr_v9_v10": dict(src="03 실험기록 §6.2", rho=0.11),
    "s1_rank": dict(src="03 실험기록 §7.7", top=[("ESTP", 31.1), ("INFJ", 30.7), ("ENFP", 28.8), ("ENTJ", 28.3)],
                    bottom=[("ISFJ", 3.8), ("ISTJ", 3.4), ("ISTP", 2.8), ("ISFP", 0.9)]),
    "probe_entj": dict(src="03 실험기록 §7.5", p1=0.64, p2=0.81),
    "capacity": dict(src="04 요소별 설계변화 §2 (용량 시뮬레이션)", personal=536, team=94, combos=768, solve_coop=0.94, solve_alone=0.0),
    "flow": dict(src="08 상호작용 지표 §3 B (v11b 24판)", via_question=3333, via_trade=1290),
    "missions": dict(src="04 요소별 설계변화 §7, 미션_개편_v10.md", ordinary=46, obstruction=4, share_obstruction="약 1/3", points=20),
}

# ---------- 8. mixed motive: secured personal mission vs disclosure / accusation (v11b) ----------
sys.path.insert(0, str(HERE))
from conflict_v11b import analyze as conflict_analyze  # noqa: E402
CONFLICT = conflict_analyze()

R = dict(conflict=CONFLICT, followthrough=FT, deception=DEC, votes=VOTE, sharing=SHARE, accept_by_affinity={f"{k[0]}|{k[1]}": v for k, v in F3.items()},
         metrics=dict(affinity=M["F_trust"], approaches=M["E_persuasion"], pairs=M["H_coalitions"], coord=M["I_coordination"],
                      settle=M["D_bargaining"]), axis={f"{k[0]}|{k[1]}": v for k, v in AX.items()}, probe=PROBE, documented=DOC)
(HERE / "results.json").write_text(json.dumps(R, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(dict(followthrough={k: {kk: vv for kk, vv in v.items() if kk != "plans"} for k, v in FT.items()},
                      deception=DEC, votes={k: {kk: v[kk] for kk in ("rounds", "votes", "first_round")} for k, v in VOTE.items()},
                      sharing=SHARE, probe=PROBE), ensure_ascii=False, indent=1))
