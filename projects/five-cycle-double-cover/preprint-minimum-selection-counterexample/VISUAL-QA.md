# PDF visual quality assurance

Date: 2026-07-29

Artifact: `main.pdf`

- Deterministically built with Tectonic 0.16.0-compatible tooling and
  `SOURCE_DATE_EPOCH=1785283200`.
- Eight US-letter pages, PDF 1.5.
- Rendered with Poppler `pdftoppm` at 130 DPI.
- Every rendered page was inspected at original rendered resolution.
- No clipping, overlap, broken glyphs, illegible equations, or margin
  violations were found.
- The final references-only page is intentionally sparse; no content is
  missing.
- The build log contains no overfull boxes, underfull boxes, undefined
  references, or undefined citations.

This is a layout audit only. Mathematical review is described in
`HUMAN-REVIEW.md`.
