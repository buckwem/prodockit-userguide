# Userguide releases

## 1.18.21 (2026-09-24)

- Cascade Prodockit 0.73.0 and qualified Zensical 0.0.64 for website and PDF builds.
- Refresh Surrey's pinned Getting started pages to the 0.73.0 release, including the academic-year GitLab path guidance.
- Add theme-aware stag icons across the guide and its Surrey RemoteLabs tabs.

## 1.18.20 (2026-09-23)

- Place About before Getting started in Surrey's top menu while preserving the imported manual's section numbering.

## 1.18.19 (2026-09-23)

- Cascade Prodockit 0.72.0 with Zensical 0.0.63, WeasyPrint 70.0 and PyMdown Extensions 12.0.1.
- Move PDF renderer preparation to the project-local cache and remove Chrome and npm from publishing builds.
- Use the managed MathJax website configuration and refresh build guidance and renderer checks.
- Refresh Surrey's pinned installation manual to the Prodockit 0.72.0 release.

## 1.18.18 (2026-09-13)

- Replace the four duplicated installation chapters with a concise Getting
  started page that directs readers to the prodockit reference manual.
- Renumber navigation and update cross-links, guide descriptions, and PDF index
  checks for the shorter authoring-focused guide.

## 1.18.17 (2026-09-13)

- Install the required PDF fonts and font verification tools in both publishing
  workflows, preventing missing-font diagnostics failures on fresh runners.
- Align build and test requirements with Prodockit 0.65.3 and Zensical 0.0.61.
- Cascade managed renderer dependencies, including the patched MathJax XML
  dependency and browser-based website checks before PDF generation.
- Regenerate MathJax website assets during builds to include the
  instant-navigation fix. PDF table headers now match website defaults and
  respect explicit alignment.

## 1.18.16 (2026-09-09)

- Raise the Prodockit build and testing floor to 0.63.0, including installer
  recovery, font verification and fresh-site configuration fixes.
- Explain editor-free repository configuration and how to respond to
  unverified fonts or interrupted installers. Preserve shared assets and
  explicitly selected Mermaid and maths components.
- Apply Adopt's baseline ignore rules for local environments and generated files.

## 1.18.15 (2026-09-09)

- Raise the Prodockit build and testing floor to 0.62.0 and align the supported
  toolchain, renderer manifests/lockfiles and missing configuration defaults
  through Adopt.
- Preserve existing stylesheet and JavaScript ordering, author customisations
  and explicitly selected Mermaid/MathJax components.
- Update adoption guidance for automatic runtime provisioning, software
  alignment, the settings-review ledger, renderer backups and environment refresh.

Earlier release history is recorded in GitHub Releases.
