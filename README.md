# [check-empty](https://pypi.org/p/check-empty)

A simple, dependency-free and intuitive [pre-commit](https://pre-commit.com) /
[prek](https://prek.j178.dev) hook, CLI, library,
[`uv` tool](https://docs.astral.sh/uv/guides/tools/) and
[GitHub Action](https://github.com/marketplace/actions/check-empty-files) conglomerate
written in Python that makes sure selected files, even within directories, are empty
according to as little filesystem stat calls as possible and clears them effectively
with minimal I/O if specified. Supports CPython 3.6+, PyPy 7.0+, GraalPy 19.0+
out-of-the-box, and most likely every Python 3.6 runtime you can think of.

## Quickstart

Without installation (just trying out the capabilities):

```bash
uvx check-empty -Q src/mylib/py.typed docs/.nojekyll static/.gitkeep some_directory
```

```bash
# uv
uv tool install check-empty # bare executable on PATH
uv pip install check-empty # if you want to import check_empty for programmatic usage

pip install check-empty # pip
```

Show the version with:

```bash
check-empty --version # or check-empty -v
```

All the snippets below should do the same thing.

Run the CLI:

```bash
check-empty -Q src/mylib/py.typed docs/.nojekyll static/.gitkeep some_directory
```

In Python:

```py
from check_empty import check

check(
    ['src/mylib/py.typed', 'docs/.nojekyll', 'static/.gitkeep', 'some_directory'],
    verbosity=1,  # default 2; each -Q decreases it by 1 and each -V increases it by 1
)
```

As a pre-commit hook:

```yaml
# .pre-commit-config.yaml
repos:
- repo: https://github.com/jonathandung/check-empty
  rev: v0.9.1 # repository version
  hooks:
    - id: check-empty # the hook
      args: # example list of arguments
        - -Q # flag to decrease output, applicable twice (shorthand for --quiet)
      files: # below: paths to files/directories to clear or keep empty, relative to
        # project root (absolute paths are possible but not recommended)
        - src/mylib/py.typed
        - docs/.nojekyll
        - static/.gitkeep
        - some_directory
```

equivalent in `prek.toml` format:

```toml
[[repos]]
repo = "https://github.com/jonathandung/check-empty"
rev = "v0.9.1"

[[repos.hooks]]
id = "check-empty"
args = ["-Q"]
files = ["src/mylib/py.typed", "docs/.nojekyll", "static/.gitkeep", "some_directory"]
```

or (TOML 1.1+):

```toml
[[repos]]
repo = "https://github.com/jonathandung/check-empty"
rev = "v0.9.1"
hooks = [{
  id = "check-empty",
  args = ["-Q"]
  files = ["src/mylib/py.typed", "docs/.nojekyll", "static/.gitkeep", "some_directory"]
}]
```

As a GitHub action step:

```yaml
steps:
- uses: jonathandung/check-empty@v0.9.1 # the latest version on the GitHub Actions
  # marketplace; this step will fail and subsequent jobs will not run if any file is
  # not empty
  with:
    python-version: '3.14' # run the script on the latest stable Python version
    # Python down to 3.6 is supported but not recommended due to end-of-life
    quiet: true
    filenames: |
      src/mylib/py.typed
      docs/.nojekyll
      static/.gitkeep
      some_directory
```

## Notes

1. If your file name starts with a hyphen, to avoid having it misinterpreted as a flag,
use a command of the form `check-empty -- -this_is_actually_a_file.txt`. Thus, for a
file literally named "--", you have little choice but to call the underlying library
function (`check`) directly.
2. Forward slashes can be used even on Windows, so there is no need to escape anything.
3. Glob patterns are supported on \*nix only. If on Windows, use a shell like Git Bash.
4. The program does not recurse into archives, since identification of compressed
archives would require reading the first few bytes of each file seen, which is
error-prone and inefficient.

## Development

If you wish to contribute to this project, you are more than welcome, but please
remember to read the
[contributing guide](https://github.com/jonathandung/.github/CONTRIBUTING.md). Tests
are run with:

```bash
python -m test_check_empty # explicit
python -m unittest discover # alternative
```

at the project root.
