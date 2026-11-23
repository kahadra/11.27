"""Build the 2026-11-27 IRV_Lab seminar deck: how do you verify a multi-agent system? (third multi-agent talk)

Series: 10.30 what an agent is (theory) -> 11.13 how to build one (practice) -> 11.27 how to know it works (verification).
Core theme (user, 2026-11-23): a multi-agent system must be verified by behaviour, not by words.
Three kinds of 'words': the agents' own words, the design's words, the textbook's words.

Reuses the 10.30 deck's CSS, navigation, notes and timer (as 11.13 did). Every number comes from results.json
(analyze.py: recomputed from run records, or quoted from an earlier analysis document with its source).
Outputs: ../index.html, ../presentation_script.md, ../assets/slide_manifest.json
"""
import html
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
root = HERE.parent
old = (root.parent / "10.30/index.html").read_text(encoding="utf8")
extra_css = (root.parent / "11.13/.work/build_deck.py").read_text(encoding="utf8")
extra_css = extra_css.split('css += r"""', 1)[1].split('"""', 1)[0]
DATE, LIMIT, PLANNED = "2026.11.27", 1200, 1140
R = json.loads((HERE / "results.json").read_text(encoding="utf8"))
esc = html.escape

# ---------- numbers ------------------------------------------------------------------------------
FT10, FTF, FTS = (R["followthrough"][k] for k in ("v10-main", "v11b-fault", "v11b-s1"))
DEC = R["deception"]
VO, VB = R["votes"]["old"], R["votes"]["b70"]
SH = R["sharing"]
ACC = R["accept_by_affinity"]
MET = R["metrics"]
AX = R["axis"]
P1, P2 = R["probe"]["p1"], R["probe"]["p2"]
D = R["documented"]


def pf(x):
    """[hit, n] -> '53%'"""
    return f"{100 * x[0] / x[1]:.0f}%" if x[1] else "–"


def pn(x):
    return f"{x[0]}/{x[1]} ({pf(x)})"


def ratio(x): return x[0] / x[1] if x[1] else 0


def pct(x): return "–" if x is None else f"{100 * x:.0f}%"


# ---------- HTML helpers -------------------------------------------------------------------------
def box(title, text, color=""): return f'<div class="box {color}"><h3>{title}</h3><p>{text}</p></div>'
def lead(s): return f'<p class="lead">{s}</p>'
def note(s): return f'<p class="reading">{s}</p>'
def take(s): return f'<div class="takeaway">{s}</div>'
def grid(*items, cols=2, cls=""): return f'<div class="grid-{cols} {cls}">' + "".join(f'<div class="cell">{x}</div>' for x in items) + "</div>"
def ul(*items): return "<ul class=\"tight\">" + "".join(f"<li>{x}</li>" for x in items) + "</ul>"


def table(headers, rows, cls=""):
    return (f'<table class="data-table {cls}"><thead><tr>' + "".join(f"<th>{h}</th>" for h in headers) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows) + "</tbody></table>")


def tiles(items):
    return '<div class="tiles">' + "".join(f'<div class="tile"><b>{v}</b><span>{l}</span></div>' for v, l in items) + "</div>"


def verdict(kind):
    return {"확인": '<span class="tag ok">확인</span>', "부분": '<span class="tag part">부분</span>',
            "미확인": '<span class="tag bad">미확인</span>', "대응": '<span class="tag ok">대응</span>'}[kind]


