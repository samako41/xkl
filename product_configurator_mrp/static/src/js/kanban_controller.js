/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { KanbanController } from "@web/views/kanban/kanban_controller";
import { KanbanView } from "@web/views/kanban/kanban_view";
import { registry } from "@web/core/registry";
import { core } from "@web/core";

const { qweb } = core;

// 1️⃣ Patch the KanbanController to add custom logic
patch(KanbanController.prototype, "product_configurator_mrp/KanbanController", {
    setup() {
        this._super(...arguments);
    },

    renderButtons() {
        this._super(...arguments);
        if (
            this.modelName === "mrp.production" &&
            this.props?.initialState?.context?.custom_create_variant &&
            this.$buttons
        ) {
            this.$buttons
                .find(".o-kanban-button-new_config")
                .css("display", "inline");
        }
    },

    async _onConfigure() {
        const result = await this.orm.call(
            "mrp.production",
            "action_config_start",
            [""],
            this.props.initialState.context
        );
        this.doAction(result);
    },

    // Register the event handler
    onEvent(ev) {
        if (
            ev.type === "click" &&
            ev.target.classList.contains("o-kanban-button-new_config")
        ) {
            return this._onConfigure();
        }
        return this._super(...arguments);
    },
});

// 2️⃣ Define and register the custom KanbanView
class ConfigKanbanView extends KanbanView {}
ConfigKanbanView.config = {
    ...KanbanView.config,
    Controller: KanbanController,
};

registry.category("views").add("product_configurator_mrp_kanban", ConfigKanbanView);
