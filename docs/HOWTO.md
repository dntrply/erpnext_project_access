# ERPNext Project Access — How To

> **Status: Alpha**
>
> This guide describes the access model and workflow validated for
> `v0.1.0-alpha.1`. The app is still under active development, so behavior and
> configuration may change before a stable release.

## 1. What this app changes

ERPNext Project Access adds a document-level access fence around **Project** and
**Task**, while leaving normal Frappe/ERPNext role permissions in place.

That means there are two layers:

1. **Role permissions** decide what a user is generally allowed to do with
   Projects and Tasks.
2. **ERPNext Project Access** decides which individual Projects and Tasks that
   user may access.

The app does not replace normal ERPNext roles and it does not create a special
worker role of its own.

Users participating in this Desk-based workflow must nevertheless be **System
Users with Desk access**. That is a Frappe/ERPNext prerequisite rather than an
app-specific Project/Task role. ERPNext Project Access does not itself convert a
Website User into a System User or grant Desk access.

For a generic reference permission model, see
[ROLE_SETUP.md](ROLE_SETUP.md).

For existing documents, a non-owner must have an explicit user-specific
`DocShare` entry for the required access. Broad roles do not bypass this scope
boundary.

## 2. Access model

### Projects

A Project appears in a non-Administrator user's Project list when either:

- the user owns the Project, or
- the Project has been explicitly shared with that user with **Read** access.

For a non-owner:

- Read / Select / Print / Email require a Project **Read** share.
- Write requires a Project **Write** share.
- Share requires a Project **Share** right.
- Other destructive or administrative rights are denied by this app even if a
  broad role would otherwise provide them.

Creating a new Project is still controlled by normal ERPNext role permissions.

### Tasks

Task access is independent of Project access.

A Task appears in a non-Administrator user's Task list when either:

- the user owns the Task, or
- the Task has been explicitly shared with that user with **Read** access.

For a non-owner:

- Read / Select / Print / Email require a Task **Read** share.
- Write requires a Task **Write** share.
- Share requires a Task **Share** right.
- Other destructive or administrative rights are denied by this app.

Creating a new Task is still controlled by normal ERPNext role permissions.

A user may therefore be able to see and work with a Task while being unable to
open the Task's parent Project. This separation is intentional.

## 3. Assignment and sharing

The worker must first be a System User who can use Desk.

The controlled worker workflow also requires the user to be an **active
assignee** of the Task. In the current implementation, that means there must be
an **Open ToDo** for the user referring to that Task.

ERPNext assignment normally creates the Read access needed for the assignee to
open the Task. The app ultimately checks the resulting Task access; it does not
treat assignment by itself as a replacement for permissions.

If a worker is assigned but cannot see the Task, check that the worker has Task
Read access / an appropriate user-specific Task share in the installation.

The worker does **not** need general Task Write permission merely to use the
controlled workflow buttons described below.

## 4. Participants in the alpha workflow

The validated alpha workflow has two participants:

- **Worker** — a Desk-capable System User who is an active Task assignee.
- **Reviewer** — currently the **Task owner**.

There is no separate configurable Reviewer field in `v0.1.0-alpha.1`.

## 5. End-to-end workflow

The alpha workflow is:

```text
Open
  ↓ Start Work
Working
  ↓ Submit for Review
Pending Review
  ↓ Return for Rework
Working
  ↓ Submit for Review
Pending Review
  ↓ Approve & Complete
Completed
```

### Step A — Create the Project

Create a Project using a user whose normal ERPNext roles allow Project creation.

Do not share the Project with the worker if your goal is to keep the Project
private while exposing only selected Tasks.

### Step B — Create the Task

Create a Task under that Project.

For the current reviewer model, the user who creates/owns the Task should be the
person expected to review it later.

### Step C — Assign the Task to the worker

Use ERPNext's normal Task assignment mechanism to assign the Task to the worker.

After assignment, verify that:

- the worker can see the Task in the normal Task list,
- the worker can open the Task,
- the worker cannot open the parent Project unless the Project was separately
  shared with them.

This is the central access pattern the app is intended to support.

### Step D — Worker starts work

Log in as the worker and open the Task while its status is **Open**.

The worker should see the custom action:

**Start Work**

Clicking it performs only this controlled transition:

```text
Open → Working
```

The worker does not need general Task Write permission for this action.

### Step E — Worker submits for review

When the Task is **Working**, the active assignee should see:

**Submit for Review**

Clicking it performs:

```text
Working → Pending Review
```

After submission, that worker action disappears because there is no worker
transition defined from `Pending Review`.

