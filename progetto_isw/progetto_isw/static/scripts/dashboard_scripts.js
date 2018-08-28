let big_button;
let form_popup;
let form_popup_field_input;
let cancel_button;

$(document).ready(function () {
    big_button = $('.big_button');
    form_popup = $('.form_popup');
    form_popup_field_input = $('input.form_popup_field-input');
    cancel_button = $('.cancel_button');

    $('.prevent_submit_on_enter_press').on('keyup keypress', function(e) {
        let keyCode = e.keyCode || e.which;
        if (keyCode === 13) {
            e.preventDefault();
            return false;
        }
    });

    big_button.on('click', function (e) {
        e.preventDefault();
        form_popup.toggleClass('hidden-popup');
        big_button.toggleClass('hidden-popup');
        form_popup_field_input.focus();
    });

    cancel_button.on('click', function (e) {
        e.preventDefault();
        form_popup.toggleClass('hidden-popup');
        big_button.toggleClass('hidden-popup');
        form_popup_field_input.val('');
    });

    form_popup_field_input.on('keyup keypress', function(e) {
        let keyCode = e.keyCode || e.which;
        if (keyCode === 13) {
            $('.form_popup_buttons-action').click();
            return false;
        }
    });

    $(document).mouseup(function (e) {
        if (e.target !== form_popup &&
            form_popup.has(e.target).length === 0) {

            form_popup.addClass('yep');
            form_popup.addClass('hidden-popup');
            big_button.removeClass('hidden-popup');
        }
    });
});

