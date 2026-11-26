"""Final standings of the last campaign (v11b scenario 1, 16 games): engine standings + per-game outcomes. Read-only."""
import collections
import json
from pathlib import Path

RUNS = Path(r"F:\multi_agent_AI_Game\unified-packages-v11\runs")
CAMP = "v11b-s1-30c-lean"


def analyze():
    b = json.loads((RUNS / CAMP / "batch.json").read_text(encoding="utf-8"))
    mbti, last_standings, games = {}, None, 0
    stat = collections.defaultdict(collections.Counter)
    for a in b["attempts"]:
        f = a.get("full_record_file")
        if not (f and Path(f).exists() and a.get("resolution")):
            continue
        games += 1
        fr = json.loads(Path(f).read_text(encoding="utf-8"))
        g = fr["game"]
        for v in g["characters"].values():
            if v.get("controller") and v.get("mbti"):
                mbti[v["controller"]] = v["mbti"]
        for aid, fb in (g.get("final_feedback") or {}).items():
            if fb.get("outcome") == "not_counted" or fb.get("participated") is False:
                continue
            s = stat[aid]
            s["games"] += 1
            s["wins"] += bool(fb.get("rank"))
            s["wrong"] += (not fb.get("rank")) and (not fb.get("survived", True))
            s["missions"] += sum(1 for m in fb.get("sub_missions", []) if m.get("achieved") and not m["mission_id"].startswith("I"))
        for e in fr["events"]:
            if e["type"] == "standings_published":
                last_standings = e["payload"]["standings"]
    rows = []
    for r in last_standings:
        aid = r["agent_id"]
        s = stat[aid]
        rows.append(dict(mbti=mbti.get(aid, "?"), total=r["cumulative_score"], games=r["games"], average=r["average_score"],
                         wins=s["wins"], wrong=s["wrong"], missions=s["missions"]))
    rows.sort(key=lambda x: -x["average"])
    return dict(src=f"{CAMP}: standings_published (last game) + final_feedback", games=games, rows=rows)


if __name__ == "__main__":
    print(json.dumps(analyze(), ensure_ascii=False, indent=1))
