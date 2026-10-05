"""EXP-003 v0.2 Windows-feedback regression analyzer."""
from __future__ import annotations
import json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RUNTIME=ROOT/"language"/"runtime"/"exp-003-runtime-export-v2.json"
CORPUS=ROOT/"benchmarks"/"exp-003-windows-feedback-v0.2.json"
WORD_RE=re.compile(r"[A-Za-z0-9]+(?:['’][A-Za-z]+)?")

def load(path):
    with path.open("r",encoding="utf-8") as handle:
        return json.load(handle)

def _digit_tokens(value):
    return ["NUM."+digit for digit in str(value)]

def parse_text(text,runtime):
    forms={row["text"].lower():tuple(row["tokens"]) for row in runtime["surface_forms"]}
    ignored=set(runtime["ignore_forms"])
    number=runtime["number_rule"]
    units=number["spoken_units"]; tens=number["spoken_tens"]
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
        if surface.isdigit() and len(surface)<=number["max_digits"]:
            tokens.extend("NUM."+digit for digit in surface); semantic_bytes+=size; i+=1; continue
        if lower in tens:
            value=tens[lower]; end=i
            if i+1<len(words):
                nxt=words[i+1].group().lower()
                if nxt in units and 1<=units[nxt]<=9:
                    value+=units[nxt]; end=i+1
            phrase=text[words[i].start():words[end].end()]
            tokens.extend(_digit_tokens(value)); semantic_bytes+=len(phrase.encode("utf-8")); i=end+1; continue
        if lower in units:
            tokens.extend(_digit_tokens(units[lower])); semantic_bytes+=size; i+=1; continue
        if lower in ignored:
            semantic_bytes+=size; i+=1; continue
        fallback.append(surface); fallback_bytes+=size; i+=1
    if text.rstrip().endswith("?"):
        tokens.insert(0,"GRAM.Q")
    denom=semantic_bytes+fallback_bytes
    coverage=100.0 if not denom else 100*semantic_bytes/denom
    return {"tokens":tokens,"fallback_spans":fallback,"fallback_bytes":fallback_bytes,
            "semantic_coverage_percent":round(coverage,1),"fallback_percent":round(100-coverage,1)}

def semantic_seconds(tokens,candidate,multiplier=3):
    timing=candidate["acoustics"]["timing_ms"]
    registry={row["id"]:row for row in candidate["tokens"]}
    total=(timing["phrase_header"]+timing["profile_marker"])*multiplier
    for token in tokens:
        row=registry[token]
        gesture=timing["short_gesture"] if row["duration_class"]=="short" else timing["root_gesture"]
        total+=(gesture+timing["token_boundary"])*multiplier
    return round(total/1000,3)

def analyze():
    runtime=load(RUNTIME); corpus=load(CORPUS); result=[]
    for row in corpus["results"]:
        parsed=parse_text(row["english"],runtime)
        duration=semantic_seconds(parsed["tokens"],runtime["candidate"],corpus["playback_multiplier"])
        result.append({
            "id":row["id"],
            "semantic_tokens":parsed["tokens"],
            "semantic_token_count":len(parsed["tokens"]),
            "unsupported_spans":parsed["fallback_spans"],
            "fallback_span_count":len(parsed["fallback_spans"]),
            "fallback_bytes":parsed["fallback_bytes"],
            "semantic_coverage_percent":parsed["semantic_coverage_percent"],
            "fallback_percent":parsed["fallback_percent"],
            "semantic_duration_seconds":duration,
            "fallback_duration_seconds":0.0,
            "total_duration_seconds":duration,
        })
    return result
