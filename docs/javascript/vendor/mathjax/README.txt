VENDORED MATHJAX
================

tex-svg-full.js is MathJax 3.2.2 (https://www.mathjax.org/), copied
verbatim from tools/mathjax/node_modules/mathjax-full/es5/. Apache-2.0,
licence text alongside it in LICENSE.

Plain text rather than Markdown on purpose: everything under docs/ is a
documentation source, so a README.md here is built into a real page on the
published site and indexed by its search. This is a note to whoever is
maintaining the file, not a page for readers.

Why vendored rather than a CDN

The website previously fetched MathJax from unpkg on every page carrying a
formula - and not once but five times, because the CommonHTML output
processor then fetched its .woff fonts at runtime too. Vendoring keeps the
site self-contained: no external request, no dependency on someone else's
uptime or retention policy, no third-party request from a reader's browser,
and the site works offline or from a network that blocks the CDN.

It also closes a version gap. The CDN URL was "mathjax@3", which floats,
while tools/mathjax pins mathjax-full to 3.2.2 exactly - and that pinned
copy is what prodockit pdf renders the PDF through. The two agreed only by
coincidence. Copying from the pinned install rather than downloading
separately is what makes them provably the same build.

Why this particular bundle

- tex-... rather than tex-mml-...: pymdownx.arithmatex emits TeX,
  never MathML, so the MathML input processor would be dead weight.
- ...-svg... rather than -chtml: the SVG output processor carries its
  glyphs as paths inside the bundle. The CommonHTML one fetches its fonts
  from a sibling directory at runtime, which would mean vendoring those
  too and would reintroduce the very runtime fetches vendoring removes.
  SVG also matches what the PDF gets, since prodockit pdf pre-renders
  through the same MathJax to SVG.
- ...-full rather than the plain build: it bundles every TeX extension.
  The plain build loads an extension on demand from a sibling path the
  moment a formula uses one, which would fail here with nothing but a
  console error and an unrendered formula.

Replacing it

Bump mathjax-full in tools/mathjax/package.json, reinstall, then copy the
file across again:

    npm install --prefix tools/mathjax
    cp tools/mathjax/node_modules/mathjax-full/es5/tex-svg-full.js \
       docs/javascript/vendor/mathjax/tex-svg-full.js

Keep the two in step. The PDF renders through tools/mathjax and the website
through this copy, so a mismatch means a formula can typeset one way in
print and another on screen - the reason this is copied from the pinned
install rather than downloaded separately.
