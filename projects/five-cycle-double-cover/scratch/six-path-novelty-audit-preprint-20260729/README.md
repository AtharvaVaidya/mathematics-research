# Provisional novelty audit and preprint draft

This directory contains a bounded primary-literature audit and a deliberately
scoped preprint draft for the six-state connector lemma proved in

```text
../cyclic4-hybrid-universal-through14-20260729/
```

It does **not** claim a proof or disproof of the Five-Cycle Double Cover
Conjecture.  This is a public research-repository draft, not an arXiv or
journal submission, and it has not been independently reviewed by a human.

Files:

- `NOVELTY-AUDIT.md`: exact comparison with the closest literature found;
- `preprint.tex`: provisional mathematical note with theorem statements,
  proof, verification protocol, limitations, and an explicit AI-use statement;
- `preprint.pdf`: rendered draft, if `tectonic preprint.tex` has been run;
- `BUILD-OUTPUT.txt`: captured typesetting output;
- `SHA256SUMS`: checksums for the audit and draft.

The computational proof objects remain in the frozen source package.  Its
top-level ledger has SHA-256 digest

```text
2fd36f21f18796c15760321806152fe60f37d5ba40575a11c26dc76c9c31f3d7
```

To verify the mathematics rather than trusting the prose:

```sh
cd ../cyclic4-hybrid-universal-through14-20260729
python3 verify.py
```

The verifier is solver-free.  It checks the frozen hash ledger, reconstructs
both six-poles from graph6 strings, checks all 2,592 local completion rows,
regenerates the macro census, reconstructs automorphism orbits, and checks all
9,278 saved macro witnesses.

## Publication status

The bounded audit found no exact antecedent for the six-state inclusion for
these two six-poles.  That is evidence of possible novelty, not proof of
novelty.  The repository release deliberately retains that limitation and the
AI-use disclosure.  Before submitting the note to arXiv or a journal:

1. obtain an independent human line-by-line review of the statement and proof;
2. have another researcher rerun the verifier from a clean checkout;
3. ask a FiveCDC/snark specialist specifically about unpublished multipole
   state tables and theses;
4. confirm the author's preferred bibliographic name and affiliation;
5. replace the provisional language only where the new review supplies
   evidence.
