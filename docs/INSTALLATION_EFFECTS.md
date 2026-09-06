# What Changes Immediately After Installation

> **Status: Alpha**
>
> Installing ERPNext Project Access is **not a passive installation** on an
> existing ERPNext site. The app registers permission hooks for `Project` and
> `Task`, so access to existing records can change as soon as the app is active.
>
> Evaluate this alpha on a test or staging site before installing it on a
> production system with existing Projects and Tasks.

## 1. The app does not wait for a special role to be configured

ERPNext Project Access does not require a role named `Worker`, `Project Access
Creator`, or any other app-specific role before its access rules become active.

Once the app is installed and its hooks are loaded, the document-level access
rules apply to Project and Task for non-Administrator users.

Normal Frappe/ERPNext role permissions still apply as the first permission
layer. The app adds an additional document-level fence.

## 2. Existing Project visibility becomes owner/share based

For a non-Administrator user, an existing Project is visible through the app
only when either:

- the user is the Project owner, or
- the Project has an explicit user-specific `DocShare` with Read access.

This means a user who previously saw many Projects only because of a broad
ERPNext role may see fewer Projects immediately after installation.

A broad role does not by itself bypass this document-level fence.

For a non-owner Project:

- Read / Select / Print / Email require an explicit Read share.
- Write requires an explicit Write share.
- Share requires an explicit Share right.
- Other destructive or administrative permission types are denied by this app
  for the non-owner.

`Administrator` bypasses this additional fence.

## 3. Existing Task visibility also becomes owner/share based

For a non-Administrator user, an existing Task is visible through the app only
when either:

- the user is the Task owner, or
- the Task has an explicit user-specific `DocShare` with Read access.

Task access is independent of Project access. A user may therefore be able to
open a Task while being unable to open its linked Project.

For a non-owner Task:

- Read / Select / Print / Email require an explicit Read share.
- Write requires an explicit Write share.
- Share requires an explicit Share right.
- Other destructive or administrative permission types are denied by this app
  for the non-owner.

Again, normal role permissions still apply in addition to this scope check.
Ownership or a DocShare does not create general DocType capability that the user
otherwise lacks.

## 4. Existing assignments may preserve Task access

ERPNext assignment normally creates the user-specific Task Read access used by
an assignee. Where that Read share exists, the assigned user can continue to
see the Task even if the linked Project is private to them.

The app's Task ACL does **not** directly test whether a user is assigned. It
tests ownership or the resulting explicit Task share.

The controlled worker actions separately require the user to be an active Task
assignee.

## 5. New Project and Task creation is not granted by installation

Installing the app does not automatically give users permission to create
Projects or Tasks.

Creation of new Projects and Tasks remains controlled by ordinary ERPNext role
permissions.

This is why a new evaluation site may need a local creator role such as the
reference configuration described in [ROLE_SETUP.md](ROLE_SETUP.md).

## 6. New controlled Task actions become available conditionally

The app adds Task form logic for narrowly controlled status transitions.

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

Installing the app does **not** automatically change the status of any existing
Task. These actions appear only when the logged-in user and current Task status
satisfy the app's authorization rules.

The controlled actions do not grant general Task Write permission.

## 7. What installation does not automatically do

The current alpha does not automatically:

- create mandatory Worker or Creator roles,
- convert Website Users into System Users,
- grant Desk access,
- share Projects or Tasks,
- change Project ownership,
- change Task ownership,
- reassign Tasks,
- change existing Task statuses,
- grant general Project or Task Write permission,
- make a Task's parent Project visible to the Task assignee.

The deployment remains responsible for its own user, role, Desk-access, and
sharing configuration.

## 8. A concrete before/after example

Imagine an existing user with a broad role that previously allowed them to see
all Projects and Tasks.

Before ERPNext Project Access:

```text
Role says user can Read Project/Task
        ↓
user may see many records allowed by the normal ERPNext model
```

After ERPNext Project Access:

```text
Normal role says user can Read Project/Task
        ↓
ERPNext Project Access additionally asks:
    owner OR explicit Read share?
        ↓
Yes → record may be accessible
No  → record is outside that user's scope
```

Therefore, installing this app on an existing site can intentionally reduce
visibility even when no role configuration is changed afterward.

## 9. Recommended pre-install review for an existing site

Before enabling the alpha on a production site with existing Project/Task data,
review at least:

- who currently owns important Projects and Tasks,
- which users rely on broad role-based visibility,
- which Projects and Tasks already have explicit user shares,
- which Tasks are assigned to users,
- whether any managers currently depend on broad delete or administrative
  access to Projects/Tasks they do not own.

A staging installation is strongly recommended so that representative users can
compare their Project and Task lists before and after the app is enabled.

## 10. Summary

The most important behavioral change is:

> **Project and Task scope becomes owner-or-explicit-share based for
> non-Administrator users, while normal ERPNext role permissions continue to
> govern their general capabilities.**

The Task worker/reviewer buttons are an additional capability, but the access
fence is the change most likely to affect an existing ERPNext installation
immediately after installation.
