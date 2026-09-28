# Visual and export acceptance

## Layout recipes

- Cover/divider: compose title, subtitle and hero as one balanced group; distribute weight across the central region. Do not leave a large accidental hole in the middle while text sits in a corner.
- Argument page: one clear conclusion, 2–4 supporting units, and a supporting visual. Reduce copy before shrinking type.
- Three-part comparison: consistent heading/image/body baselines, comparable image area and crop scale, consecutive visible numbers starting at 01. Keep essential evidence visible in all three images.
- Process: center arrows in the gap between boxes, anchored to the boxes rather than paragraph lengths; use the same vertical reference across the row.
- Matrix: compare the same dimensions; distinguish unavailable information from poor performance. Do not manufacture scores.

## Per-page inspection

Inspect rendered final pages at reading size and full resolution, then review the contact sheet for pacing. Check:
1. Official names and first-use explanations; natural Chinese; no unexplained jargon.
2. Intentional title wrapping; clear hierarchy; consistent padding; no clipping or overlaps.
3. Balanced text/image weights and vertical distribution; no upper-half pileup or accidental central void. Do not eliminate purposeful whitespace indiscriminately.
4. Sequential labels and aligned arrows; parallel cards have comparable visual treatment.
5. Image meaning: actual product, hands, screens or interaction supporting the claim remain visible. Crop is checked after `object-fit`/container scaling, not just in the original.
6. No unwanted embedded video logo/subtitles, lower-left image overlay, or source footer under the user's chosen style. Keep attribution in notes/register.
7. Slide number/order, stable IDs, source traceability and approved content unchanged unless authorized.

For each issue log slide ID, defect class, fix and reviewed output revision. Search all slides for the class. Re-render affected pages and re-check global rhythm. Check image crops visually even when subject bounding boxes pass.

## Export pitfalls

- HTML applications may render only the active slide. Print a deterministic all-slides view; wait for fonts and images and choose final animation states.
- Use explicit page dimensions and page breaks; verify no blank trailing pages. Match slide aspect ratio.
- Check Chinese font embedding/substitution, bold variants, searchable text, missing glyphs and line breaks.
- Renderer support differs for CSS grid, masks, filters, aspect-ratio and backgrounds. Use export-compatible styles where needed and inspect actual output; do not assume browser equivalence.
- Do not bypass browser/security restrictions. Select an available permitted renderer and disclose material fidelity limits.
- Offline ZIP: local relative assets, entry page, no required remote fonts, all navigation usable offline.
- PDF/PPTX/HTML/Site: compare actual count, order, titles, terminology and revision; check imagery and content parity, not necessarily pixel equality.

A recorded visual pass means the actual current artifact was inspected. Structural validation, successful export and a contact sheet alone are insufficient proof of legibility and crop quality.
