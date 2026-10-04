# Tests

Chordic uses automated tests to protect machine-readable language invariants as they become meaningful.

Run the current suite from the repository root with:

```bash
python -m unittest discover -s tests -v
```

The v0.0 suite validates repository/data integrity. It does **not** claim that the language, audio, recognition, translation, or human usability has been tested.

Later suites should be separated by purpose (vocabulary, grammar, collisions, translation, recognition, regression) when those capabilities actually exist.
