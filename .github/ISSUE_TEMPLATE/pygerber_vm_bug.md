---
name: PyGerber Virtual Machine Bug Report
about:
  Report a bug somewhere in PyGerber. If possible, please use more specific templates.
title: "[PyGerber]: <when-i-am-doing-something-then-something-fails>"
labels: ["virtual-machine", "bug", "waiting-for-checkboxes"]
projects: ["argmaster/3"]
assignees: "Argmaster"
---

# PyGerber Virtual Machine Bug

This virtual machine bug applies to following virtual machine implementations (select
all that apply):

- [ ] `pygerber.vm`
- [ ] `pygerber.vm.pillow`
- [ ] `pygerber.vm.shapely`

## Mandatory checks

> Checks listed below are mandatory for opening a new issue.

> If haven't done any of the checks listed below, please do that, we will not look into
> the issue until all of the checks in mandatory checks section are checked.

### Before opening this issue:

- [ ] I have reviewed the README for guidelines and haven't found a solution there.
- [ ] I have reviewed the PyGerber documentation and haven't found a solution there.
- [ ] I have reviewed the existing open issues and verified that this is not a
      duplicate.
- [ ] I have reviewed the existing closed issues and verified that this was already
      resolved or marked as won't fix.
- [ ] I have reviewed the existing pull requests and verified that this is not a already
      known issue.
- [ ] I have reviewed the existing discussions and verified that this is not a already
      known issue.

> If you have found a issue / discussion / pull request describing similar but not quite
> matching issue, You can still open new issue, we will review it and decide if we want
> to merge them. If you can, please reference this issue here:

## To Reproduce

> Please provide a clear list of steps to reproduce the behavior.

> You can include code snippets or screenshots for individual steps to make it easier to
> reproduce.

1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

## Expected behavior

> A clear and concise description of what you expected to happen. If this issue is
> related to image rendering, please post a screenshot from
> [Reference Gerber Viewer](https://gerber-viewer.ucamco.com/) or CAD software used. If
> the design is confidential, follow guidelines regarding confidential files available
> in `Additional context` section below.

## Additional context

> If applicable, add screenshots, code examples, or any other resources that can speed
> up process of reproducing and fixing the issue.

> If your issue was discovered with use of specific source file (e.g. in Gerber format),
> please attach it to the issue. If file is confidential, please create minimal subset
> of the file which can be shared in public and allows to reproduce the issue.

> If you are not able to create minimal reproduction for confidential source, you can
> email me the confidential file at `argmaster.world@gmail.com` with the issue title in
> the subject. I will not share the file anywhere in public and will delete it after the
> issue is resolved. We can discuss NDA agreements via email if needed.

> You still should create a public issue based on this template for the issue to be
> investigated, please use `<confidential-file>`, `<confidential-image>`, etc. as a
> placeholders for the confidential files.

## Environment:

**Please complete the following information:**

- Operating system: [e.g. `Ubuntu 24.04`]
- Python version: [e.g. `3.9.0`]
- PyGerber version: [e.g. `3.0.0`]

## Optional checks

> Agreements listed below are optional, but consider checking them if it is not harmful
> for you to do so. You can greatly improve PyGerber doing so.

- [ ] I want to contribute example source files attached to this issue in the test suite
      of PyGerber for regression testing purposes.
- [ ] I want to include separate LICENSE file for resource files attached as a result of
      an agreement described in first checkbox in this section.
- [ ] I want to include separate README file for resource files attached as a result of
      an agreement described in first checkbox in this section.
