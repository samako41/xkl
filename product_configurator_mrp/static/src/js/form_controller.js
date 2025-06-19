/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { registry } from "@web/core/registry";
import { FormController } from "@web/views/form/form_controller";
import { FormView } from "@web/views/form/form_view";
import { core } from "@web/core";

const { qweb } = core;

// 1️⃣ Patch FormController to add configure button & action
patch(FormController.prototype, "product_configurator_mrp/FormController", {
    setup() {
        this._super(...arguments);
        // no special state needed
    },
    renderButtons() {
        this._super(...arguments);
        if (
            this.modelName === "mrp.production" &&
            this.props.initialState.context.custom_create_variant &&
            this.$buttons
        ) {
            const $btnCreate = this.$buttons.find(".o_form_button_create");
            const $btnConfig = $(qweb.render("ConfigFormView.buttons", { widget: this }));
            $btnConfig.insertAfter($btnCreate);
            $btnConfig.filter(".o_form_button_create_config").show();
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
    // Connect button click to _onConfigure
    onEvent(ev) {
        if (ev.type === "click" && ev.target.classList.contains("o_form_button_create_config")) {
            return this._onConfigure();
        }
        return this._super(...arguments);
    },
});

// 2️⃣ Define & register the updated Form View
class ConfigFormView extends FormView {
    constructor() {
        super(...arguments);
    }
}
ConfigFormView.config = {
    ...FormView.config,
    Controller: FormController,
};
registry.category("views").add("product_configurator_mrp_form", ConfigFormView);
