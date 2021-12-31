odoo.define('add_new_parent_widget.action', function(require) {
    'use strict';

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');

    var BaseAction = AbstractAction.extend({
        hasControlPanel: false,
        template: "ClientAction",
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
            console.log('clicked');
            var data = {
                'aicsk_first_name': name,
                'aicsk_family_name': family_name,
                'name':  name.concat(" ", family_name),
                'mobile': mobile,
            };
            if (name.length > 0 && family_name.length > 0 && mobile.length > 0 ){
            var parent =  this._rpc({
                model: 'res.partner',
                method: 'create',
                args: [data],
            });
            if (parent) {
                this.trigger_up('show_effect', {
                    message: 'WELCOME TO AICSK',
                    type: 'rainbow_man',
                });
            }
            location.reload();
            }

        },
    });

    core.action_registry.add('add_new_parent_widget.action', BaseAction);
});