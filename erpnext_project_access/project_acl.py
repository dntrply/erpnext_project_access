import frappe

from erpnext_project_access.settings import is_enabled


def get_project_permission_query_conditions(user=None):
	"""Limit Project lists to projects owned by or explicitly shared with user."""
	if not is_enabled():
		return ""

	user = user or frappe.session.user

	if user == "Administrator":
		return ""

	user_escaped = frappe.db.escape(user)

	return f"""
		(
			`tabProject`.`owner` = {user_escaped}
			OR EXISTS (
				SELECT 1
				FROM `tabDocShare`
				WHERE
					`tabDocShare`.`share_doctype` = 'Project'
					AND `tabDocShare`.`share_name` = `tabProject`.`name`
					AND `tabDocShare`.`user` = {user_escaped}
					AND `tabDocShare`.`read` = 1
			)
		)
	"""


def _has_project_share(docname, user, right):
	return bool(
		frappe.db.exists(
			"DocShare",
			{
				"share_doctype": "Project",
				"share_name": docname,
				"user": user,
				right: 1,
			},
		)
	)


def has_project_permission(doc, ptype="read", user=None, debug=False):
	"""
	Project access control fence.

	Normal Frappe/ERPNext role permissions still apply. When ERPNext Project
	Access is disabled, this hook is deliberately neutral and native permissions
	remain in effect.

	For an existing Project, a non-owner must additionally have an explicit
	DocShare entry for the requested access.
	"""
	if not is_enabled():
		return True

	user = user or frappe.session.user

	if user == "Administrator":
		return True

	# New Project creation remains controlled by normal role permissions.
	if doc.is_new():
		return True

	# Project creator/owner remains controlled by normal role permissions.
	if doc.owner == user:
		return True

	# Frappe calls get_doc_permissions(doc) with ptype=None while loading
	# form permission metadata. Permit that evaluation for a user who can
	# at least read this Project. Specific operations are checked again
	# below using their actual permission type.
	if ptype is None:
		return _has_project_share(doc.name, user, "read")

	if ptype in ("read", "select", "print", "email"):
		return _has_project_share(doc.name, user, "read")

	if ptype == "write":
		return _has_project_share(doc.name, user, "write")

	if ptype == "share":
		return _has_project_share(doc.name, user, "share")

	# Do not let broad roles such as HR Manager supply destructive or
	# administrative Project rights to a non-owner merely because the
	# Project was shared with them.
	return False
