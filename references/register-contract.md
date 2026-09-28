# Project register contract

Use UTF-8 JSON. Resolve local paths relative to the register file. Never embed credentials. Empty template arrays are preparation placeholders, not completed work.

- `revision`: approved content/assets revision; change when either changes.
- `manifest`: canonical manifest path. Synchronize slide identity/order/title from it; never edit content only in this register.
- `sources`: objects `{id, kind, url, designated_by_user}`. Kind: `video`, `official`, `transcript`. URL can be a local path for supplied transcript. Only mark designation true with session evidence.
- `claims`: `{id, type, text, evidence:[{source_id, locator}], uncertainty}`. Type: `fact`, `demo`, `plan`, `inference`. Locator is timestamp, section or page. Inferences also require evidence.
- `glossary`: `{official_name, description, first_slide_id}`. Validate exact naming and first-use explanation manually against rendered text; the validator cannot infer semantics.
- `slides`: ordered `{id, title, claim_ids, asset_ids, parallel_groups}`; `parallel_groups` is optional list of lists of asset IDs, e.g. `[["a1","a2","a3"]]`. Use it only for parallel visual cards; all-text layouts require no image group. No second copy of slide body here.
- `assets`: `{id, source_id, locator, supports_claim, slide_ids, status, path, crop, subject_box}`. Status: `planned` or `saved`. Path required for saved files. Crop/subject_box are `[left, top, right, bottom]` in normalized original-image coordinates 0..1. Subject box bounds the protected content, not the whole scene. The crop must contain it. Multiple essential subjects: use their enclosing box. Whole-image use: crop `[0,0,1,1]`. These assertions require source and final-crop visual inspection.
- `requested_formats`: subset of `html`, `pdf`, `pptx`, `zip`. Track Site in `site`, not as a hashed local file.
- `artifacts`: generated via `record_artifact.py`: `{format,path,sha256,revision,slides:[{id,title}],visual_review}`. After actually reviewing the current output, set `visual_review` to `passed`. Re-recording resets it to `pending`. Directory-based HTML should be packaged as a ZIP for a full-package checksum in addition to the entry HTML hash.
- `site`: null, or `{url,revision,verified}`; true only after checking the actual deployment. Do not store credentials or assume publishing was authorized.

Run `validate_project.py register.json` while working; errors exit 1, clean checks exit 0, unreadable/invalid input exits 2. Add `--delivery` to require an existing manifest, nonempty slides, saved assets, requested outputs, matching hashes/revisions/ordered slides and actual visual review records. Source omissions are warnings during preparation; any source used by a claim/asset must still be designated and registered. Delivery requires at least one designated source, but does not demand video when no video evidence was requested. Check source completeness against the brief separately.

These tools verify declared metadata, local files and protected-box containment. They cannot verify the truth of claims, detect actual logos/subtitles, extract slide structure from every format, or certify visual quality. Use actual extraction/render tools and record their observations. Never mark a check passed just to satisfy the validator.
