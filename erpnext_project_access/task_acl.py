import frappe


def get_task_permission_query_conditions(user=None):
    """Limit Task lists to tasks owned by or explicitly shared with user."""
    user = user or frappe.session.user

    if user == "Administrator":
        return ""

    user_escaped = frappe.db.escape(user)

    return f"""
        (
            `tabTask`.`owner` = {user_escaped}
            OR EXISTS (
                SELECT 1
                FROM `tabDocShare`
                WHERE
                    `tabDocShare`.`share_doctype` = 'Task'
                    AND `tabDocShare`.`share_name` = `tabTask`.`name`
                    AND `tabDocShare`.`user` = {user_escaped}
                    AND `tabDocShare`.`read` = 1
            )
        )
    """


def _has_task_share(docname, user, right):
    return bool(
        frappe.db.exists(
            "DocShare",
            {
                "share_doctype": "Task",
                "share_name": docname,
                "user": user,
                right: 1,
            },
        )
    )


def has_task_permission(doc, ptype="read", user=None, debug=False):
    """
    Task access control fence.

    Normal Frappe/ERPNext role permissions still apply.

    For an existing Task, a non-owner must additionally have an explicit
    DocShare entry for the requested access.
    """
    user = user or frappe.session.user

    if user == "Administrator":
        return True

    # New Task creation remains controlled by normal role permissions.
    if doc.is_new():
        return True

    # Task creator/owner remains controlled by normal role permissions.
    if doc.owner == user:
        return True

    # Frappe may evaluate the complete permission dictionary with ptype=None.
    if ptype is None:
        return _has_task_share(doc.name, user, "read")

    if ptype in ("read", "select", "print", "email"):
        return _has_task_share(doc.name, user, "read")

    if ptype == "write":
        return _has_task_share(doc.name, user, "write")

    if ptype == "share":
        return _has_task_share(doc.name, user, "share")

    # Do not let a broad role such as HR Manager provide delete or other
    # administrative Task rights to a non-owner.
    return False
