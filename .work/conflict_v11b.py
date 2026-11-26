"""Mixed-motive analysis (v11b: fault 8 + scenario-1 16 games). Read-only over engine records.

Question (team report 1.1/1.2): when the shared goal (solve the case) conflicts with a personal goal, how do agents
disclose / withhold, and where does cooperation continue or stop?
Personal goal here = sub-missions (20 pts each). Under winner-take-all a survivor loses mission points when someone
else solves the case; a wrong accusation kills the accuser but keeps the mission points.

State of an agent at a moment: 'secured' = at least one ordinary sub-mission (M*) already achieved, else 'open'.
Only engine facts are used; the one text measure (accusation reasons mentioning a mission) is a keyword count
over the agent's own deliberation journal, reported as such.
"""
import collections
import json
from pathlib import Path

RUNS = Path(r"F:\multi_agent_AI_Game\unified-packages-v11\runs")
CAMPAIGNS = ["v11b-fault-30c-lean", "v11b-s1-30c-lean"]
LATE = 15          # cycles >= LATE count as 'late' (missions are mostly secured late)
MISSION_WORDS = ("미션", "임무")


def _records():
    for c in CAMPAIGNS:
        b = json.loads((RUNS / c / "batch.json").read_text(encoding="utf-8"))
        for a in b["attempts"]:
            f = a.get("full_record_file")
            if f and Path(f).exists() and a.get("resolution"):
                yield Path(f)


def analyze():
    expo, prop, give, acc = collections.Counter(), collections.Counter(), collections.Counter(), collections.Counter()
    ded = collections.Counter()
    ded_cycles = {"secured": [], "open": []}
    imiss_assigned, imiss_done = collections.Counter(), collections.Counter()
    m_done = 0
    games = 0
    for f in _records():
        games += 1
        fr = json.loads(f.read_text(encoding="utf-8"))
        g, ev = fr["game"], fr["events"]
        truth = g["truth"]
        agent_of = {int(k): v.get("controller") for k, v in g["characters"].items()}
        imission = {}
        for v in g["characters"].values():
            sm = (v.get("goal") or {}).get("sub_missions") or []
            imission[v.get("controller")] = [m["mission_id"] for m in sm if m["mission_id"].startswith("I")]
            for m in imission[v.get("controller")]:
                imiss_assigned[m] += 1
        seq_cycle = []
        for e in ev:
            if e["type"] == "action_completed":
                r = e["payload"].get("result") or {}
                if r.get("cycle_id") is not None:
                    seq_cycle.append((e["sequence"], r["cycle_id"]))

        def cyc(seq):
            c = 0
            for s, cc in seq_cycle:
                if s > seq:
                    break
                c = cc
            return c

        first = {}
        for e in ev:
            if e["type"] != "mission_achieved":
                continue
            p = e["payload"]
            if p["mission_id"].startswith("I"):
                imiss_done[p["mission_id"]] += 1
            elif not p.get("at_game_end"):
                m_done += 1
                first.setdefault(p["agent_id"], e["sequence"])
        died = {agent_of.get(e["payload"]["character_id"]): e["sequence"] for e in ev if e["type"] == "actor_died"}
        last = g.get("cycle_id") or max((c for _, c in seq_cycle), default=30)
        fm_cycle = {a: cyc(s) for a, s in first.items()}

        def state(a, seq):
            return "secured" if a in first and first[a] < seq else "open"

        def band(c):
            return "late" if c >= LATE else "early"

        for a in imission:
            if a is None:
                continue
            end = cyc(died[a]) if a in died else last
            for c in range(1, end + 1):
                st = "secured" if a in fm_cycle and fm_cycle[a] < c else "open"
                expo[st] += 1
                expo[f"{st}|{band(c)}"] += 1
        for e in ev:
            if e["type"] == "trade_proposed":
                p, s = e["payload"]["proposer"], e["sequence"]
                st = state(p, s)
                prop[st] += 1
                prop[f"{st}|{band(cyc(s))}"] += 1
        decided = {e["payload"]["trade_id"]: (e["sequence"], e["type"], e["payload"].get("reason"))
                   for e in ev if e["type"] in ("trade_settled", "trade_refused")}
        for tid, t in g["trades"].items():
            if tid not in decided:
                continue
            seq, typ, reason = decided[tid]
            if typ == "trade_refused" and reason != "refused":
                continue  # mechanical refusals (another offer chosen, crossed, action used): not the recipient's choice
            st = state(t["recipient"], seq)
            for key in (st, f"{st}|{band(cyc(seq))}"):
                acc[key + "|n"] += 1
                acc[key + "|ok"] += typ == "trade_settled"
        for d in g["disclosures"]:
            if d["kind"] == "trade":
                s = d["sender"]
                st = "secured" if s in fm_cycle and fm_cycle[s] < d["cycle"] else "open"
                give[st] += 1
                give[f"{st}|{band(d['cycle'])}"] += 1
        # accusations and the agent's own stated reason (deduction-phase journal of the same cycle)
        journal = collections.defaultdict(list)
        det = f.parent / "detail.jsonl"
        if det.exists():
            for line in det.open(encoding="utf-8"):
                r = json.loads(line)
                rec = r.get("record") or {}
                if r.get("phase") == "deduction" and r.get("event") == "agent_journal" and rec.get("event") == "consideration":
                    journal[(r["agent_id"], r.get("cycle_id"))].append(rec.get("text") or "")
        for e in ev:
            if e["type"] != "deduction_submission":
                continue
            a, gs, s = e["payload"]["agent_id"], e["payload"]["guess"], e["sequence"]
            right = all(gs.get(k) == truth.get(k) for k in ("suspect", "weapon", "place"))
            st = state(a, s)
            c = cyc(s)
            ded[f"{st}|{'right' if right else 'wrong'}"] += 1
            ded_cycles[st].append(c)
            texts = journal.get((a, c), [])
            if texts:
                ded[f"{st}|with_reason"] += 1
                ded[f"{st}|cites_mission"] += any(w in texts[-1] for w in MISSION_WORDS)

    def med(xs):
        xs = sorted(xs)
        return xs[len(xs) // 2] if xs else None

    return dict(
        src="conflict_v11b.py over unified-packages-v11/runs (" + ", ".join(CAMPAIGNS) + ")", games=games, late_from=LATE,
        exposure=dict(expo), proposals=dict(prop), trade_clues_given=dict(give),
        accept={k: [acc[k + "|ok"], acc[k + "|n"]] for k in ("open", "secured", "open|early", "open|late", "secured|early", "secured|late")},
        accusations=dict(ded), accusation_cycle_median={k: med(v) for k, v in ded_cycles.items()},
        missions_achieved=m_done, imission_assigned=dict(imiss_assigned), imission_achieved=dict(imiss_done))


if __name__ == "__main__":
    print(json.dumps(analyze(), ensure_ascii=False, indent=1))
