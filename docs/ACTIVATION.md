# Activation and Configuration

> **Status: alpha.2 development**
>
> ERPNext Project Access is designed to be installed **without immediately
> changing Project or Task access**. A fresh installation is disabled by default.
> A System Manager must explicitly enable it before the app's access fence and
> controlled Task workflow become active.

## 1. The three operating states

| State | Project/Task access | Controlled Task actions |
| --- | --- | --- |
| App not installed | Native ERPNext/Frappe behavior | Not available |
| App installed, disabled | Native ERPNext/Frappe behavior | Not available |
| App installed, enabled | Native role permissions **plus** the app's owner/share fence | Available when worker/reviewer conditions are satisfied |

The important contract is:

> **Installing the app makes the capability available. Enabling the app changes
> the site's Project/Task access policy.**

## 2. Fresh installations default to disabled

After a fresh alpha.2 installation and migration, the setting:

**ERPNext Project Access Settings → Enable ERPNext Project Access**

is off by default.

While it is off:

- Project list/query behavior remains native ERPNext/Frappe behavior,
- Task list/query behavior remains native ERPNext/Frappe behavior,
- the app's Project/Task `has_permission` hooks are neutral,
- `Start Work` and `Submit for Review` are not offered by this app,
- `Return for Rework` and `Approve & Complete` are not offered by this app,
- direct calls to the app's controlled mutation endpoints are rejected.

No app-specific role is required merely to leave the app installed in this
inactive state.

## 3. Before enabling on an existing site

Enabling the setting can immediately reduce which existing Projects and Tasks
non-Administrator users can access.

Before enabling, review at least:

- who owns important Projects and Tasks,
- which users currently rely on broad role-based Project/Task visibility,
- which Projects and Tasks have explicit user-specific shares,
- which Tasks are assigned to workers,
- whether managers depend on broad write/delete/admin access to documents they
  do not own.

For an existing production site, first test representative users on staging.

See [INSTALLATION_EFFECTS.md](INSTALLATION_EFFECTS.md) for the detailed
before/after access model.

## 4. Enable the app

Log in as a user with **System Manager** permission.

1. In Desk, search for **ERPNext Project Access Settings**.
2. Open the Single settings document.
3. Review the warning shown on the page.
4. Check **Enable ERPNext Project Access**.
5. Save.
6. Refresh any already-open Project or Task forms before testing.

A process restart is not required merely to toggle the setting. The setting is
read by the server on subsequent requests.

Once enabled, normal ERPNext role permissions still apply, but the app adds its
document-level Project/Task scope rules and controlled Task actions.

## 5. What enabling changes

For non-Administrator users, an existing Project or Task must now be either:

- owned by the user, or
- explicitly shared with that user with the required right.

Read scope therefore becomes owner-or-explicit-Read-share based. Write and Share
for non-owners require the corresponding explicit share rights.

Task access remains independent of Project access. A worker can therefore be
allowed to read an assigned Task while the parent Project remains private.

The controlled Task transitions also become available when their authorization
conditions are satisfied:

```text
Active assignee:
Open → Working
Working → Pending Review

Task owner (alpha reviewer):
Pending Review → Working
Pending Review → Completed
```

These narrow actions do not grant general Task Write permission.

## 6. Disable without uninstalling

A System Manager can return to native ERPNext/Frappe Project/Task access behavior
without uninstalling the app:

1. Open **ERPNext Project Access Settings**.
2. Uncheck **Enable ERPNext Project Access**.
3. Save.
4. Refresh already-open Project/Task forms.
5. Re-test representative users.

After disabling:

- the owner/share access fence is no longer applied by this app,
- the app's controlled Task buttons disappear,
- direct controlled mutation calls are rejected,
- normal ERPNext/Frappe permissions, shares, User Permissions and other installed
  customizations remain in force.

Disabling does **not** undo business data changes that occurred while the app was
enabled. It does not revert Task statuses, reopen completed assignments, remove
shares, restore old owners, or remove local roles.

## 7. Upgrade behavior from alpha.1

`v0.1.0-alpha.1` had no activation switch: its hooks became active as soon as
the app was installed.

For safety, an existing alpha.1 site upgrading to alpha.2 is treated differently
from a fresh alpha.2 installation:

- **fresh alpha.2 install:** disabled by default;
- **existing alpha.1 installation upgraded through `bench migrate`:** remains
  enabled so that an upgrade does not unexpectedly broaden Project/Task access.

A migration patch sets the new setting to enabled for existing installations.
The administrator can then disable it deliberately after reviewing the resulting
native ERPNext access model.

This preserves the safer principle on both sides:

- installation should not unexpectedly restrict a new site;
- upgrade should not unexpectedly remove an existing security fence.

## 8. Administrator boundary

Only **System Manager** is granted read/write access to the app's Settings
DocType in the reference implementation.

The app continues to exempt the `Administrator` user from its additional
Project/Task owner/share fence when enabled.

## 9. Recommended evaluation sequence

For a clean trial:

1. Install the app while it is disabled.
2. Verify native Project/Task behavior is unchanged.
3. Configure or reuse the reference creator/Desk roles described in
   [ROLE_SETUP.md](ROLE_SETUP.md).
4. Review ownership, assignment and explicit shares.
5. Enable ERPNext Project Access.
6. Run the acceptance test in [HOWTO.md](HOWTO.md).
7. Disable it again and confirm native ERPNext behavior returns.
8. Re-enable it and repeat the key access checks before considering production
   use.

This enable/disable cycle is part of the alpha.2 validation plan.
