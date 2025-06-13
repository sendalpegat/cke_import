# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Product App",
    "version": "14.0.1.7.2",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "application": True,
    "depends": [
        "product",
        "ssi_decorator",
        "ssi_master_data_mixin",
    ],
    "data": [
        "security/ir_module_category_data.xml",
        "security/res_group_data.xml",
        "security/ir.model.access.csv",
        "templates/product_category_m2_configurator_templates.xml",
        "templates/product_product_m2_configurator_templates.xml",
        "templates/product_template_m2_configurator_templates.xml",
        "templates/product_pricelist_m2_configurator_templates.xml",
        "menu.xml",
        "views/uom_category_views.xml",
        "views/uom_uom_views.xml",
        "views/product_category_views.xml",
        "views/product_packaging_views.xml",
        "views/product_template_views.xml",
        "views/product_product_views.xml",
        "views/product_pricelist_views.xml",
        "views/product_attribute_views.xml",
        "views/product_supplierinfo_views.xml",
        "views/product_brand_views.xml",
        # "views/product_key_views.xml",
    ],
    "demo": [],
}
