# Quarto Academic Website Publication Workflow

This project builds an academic website and CV from a shared, structured data model. The basic idea is to maintain a single source of truth for publications and related career data, then generate website-specific YAML during the Quarto render process.

The goal is to avoid hand-maintaining a separate website publication list, a CV publication list, and individual publication pages unless those pages are genuinely useful.

## Overview

The planned workflow is:

```text
cv-data.yaml + references.bib + files/papers/
        ↓
pre-render script
        ↓
website/_generated/publications.yaml
        ↓
Quarto listing + custom EJS template
        ↓
publications page
```

The hand-maintained files should stay simple and durable. The generated files should be disposable. If a generated file is deleted, it should be possible to recreate it by running `quarto render`.

## Design Principles

### 1. One source of truth

The canonical source for career metadata is `cv-data.yaml`. This file contains the publication order, CV section, status, display flags, and optional links. It should not contain website styling details.

The canonical source for citation metadata is a bibliography file exported from Zotero, likely through Better BibTeX. This file contains titles, authors, venues, years, DOIs, abstracts, and other bibliographic fields.

### 2. Website data is derived data

The website will not directly use `cv-data.yaml` in raw form. Instead, a script will reshape and enrich it into `_generated/publications.yaml`, which is better suited to Quarto listings.

This keeps the source data clean while letting the website use whatever structure is easiest for rendering.

### 3. Publication pages are optional

A publication listing item does not need to correspond to a real `.qmd` page. The generated YAML can contain all the data needed to render an entry directly on the publications page.

Separate pages like `pashley2025audit.qmd` should only exist for flagship projects where a richer explanation is worthwhile.

### 4. PDFs follow a convention

PDF links can be handled by convention rather than manual metadata:

```text
files/papers/{citation_key}.pdf
```

For example:

```text
files/papers/pashley2025audit.pdf
```

If the file exists, the generated YAML includes a PDF link. If the file does not exist, the PDF button is omitted.

Manual overrides are still allowed when needed.

### 5. The template should be small and stable

The EJS template should only decide how to display each publication card. It should not contain scholarly data or complicated logic. Most of the logic should live in the Python or R pre-render script.

## Reference Models and Documentation

These are useful examples and references to consult while implementing the project.

