"""Publish a review notebook as a page on the site.

Usage (from the repo root):
    .venv/bin/python reviews/build_review.py [reviews/mapping-inequality]

Converts the saved notebook (it is not re-run), drops cells tagged `prompt` or `exclude`, hides all code,
and writes index.html next to the notebook using the site's header and styles.
"""
import re
import sys
from pathlib import Path

import nbformat
from nbconvert import HTMLExporter
from nbconvert.preprocessors import TagRemovePreprocessor

review_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "reviews/mapping-inequality").resolve()
notebook_path = review_dir / "review.ipynb"
site_root = Path(__file__).resolve().parent.parent
to_root = "../" * len(review_dir.relative_to(site_root).parts)

nb = nbformat.read(notebook_path, as_version=4)

remove = TagRemovePreprocessor(remove_cell_tags={"prompt", "exclude"}, remove_input_tags=set())
remove.enabled = True
nb, _ = remove.preprocess(nb, {})

exporter = HTMLExporter(template_name="basic", exclude_input=True, exclude_input_prompt=True, exclude_output_prompt=True)
body, _ = exporter.from_notebook_node(nb)

h1 = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S)
title = "Review: " + re.sub(r"<[^>]+>|¶", "", h1.group(1)).strip() if h1 else "Review"

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>{title} | Luke Jordan Swiggett</title>
	<meta property="og:title" content="{title}">
	<meta property="og:type" content="article">
	<link rel="icon" href="{to_root}assets/favicon.svg" type="image/svg+xml">
	<link rel="stylesheet" href="{to_root}style.css">
	<link rel="stylesheet" href="{to_root}reviews/review.css">
</head>
<body>
	<header class="site-header">
		<div class="container nav-wrapper">
			<a class="site-title" href="{to_root}index.html">Luke Swiggett</a>
			<nav class="site-nav" aria-label="Main navigation">
				<a class="nav-hide-sm" href="{to_root}index.html#experience">Experience</a>
				<a href="{to_root}portfolio.html" aria-current="page">Projects</a>
				<a class="nav-hide-sm" href="{to_root}index.html#about">About</a>
				<a href="{to_root}index.html#contact">Contact</a>
				<a class="nav-resume" href="{to_root}assets/resume.pdf">Resume</a>
			</nav>
		</div>
	</header>

	<main class="container page-content review">
		<article>
{body}
		</article>
	</main>

	<footer class="site-footer">
		<div class="container footer-inner">
			<p>&copy; 2026 Luke Jordan Swiggett</p>
			<div class="footer-links">
				<a href="mailto:swigge_l2@denison.edu">Email</a>
				<a href="https://www.linkedin.com/in/lukeswiggett" target="_blank" rel="noopener">LinkedIn</a>
				<a href="https://github.com/lswiggett" target="_blank" rel="noopener">GitHub</a>
			</div>
		</div>
	</footer>
</body>
</html>
"""

out = review_dir / "index.html"
out.write_text(page, encoding="utf-8")
print(f"Wrote {out.relative_to(site_root)}")
