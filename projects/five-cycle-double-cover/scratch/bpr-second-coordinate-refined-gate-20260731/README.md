# Refined second-coordinate gate

This package proves the exact fixed-residual change formula for the BPR
second-coordinate potential.  From old tight count zero, only old even
components with total cut size four must be parity-protected.  After that
protection, strict descent is equivalent to positivity of one aggregate
integer gain.  This strictly weakens the earlier componentwise conditions.

An independent exact analysis of the frozen order-80 girth-ten,
cyclically-4 control shows that the reduced cut-space obstruction can still
occur.  One ((5,1)) blocker has no partner-free direction satisfying the
reduced parity system.  The host is directly certified Tait-colourable, so
this is a structural countercontrol, not a non-Tait BPR counterexample.

Run:

```sh
python3 -B verify_refined_formula.py
python3 -B analyze_order80_control.py
shasum -a 256 -c SHA256SUMS
shasum -a 256 -c SOURCE-SHA256SUMS
```

This is not a universal descent theorem, BPR proof, or FiveCDC resolution.
The work was produced by OpenAI Codex under human direction and has not had
independent human peer review.
