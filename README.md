# ERPNext Project Access

> **Status: Alpha — current prerelease: `v0.1.0-alpha.2`**

ERPNext Project Access adds scoped access control and controlled Task workflow
actions to ERPNext Projects and Tasks.

The project is under active development. `v0.1.0-alpha.2` adds an explicit
administrator activation switch so a fresh installation is passive until a
System Manager enables it.

## Safe-by-default activation

A **fresh alpha.2 installation is disabled by default**.

Installing the app makes the capability available, but does not by itself change
Project/Task access. A System Manager must explicitly enable:

**ERPNext Project Access Settings → Enable ERPNext Project Access**

Only then does the app's owner/share access fence and controlled Task workflow
become active.

An existing `v0.1.0-alpha.1` installation that upgrades through `bench migrate`
is kept enabled by a migration patch so that an upgrade does not unexpectedly
remove an existing access-control fence.

See [docs/ACTIVATION.md](docs/ACTIVATION.md) for the full enabled/disabled model.

## Current capabilities

When enabled:

- Project visibility restricted to owners and explicitly shared users
- Task visibility restricted to owners and explicitly shared users
- ERPNext assignment-based Task visibility preserved
- Assignment does not grant general Task Write access
- Controlled assignee workflow:
  - Open → Working
  - Working → Pending Review
- Controlled reviewer workflow:
  - Pending Review → Working
  - Pending Review → Completed
- Normal ERPNext Task validation and completion lifecycle are preserved

When disabled, the app's Project/Task permission hooks are neutral and the
controlled Task actions are unavailable.

## Security model

Standard ERPNext role permissions determine what a user is generally capable of
doing.

When enabled, ERPNext Project Access adds a document-level scope boundary
determining which Projects and Tasks a user may access.

Controlled workflow actions allow narrowly authorized state transitions without
granting general Write permission to the document.

The app does not require particular role names or install a mandatory Worker or
Project Creator role. Users participating in the Desk workflow must, however,
be System Users with Desk access; the app does not itself grant Desk access.

## Install, configure, test, uninstall

See [docs/INSTALL.md](docs/INSTALL.md) for installation, activation, disabling
and uninstall instructions.

Before enabling on a site with existing Projects/Tasks, read
[docs/INSTALLATION_EFFECTS.md](docs/INSTALLATION_EFFECTS.md).

See [docs/ROLE_SETUP.md](docs/ROLE_SETUP.md) for the reference permission model,
including:

- the System User / Desk-access prerequisite
- a restricted worker persona
- a creator/reviewer reference configuration
- reproducible Role Permission Manager settings

See [docs/HOWTO.md](docs/HOWTO.md) for the validated worker/reviewer workflow and
acceptance test.

See [docs/UNINSTALLATION_EFFECTS.md](docs/UNINSTALLATION_EFFECTS.md) for what
persists and what access may change when the app is disabled or removed.

## Alpha compatibility

### Clean stable-v16 smoke test

A clean installation/activation smoke test passes against the official ERPNext
v16 container with:

- Frappe Framework 16.33.0
- ERPNext 16.34.1
- MariaDB 11.8
- Redis 8
- ERPNext Project Access 0.1.0a2

That automated smoke test creates a fresh ERPNext site, installs this app,
confirms that a fresh installation starts disabled, verifies that the Project
and Task query hooks are neutral while disabled, enables the app, and verifies
that the enabled query conditions contain the explicit-share fence.

This smoke test is **not** a full worker/reviewer workflow certification for
stable ERPNext v16.

### End-to-end reference workflow

The complete worker/reviewer workflow has also been exercised end-to-end on the
JSS reference deployment with:

- Frappe Framework 16.29.0
- ERPNext 17.0.0-dev
- HRMS 17.0.0-dev
- ERPNext Project Access 0.1.0a2 / release tag `v0.1.0-alpha.2`

That reference deployment validated restricted Task access with a private parent
Project, disable/re-enable behavior, and the complete workflow:

```text
Open → Working → Pending Review → Working → Pending Review → Completed
```

The JSS environment is an intentionally mixed development stack and should not
be interpreted as a broad compatibility guarantee.

Frappe versions prior to 16.29.0 contain a linked-table permission-query issue
that can cause an otherwise readable Task to be omitted from Task List when its
linked Project is inaccessible. For this alpha, Frappe 16.29.0 or newer is
recommended unless an equivalent fix has been independently validated.

Additional ERPNext/Frappe versions will be documented only after testing.

## Release

The current prerelease is
[`v0.1.0-alpha.2`](https://github.com/dntrply/erpnext_project_access/releases/tag/v0.1.0-alpha.2).

Alpha-quality software: APIs, configuration, permissions behavior and workflow
behavior may still change before a stable release.

## License

GPL-3.0-only
