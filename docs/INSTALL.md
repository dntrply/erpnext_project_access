# Install and Uninstall

> **Status: Alpha**
>
> The commands below are for a self-managed Frappe/ERPNext Bench. Deployment
> platforms such as Frappe Cloud may expose equivalent install/uninstall actions
> through their own UI.

## 1. Before installing

Installing ERPNext Project Access is **not passive** on a site that already has
Projects and Tasks. Once the app hooks are active, non-Administrator Project and
Task access is additionally restricted to records the user owns or that have
been explicitly shared with that user.

Read [INSTALLATION_EFFECTS.md](INSTALLATION_EFFECTS.md) before installing on an
existing site. For this alpha, use a test/staging site first.

## 2. Install the tagged alpha release

For reproducible testing, install the tagged release rather than `main`.

From the Bench directory:

```bash
bench get-app --branch v0.1.0-alpha.1 \
  https://github.com/dntrply/erpnext_project_access.git
```

Then install the app on the target site:

```bash
bench --site your-site.example.com install-app erpnext_project_access
```

Run the normal site migration:

```bash
bench --site your-site.example.com migrate
```

Build the app assets if your deployment process does not already do so:

```bash
bench build --app erpnext_project_access
```

Reload/restart Frappe processes according to the deployment method used by the
site. A self-managed production Bench may use `bench restart`; containerized
installations and managed platforms use their own process/deployment mechanism.

Do not assume that one restart command applies to every deployment type.

## 3. Verify installation

Run:

```bash
bench --site your-site.example.com list-apps
```

Confirm that the output contains:

```text
erpnext_project_access
```

Then review:

- [INSTALLATION_EFFECTS.md](INSTALLATION_EFFECTS.md) — what changes immediately
  because the app is active
- [ROLE_SETUP.md](ROLE_SETUP.md) — reference System User / role setup
- [HOWTO.md](HOWTO.md) — end-to-end worker/reviewer acceptance workflow

The documentation on `main` may be newer than the `v0.1.0-alpha.1` source tag.
That is intentional: the alpha runtime code remains reproducible from the tag,
while the living documentation continues to improve on `main`.

## 4. Before uninstalling

Uninstalling also changes behavior immediately because it removes the app's
Project/Task permission hooks and Task form workflow actions from the site.

Read [UNINSTALLATION_EFFECTS.md](UNINSTALLATION_EFFECTS.md) before uninstalling,
especially on a site where users have come to rely on the app's restricted
visibility model.

Frappe's `uninstall-app` command takes a site backup by default. Do **not** use
`--no-backup` for this alpha unless you have a separate verified backup and a
specific reason to bypass the default.

## 5. Preview the uninstall

First run Frappe's dry run:

```bash
bench --site your-site.example.com uninstall-app erpnext_project_access --dry-run
```

Review the output before continuing.

The current alpha does not replace ERPNext's standard Project or Task DocTypes,
but Frappe's uninstall mechanism is generally destructive for data owned by the
app being removed. Always inspect the dry run rather than assuming an uninstall
is harmless.

## 6. Uninstall from the site

Run:

```bash
bench --site your-site.example.com uninstall-app erpnext_project_access
```

Confirm the interactive prompt when satisfied with the backup and dry-run
review.

After uninstall, verify that the app is no longer installed on the site:

```bash
bench --site your-site.example.com list-apps
```

`erpnext_project_access` should no longer appear.

If users still appear to see cached Task form buttons or stale permission
behavior, clear the site cache and reload/restart the site's Frappe processes
using the mechanism appropriate to that deployment:

```bash
bench --site your-site.example.com clear-cache
```

For a traditional self-managed production Bench, a process restart may also be
appropriate:

```bash
bench restart
```

Do not use that command blindly on containerized or managed deployments; use the
platform's normal restart/deploy mechanism instead.

## 7. Optional: remove the app source from the Bench

`uninstall-app` removes the app from a **site**. It is different from removing
the app source from the whole Bench.

Only after the app has been uninstalled from every site on that Bench, and only
if you no longer want the source present, you may use:

```bash
bench remove-app erpnext_project_access
```

Do not run `remove-app` merely to disable the app on one site when other sites on
the same Bench may still use it.

## 8. What uninstall does not reverse

Uninstall is not a historical rollback of everything users did while the app was
installed.

In particular, uninstall does not automatically restore previous Task statuses,
reopen completed assignments, delete shares created during the trial, delete
locally created roles, change Users back to Website Users, or undo Project/Task
ownership changes made by administrators.

For the detailed before/after behavior, see
[UNINSTALLATION_EFFECTS.md](UNINSTALLATION_EFFECTS.md).
