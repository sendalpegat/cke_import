# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Master Data Mixin",
    "version": "14.0.4.1.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "mail",
        "ssi_print_mixin",
        "ssi_sequence_mixin",
    ],
    "data": [
        "views/mixin_master_data_views.xml",
    ],
}
