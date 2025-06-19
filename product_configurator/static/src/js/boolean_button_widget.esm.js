/** @odoo-module **/
import { useEffect, useRef, reactive, onMounted } from "@odoo/owl";
import { BooleanField, booleanField } from "@web/views/fields/boolean/boolean_field";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

export class BooleanButton extends BooleanField {
    static template = "product_configurator.BooleanButtonField";
    static props = {
        ...standardFieldProps,
        activeString: { type: String },
        inactiveString: { type: String, optional: true },
    };

    setup() {
        super.setup();

        this.root = useRef("root");
        this.state = reactive({
            text: "",
            hover: "",
            valColor: "",
            hoverColor: "",
        });

        onMounted(() => {
            this.updateDisplay();
        });

        useEffect(() => {
            this.updateDisplay();
        }, () => [this.state.value]);
    }

    updateDisplay() {
        const isActive = this.state.value;
        this.state.text = isActive ? this.props.activeString : this.props.inactiveString;
        this.state.hover = isActive ? this.props.inactiveString : this.props.activeString;
        this.state.valColor = isActive ? "text-success" : "text-danger";
        this.state.hoverColor = isActive ? "text-danger" : "text-success";
    }

    get displayData() {
        return {
            text: this.state.text,
            hover: this.state.hover,
            valColor: this.state.valColor,
            hoverColor: this.state.hoverColor,
        };
    }
}

export const BooleanButtonField = {
    ...booleanField,
    component: BooleanButton,
    extractProps: ({ options }) => ({
        activeString: options.active,
        inactiveString: options.inactive,
    }),
};

// Register it
registry.category("fields").add("boolean_button", BooleanButtonField);
