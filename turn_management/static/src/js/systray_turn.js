odoo.define('turn_management.turn', function(require) {
    "use strict";
    var Widget = require('web.Widget');
    var SystrayMenu = require('web.SystrayMenu');
    var rpc = require('web.rpc');
    var Trun = Widget.extend({
        template: 'systray_turn',
        events: {
            "click #turn_widget": "_onClickGetTurn"
        },
        _onClickGetTurn: function(event) {
            event.stopPropagation();
            var self = this;
            rpc.query({
                    model: 'aicsk.turn',
                    method: 'get_coming_turn',
                    args: [],
                })
                .then(function(result) {
                    if (result) {
                        $('#current_turn_info').text(result);
                    }
                });
            $('#ul_turn').toggle();
        },

    });
    SystrayMenu.Items.push(Trun);
    return Trun;
});