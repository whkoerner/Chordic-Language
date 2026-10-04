# Chordic v0.0 Data Model

**Language version:** v0.0 — Concept  
**Data-model revision:** 0.1  
**Status:** Experimental

This document defines how Chordic stores language research data before the language itself has been designed. It does not define phonology, grammar, vocabulary, or recognition behavior.

## General rules

- `language_version` records the language milestone represented by a file.
- `schema_version` records the structure of that machine-readable file.
- Empty arrays are valid when no canonical items exist.
- `null` means a value is intentionally absent/not yet available.
- The string `not_yet_determined` may be used for an unresolved design choice.
- Unsupported acceptance examples must not contain invented semantic or tonal translations.

## Dictionary

`language/dictionary.json` contains canonical primitive entries in `entries`.

When entries eventually exist, each should support fields such as:

- `id`
- `category`
- `semantic_concept`
- `definition`
- `tonal_representation`
- `grammatical_function`
- `combinable_concepts`
- `status`
- `introduced_version`
- `deprecated_version`
- `notes`

Not every field is meaningful at v0.0. No primitive entries currently exist.

## Grammar

`language/grammar.json` contains canonical grammar rules in `rules`.

Each future rule must have a unique ID and must reference only defined canonical concepts/rules where references are used.

No grammar rules currently exist.

## Phonology

`language/phonology.json` records sound-system decisions only after they are made.

At v0.0, pitch reference, tone inventory, duration, boundaries, and related behavior remain unresolved.

## Gestures

`language/gestures.json` stores optional canonical gestures separately from the tonal language.

Future gesture records should track:

- `id`
- `physical_description`
- `semantic_meaning`
- `modifies_spoken_expression`
- `can_stand_alone`
- `ambiguity_concerns`
- `cultural_interpretation_risks`
- `robot_implementation_constraints`
- `introduced_version`
- `status`

No canonical gestures currently exist.

## Acceptance examples

`language/examples.json` preserves communication targets.

An example with `support_status: "unsupported"` is a future acceptance target. Its `semantic_representation` and `chordic_form` must remain `null` until the required vocabulary/grammar has actually been defined and tested.

The goal is compositional expression through reusable language rules, not arbitrary whole-sentence codes.

## Entry status vocabulary

When canonical entries exist, allowed maturity statuses are:

- `experimental`
- `candidate`
- `stable`
- `deprecated`
- `reserved`

These statuses do not claim test results by themselves.
