# Userguide releases

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
