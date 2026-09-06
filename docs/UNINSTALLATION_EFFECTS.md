# What Changes Immediately After Uninstall

> **Status: Alpha**
>
> Uninstalling ERPNext Project Access removes the app's Project/Task permission
> hooks and controlled Task form actions from the site. This can broaden access
> again for users whose normal ERPNext roles permit wider Project/Task access.
>
> Review this document before uninstalling from a production site.

## 1. The additional Project/Task access fence goes away

While ERPNext Project Access is installed, a non-Administrator user's access to
an existing Project or Task is additionally constrained by the app's
owner-or-explicit-share checks.

After uninstall, that additional app-level fence no longer applies once Frappe
has reloaded its hooks and caches.

Project and Task access then falls back to the site's normal Frappe/ERPNext
permission model, including any roles, User Permissions, shares, ownership rules,
and other installed-app customizations that remain active.

## 2. Some users may immediately see more Projects or Tasks

This is the most important uninstall effect.

Imagine a manager with a broad normal ERPNext role.

While the app is installed:

```text
normal role permission
        +
owner / explicit-share fence
        ↓
restricted Project/Task scope
```

After uninstall:

```text
normal ERPNext permission model
        ↓
whatever scope that model allows
```

If that user's role would normally allow broad Project or Task visibility, they
may regain access to records they could not see while ERPNext Project Access was
installed.

Therefore, uninstall should not be treated merely as removing some workflow
buttons. It can materially change document visibility.

## 3. Explicit shares are not automatically removed

Project and Task `DocShare` records created before or during the app trial are
normal Frappe records. The app does not own those records merely because its ACL
consulted them.

Uninstalling the app does not intentionally delete those shares.

After uninstall, those shares may continue to affect access under Frappe's normal
sharing rules.

If you created temporary shares solely for an evaluation, review them separately
if you want to return the site to its previous sharing configuration.

## 4. Local roles and System User configuration remain

The app does not install mandatory roles such as `Project Access Creator` or
`Project Access Desk User`.

If you created those roles (or equivalent local roles) while following the
reference setup, they are deployment configuration rather than app-owned runtime
objects.

Uninstalling ERPNext Project Access does not intentionally:

- delete those local roles,
- remove them from users,
- change System Users back to Website Users,
- remove Desk access granted by those roles,
- restore any previous role configuration automatically.

Review or remove local trial roles separately if they are no longer wanted.

## 5. Controlled Task actions disappear

The app adds controlled Task actions for:

```text
Open → Working
Working → Pending Review
Pending Review → Working
Pending Review → Completed
```

After uninstall and hook/asset reload, those custom actions are no longer
provided by ERPNext Project Access.

Users then interact with Task status according to the native ERPNext UI,
permissions, workflows, and any other installed customizations.

## 6. Existing Task statuses do not roll back

Uninstall does not reverse business actions already completed while the app was
installed.

For example, if a worker used **Submit for Review** and the Task is now
`Pending Review`, uninstall does not restore the prior `Working` status.

If a reviewer used **Approve & Complete** and the Task became `Completed` with
progress `100%`, uninstall does not automatically reopen it.

Likewise, assignments or ToDos that ERPNext closed as part of its normal Task
completion lifecycle are not automatically reopened merely because the app is
removed.

## 7. Project and Task records remain ERPNext records

The current alpha hooks into ERPNext's existing standard `Project` and `Task`
DocTypes; it does not replace them with app-owned Project/Task DocTypes.

Uninstalling ERPNext Project Access therefore should not be interpreted as
"delete all Projects and Tasks created while the app was installed."

However, Frappe's `uninstall-app` command is generally a destructive app-removal
operation for app-owned metadata/data. Always run:

```bash
bench --site your-site.example.com uninstall-app erpnext_project_access --dry-run
```

and review the output before proceeding.

## 8. Ownership changes remain

If an administrator changed the `owner` of a Project or Task during the trial,
that is persistent document state.

Uninstall does not restore an earlier owner automatically.

The same principle applies to other ordinary Project/Task field changes made
while the app was installed.

## 9. Assignment and ToDo records remain subject to normal ERPNext behavior

The app's worker authorization checks an active Task assignment represented by an
Open `ToDo`, but assignment itself is normal Frappe/ERPNext data.

Uninstalling the app does not, by itself, unassign users from every Task or
delete their remaining ToDos.

Existing assignments continue to be handled by the site's normal ERPNext/Frappe
behavior after uninstall.

## 10. Cached UI or permission behavior may persist briefly

Because Frappe caches hooks, permissions, and assets, a browser or long-running
process may temporarily retain stale behavior after uninstall.

After uninstall, verify the app is gone with:

```bash
bench --site your-site.example.com list-apps
```

Then clear site cache if necessary:

```bash
bench --site your-site.example.com clear-cache
```

Reload/restart the site's Frappe processes using the mechanism appropriate to
your deployment. Also hard-refresh or sign out/in in the browser when validating
permission changes.

## 11. Recommended post-uninstall checks

Using representative non-Administrator users, verify:

- which Projects they can now see,
- which Tasks they can now see,
- whether broad roles have restored wider access,
- whether temporary Project/Task shares should be removed,
- whether trial-only roles should be removed or retained,
- whether Tasks left in `Pending Review` need an administrative decision,
- that the app's custom Task action buttons are gone.

Do not assume the site's security posture after uninstall is identical to its
pre-install state merely because the app itself is no longer installed.

## 12. Summary

The most important uninstall effect is:

> **The app's owner-or-explicit-share Project/Task fence disappears, so the
> site's remaining native role/share permission model once again determines
> document scope.**

At the same time, normal data changes made during the trial — statuses, shares,
roles, assignments, ownership, and user configuration — are not automatically
rolled back.
