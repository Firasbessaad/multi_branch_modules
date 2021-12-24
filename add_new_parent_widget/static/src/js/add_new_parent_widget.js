odoo.define('add_new_parent_widget.view', function(require) {
    'use strict';

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');

    var BaseAction = AbstractAction.extend({
        hasControlPanel: false,
        template: "add_new_parent_widget.ClientAction",
        events: {
            'click .add_new_parent': '_onClickAddRecord',
        },
        init: function() {
            this._super.apply(this, arguments);
            console.log('Module initialized');
        },
        _onClickAddRecord: function() {
            var name = $("input[name='name']").val();
            var family_name = $("input[name='family_name']").val();
            var mobile = $("input[name='mobile']").val();
            data = {
                'name': name,
                'family_name': family_name,
                'mobile': mobile,
            }
            return this._rpc({
                model: 'res.partner',
                method: 'create',
                args: [data],
            });
        },
    });

    core.action_registry.add('add_new_parent_widget.action', BaseAction);
});