def bars(cats, series, w=560, h=270):
    """Grouped vertical bars, values 0..1. series: [(name, color, [v per cat])]."""
    pad_l, pad_b, pad_t = 44, 62, 26
    plot_w, plot_h = w - pad_l - 10, h - pad_b - pad_t
    gw = plot_w / len(cats)
    bw = min(56, (gw - 30) / len(series))
    out = [f'<svg class="chart" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">']
    for t in (0, .25, .5, .75, 1):
        y = pad_t + plot_h * (1 - t)
        out.append(f'<line x1="{pad_l}" x2="{w - 10}" y1="{y:.1f}" y2="{y:.1f}" class="grid"/>'
                   f'<text x="{pad_l - 8}" y="{y + 5:.1f}" class="axis" text-anchor="end">{pct(t)}</text>')
    for ci, c in enumerate(cats):
        x0 = pad_l + gw * ci + (gw - bw * len(series) - 3 * (len(series) - 1)) / 2
        for si, (name, color, vals) in enumerate(series):
            v = vals[ci]
            bh = plot_h * v
            x, y = x0 + si * (bw + 3), pad_t + plot_h - bh
            r = min(4, bh / 2)
            out.append(f'<path d="M{x:.1f},{pad_t + plot_h} V{y + r:.1f} Q{x:.1f},{y:.1f} {x + r:.1f},{y:.1f} H{x + bw - r:.1f} '
                       f'Q{x + bw:.1f},{y:.1f} {x + bw:.1f},{y + r:.1f} V{pad_t + plot_h}Z" fill="{color}"><title>{esc(name)} · {esc(c)}: {pct(v)}</title></path>'
                       f'<text x="{x + bw / 2:.1f}" y="{y - 7:.1f}" class="val" text-anchor="middle">{pct(v)}</text>')
        cx = pad_l + gw * ci + gw / 2
        lines = c.split("\n")
        spans = "".join(f'<tspan x="{cx:.1f}" dy="{0 if k == 0 else 17}">{esc(s)}</tspan>' for k, s in enumerate(lines))
        out.append(f'<text x="{cx:.1f}" y="{h - pad_b + 22}" class="axis cat" text-anchor="middle">{spans}</text>')
    out.append(f'<line x1="{pad_l}" x2="{w - 10}" y1="{pad_t + plot_h}" y2="{pad_t + plot_h}" class="base"/></svg>')
    legend = "".join(f'<span><i style="background:{c}"></i>{esc(n)}</span>' for n, c, _ in series)
    return f'<figure class="chart-fig">{"".join(out)}<figcaption class="legend">{legend}</figcaption></figure>'


BLUE, AMBER, GREY = "#2867d8", "#b7791f", "#9aa6b8"
slides = []


def add(title, section, seconds, body, notes, source, short=""):
    slides.append(dict(title=title, section=section, seconds=seconds, body=body, notes=notes, source=source, short=short, aside=""))


exec((HERE / "content_main.py").read_text(encoding="utf8"))

MAIN = len(slides)
assert sum(s["seconds"] for s in slides) == PLANNED, sum(s["seconds"] for s in slides)
exec((HERE / "content_appendix.py").read_text(encoding="utf8"))

# ---------- render (same engine as 10.30 / 11.13) ------------------------------------------------
css = re.search(r"<style>(.*?)</style>", old, re.S)[1] + extra_css + r"""
.series{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:14px}
.scard{position:relative;background:white;border:1px solid var(--line);border-radius:12px;padding:14px 16px;min-height:200px}
.scard:not(:last-child):after{content:'→';position:absolute;right:-15px;top:50%;transform:translateY(-50%);color:var(--teal);font-weight:800;font-size:20px}
.scard small{display:block;font-size:13px;font-weight:800;color:#61708a;letter-spacing:.4px}.scard h3{font-size:22px;margin:4px 0 8px;color:#172840}
.scard p{font-size:15.5px;line-height:1.5;color:#3f4f68}.scard.now{background:#f2faf9;border-color:#0d6f6a;border-width:2px}
.saymap{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:12px}
.say{background:white;border:1px solid var(--line);border-radius:12px;overflow:hidden}
.say h3{font-size:19px;color:white;padding:10px 14px;margin:0}.say.a h3{background:#0d6f6a}.say.d h3{background:#b7791f}.say.t h3{background:#5b3f94}
.say .row{display:grid;grid-template-columns:62px 1fr;gap:8px;padding:9px 14px;border-top:1px solid var(--line)}
.say .row b{font-size:13.5px;color:#61708a}.say .row span{font-size:15.5px;line-height:1.45;color:#22324c}
.mini-title{font-size:15px;font-weight:800;color:#172840;margin:0 0 6px}
.hl{background:#fff3dc}
"""


