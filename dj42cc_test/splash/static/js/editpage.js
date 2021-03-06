var show_msg = function(msg) {
    $(".status").html(msg);

    setInterval(function() {
        show_msg("");
    }, 3000);
};

var form_success = function(form, data, status) {
    $(form).find('input').removeAttr("disabled");
    $(form).find('textarea').removeAttr("disabled");
    $(form).find("ul.errorlist").remove();
    $('input.error').removeClass('error');

    if(status != 'success') {
        show_msg("internal server eror");
        return
    }
    if(data.status=='ok') {
        show_msg("saved ok");
        return;
    }

    for(key in data.fields) {
        var field = $("#id_"+key);
        field.addClass("error");

        var errorlist = $("<ul></ul>");
        errorlist.addClass("errorlist");
        errorlist.insertBefore(field);

        var errors = data.fields[key];

        for(i=0;i<errors.length; i++) {
            box = $("<li></li>");
            box.text(errors[i]);

            errorlist.append(box);
        }
    }
};

var form_beforesubmit = function(form) {
    show_msg();
    $(form).find('input').attr("disabled", "disabled");
    $(form).find('textarea').attr("disabled", "disabled");
};

var ajaxify_form = function (form) {

    var options = {
        success: function(data, status) {
                     form_success(form, data, status)
        },
        beforeSubmit: function() {form_beforesubmit(form)},
        url : EDIT_PERSON_URL,
    };

    $(form).ajaxForm(options);
};

$(document).ready( function() {
    $('.jquery-date').datepicker();
    ajaxify_form('.contact_edit');

    $(".loading").ajaxStart(function(){
        $(this).show();
    });
    $(".loading").ajaxStop(function(){
        $(this).hide();
    });
});
