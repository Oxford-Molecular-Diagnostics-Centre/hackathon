# Oxford Cancer AI Challenges

A static, responsive PI discussion draft. The model is to identify clinical research questions, agree the required samples/assays/data/compute, then invite AI teams once the brief and arrangements are approved.

## Pages

- `index.html`: concise overview and routes into the programme.
- `programme.html`: phases, possible formats, participation, IP, publication, glossary and review conditions.
- `challenges.html`: illustrated catalogue, accessible expandable briefs and data-readiness filters. Includes two new assay concepts and expands overlapping existing tasks.
- `vaccines.html`: the single canonical cancer vaccine epitope family, cancer-type options, prior-art comparison and a proposed evaluation specification.
- `resources.html`: candidate data resources, possible partner support, data protection and research sources.
- `precedents.html`: seven source-linked event comparisons, nine opening-deck example mappings, and explicit duplicate/overlap decisions.
- `propose.html`: researcher-friendly form that prepares, copies and downloads a local draft.

## Preview and edit

```sh
python3 -m http.server 8000
```

Visit http://localhost:8000. GitHub Pages serves these static files without a runtime or framework.

Edit page fragments in `content/pages/`, metadata in `content/pages.json`, and the shared header/footer in `content/layout.html`. The event comparison is built from `research/precedents.json`. Then regenerate the HTML:

```sh
python3 scripts/build_site.py
python3 scripts/check_site.py
```

`styles.css` holds the retained original styles; `visuals.css` the illustration layer; `site.css` the multi-page components. `site.js` holds guarded page interactions. The builder refreshes its marked legacy-route section so old single-page fragment links continue to work. `site-config.js` contains the disabled submission configuration.

The original Oxford and CRUK logos were extracted unchanged to local `assets/brand/` files, avoiding repeated embedded copies. Original illustration provenance and generation prompt remain in `assets/illustrations/README.txt`; the new assay icon is a native SVG schematic.

## Research and duplication review

The supplied opening deck was read from the saved 25-slide HTML outside this repository. Its raw files, photographs and third-party assets are not republished. The public artifact was access-blocked, so the local copy supplied by the user was used to verify the examples.

The review maps Binder-Sieve, Synapse-Switch and Trust-Curve into the existing binding brief; Fail-Forward into harmonisation; hardware prompts into one assay-prototyping concept; and four omics examples into alternative work packages within one functional-omics concept. The vaccine family already existed and is refined, not duplicated. TESLA, IMMREP25, CASP–DREAM TAP, Adaptyv, GEM and Anti–PD-1 DREAM provide explicit precedents or adjacent tasks. This is a targeted landscape comparison, not an exhaustive novelty or patent search.

## Status and collection

All pages remain `noindex` discussion drafts. If hosted, they are publicly reachable, not access-controlled or suitable for confidential data. Organisational permissions, research-proposal descriptions, governance and approved collection/privacy arrangements remain prerequisites for launch. A later OxCODE move is subject to approval. No organisation is represented as a confirmed partner.

The form defaults to local preparation only. Online collection requires explicit enablement plus an approved HTTPS endpoint and privacy notice; those are not configured. Native submit buttons stay disabled without JavaScript so entered values are not accidentally sent in a GET URL. No sample access, assays, credits, funding, prizes or publications are promised. No deployment is included in this local update.
