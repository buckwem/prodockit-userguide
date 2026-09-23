# Surrey Getting started source snapshot

This directory contains the Getting started Markdown pages and their referenced
diagrams from `buckwem/prodockit-extensions` 0.72.0 at the commit recorded in
`manifest.toml`. The source is MIT-licensed; see `LICENSE.md`. These files are
kept outside `docs/` so the public GitHub User Guide still publishes its short
`docs/gettingstarted.md` summary.

The Surrey build preparation copies these files into an ephemeral checkout,
replaces the single Getting started nav entry, and resolves links from the
imported pages to reference-manual pages outside this section. Surrey-specific
wording is authored in the Extensions manual using its `is_surrey` macro; keep
this snapshot byte-identical to that release. The Surrey preparation omits the
overview's final “Support prodockit” / “Buy
me a coffee” subsection without changing this pinned source file.

To refresh, review the upstream `zensical.toml` Getting started nav at a
specific release commit, update this snapshot and `manifest.toml` together,
then run the source verification and both GitHub and Surrey build tests. For
the current snapshot, an Extensions checkout can be checked without network
access using:

```sh
python tools/surrey_getting_started.py verify-upstream \
  --extensions-checkout /path/to/prodockit-extensions
```

Run `python tools/surrey_getting_started.py verify` in CI to check that the
declared files are present. The GitLab pipeline then runs `prepare` on its
ephemeral checkout. For local comparison, create a **disposable worktree**
from the User Guide branch and run `prepare --preview` there before
`zensical serve`. The command intentionally replaces that worktree's
`docs/gettingstarted.md` and `zensical.toml`; never run it in a checkout
containing work you need to preserve. The ordinary GitHub preview should run
from an unprepared checkout.
