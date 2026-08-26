# [check-empty](https://pypi.org/p/check-empty)

A simple, dependency-free [pre-commit](https://pre-commit.com) /
[prek](https://prek.j178.dev) hook, CLI, library and
[GitHub Action](https://github.com/marketplace/actions/check-empty-files) conglomerate
written in Python.

Makes sure selected files, even within directories, are empty according to as little
filesystem stat calls as possible, and clears them effectively with minimal I/O if
specified.

## Prerequisites

Supports CPython 3.6+, PyPy 7.0+, GraalPy 19.0+ out-of-the-box, and most likely every
Python 3.6 runtime you can think of. This is the only requirement to use this tool.

## Quickstart

If using double-asterisk globbing in the CLI, make sure it is enabled:

```bash
shopt -s globstar
```

similarly for extglob:

```bash
shopt -s extglob
```

Without installation (just trying out the capabilities):

```bash
uvx check-empty -Q src/mylib/py.typed docs/.nojekyll static/.gitkeep some_dir **/*.lock
```

### Installation

```bash
# uv
uv tool install check-empty # bare executable on PATH
uv pip install check-empty # if you want to import check_empty for programmatic usage

pip install check-empty # pip
```

Show the help with:

```bash
check-empty --help # or check-empty -?
```

## Usage

All the snippets below are equivalent, assuming globstar is on.

Run the CLI:

```bash
check-empty -Q src/mylib/py.typed docs/.nojekyll static/.gitkeep some_dir **/*.lock
```

In Python:

```py
from check_empty import check
import glob

a = ['src/mylib/py.typed', 'docs/.nojekyll', 'static/.gitkeep', 'some_dir']
a.extend(glob.iglob('**/*.lock', recursive=True))
# build a list of paths to files or directories by manual globbing
check(a, verbosity=1)
# default verbosity is 2; in the command line, each -Q decreases it by 1 and
# each -V increases it by 1
```

As a pre-commit hook:

```yaml
# .pre-commit-config.yaml
repos:
- repo: https://github.com/jonathandung/check-empty
  rev: v1.1.1 # repository version
  hooks:
    - id: check-empty # the hook
      args: # example list of arguments
        - -Q # flag to decrease output, applicable twice (shorthand for --quiet)
      files: ^src/mylib/py\.typed|docs/\.nojekyll|static/\.gitkeep|some_dir/.*|.*\.lock$
      # paths to files/directories to clear or keep empty as a single regular
      # expression (as per the somewhat restrictive pre-commit config schema),
      # relative to project root
```

equivalent in `prek.toml` format:

```toml
[[repos]]
repo = "https://github.com/jonathandung/check-empty"
rev = "v1.1.1"

[[repos.hooks]]
id = "check-empty"
args = ["-Q"]

[[repos.hooks.files]]
glob = [ # globset reference: https://docs.rs/globset/latest/globset/#syntax
  # this form is only supported by prek; see
  # https://prek.j178.dev/reference/configuration/?h=globs#files
  "src/mylib/py.typed",
  "docs/.nojekyll",
  "static/.gitkeep",
  "some_dir/**", # since directories cannot be passed directly, glob the files within
  "**/*.lock"
]
```

or (TOML 1.1+):

```toml
# using multiline inline tables
[[repos]]
repo = "https://github.com/jonathandung/check-empty"
rev = "v1.1.1"
hooks = [{
  id = "check-empty",
  args = ["-Q"],
  files = {
    glob = [
      "src/mylib/py.typed",
      "docs/.nojekyll",
      "static/.gitkeep",
      "some_dir/**",
      "**/*.lock"
    ]
  },
}]
```

As a GitHub Actions workflow step:

```yaml
steps:
- uses: jonathandung/check-empty@v1.1.1 # the latest version on the GitHub Actions
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
      some_dir
    globs: '**/*.lock'
    # can also be an array of globs joined into a newline-delimited multiline string,
    # as in filenames
```

[Accepted action inputs and descriptions thereof](https://github.com/jonathandung/check-empty/blob/main/action.yaml)

## Notes

1. If your file name starts with a hyphen, to avoid having it misinterpreted as a flag,
use a command of the form `check-empty -- -this_is_actually_a_file.txt`.
2. Forward slashes can be used even on Windows, so there is no need to escape anything.
3. Glob patterns are supported on \*nix only. If on Windows, use a shell like Git Bash.
4. To pass an
[argfile](https://docs.python.org/3/library/argparse.html#fromfile-prefix-chars), use
the `@` prefix, and escape files whose names actually start with `@` using the
double-hyphen syntax.
5. It may be unintuitive that a directory being "empty" means all its files are empty,
but this project explicitly targets files, since version control systems track files
rather than directories.
6. The program does not recurse into archives, since identification of compressed
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
