import frappe

SETTINGS_DOCTYPE = "ERPNext Project Access Settings"


def execute():
	"""Preserve alpha.1 behavior when an existing installation upgrades.

	Fresh installs do not execute historical patches during install_app; Frappe
	marks them completed. Therefore a fresh alpha.2 installation keeps the
	settings DocType default (disabled), while an existing alpha.1 site running
	bench migrate executes this patch and remains enabled until an administrator
	explicitly disables it.
	"""
	if not frappe.db.exists("DocType", SETTINGS_DOCTYPE):
		return

	frappe.db.set_single_value(SETTINGS_DOCTYPE, "enabled", 1)
