"""EXP-003 reproducible semantic-coverage, timing and contour-code analysis."""
from __future__ import annotations
import json, re, statistics
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RUNTIME=ROOT/"language"/"runtime"/"exp-003-runtime-export.json"
CORPUS=ROOT/"benchmarks"/"exp-003-open-conversation.json"
WORD_RE=re.compile(r"[A-Za-z0-9]+(?:['’][A-Za-z]+)?")

def load(path):
    with path.open("r",encoding="utf-8") as h:
        return json.load(h)

def parse_text(text,runtime):
    forms={row["text"].lower():tuple(row["tokens"]) for row in runtime["surface_forms"]}
    ignored=set(runtime["ignore_forms"])
    words=list(WORD_RE.finditer(text))
    tokens=[]; fallback=[]; semantic_bytes=0; fallback_bytes=0; i=0
    while i<len(words):
        matched=False
        for count in range(min(4,len(words)-i),0,-1):
            surface=text[words[i].start():words[i+count-1].end()]
            mapped=forms.get(surface.lower())
            if mapped is not None:
                tokens.extend(mapped); semantic_bytes+=len(surface.encode("utf-8")); i+=count; matched=True; break
        if matched:
            continue
        surface=words[i].group(); lower=surface.lower(); size=len(surface.encode("utf-8"))
        if surface.isdigit() and len(surface)<=runtime["number_rule"]["max_digits"]:
            tokens.extend("NUM."+digit for digit in surface); semantic_bytes+=size
        elif lower in ignored:
            semantic_bytes+=size
        else:
            fallback.append(surface); fallback_bytes+=size
        i+=1
    if text.rstrip().endswith("?"):
        tokens.insert(0,"GRAM.Q")
    denom=semantic_bytes+fallback_bytes
    coverage=100.0 if not denom else 100*semantic_bytes/denom
    return {"tokens":tokens,"fallback_spans":fallback,"fallback_bytes":fallback_bytes,
            "semantic_coverage_percent":round(coverage,1),"fallback_percent":round(100-coverage,1)}

def semantic_seconds(tokens,candidate,multiplier):
    t=candidate["acoustics"]["timing_ms"]
    registry={row["id"]:row for row in candidate["tokens"]}
    total=(t["phrase_header"]+t["profile_marker"])*multiplier
    for token in tokens:
        row=registry[token]
        gesture=t["short_gesture"] if row["duration_class"]=="short" else t["root_gesture"]
        total+=(gesture+t["token_boundary"])*multiplier
    return total/1000

def fallback_seconds(spans,candidate,multiplier):
    if not spans:
        return 0.0
    t=candidate["acoustics"]["timing_ms"]; total=0
    for span in spans:
        total+=t["fallback_marker"]+t["fallback_boundary"]
        total+=len(span.encode("utf-8"))*(t["fallback_byte"]+t["fallback_default_gap"])
    return total*multiplier/1000

def analyze():
    runtime=load(RUNTIME); corpus=load(CORPUS); candidate=runtime["candidate"]; mult=corpus["playback_multiplier"]
    rows=[]
    for source in corpus["results"]:
        parsed=parse_text(source["english"],runtime)
        semantic=semantic_seconds(parsed["tokens"],candidate,mult)
        fallback=fallback_seconds(parsed["fallback_spans"],candidate,mult)
        rows.append({
            "id":source["id"],"class":source["class"],"english":source["english"],
            "semantic_token_count":len(parsed["tokens"]),"unsupported_spans":parsed["fallback_spans"],
            "fallback_span_count":len(parsed["fallback_spans"]),"fallback_bytes":parsed["fallback_bytes"],
            "semantic_coverage_percent":parsed["semantic_coverage_percent"],"fallback_percent":parsed["fallback_percent"],
            "semantic_duration_seconds":round(semantic,3),"fallback_duration_seconds":round(fallback,3),
            "total_duration_seconds":round(semantic+fallback,3),
        })
    return rows