def clock(n): return f"{n // 60:02}:{n % 60:02}"


t = 0
for s in slides:
    s["start"] = clock(t); t += s["seconds"]; s["end"] = clock(t); s["duration"] = clock(s["seconds"])
    s["page"] = 1; s["cue"] = ""


def fill_times(text):
    text = re.sub(r"@@S(\d+)@@", lambda m: slides[int(m.group(1)) - 1]["start"], text)
    return re.sub(r"@@E(\d+)@@", lambda m: slides[int(m.group(1)) - 1]["end"], text)


for s in slides:
    s["body"] = fill_times(s["body"])
parts = []
for i, s in enumerate(slides):
    if i == 0:
        body = ('<div class="title-top"><span class="pill dark">MULTI-AGENT · PART 3 · VERIFICATION</span><span>IRV_LAB SEMINAR · 20 MIN</span></div>'
                '<div class="title-main"><div class="title-rule"></div><h1>멀티에이전트,<br>어떻게 검증하는가</h1>'
                '<h2>말이 아니라 행동으로 — LLM 에이전트 12명 추리 게임, 한 학기의 마무리</h2>'
                '<p class="title-korean">10.30 무엇인가 · 11.13 어떻게 만드는가 · 11.27 작동하는지 어떻게 아는가</p>'
                '<p class="authors">수업 팀 프로젝트 · 교재 I (Wooldridge) · 교재 II (Albada)</p></div>'
                '<div class="title-meta"><div><small>PRESENTER</small><b>박천웅</b></div><div><small>AFFILIATION</small><b>IRV_Lab</b></div>'
                '<div><small>DATE</small><b>2026. 11. 27.</b></div><div><small>TIME LIMIT</small><b>20 min</b></div></div>')
    else:
        stamp = f'{s["start"]}–{s["end"]} · {s["duration"]}' if s["seconds"] else "질의응답용 · 본편 시간 미포함"
        body = (f'<header class="slide-header"><div><div class="eyebrow">{s["section"]}</div><h2 class="slide-title">{s["title"]}</h2></div>'
                f'<div class="slide-kicker">Multi-Agent · {DATE}<br>{stamp}</div></header><div class="slide-body">{s["body"]}</div>'
                f'<footer class="slide-footer"><span class="source"><a href="SOURCES.md" target="_blank">{esc(s["source"])}</a></span>'
                f'<span class="slide-no">{i + 1:02} / {len(slides):02} · ' + ("MAIN" if i < MAIN else "APPENDIX") + "</span></footer>")
    parts.append(f'<section class="slide {"title-slide" if i == 0 else ""}" data-title="{esc(s["title"])}" aria-label="{i + 1}. {esc(s["title"])}">{body}</section>')

controls = old[old.index("<nav"):old.index("<script>")]
controls = re.sub(r'max="\d+"', f'max="{len(slides)}"', controls)
controls = re.sub(r"/ \d+</label>", f"/ {len(slides)}</label>", controls)
js = old[old.index("const slides=[...document.querySelectorAll"):old.rindex("</script>")]
js = re.sub(r"const mainCount=\d+", f"const mainCount={MAIN}", js)
js = js.replace("| AI Agents Seminar", "| Multi-Agent Seminar").replace("toolUseTimer", "multiAgentVerifyTimer")
assert f"const mainCount={MAIN}" in js and "multiAgentVerifyTimer" in js
head = old[:old.index("<style>")]
head = re.sub(r'<meta name="description" content="[^"]*">',
              '<meta name="description" content="멀티에이전트, 어떻게 검증하는가 · IRV_Lab 2026.11.27 · 박천웅 · 20분 세미나">', head)
