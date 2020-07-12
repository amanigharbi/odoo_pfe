odoo.school= function(instance, local) {
    var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;

    local.HomePage = instance.Widget.extend({
        start: function() {
            console.log('hi');
            this.do_action({
                type: 'ir.actions.act_window',
                res_model: "student.desciplines",
                res_id: 1,
                views: [[false, 'form']],
                target: 'current',
                context: {
                    'click #but_javascript button': 'But_click'
                },
            });
        },
        But_click: function() {
                    console.log('TOTO');
                },
    });
}