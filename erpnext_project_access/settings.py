import frappe
from frappe import _
from frappe.utils import cint


SETTINGS_DOCTYPE = "ERPNext Project Access Settings"
_LOCAL_CACHE_KEY = "_erpnext_project_access_enabled"


def clear_local_activation_cache():
	"""Clear the request-local activation flag after settings are changed."""
	if hasattr(frappe.local, _LOCAL_CACHE_KEY):
		delattr(frappe.local, _LOCAL_CACHE_KEY)


def is_enabled():
	"""Return whether ERPNext Project Access is explicitly enabled for this site.

	The feature deliberately fails open to native ERPNext behavior when the
	settings DocType is not yet available (for example during installation or
	migration). Fresh installations default to disabled.
	"""
	if hasattr(frappe.local, _LOCAL_CACHE_KEY):
		return getattr(frappe.local, _LOCAL_CACHE_KEY)

	enabled = False

	try:
		if frappe.db.exists("DocType", SETTINGS_DOCTYPE):
			enabled = bool(
				cint(frappe.db.get_single_value(SETTINGS_DOCTYPE, "enabled"))
			)
	except Exception:
		# A missing/incomplete settings schema must never make installation or
		# migration accidentally enforce the Project/Task access fence.
		enabled = False

	setattr(frappe.local, _LOCAL_CACHE_KEY, enabled)
	return enabled


def require_enabled():
	"""Reject a controlled workflow mutation when the feature is disabled."""
	if not is_enabled():
		frappe.throw(
			_("ERPNext Project Access is disabled."),
			frappe.PermissionError,
		)
