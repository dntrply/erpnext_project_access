frappe.ui.form.on("Task", {
    refresh(frm) {
        if (frm.is_new()) {
            return;
        }

        add_assignee_action(frm);
        add_reviewer_actions(frm);
    },
});


function add_assignee_action(frm) {
    frappe.call({
        method: "erpnext_project_access.task_actions.get_available_assignee_action",
        args: {
            task_name: frm.doc.name,
        },
        callback(r) {
            if (!r.message) {
                return;
            }

            const action = r.message;

            frm.add_custom_button(__(action.label), () => {
                frappe.call({
                    method: "erpnext_project_access.task_actions.change_assigned_task_status",
                    args: {
                        task_name: frm.doc.name,
                        target_status: action.target_status,
                    },
                    freeze: true,
                    freeze_message: __("Updating Task status..."),
                    callback(response) {
                        if (!response.message) {
                            return;
                        }

                        frappe.show_alert({
                            message: __(
                                "Task status changed to {0}",
                                [response.message.status]
                            ),
                            indicator: "green",
                        });

                        frm.reload_doc();
                    },
                });
            });
        },
    });
}


function add_reviewer_actions(frm) {
    frappe.call({
        method: "erpnext_project_access.task_actions.get_available_reviewer_actions",
        args: {
            task_name: frm.doc.name,
        },
        callback(r) {
            const actions = r.message || [];

            actions.forEach((action) => {
                frm.add_custom_button(
                    __(action.label),
                    () => run_reviewer_action(frm, action),
                    __("Review")
                );
            });
        },
    });
}


function run_reviewer_action(frm, action) {
    frappe.call({
        method: "erpnext_project_access.task_actions.change_reviewed_task_status",
        args: {
            task_name: frm.doc.name,
            target_status: action.target_status,
        },
        freeze: true,
        freeze_message: __("Updating Task status..."),
        callback(response) {
            if (!response.message) {
                return;
            }

            frappe.show_alert({
                message: __(
                    "Task status changed to {0}",
                    [response.message.status]
                ),
                indicator: "green",
            });

            frm.reload_doc();
        },
    });
}
