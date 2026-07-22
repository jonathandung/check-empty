# check-empty

A simple, dependency-free and intuitive [pre-commit](https://pre-commit.com) /
[prek](https://prek.j178.dev) hook, CLI, library and GitHub Action conglomerate that
makes sure selected files are empty according to a filesystem stat call and clears them
effectively with minimal I/O if required, written in Python. Also available as a tool on
uv. Supports CPython 3.6+, PyPy 7.0+, GraalPy 19.0+ and most likely every Python 3.6
runtime you can think of.

## Quickstart

Without installation (testing out the capabilities):

```bash
uvx check-empty -Q src/mylib/py.typed docs/.nojekyll static/.gitkeep some_directory
```

```bash
# uv
uv tool install check-empty # bare executable on PATH
uv pip install check-empty # if you want the library as well

pip install check-empty # pip
```

Check the version with:

```bash
check-empty --version # or check-empty -v
```

Run the CLI:

```bash
check-empty -Q src/mylib/py.typed docs/.nojekyll static/.gitkeep some_directory
```

As a pre-commit hook:

```yaml
# .pre-commit-config.yaml
repos:
- repo: https://github.com/jonathandung/check-empty
  rev: v0.6.0 # repository version
  hooks:
    - id: check-empty # the hook
      args: # example list of arguments
        - -Q # flag to silence output (shorthand for --quiet)
        # below: paths to files/directories to clear or keep empty, relative to project
        # root (absolute paths are possible but not recommended)
        - src/mylib/py.typed
        - docs/.nojekyll
        - static/.gitkeep
        - some_directory
```

equivalent in `prek.toml` format:

```toml
[[repos]]
repo = "https://github.com/jonathandung/check-empty"
rev = "v0.6.0"

[[repos.hooks]]
id = "check-empty"
args = [
  "-Q",
  "src/mylib/py.typed",
  "docs/.nojekyll",
  "static/.gitkeep",
  "some_directory"
]
```

or a more terse format (TOML 1.1+):

```toml
[[repos]]
repo = "https://github.com/jonathandung/check-empty"
rev = "v0.6.0"
hooks = [{
  id = "check-empty",
  args = [
    "-Q", "src/mylib/py.typed", "docs/.nojekyll", "static/.gitkeep", "some_directory"
  ]
}]
```

As a GitHub action step:

```yaml
steps:
- uses: jonathandung/check-empty@v0.6.0 # the latest version on the GitHub Actions
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

## Development

If you wish to contribute to this project, you are more than welcome, but please
remember to read the [contributing guide](CONTRIBUTING.md).
