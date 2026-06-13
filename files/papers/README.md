# Paper PDFs

Place public paper PDFs in this folder using the BibTeX key as the filename:

```text
files/papers/{BibTeX-key}.pdf
```

For example:

```text
files/papers/libgoberLawyersLobbyistsRegulatory2024.pdf
files/papers/pashley2025audit.pdf
```

During `quarto render`, `scripts/build_publications_listing.py` checks this folder. If a file named `{key}.pdf` exists for a publication in `cv-data/publications.bib`, the generated research listing automatically adds a PDF link.

For exceptions, add a manual override to the publication record in `cv-data/cv.yaml`:

```yaml
pdf: "files/papers/custom-file-name.pdf"
```
