# ERPNext Project Access

> **Status: Alpha**

ERPNext Project Access adds scoped access control and controlled Task workflow
actions to ERPNext Projects and Tasks.

The project is under active development. Its first real-world alpha deployment
has been used to validate the access-control and workflow model before a stable
release.

## Important: installation changes existing Project/Task access

Installing this app is **not passive** on a site that already contains Projects
and Tasks.

Once the app's permission hooks are active, non-Administrator access to existing
Projects and Tasks is additionally constrained to records the user **owns or has
been explicitly shared**. A user who previously relied on a broad ERPNext role
to see many Projects or Tasks may therefore see fewer records immediately after
installation, even if no role configuration is changed afterward.

The app does not automatically change ownership, create shares, change Task
statuses, create mandatory roles, or grant Desk access.

Before installing on an existing production site, read
[docs/INSTALLATION_EFFECTS.md](docs/INSTALLATION_EFFECTS.md) and evaluate the
alpha on a staging/test site with representative users.

## Install

For a self-managed Bench, the tagged alpha can be installed with:

```bash
bench get-app --branch v0.1.0-alpha.1 \
  https://github.com/dntrply/erpnext_project_access.git

bench --site your-site.example.com install-app erpnext_project_access
bench --site your-site.example.com migrate
bench build --app erpnext_project_access
```

Then reload/restart Frappe processes using the mechanism appropriate to your
deployment and verify:

```bash
bench --site your-site.example.com list-apps
```

For full installation instructions, deployment notes, verification, and the
required pre-install warning, see [docs/INSTALL.md](docs/INSTALL.md).

## Uninstall

Before uninstalling, read
[docs/UNINSTALLATION_EFFECTS.md](docs/UNINSTALLATION_EFFECTS.md). Removing the
app removes its Project/Task access fence, so users with broad native ERPNext
permissions may regain wider visibility.

Preview the uninstall first:

```bash
bench --site your-site.example.com uninstall-app erpnext_project_access --dry-run
```

Then, when ready:

```bash
bench --site your-site.example.com uninstall-app erpnext_project_access
```

Frappe's uninstall command takes a site backup by default. Do not use
`--no-backup` casually for this alpha.

Uninstall is **not** a historical rollback: Task statuses, shares, assignments,
ownership changes, locally created roles, and System User configuration made
during the trial are not automatically restored to their pre-install state.

See [docs/INSTALL.md](docs/INSTALL.md) for the complete uninstall procedure.

## Current capabilities

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

## Security model

Standard ERPNext role permissions determine what a user is generally capable
of doing.

ERPNext Project Access adds a document-level scope boundary determining which
Projects and Tasks a user may access.

Controlled workflow actions allow narrowly authorized state transitions without
granting general Write permission to the document.

The app does not require particular role names or install a mandatory Worker or
Project Creator role. Users participating in the Desk workflow must, however,
be System Users with Desk access; the app does not itself grant Desk access.

## How to use it

See [docs/HOWTO.md](docs/HOWTO.md) for the validated alpha workflow, including:

- Project and Task access rules
- Task assignment and sharing
- Worker actions: Start Work and Submit for Review
- Reviewer actions: Return for Rework and Approve & Complete
- A minimal end-to-end acceptance test
- Troubleshooting guidance

See [docs/ROLE_SETUP.md](docs/ROLE_SETUP.md) for the reference permission model,
including:

- the System User / Desk-access prerequisite
- a restricted worker persona
- a creator/reviewer reference configuration
- which permissions are app requirements versus deployment choices

See [docs/INSTALLATION_EFFECTS.md](docs/INSTALLATION_EFFECTS.md) for the exact
behavioral changes that occur simply because the app has been installed and its
hooks are active.

See [docs/UNINSTALLATION_EFFECTS.md](docs/UNINSTALLATION_EFFECTS.md) for the
behavioral changes and persistent site state to expect when the app is removed.

## Alpha compatibility

The first end-to-end alpha validation was performed with:

- Frappe Framework 16.29.0
- ERPNext 17.0.0-dev
- HRMS 17.0.0-dev
- ERPNext Project Access 0.1.0a1 / release tag v0.1.0-alpha.1

Frappe versions prior to 16.29.0 contain a linked-table permission-query issue
that can cause an otherwise readable Task to be omitted from Task List when its
linked Project is inaccessible. For this alpha, Frappe 16.29.0 or newer is
recommended unless an equivalent fix has been independently validated.

This is an unusual mixed development environment and should not be interpreted
as a general compatibility guarantee.

Additional ERPNext/Frappe versions will be documented only after testing.

## License

GPL-3.0-only
