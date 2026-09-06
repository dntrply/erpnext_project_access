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

	If the settings DocType does not yet exist (for example while a fresh install
	is being synchronized), the app is neutral and native ERPNext behavior
	continues. Once the settings DocType exists, database errors are deliberately
	not swallowed: an enabled security policy must never silently fail open.
	"""
	if hasattr(frappe.local, _LOCAL_CACHE_KEY):
		return getattr(frappe.local, _LOCAL_CACHE_KEY)

	if not frappe.db.exists("DocType", SETTINGS_DOCTYPE):
		enabled = False
	else:
		enabled = bool(
			cint(frappe.db.get_single_value(SETTINGS_DOCTYPE, "enabled"))
		)

	setattr(frappe.local, _LOCAL_CACHE_KEY, enabled)
	return enabled


def require_enabled():
	"""Reject a controlled workflow mutation when the feature is disabled."""
	if not is_enabled():
		frappe.throw(
			_("ERPNext Project Access is disabled."),
			frappe.PermissionError,
		)
