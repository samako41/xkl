
{
    "name": "Product Configurator Manufacturing",
    "version": "18.0.1.0.0",
    "category": "Manufacturing",
    "summary": "BOM Support for configurable products",
    "author": "Olajide Idowu ICIT",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/product-configurator",
    "depends": ["mrp", "product_configurator"],
    "data": [
        "data/menu_product.xml",
        "views/mrp_view.xml",
        "security/configurator_security.xml",
        "security/ir.model.access.csv",
    ],
    "assets": {
        "web.assets_backend": [
            "/product_configurator_mrp/static/src/scss/mrp_config.scss",
            "/product_configurator_mrp/static/src/js/list_controller.js",
        ],
        "web.assets_qweb": [
            "/product_configurator_mrp/static/src/xml/mrp_production_views.xml",
        ],
    },
    "demo": ["demo/product_template.xml"],
    "installable": True,
    "auto_install": False,
    "development_status": "Beta",
}
