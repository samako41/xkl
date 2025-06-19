/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ListController } from "@web/views/list/list_controller";
import { ListView } from "@web/views/list/list_view";
import { registry } from "@web/core/registry";

// 1️⃣ Patch ListController to add custom Configure button
patch(ListController.prototype, "product_configurator_mrp.ListController", {
    renderButtons(...args) {
        const buttons = super.renderButtons(...args);

        if (
            this.modelName === "mrp.production" &&
            this.props?.context?.custom_create_variant
        ) {
            const configureBtn = document.createElement("button");
            configureBtn.type = "button";
            configureBtn.className = "btn btn-primary o_list_button_add_config";
            configureBtn.accessKey = "c";
            configureBtn.textContent = "Configure";
            configureBtn.addEventListener("click", () => this._onConfigure());
            buttons.appendChild(configureBtn);
        }

        return buttons;
    },

    async _onConfigure() {
        const result = await this.orm.call(
            "mrp.production",
            "action_config_start",
            [""],
            { context: this.props.context }
        );
        this.actionService.doAction(result);
    },
});

// 2️⃣ Define ListView using patched controller
class ConfigListView extends ListView {}
ConfigListView.config = {
    ...ListView.config,
    Controller: ListController,
};

// 3️⃣ Register the new list view
registry.category("views").add("product_configurator_mrp_tree", ConfigListView);
