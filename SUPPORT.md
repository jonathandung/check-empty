# Support Guidelines

Thank you for using check-empty! This document outlines how to get help.

Before jumping to seek support, do skim through
[the readme](https://github.com/jonathandung/check-empty#check-empty).

## Bug Reports

If you've found a bug, please:

1. Check if it's already reported in
[Issues](https://github.com/jonathandung/check-empty/issues)
2. If so, participate meaningfully there
3. Otherwise, create a new issue

## Feature Requests

Have an idea? We'd love to hear it!

- Search existing issues to avoid duplicates
- Explain the use case and expected behaviour
- Include examples

## Questions

### Community Support

- [GitHub Discussions](https://github.com/jonathandung/check-empty/discussions)
- Stack Overflow: Tag questions with `[python]` and `[check-empty]`

### Quick Questions

For quick questions, consider:

- Checking existing issues/discussions
- Reading the FAQ section below
- Asking in community channels

## Common Issues & Solutions

### Installation Problems

Update your package installer, then try the following fixes:

```bash
uv tool install -U check-empty # Upgrade
uv tool uninstall check-empty && uv tool install check-empty # Clean install
```

Other (slower) package managers:

```bash
# pip
pip install -U check-empty # Upgrade
pip uninstall check-empty && pip install check-empty # Clean install

# pipx, installed with pip
pip install -U pipx
pipx ensurepath
```

### Import Errors

Check if check-empty is installed:

```bash
pip list | grep check-empty
# or
pip show check-empty

# uv
uv tool list # if installed as a tool
uv pip show check-empty # if installed as a package
```

If the package is not working, check `sys.path` in your Python installation.

## Response Times

As fast as I can; that is:

- Bug reports: 3 days
- Feature requests: Reviewed biweekly
- Security issues: 1 day
- General questions: Community-driven

I will try to make a post on the discussions page (e.g. hiatus announcement) and set my
status to 'On vacation' or similar in case of inactivity such that I cannot fulfil
these promises or meet other deadlines I set myself.

## Remarks

Don't:

- Bump issues with +1 or "me too"
- Email maintainers unless urgent
- Ask about ETA of features/fixes
- Post API keys or passwords

Instead:

- React to issues
- Open discussions or issues, or a pull request if the problem is easily fixable
- Be patient

Once again, thank you for supporting this small project. Happy programming!
