# Install, Activate, Disable and Uninstall

> **Status: alpha.2 development**
>
> These commands are for a self-managed Frappe/ERPNext Bench. Managed platforms
> such as Frappe Cloud may expose equivalent actions through their own UI.

## 1. Fresh alpha.2 installation is passive

A fresh alpha.2 installation is **disabled by default**. Installing the app does
not by itself apply the Project/Task owner-share fence or controlled Task
workflow.

The policy changes only after a System Manager explicitly enables:

**ERPNext Project Access Settings → Enable ERPNext Project Access**

Read [ACTIVATION.md](ACTIVATION.md) and
[INSTALLATION_EFFECTS.md](INSTALLATION_EFFECTS.md) before enabling on a site with
existing Projects and Tasks.

## 2. Install for alpha.2 development testing

The alpha.2 activation switch is not yet a tagged release. Until validation is
complete, test the development branch rather than treating it as a public
release:

```bash
cd /path/to/frappe-bench
bench get-app --branch alpha2-config-switch \
  https://github.com/dntrply/erpnext_project_access.git
```

Install it on the target site:

```bash
bench --site your-site.example.com install-app erpnext_project_access
```

Then migrate:

```bash
bench --site your-site.example.com migrate
```

Build assets if your deployment process does not already do so:

```bash
bench build --app erpnext_project_access
```

Reload/restart processes according to the deployment method. A self-managed
production Bench may use `bench restart`; containerized and managed deployments
have their own deployment/restart mechanism.

## 3. Verify that the app is installed but disabled

Confirm installation:

```bash
bench --site your-site.example.com list-apps
```

The output should include:

```text
erpnext_project_access
```

Before enabling, log in as representative non-Administrator users and verify
that Project and Task behavior still matches native ERPNext/Frappe behavior.

A System Manager can then open **ERPNext Project Access Settings** and confirm
that **Enable ERPNext Project Access** is unchecked.

## 4. Configure users and roles

The app does not install mandatory Worker or Creator roles.

Before activation, configure or reuse the roles appropriate to your site. For a
reproducible reference setup, see [ROLE_SETUP.md](ROLE_SETUP.md).

At minimum, participants in the Desk workflow must be System Users with Desk
access. The restricted worker does not need general Task Write permission merely
to use the controlled workflow.

## 5. Enable the policy

As a **System Manager**:

1. Search Desk for **ERPNext Project Access Settings**.
2. Open the settings document.
3. Review the warning.
4. Check **Enable ERPNext Project Access**.
5. Save.
6. Refresh any already-open Project/Task forms.

Then run the acceptance workflow in [HOWTO.md](HOWTO.md).

No process restart is required merely to toggle the setting; subsequent requests
read the new setting.

## 6. Disable without uninstalling

Disabling is the preferred first rollback step.

As a System Manager:

1. Open **ERPNext Project Access Settings**.
2. Uncheck **Enable ERPNext Project Access**.
3. Save.
4. Refresh existing Project/Task forms.
5. Re-test representative users.

Once disabled, this app no longer narrows Project/Task access and no longer
offers the controlled Task actions. Native ERPNext/Frappe permissions and any
other installed customizations remain in force.

Disabling does not undo Task statuses, ownership, assignments, shares or local
role configuration that changed while the app was enabled.

## 7. Upgrading an existing alpha.1 installation

`v0.1.0-alpha.1` was active immediately after installation. To avoid an upgrade
unexpectedly broadening access, an existing alpha.1 site remains **enabled** when
upgraded to alpha.2 through `bench migrate`.

For development testing from an existing checkout:

```bash
cd /path/to/frappe-bench/apps/erpnext_project_access
git fetch origin
git switch alpha2-config-switch
git pull --ff-only
```

Then from the Bench directory:

```bash
bench --site your-site.example.com migrate
bench build --app erpnext_project_access
```

Restart/redeploy only as required by your deployment method.

After migration, confirm **ERPNext Project Access Settings** is enabled and
verify that the previously validated restricted-access behavior still holds.

The migration patch intentionally preserves alpha.1 behavior. Do not assume an
upgrade will disable the app automatically.

## 8. Before uninstalling

Prefer this sequence:

```text
Disable
  ↓
verify native ERPNext access
  ↓
uninstall only if the app is no longer wanted
```

Read [UNINSTALLATION_EFFECTS.md](UNINSTALLATION_EFFECTS.md), especially if users
have relied on the restricted visibility model.

Frappe's `uninstall-app` takes a site backup by default. Do not use
`--no-backup` for this alpha unless you have a separately verified backup and a
specific reason to bypass the default.

## 9. Preview uninstall

Run Frappe's dry run first:

```bash
bench --site your-site.example.com uninstall-app erpnext_project_access --dry-run
```

Review the output before proceeding.

The app hooks into ERPNext's standard Project and Task DocTypes rather than
replacing them, but Frappe uninstall is generally destructive for app-owned
metadata/data. The dry run should still be reviewed.

## 10. Uninstall from the site

Run:

```bash
bench --site your-site.example.com uninstall-app erpnext_project_access
```

Confirm the prompt after reviewing the backup/dry run.

Then verify:

```bash
bench --site your-site.example.com list-apps
```

`erpnext_project_access` should no longer appear for that site.

Clear cache if needed:

```bash
bench --site your-site.example.com clear-cache
```

Reload/restart processes according to your deployment method so hooks/assets are
fully refreshed.

## 11. Removing app source from the Bench

Uninstalling from a site and removing source code from the Bench are separate
operations. If no site on the Bench uses the app and you intentionally want to
remove its source, use the Bench/app-management procedure appropriate to your
deployment only after confirming it is uninstalled from every relevant site.

Do not remove the source checkout first and then attempt a site uninstall.

## 12. What persists after disable/uninstall

Neither disabling nor uninstalling should be treated as a time-machine rollback.
Ordinary site state may remain, including:

- explicit Project/Task shares,
- locally created reference roles,
- user role assignments and System User status,
- Project/Task ownership changes,
- Task statuses reached while the app was enabled,
- assignment/ToDo lifecycle changes already performed by ERPNext.

See [UNINSTALLATION_EFFECTS.md](UNINSTALLATION_EFFECTS.md) for details.