- [Dr. Gang He’s Quarto Academic Website Template](https://github.com/drganghe/quarto-academic-website-template): closest model for this project. It uses structured publication data, generated YAML, and a custom publication listing.
- [Dr. Gang He’s note on generating publication listings](https://drganghe.github.io/notes/generate-publications-listing.html): explains the Excel-to-YAML workflow and how the generated YAML feeds the Quarto listing.
- [Dr. Gang He’s academic website examples and tips](https://drganghe.github.io/quarto-academic-site-examples.html): includes the pre-render idea for generating publication listings.
- [Quarto documentation on document listings](https://quarto.org/docs/websites/website-listings.html): explains how Quarto listings can use documents or custom data.
- [Quarto documentation on custom listings](https://quarto.org/docs/websites/website-listings-custom.html): explains how custom EJS templates work with listing data.
- [Quarto documentation on project scripts](https://quarto.org/docs/projects/scripts.html): explains `pre-render` and `post-render` scripts.
- [Silvia Canelón’s post on moving a website to Quarto](https://silviacanelon.com/blog/2023-09-29-hello-quarto/): useful example of an academic/personal website migration to Quarto.
- [Meghan Hall’s post on moving to Quarto](https://meghan.rbind.io/blog/2024-02-11-moving-to-quarto/): useful because it notes that controlling custom listings can be the hardest part of a Quarto migration.
- [David Folio’s post on publication listings in Quarto](https://dfolio.fr/posts/2023/2023-08-17_publications.html): another example of creating a publications page with Quarto.

## Proposed Repository Structure

A possible repository structure is:

```text
website/
  _quarto.yml
  index.qmd
  publications.qmd
  publication-card.ejs
  styles.css

  cv-data.yaml
  references.bib

  files/
    papers/
      pashley2025audit.pdf
      HolverscheidLibgoberPouliot2024.pdf

  scripts/
    build_publications_listing.py

  _generated/
    publications.yaml
    publications.hash
```

If the CV and website are separate repositories, then `cv-data.yaml` and `references.bib` may instead live in a shared data repository:

```text
profile-data/
  cv-data.yaml
  references.bib

cv/
  cv.typ

website/
  _quarto.yml
  publications.qmd
  scripts/
    build_publications_listing.py
```

In that version, both the CV and the website read from the shared data repository.

## Source Data: `cv-data.yaml`

The existing `cv-data.yaml` can remain organized around CV sections.

Example:

```yaml
publications:
  peer:
    - key: pashley2025audit
      status: "Forthcoming"
      selected: true
      show_on_cv: true
      show_on_website: true
      pdf: "files/papers/pashley2025audit.pdf"
      tags:
        - courts
        - audit study
        - representation

    - key: HolverscheidLibgoberPouliot2024
      status: "Accepted"

    - key: fernandesPartisanRhetoricInstitutional2025

    - key: Omari2025FederalProcurementDataset
      data: "https://dataverse.harvard.edu/"
      tags:
        - procurement
        - dataset

  working:
    - key: LibgoberLawyersLobbyingAdministrativeState
      status: "Book manuscript"
      selected: true
      show_on_cv: true
      show_on_website: true
      website_slug: "lawyers-lobbying-administrative-state"
      website_blurb: >-
        A book project on lawyers, lobbying, and the administrative state.
      tags:
        - administrative state
        - lobbying
        - law
```

The entries can stay sparse. Only add extra metadata where it is useful.

## Suggested Fields in `cv-data.yaml`

### Required

```yaml
key:
```

The `key` should match the citation key in `references.bib`.

### Common optional fields

```yaml
status:
year:
order:
selected:
show_on_cv:
show_on_website:
pdf:
doi:
url:
code:
data:
slides:
website_slug:
website_blurb:
cv_note:
tags:
title_override:
venue_override:
```

### Field meanings

| Field | Purpose |
|---|---|
| `key` | Citation key used to join `cv-data.yaml` to `references.bib` |
| `status` | Forthcoming, accepted, under review, working paper, book manuscript, etc. |
| `year` | Optional year override for sorting |
| `order` | Optional manual order within a section |
| `selected` | Whether the item appears in a selected/featured section |
| `show_on_cv` | Whether the item appears on the CV |
| `show_on_website` | Whether the item appears on the website |
| `pdf` | Manual PDF link, if not using the citation-key convention |
| `doi` | Manual DOI override |
| `url` | Canonical external URL |
| `code` | GitHub, OSF, or other code repository |
| `data` | Dataverse, OSF, or other data repository |
| `slides` | Slides link |
| `website_slug` | Optional detail page slug |
| `website_blurb` | Short website-only prose |
| `cv_note` | Short CV-only note |
| `tags` | Website categories |
| `title_override` | Override bad or awkward BibTeX title |
| `venue_override` | Override bad or awkward BibTeX venue |

## Bibliography Data: `references.bib`

The bibliography file should come from Zotero, probably through Better BibTeX.

The script should use the citation key to pull fields such as:

```text
title
author
year
journal
booktitle
publisher
volume
number
pages
doi
url
abstract
entry type
```

The generated website YAML can then contain both citation-derived data and CV-derived data.

## Generated Data: `_generated/publications.yaml`

The pre-render script should produce a file shaped for the website, not for the CV.

Example generated item:

```yaml
- key: pashley2025audit
  section: peer
  section_label: Peer-reviewed Articles
  title: "Audit Study of ..."
  authors: "Pashley, Libgober, and ..."
  year: 2025
  date: "2025-01-01"
  venue: "Journal Name"
  status: "Forthcoming"
  abstract: "This article..."
  citation: "Pashley, ... 2025. “Audit Study of ...” Journal Name."
  pdf: "files/papers/pashley2025audit.pdf"
  doi: "10.xxxx/xxxxx"
  selected: true
  categories:
    - peer-reviewed
    - courts
    - audit study
```

This file is generated. It should not be hand edited.

## Quarto Listing Page

The `publications.qmd` page should point to the generated YAML.

Example:

```yaml
---
title: "Publications"
listing:
  id: pubs
  contents: _generated/publications.yaml
  type: custom
  template: publication-card.ejs
  sort: "date desc"
---
```

Then place the listing in the page body:

```markdown
## Publications

::: {#pubs}
:::
```

The listing does not require separate publication pages. It only requires data in `_generated/publications.yaml`.

## EJS Template

The custom template controls display.

Example `publication-card.ejs`:

```ejs
<% for (const item of items) { %>
  <div class="publication">
    <p class="citation"><%- item.citation %></p>

    <% if (item.status) { %>
      <p class="status"><%= item.status %></p>
    <% } %>

    <% if (item.website_blurb) { %>
      <p class="blurb"><%= item.website_blurb %></p>
    <% } %>

    <% if (item.abstract) { %>
      <details>
        <summary>Abstract</summary>
        <p><%= item.abstract %></p>
      </details>
    <% } %>

    <p class="links">
      <% if (item.pdf) { %>
        <a href="<%= item.pdf %>">PDF</a>
      <% } %>

      <% if (item.doi) { %>
        <a href="https://doi.org/<%= item.doi %>">DOI</a>
      <% } %>

      <% if (item.code) { %>
        <a href="<%= item.code %>">Code</a>
      <% } %>

      <% if (item.data) { %>
        <a href="<%= item.data %>">Data</a>
      <% } %>
    </p>
  </div>
<% } %>
```

EJS is Embedded JavaScript. The useful syntax is:

```text
<% ... %>   run JavaScript without printing
<%= ... %>  print escaped text
<%- ... %>  print raw HTML
```

If the Python script creates `citation_html`, use `<%- item.citation_html %>`. If it creates plain text, use `<%= item.citation %>`.

## Pre-render Script

The pre-render script should be called from `_quarto.yml`.

Example:

```yaml
project:
  type: website
  pre-render:
    - python scripts/build_publications_listing.py
```

The script should:

1. Read `cv-data.yaml`.
2. Read `references.bib`.
3. Join publication entries by citation key.
4. Flatten sections like `peer`, `working`, `book_chapters`, and `datasets`.
5. Add section labels.
6. Add citation fields from BibTeX.
7. Check whether `files/papers/{key}.pdf` exists.
8. Add PDF links where available.
9. Add website fields such as tags, categories, selected status, code links, and data links.
10. Write `_generated/publications.yaml`.

## Incremental Build Check

The script can avoid unnecessary writes by checking whether inputs have changed.

Inputs to hash:

```text
cv-data.yaml
references.bib
files/papers/*.pdf
scripts/build_publications_listing.py
```

Generated cache file:

```text
_generated/publications.hash
```

Basic logic:

```text
compute hash of inputs
if hash matches previous hash and output exists:
    skip rebuild
else:
    rebuild publications.yaml
    update hash
```

This prevents Quarto from seeing unnecessary file changes on every render.

## Validation

The script should fail loudly when the data are inconsistent.

Recommended checks:

1. Every publication key in `cv-data.yaml` exists in `references.bib`.
2. No duplicate keys appear in `cv-data.yaml`.
3. Every manually specified PDF path exists.
4. Every manually specified link is a string.
5. Every generated website item has a title.
6. Every generated website item has a year or date.
7. Every item has a section label.
8. The generated YAML is valid.
9. `show_on_cv` and `show_on_website` are booleans when present.
10. Unknown fields are either allowed intentionally or flagged as possible typos.

Validation should happen before writing the generated YAML.

## GitHub Actions

The GitHub Action does not need a separate step for the publication generator if `_quarto.yml` has a `pre-render` command.

A simple build step can be:

```yaml
- name: Render site
  run: quarto render
```

Quarto will call the pre-render script automatically.

A more verbose version can be useful while debugging:

```yaml
- name: Build publication listing
  run: python scripts/build_publications_listing.py --force

- name: Render site
  run: quarto render
```

Once stable, the first version is cleaner.

## Files to Commit

Commit:

```text
cv-data.yaml
references.bib
scripts/build_publications_listing.py
publications.qmd
publication-card.ejs
styles.css
files/papers/*.pdf
```

Usually do not commit:

```text
_generated/publications.yaml
_generated/publications.hash
```

However, it may be useful to commit `_generated/publications.yaml` during early development so that diffs are easy to inspect.

## Implementation Plan

### Step 1: Decide repository layout

Choose whether `cv-data.yaml` and `references.bib` live inside the website repository or in a shared profile-data repository.

For the first version, keeping them in the website repository is simplest.

### Step 2: Normalize `cv-data.yaml`

Make sure all publication entries use a citation key:

```yaml
publications:
  peer:
    - key: pashley2025audit
      status: "Forthcoming"
```

Add optional fields only where useful.

### Step 3: Export `references.bib`

Export the bibliography from Zotero. Better BibTeX is useful because it can provide stable citation keys.

The citation keys in `references.bib` must match the `key` fields in `cv-data.yaml`.

### Step 4: Create the PDF convention

Place public PDFs at:

```text
files/papers/{key}.pdf
```

Example:

```text
files/papers/pashley2025audit.pdf
```

### Step 5: Write `build_publications_listing.py`

The script should start simple:

1. Load YAML.
2. Load BibTeX.
3. Join by key.
4. Write generated YAML.

Then add validation, PDF detection, citation formatting, and hash-based skipping.

### Step 6: Add Quarto pre-render hook

In `_quarto.yml`:

```yaml
project:
  type: website
  pre-render:
    - python scripts/build_publications_listing.py
```

### Step 7: Create `publications.qmd`

Point the listing to the generated YAML:

```yaml
---
title: "Publications"
listing:
  id: pubs
  contents: _generated/publications.yaml
  type: custom
  template: publication-card.ejs
  sort: "date desc"
---
```

Then add:

```markdown
::: {#pubs}
:::
```

### Step 8: Create a minimal EJS template

Start with citation, status, and links. Add abstracts, tags, and detail-page links only after the basic version works.

### Step 9: Style lightly

Use CSS for spacing, button styling, and typography. Keep the data model independent of the styling.

### Step 10: Add optional detail pages later

For selected flagship projects, add optional `.qmd` pages. These should be exceptions, not a requirement for every publication.

## Open Design Decisions

### Should generated YAML be committed?

Initial recommendation: commit during development, ignore later.

### Should the citation be plain text or HTML?

Plain text is safer. HTML allows italicized journal names and linked DOIs. If using HTML, the EJS template should render with `<%- item.citation_html %>`.

### Should BibTeX or CSL JSON be the bibliography source?

BibTeX is simpler to start with. CSL JSON may be better if citation rendering becomes more sophisticated.

### Should the CV use the generated YAML?

Probably not. The CV and website should be sibling outputs from shared source data. The generated website YAML is a website view model, not the canonical data source.

## Summary

This system keeps the website low-maintenance while allowing richer publication display than a CV. The durable source data remain in `cv-data.yaml` and `references.bib`. A pre-render script reshapes those files into a Quarto-friendly listing YAML. Quarto then uses a small custom EJS template to render a clean publications page.

The key advantage is that adding a new publication should usually require only:

1. adding or updating the item in Zotero;
2. exporting `references.bib`;
3. adding a short entry to `cv-data.yaml`;
4. optionally placing a PDF at `files/papers/{key}.pdf`;
5. running `quarto render`.
