# Installation and Activation Effects

> **Status: alpha.2 development**
>
> Fresh alpha.2 installations are **disabled by default**. Installation itself
> is intended to be passive. The access-control behavior described below begins
> only after a System Manager explicitly enables ERPNext Project Access.

## 1. Fresh install: no Project/Task behavior change while disabled

After a fresh install and migration, the setting:

**ERPNext Project Access Settings → Enable ERPNext Project Access**

is off.

While it remains off:

- Project lists use native ERPNext/Frappe permission behavior,
- Task lists use native ERPNext/Frappe permission behavior,
- direct Project/Task permission checks are not narrowed by this app,
- the app's controlled Task workflow buttons are not offered,
- the app's controlled status-mutation endpoints reject use.

The app does not wait for a special role to be configured, but it also does not
activate its policy merely because it is installed.

## 2. Enabling is the policy-changing action

Once a System Manager explicitly enables the app, normal ERPNext role
permissions continue to apply as the first permission layer and the app adds a
second, document-level fence.

For non-Administrator users, existing Project and Task scope becomes based on:

- ownership, or
- an explicit user-specific `DocShare` with the required right.

This can immediately reduce visibility for users who previously relied on broad
role-based access.

## 3. Existing Project visibility when enabled

For a non-Administrator user, an existing Project is in scope through this app
only when either:

- the user is the Project owner, or
- the Project has an explicit user-specific `DocShare` with Read access.

For a non-owner Project:

- Read / Select / Print / Email require an explicit Read share,
- Write requires an explicit Write share,
- Share requires an explicit Share right,
- other destructive or administrative permission types are denied by this app.

`Administrator` bypasses this additional fence.

## 4. Existing Task visibility when enabled

For a non-Administrator user, an existing Task is in scope through this app only
when either:

- the user is the Task owner, or
- the Task has an explicit user-specific `DocShare` with Read access.

Task access is independent of Project access. A user may therefore be able to
open an explicitly accessible Task while being unable to open its parent Project.

For a non-owner Task:

- Read / Select / Print / Email require an explicit Read share,
- Write requires an explicit Write share,
- Share requires an explicit Share right,
- other destructive or administrative permission types are denied by this app.

Normal role permissions still apply in addition to this scope check. Ownership
or a DocShare does not create general DocType capability the user otherwise
lacks.

## 5. Existing assignments may preserve Task access

ERPNext assignment normally creates the user-specific Task Read access used by
an assignee. Where that Read share exists, the assigned user can continue to see
the Task even if the linked Project is private to them.

The app's Task ACL does **not** directly test assignment. It tests ownership or
the resulting explicit Task share. The controlled worker actions separately
require an active Task assignment.

## 6. Creation permissions are not granted

Enabling ERPNext Project Access does not automatically give users permission to
create Projects or Tasks.

Creation remains controlled by ordinary ERPNext role permissions. A new
evaluation site may therefore need a local creator role such as the reference
configuration in [ROLE_SETUP.md](ROLE_SETUP.md).

## 7. Controlled Task actions when enabled

For an active assignee who can Read the Task:

```text
Open → Working
Working → Pending Review
```

For the current alpha reviewer, which is the Task owner:

```text
Pending Review → Working
Pending Review → Completed
```

Enabling the app does **not** automatically change the status of an existing
Task. The actions become available only when user/status authorization conditions
are satisfied.

The controlled actions do not grant general Task Write permission.

## 8. What enabling does not automatically do

Enabling does not automatically:

- create mandatory Worker or Creator roles,
- convert Website Users into System Users,
- grant Desk access,
- share Projects or Tasks,
- change Project or Task ownership,
- reassign Tasks,
- change existing Task statuses,
- grant general Project or Task Write permission,
- make a Task's parent Project visible to the Task assignee.

The deployment remains responsible for its own users, roles, Desk access and
sharing configuration.

## 9. Before/after example

Before enabling:

```text
Native ERPNext/Frappe permission model
        ↓
normal site behavior
```

After enabling:

```text
Normal role permission
        ↓
ERPNext Project Access additionally asks:
    owner OR explicit share?
        ↓
Yes → record may remain accessible
No  → record is outside that user's app-defined scope
```

## 10. Existing alpha.1 installations upgrading to alpha.2

`v0.1.0-alpha.1` was active immediately after installation. An alpha.1 site that
upgrades to alpha.2 through `bench migrate` is therefore kept **enabled** by a
migration patch.

This is intentional. Automatically disabling during an upgrade could broaden
Project/Task access for users with broad native ERPNext roles.

Fresh alpha.2 installs and alpha.1 upgrades therefore have different safe
defaults:

```text
Fresh alpha.2 install → disabled
Alpha.1 → alpha.2 upgrade → remains enabled
```

The administrator may then disable deliberately after reviewing native ERPNext
access behavior.

## 11. Recommended pre-activation review

Before enabling on an existing production site, review at least:

- who owns important Projects and Tasks,
- which users rely on broad role-based visibility,
- which Projects and Tasks already have explicit user shares,
- which Tasks are assigned to users,
- whether managers depend on broad delete/admin rights for documents they do not
  own.

Use staging and representative users first.

## 12. Summary

For alpha.2, **installation is passive; activation is not**.

The main behavioral change after activation is:

> **Project and Task scope becomes owner-or-explicit-share based for
> non-Administrator users, while normal ERPNext role permissions continue to
> govern general capabilities.**
