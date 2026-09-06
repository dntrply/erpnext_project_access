# Reference Role and Permission Setup

> **Status: Alpha**
>
> ERPNext Project Access does not require particular role names and does not
> install a mandatory Worker or Project Creator role. This document describes
> the minimum model established by the first validated alpha deployment and a
> reference configuration that can be used to evaluate the app.

## 1. Two different permission layers

ERPNext Project Access is intentionally role-agnostic.

Frappe/ERPNext role permissions answer:

> What kinds of actions may this user generally perform?

ERPNext Project Access adds a second question:

> Which individual Projects and Tasks may this user perform them on?

The app therefore does not replace Role Permission Manager and does not require
an organization's existing role model to be renamed or replaced.

## 2. Desk access is a prerequisite, not an app role

Users who participate in the Desk-based Project/Task workflow must be **System
Users with Desk access**.

ERPNext Project Access does not itself turn a Website User into a System User
and does not grant Desk access.

An installation may satisfy this prerequisite using any appropriate existing
role or local baseline role that has Desk access. The role's name is not
significant to this app.

A role used only to provide Desk access may legitimately have no Project, Task,
or ToDo DocType permissions of its own. That is distinct from the document
permissions described below.

## 3. Reference persona: Restricted Worker

The first alpha validation established the following worker model.

### Required by the validated workflow

- The user is a **System User** and can use Desk.
- The user can **Read** the specific Task.
- The user is an **active assignee** of the Task. In the current implementation,
  this means an Open `ToDo` exists for that user and Task.

ERPNext assignment normally creates the user-specific Task Read access needed by
an assignee. The app still checks Task Read permission; assignment by itself is
not treated as a permission bypass.

### Not required by the controlled worker actions

The controlled `Start Work` and `Submit for Review` actions do **not** require
that the worker be given general Task Write permission.

The worker also does not need access to the parent Project merely to work on an
individually accessible Task.

The app does not require a role named `Worker`, `Project Access Worker`, or any
other app-specific worker role.

## 4. Reference persona: Project/Task Creator and Reviewer

Creating Projects and Tasks remains governed by ordinary Frappe/ERPNext role
permissions.

For the current alpha reviewer model, the reviewer is the **Task owner**. The
controlled review actions themselves require that the Task owner can Read the
Task; they do not require general Task Write permission as a prerequisite to the
narrow review transition.

A practical creator role will usually need enough normal ERPNext permissions to
create and maintain the creator's own Projects and Tasks.

### Configuration used in the validated alpha deployment

The first alpha deployment used this local creator-role configuration at
permission level 0:

| DocType | Read | Write | Create | Delete | Share | If Owner |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Project | Yes | Yes | Yes | No | Yes | Yes |
| Task | Yes | Yes | Yes | No | Yes | Yes |

`Report`, `Export`, `Import`, `Print`, and `Email` were not granted by that local
role.

This table is a **validated reference configuration**, not a mandatory role
contract for the app.

In particular, `Share` was present in the tested creator role because that role
was used for the pilot's normal Project/Task setup. It should not be interpreted
as a requirement of the controlled reviewer action itself.

## 5. ToDo permissions

The validated deployment did not add any custom `ToDo` permission through its
local Desk-access role or creator role.

The normal Frappe Desk environment supplied the surrounding assignment behavior.
Because the alpha has not independently reduced all built-in/effective Frappe
permissions around `ToDo`, this should not yet be interpreted as a broad claim
that no `ToDo` permission can ever be required in every ERPNext/Frappe version.

## 6. Recommended evaluation setup

For a minimal evaluation, use two System Users:

### User A — Creator / Reviewer

Give User A an ordinary role configuration that permits the user to create and
maintain their own Projects and Tasks. The table above is one validated example.

### User B — Restricted Worker

Give User B whatever local role is necessary to make the account a System User
with Desk access, but do not grant broad Task Write permission merely for this
workflow.

Then:

1. User A creates a Project and Task.
2. User A assigns the Task to User B.
3. Do not share the parent Project with User B.
4. Confirm User B can see and open the Task but cannot open the Project.
5. Confirm User B can use **Start Work** and **Submit for Review**.
6. Confirm User A can use **Return for Rework** and **Approve & Complete** as
   Task owner.

See [HOWTO.md](HOWTO.md) for the full acceptance workflow.

## 7. What downstream deployments should customize

Organizations are expected to keep their own role names and broader permission
model.

For example, an installation may already have roles such as `Employee`,
`Projects User`, `Project Coordinator`, or locally defined roles. Those can be
used as long as their underlying permissions satisfy the required capabilities.

ERPNext Project Access should remain responsible for the reusable
**document-level access boundary and controlled workflow actions**, while each
organization remains responsible for its own **general role model and Desk
access policy**.