head = re.sub(r"<title>.*?</title>", "<title>Multi-Agent Verification · 2026.11.27 Seminar</title>", head)
data = [{k: v for k, v in s.items() if k != "body"} for s in slides]
result = (head + "<style>" + css + '</style></head><body class="deck"><main class="viewport"><div id="deck">' + "".join(parts)
          + "</div></main>" + controls + "<script>const slideData=" + json.dumps(data, ensure_ascii=False) + ";\n" + js + "</script></body></html>")
(root / "index.html").write_text(result, encoding="utf8")
(root / "assets").mkdir(exist_ok=True)
(root / "assets/slide_manifest.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf8")

chars = sum(len(s["notes"]) for s in slides[:MAIN])
RATE = 5.1   # user's measured speaking rate (chars/s, 2026-11-01 rehearsal)
script = ["# 멀티에이전트, 어떻게 검증하는가 — 세미나 발표 대본", "", f"박천웅 · IRV_Lab · {DATE}", "",
          f"본편 **{MAIN}장 · 계획 {clock(PLANNED)}**, 전환 여유 **{clock(LIMIT - PLANNED)}**, 발표 제한 **{clock(LIMIT)}**. 부록 {len(slides) - MAIN}장은 본편에 포함하지 않습니다.",
          f"본편 대본 {chars:,}자 · 발표자 리허설 속도(초당 {RATE}자) 기준 약 {chars / RATE / 60:.1f}분. 실제 시간은 리허설로 확인해야 합니다.", "",
          "## 핵심 주제", "", "> **멀티에이전트는 말이 아니라 행동으로 검증해야 한다.**", "",
          "- 시리즈: 10.30 멀티에이전트란 무엇인가(이론) → 11.13 어떻게 만드는가(실전) → 11.27 작동하는지 어떻게 아는가(검증).",
          "- '말' 세 가지: 에이전트의 말(회고, 관계 점수, 기억) · 설계의 말(인수인계 규칙, 성격 설명문) · 교재의 말(멀티에이전트의 강점).", "",
          "## 시간 운영", "",
          "- 표지에서 `T`를 눌러 20분 타이머를 시작합니다. `T`는 일시정지/재개, `↺`는 초기화입니다.",
          "- 체크포인트: @@E5@@ 도입 종료 / @@E9@@ 에이전트의 말 종료 / @@E15@@ 설계의 말 종료 / @@E18@@ 교재의 말 종료 / @@E20@@ 정리 종료.",
          "- 1분 이상 늦으면 7장(담화방)과 15장(성격은 행동에서)은 표의 마지막 줄만 말하고 넘어갑니다.", "",
          "## 본편 시간표", "", "| 장 | 주제 | 구간 | 배정 |", "|---|---|---|---|"]
for i, s in enumerate(slides[:MAIN]):
    script.append(f'| {i + 1:02} | {s["title"]} | {s["start"]}–{s["end"]} | {s["duration"]} |')
for i, s in enumerate(slides):
    script += ["", f"## Slide {i + 1:02}. {s['title']}", "",
               f"- 시간: {s['start']}–{s['end']} / {s['duration']} · 대본 {len(s['notes'])}자 (약 {len(s['notes']) / RATE:.0f}초)" if s["seconds"] else "- 시간: 질의응답용 · 본편 미포함",
               f"- 근거: {s['source']}", "", s["notes"]]
(root / "presentation_script.md").write_text(fill_times("\n".join(script)) + "\n", encoding="utf8")
print(json.dumps({"slides": len(slides), "main": MAIN, "script_chars_main": chars, "est_minutes": round(chars / RATE / 60, 1),
                  "over": [(i + 1, s["title"], len(s["notes"]), s["seconds"]) for i, s in enumerate(slides[:MAIN]) if len(s["notes"]) / RATE > s["seconds"] * 1.15]},
                 ensure_ascii=False))
