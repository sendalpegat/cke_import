odoo.define('cke_po_receipt_date.purchase_order', function (require) {
"use strict";

var FormController = require('web.FormController');
var FormView = require('web.FormView');

var PurchaseOrderFormController = FormController.extend({
    
    /**
     * Override untuk memicu onchange saat form dimuat
     */
    _onFieldChanged: function (event) {
        var self = this;
        var result = this._super.apply(this, arguments);
        
        // Jika model adalah purchase.order dan field yang berubah adalah date_order atau partner_id
        if (this.modelName === 'purchase.order' && 
            (event.data.name === 'date_order' || event.data.name === 'partner_id')) {
            
            // Trigger onchange untuk memperbarui receipt date
            this._rpc({
                model: 'purchase.order',
                method: 'onchange',
                args: [[], {
                    'partner_id': this.model.localData[this.handle].data.partner_id,
                    'date_order': this.model.localData[this.handle].data.date_order,
                }],
                context: this.model.localData[this.handle].context,
            }).then(function (result) {
                if (result.value && result.value.order_line) {
                    // Update order_line dengan receipt date yang baru
                    self.trigger_up('field_changed', {
                        dataPointID: self.handle,
                        changes: result.value,
                    });
                }
            });
        }
        
        return result;
    },
    
    /**
     * Override untuk set default receipt date saat form baru dibuat
     */
    _onCreate: function () {
        var self = this;
        var result = this._super.apply(this, arguments);
        
        if (this.modelName === 'purchase.order') {
            // Trigger onchange untuk set default receipt date
            var record = this.model.localData[this.handle];
            if (record && record.data.date_order) {
                this._rpc({
                    model: 'purchase.order',
                    method: 'onchange',
                    args: [[], {
                        'partner_id': record.data.partner_id,
                        'date_order': record.data.date_order,
                    }],
                    context: record.context,
                }).then(function (result) {
                    if (result.value) {
                        self.trigger_up('field_changed', {
                            dataPointID: self.handle,
                            changes: result.value,
                        });
                    }
                });
            }
        }
        
        return result;
    },
});

var PurchaseOrderFormView = FormView.extend({
    config: _.extend({}, FormView.prototype.config, {
        Controller: PurchaseOrderFormController,
    }),
});

// Register view hanya untuk purchase.order
var viewRegistry = require('web.view_registry');
viewRegistry.add('purchase_order_form', PurchaseOrderFormView);

return {
    PurchaseOrderFormController: PurchaseOrderFormController,
    PurchaseOrderFormView: PurchaseOrderFormView,
};

});