import frappe
from frappe import _

from erpnext_project_access.settings import is_enabled, require_enabled

ALLOWED_ASSIGNEE_TRANSITIONS = {
	"Open": "Working",
	"Working": "Pending Review",
}

ACTION_LABELS = {
	"Working": "Start Work",
	"Pending Review": "Submit for Review",
}

ALLOWED_REVIEWER_TRANSITIONS = {
	"Pending Review": {"Working", "Completed"},
}


def _is_active_assignee(task_name, user):
	return bool(
		frappe.db.exists(
			"ToDo",
			{
				"reference_type": "Task",
				"reference_name": task_name,
				"allocated_to": user,
				"status": "Open",
			},
		)
	)


@frappe.whitelist(methods=["POST"])
def change_assigned_task_status(task_name, target_status):
	"""
	Allow an active Task assignee to perform only narrowly-approved
	workflow transitions without granting general Task Write permission.
	"""
	user = frappe.session.user

	if user == "Guest":
		frappe.throw(_("Login required."), frappe.PermissionError)

	require_enabled()

	task = frappe.get_doc("Task", task_name)

	# Assignment normally creates Read access. Require that access to
	# still exist before allowing this controlled mutation.
	task.check_permission("read")

	if not _is_active_assignee(task.name, user):
		frappe.throw(
			_("You are not currently assigned to this Task."),
			frappe.PermissionError,
		)

	current_status = task.status
	allowed_target = ALLOWED_ASSIGNEE_TRANSITIONS.get(current_status)

	if allowed_target != target_status:
		frappe.throw(
			_(
				"Task status cannot be changed from {0} to {1} using this action."
			).format(current_status, target_status),
			frappe.PermissionError,
		)

	task.status = target_status

	# Our narrower authorization checks have already succeeded.
	# Let ERPNext run its normal Task validation/on_update lifecycle.
	task.save(ignore_permissions=True)

	return {
		"name": task.name,
		"status": task.status,
	}


@frappe.whitelist(methods=["POST"])
def get_available_assignee_action(task_name):
	"""Return the controlled Task action available to the logged-in assignee."""
	if not is_enabled():
		return None

	user = frappe.session.user

	if user == "Guest":
		return None

	task = frappe.get_doc("Task", task_name)
	task.check_permission("read")

	if not _is_active_assignee(task.name, user):
		return None

	target_status = ALLOWED_ASSIGNEE_TRANSITIONS.get(task.status)

	if not target_status:
		return None

	return {
		"target_status": target_status,
		"label": ACTION_LABELS[target_status],
	}


@frappe.whitelist(methods=["POST"])
def get_available_reviewer_actions(task_name):
	"""Return controlled review actions when the logged-in user is the Task owner."""
	if not is_enabled():
		return []

	user = frappe.session.user

	if user == "Guest":
		return []

	task = frappe.get_doc("Task", task_name)
	task.check_permission("read")

	if task.owner != user:
		return []

	if task.status != "Pending Review":
		return []

	return [
		{
			"target_status": "Completed",
			"label": "Approve & Complete",
		},
		{
			"target_status": "Working",
			"label": "Return for Rework",
		},
	]


@frappe.whitelist(methods=["POST"])
def change_reviewed_task_status(task_name, target_status):
	"""
	Allow the Task owner to review a Pending Review Task without granting
	general Task Write permission.
	"""
	user = frappe.session.user

	if user == "Guest":
		frappe.throw(_("Login required."), frappe.PermissionError)

	require_enabled()

	task = frappe.get_doc("Task", task_name)
	task.check_permission("read")

	if task.owner != user:
		frappe.throw(
			_("Only the Task owner can perform this review action."),
			frappe.PermissionError,
		)

	allowed_targets = ALLOWED_REVIEWER_TRANSITIONS.get(task.status, set())

	if target_status not in allowed_targets:
		frappe.throw(
			_(
				"Task status cannot be changed from {0} to {1} using this review action."
			).format(task.status, target_status),
			frappe.PermissionError,
		)

	task.status = target_status

	# ERPNext's normal Task save lifecycle remains active. In particular,
	# completing a Task sets progress and closes its assignments.
	task.save(ignore_permissions=True)

	return {
		"name": task.name,
		"status": task.status,
	}
