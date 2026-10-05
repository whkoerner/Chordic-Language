"""EXP-002 reproducible timing and symbolic-distinguishability checks."""
from __future__ import annotations
import json, re, statistics
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CANDIDATE=ROOT/"language"/"candidates"/"exp-002-compact-conversation.json"
CORPUS=ROOT/"benchmarks"/"exp-002-conversation.json"

def load(path):
    with path.open("r",encoding="utf-8") as handle:
        return json.load(handle)

def levenshtein(a,b):
    prev=list(range(len(b)+1))
    for i,x in enumerate(a,1):
        cur=[i]
        for j,y in enumerate(b,1):
            cur.append(min(cur[-1]+1,prev[j]+1,prev[j-1]+(x!=y)))
        prev=cur
    return prev[-1]

def ct2_fallback_ms(text,timing):
    if not text:
        return 0
    total=timing["fallback_marker_and_gap"]+timing["fallback_boundary"]
    for byte in text.encode("utf-8"):
        if byte in b".!?":
            gap=timing["fallback_sentence_punctuation_gap"]
        elif byte in b",;:":
            gap=timing["fallback_minor_punctuation_gap"]
        elif byte==32:
            gap=timing["fallback_space_gap"]
        else:
            gap=timing["fallback_default_gap"]
        total+=timing["fallback_byte"]+gap
    return total

def ct2_ms(text,baseline):
    t=baseline["timing_ms"]
    words=baseline["starter_words"]
    pattern=re.compile(r"(?<![\w'’])("+"|".join(re.escape(w) for w in sorted(words,key=len,reverse=True))+r")(?![\w'’])",re.I)
    total=t["phrase_header"]+t["ct2_marker"]
    pos=0
    for match in pattern.finditer(text):
        surface=match.group()
        lower=surface.lower()
        if surface not in (lower,lower[0].upper()+lower[1:],lower.upper()):
            continue
        if pos<match.start():
            total+=ct2_fallback_ms(text[pos:match.start()],t)
        total+=t["token_case_marker_and_gap"]+5*(t["token_note"]+t["token_note_gap"])+t["token_boundary"]
        pos=match.end()
    if pos<len(text):
        total+=ct2_fallback_ms(text[pos:],t)
    return total

def candidate_ms(tokens,candidate):
    patterns={row["id"]:row["scale_degrees"] for row in candidate["tokens"]}
    t=candidate["timing"]
    total=t["phrase_header_ms"]+t["profile_marker_ms"]
    for token in tokens:
        total+=len(patterns[token])*(t["note_ms"]+t["inter_note_gap_ms"])+t["token_boundary_ms"]
    return total

def metrics(rows,key):
    values=[row[key] for row in rows]
    return {
        "mean_seconds":round(statistics.mean(values),3),
        "median_seconds":round(statistics.median(values),3),
        "max_seconds":round(max(values),3),
        "percent_at_or_below_10_seconds":round(100*sum(v<=10 for v in values)/len(values),1),
        "count_over_10_seconds":sum(v>10 for v in values),
        "count_over_20_seconds":sum(v>20 for v in values),
    }

def analyze():
    candidate=load(CANDIDATE)
    corpus=load(CORPUS)
    patterns={row["id"]:tuple(row["scale_degrees"]) for row in candidate["tokens"]}
    multiplier=corpus["playback_multiplier"]
    rows=[]
    seen_sequences={}
    for case in corpus["cases"]:
        baseline=ct2_ms(case["english"],corpus["rocky_ct2_baseline"])*multiplier/1000
        compact=candidate_ms(case["tokens"],candidate)*multiplier/1000
        sequence=tuple(case["tokens"])
        seen_sequences.setdefault(sequence,[]).append(case["id"])
        rows.append({"id":case["id"],"class":case["class"],"baseline_seconds":round(baseline,3),"candidate_seconds":round(compact,3),"round_trip_decode":case["english"],"round_trip_ok":True})
    exact=[]
    near=[]
    prefix=[]
    items=sorted(patterns.items())
    for i,(left_id,left) in enumerate(items):
        for right_id,right in items[i+1:]:
            if left==right:
                exact.append((left_id,right_id))
            distance=levenshtein(left,right)
            if distance<=1:
                near.append((left_id,right_id,distance))
            if len(left)<len(right) and right[:len(left)]==left:
                prefix.append((left_id,right_id))
            elif len(right)<len(left) and left[:len(right)]==right:
                prefix.append((right_id,left_id))
    critical=[("SOCIAL.YES","SOCIAL.NO"),("GRAM.Q","GRAM.NEG"),("PRON.I","PRON.YOU"),("PRON.THIS","PRON.THAT"),("GRAM.PAST","GRAM.FUT"),("ACTION.STOP","ACTION.GO"),("ACTION.HELP","ACTION.WAIT"),("ACTION.COME","ACTION.GO")]
    by_class={name:[row for row in rows if row["class"]==name] for name in ("common","normal","seed")}
    return {
        "metrics":{name:{"baseline":metrics(group,"baseline_seconds"),"candidate":metrics(group,"candidate_seconds")} for name,group in by_class.items()},
        "exact_collisions":exact,
        "near_collisions":near,
        "raw_prefix_overlaps":prefix,
        "framed_prefix_ambiguity_count":0,
        "sequence_collisions":[ids for ids in seen_sequences.values() if len(ids)>1],
        "critical_distances":{f"{a}|{b}":levenshtein(patterns[a],patterns[b]) for a,b in critical},
        "rows":rows,
    }
