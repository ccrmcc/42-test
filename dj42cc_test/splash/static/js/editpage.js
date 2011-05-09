var form_success = function(form) {
    $(form).find('input').removeAttr("disabled");
    $(form).find('textarea').removeAttr("disabled");

};

var form_beforesubmit = function(form) {
    $(form).find('input').attr("disabled", "disabled");
    $(form).find('textarea').attr("disabled", "disabled");
};

var ajaxify_form = function (form) {

    var options = {
        success: function() { form_success(form) },
        beforeSubmit: function() {form_beforesubmit(form)}
    };

    $(form).ajaxForm(options);
};

$(document).ready( function() {
    $('.jquery-date').datepicker();
    ajaxify_form('.contact_edit');
});
