from frappe.model.document import Document

from erpnext_project_access.settings import clear_local_activation_cache


class ERPNextProjectAccessSettings(Document):
	def on_update(self):
		clear_local_activation_cache()
