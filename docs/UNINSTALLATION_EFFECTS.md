# Disable and Uninstall Effects

> **Status: `v0.1.0-alpha.2` prerelease**
>
> Alpha.2 separates **disabling the policy** from **uninstalling the app**.
> Administrators should normally disable first, verify native ERPNext behavior,
> and uninstall only if the app is no longer wanted.

## 1. Disabling removes the additional access fence

While ERPNext Project Access is enabled, a non-Administrator user's access to an
existing Project or Task is additionally constrained by the app's
owner-or-explicit-share checks.

After a System Manager disables the app in **ERPNext Project Access Settings**,
that additional fence is no longer applied by this app.

Project and Task access then falls back to the site's normal Frappe/ERPNext
permission model, including roles, User Permissions, shares, ownership rules and
other installed-app customizations that remain active.

## 2. Some users may immediately see more Projects or Tasks

This is the most important disable/uninstall effect.

While enabled:

```text
normal ERPNext permission
        +
owner / explicit-share fence
        ↓
restricted Project/Task scope
```

After disabling or uninstalling:

```text
normal ERPNext/Frappe permission model
        ↓
whatever scope that model allows
```

A user with a broad normal ERPNext role may therefore regain access to records
they could not see while ERPNext Project Access was enabled.

This is why disabling should be tested with representative users before an
uninstall on an existing site.

## 3. Controlled Task actions disappear when disabled

The app's controlled actions are available only while the feature is enabled:

```text
Open → Working
Working → Pending Review
Pending Review → Working
Pending Review → Completed
```

After disabling, those actions are no longer returned to the Task form and
direct calls to the app's controlled mutation endpoints are rejected.

Users then interact with Task status according to native ERPNext behavior,
permissions, workflows and any other installed customizations.

## 4. Uninstall removes the settings and hooks entirely

Uninstalling the app removes its app-owned metadata, including the
**ERPNext Project Access Settings** DocType, and removes the app's Project/Task
permission hooks and Task form code once hooks/assets are reloaded.

If the app was already disabled, the main Project/Task access behavior should
already have returned to native ERPNext before uninstall. This makes disabling a
useful safety check before removal.

Always run Frappe's uninstall dry run and review the backup before proceeding.

## 5. Explicit shares are not app-owned policy data

Project and Task `DocShare` records created before or during the trial are normal
Frappe records. The app consults them; it does not own them merely because they
were used by its ACL.

Disabling does not remove them. Uninstalling is not intended to remove them.

If you created temporary shares solely for an evaluation, review and remove them
separately if you want to return the site to its previous sharing configuration.

## 6. Local roles and System User configuration remain

The app does not install mandatory roles such as `Project Access Creator` or
`Project Access Desk User`.

Roles created while following the reference setup are deployment configuration.
Disabling or uninstalling the app does not intentionally:

- delete those local roles,
- remove them from users,
- change System Users back to Website Users,
- remove Desk access granted by those roles,
- restore previous role configuration automatically.

Review local trial roles separately if they are no longer wanted.

## 7. Existing Task statuses do not roll back

Disable/uninstall does not reverse business actions already completed while the
app was enabled.

For example:

- a Task already moved to `Pending Review` remains in that status,
- a Task completed through **Approve & Complete** remains `Completed`,
- progress already set to `100%` remains,
- assignments/ToDos already closed by ERPNext's normal completion lifecycle are
  not automatically reopened.

## 8. Project and Task records remain ERPNext records

ERPNext Project Access hooks into ERPNext's existing standard `Project` and
`Task` DocTypes. It does not replace those DocTypes with app-owned versions.

Uninstall should therefore not be interpreted as deleting Projects or Tasks
merely because they were created while the app was installed.

Frappe's uninstall process is nevertheless destructive for metadata/data owned
by the app being removed, so always review:

```bash
bench --site your-site.example.com uninstall-app erpnext_project_access --dry-run
```

before uninstalling.

## 9. Ownership and ordinary field changes remain

If an administrator changed the owner of a Project or Task while the app was in
use, that is persistent ERPNext document state.

Disable/uninstall does not restore an earlier owner automatically. The same
principle applies to ordinary Project/Task field changes made during the trial.

## 10. Assignment and ToDo records remain subject to normal ERPNext behavior

The controlled worker authorization checks an active Task assignment represented
by an Open `ToDo`, but assignment itself is normal Frappe/ERPNext data.

Disabling or uninstalling the app does not, by itself, unassign every Task or
delete remaining ToDos. Existing assignments continue under native
ERPNext/Frappe behavior.

## 11. Cached UI behavior

After changing the enable setting, refresh already-open Project/Task forms.

After uninstall, clear site cache and reload/restart the relevant processes as
required by the deployment method so that old hooks/assets are not retained by
long-running workers or browsers.

## 12. Preferred rollback sequence

For an existing site:

```text
1. Take/verify a backup
2. Disable ERPNext Project Access
3. Refresh/re-login representative users
4. Verify native Project/Task visibility and permissions
5. Review temporary shares/roles if desired
6. Run uninstall-app --dry-run
7. Uninstall only if the app is no longer wanted
8. Clear cache / reload deployment processes as appropriate
9. Re-test representative users
```

This sequence separates **policy rollback** from **software removal**, making
access changes easier to reason about and verify.
