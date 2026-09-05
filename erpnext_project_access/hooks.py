app_name = "erpnext_project_access"
app_title = "ERPNext Project Access"
app_publisher = "Piyush Mehta"
app_description = (
    "Scoped Project and Task access control with controlled Task workflow for ERPNext"
)
app_license = "GPL-3.0-only"

required_apps = ["erpnext"]


# Project and Task access control
permission_query_conditions = {
    "Project": (
        "erpnext_project_access.project_acl."
        "get_project_permission_query_conditions"
    ),
    "Task": (
        "erpnext_project_access.task_acl."
        "get_task_permission_query_conditions"
    ),
}

has_permission = {
    "Project": "erpnext_project_access.project_acl.has_project_permission",
    "Task": "erpnext_project_access.task_acl.has_task_permission",
}


# Controlled Task workflow actions
doctype_js = {
    "Task": "public/js/task_actions.js",
}