### Step F — Task owner reviews

Log in as the Task owner and open the Task while its status is **Pending Review**.

The Task owner should see two actions under **Review**:

- **Approve & Complete**
- **Return for Rework**

#### Return for Rework

This performs:

```text
Pending Review → Working
```

The worker can then continue working and later use **Submit for Review** again.

#### Approve & Complete

This performs:

```text
Pending Review → Completed
```

The app saves the Task through ERPNext's normal Task lifecycle after its narrow
authorization checks have succeeded.

In the validated alpha test, completion also:

- set Task progress to `100%`, and
- closed the worker's Task ToDo.

## 6. What the worker should and should not be able to do

A typical restricted worker should be able to:

- use Desk as a System User,
- see an explicitly accessible / assigned Task,
- open that Task,
- use **Start Work** when the Task is Open,
- use **Submit for Review** when the Task is Working,
- continue to read the Task while it is Pending Review.

The same worker does not need to be able to:

- open the parent Project,
- freely edit arbitrary Task fields,
- manually change the Task to any status,
- approve their own Task merely because they are assigned to it,
- delete or administratively manage the Task.

Normal role permissions still matter. ERPNext Project Access narrows document
scope; it does not grant Desk access or general DocType permissions that the
user does not otherwise have.

## 7. What the reviewer should and should not be able to do

For `v0.1.0-alpha.1`, review actions are available only when:

- the logged-in user is the Task owner, and
- the Task status is `Pending Review`.

The controlled review actions permit only:

- `Pending Review → Working`, or
- `Pending Review → Completed`.

They are not a general-purpose bypass for arbitrary Task edits.

## 8. A minimal acceptance test

Use three objects/users:

- a creator/reviewer System User,
- a restricted worker System User,
- one private Project containing one Task assigned to the worker.

Then verify this sequence:

1. Worker can see the Task in Task List.
2. Worker can open the Task.
3. Worker cannot open the parent Project.
4. Worker clicks **Start Work** and status becomes Working.
5. Worker clicks **Submit for Review** and status becomes Pending Review.
6. Task owner clicks **Return for Rework** and status becomes Working.
7. Worker submits again.
8. Task owner clicks **Approve & Complete**.
9. Task becomes Completed.
10. Task progress becomes 100%.
11. The worker's Task ToDo closes.
12. The private parent Project remains inaccessible to the worker throughout.

This is the end-to-end scenario validated for the first alpha deployment.

## 9. Troubleshooting

### Worker cannot use Desk

Confirm that the account is a **System User** with Desk access. ERPNext Project
Access does not grant Desk access and does not require a particular role name to
provide it.

### Assigned Task does not appear in Task List

First confirm that the worker can open the Task directly and that the Task has
Read access for that user.

Also check the Frappe version. Frappe versions prior to **16.29.0** contain a
linked-table permission-query issue that can cause an otherwise readable Task to
be omitted from Task List when its linked Project is inaccessible.

For this alpha, use Frappe **16.29.0 or newer** unless you have independently
validated an equivalent fix in your branch.

### Start Work does not appear

Check that:

- the Task status is `Open`,
- the logged-in user is an active assignee,
- the assignment ToDo is still `Open`, and
- the user can read the Task.

### Submit for Review does not appear

Check that:

- the Task status is `Working`,
- the logged-in user is still an active assignee, and
- the user can read the Task.

### Review actions do not appear

Check that:

- the Task status is `Pending Review`,
- the logged-in user is the Task owner, and
- the Task owner can read the Task.

### Worker can open the Project unexpectedly

Project and Task sharing are independent. Check whether the Project has been
explicitly shared with the worker or whether the worker is the Project owner.

## 10. Compatibility of the validated alpha

The first end-to-end alpha validation was performed with:

- Frappe Framework `16.29.0`
- ERPNext `17.0.0-dev`
- HRMS `17.0.0-dev`
- ERPNext Project Access `0.1.0a1` / release tag `v0.1.0-alpha.1`

This was an intentionally mixed development environment and is **not** a broad
compatibility guarantee for all ERPNext/Frappe combinations.

## 11. Current alpha limitations

The first alpha deliberately keeps the model small:

- Reviewer is the Task owner; there is no separate Reviewer field yet.
- Access scope is based on ownership and explicit user-specific DocShare.
- Controlled workflow actions cover only the transitions documented above.
- The app does not replace ERPNext role configuration or grant Desk access.
- Compatibility has only been validated on the environment listed above.

These constraints are intentional while the access and workflow model is being
validated before broader feature development.
