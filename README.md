# ERPNext Project Access

> **Status: Alpha**

ERPNext Project Access adds scoped access control and controlled Task workflow
actions to ERPNext Projects and Tasks.

The project is under active development. Its first real-world alpha deployment
is being used to validate the access-control and workflow model before a stable
release.

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

## Alpha compatibility

The first alpha deployment is currently being exercised with:

- Frappe Framework 16.19.0
- ERPNext 17.0.0-dev

This is an unusual mixed development environment and should not be interpreted
as a general compatibility guarantee.

Additional ERPNext/Frappe versions will be documented only after testing.

## License

GPL-3.0-only
