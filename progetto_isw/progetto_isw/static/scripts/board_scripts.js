// gestione pulsanti nome colonna e cards
function show_button(e) {
    let focused = document.activeElement;
    let column_title;
    let card_title;
    let new_column_title;
    let edit_column;
    let discard_changes;

    if (focused.classList.contains('start_changes')) {
        edit_column = focused;
        edit_column.parentElement.classList.remove('hide_column_name_input');
        edit_column.parentElement.classList.add('hide_column_name_link');
        edit_column.parentElement.classList.remove('hide_delete-button');
        edit_column.getParentNode().find('input').focus();
    }

    if (focused.classList.contains('discard_column_name_modifications')) {
        discard_changes = focused;
        discard_changes.parentElement.classList.remove('hide_column_name_link');
        discard_changes.parentElement.classList.add('hide_column_name_input');
        discard_changes.parentElement.classList.add('hide_submit-button');
        discard_changes.parentElement.classList.add('hide_delete-button');
        discard_changes.parentElement.classList.remove('verify-delete');
    }

    if (focused.classList.contains('column-title') &&
        focused.classList.contains('input-field')) {

        column_title = focused;

        if (column_title.value.toString() !== '') {
            if (column_title.value.toString() !== '') {
                column_title.parentElement.classList.remove('hide_submit-button');
                column_title.parentElement.classList.add('hide_delete-button');
            } else {
                column_title.parentElement.classList.add('hide_submit-button');
                column_title.parentElement.classList.add('hide_delete-button');
            }
        } else {
            column_title.parentElement.classList.add('hide_submit-button');
            column_title.parentElement.classList.remove('hide_delete-button');
        }
    }

    if (focused.classList.contains('card-title') &&
        !focused.parentElement.classList.contains('new_card')) {
        card_title = focused;
        if (card_title.value.toString() !== '') {
            if (card_title.defaultValue.toString() !== focused.value.toString()) {
                card_title.parentElement.classList.remove('hide_submit-card-button');
                card_title.parentElement.classList.add('hide_delete-card-button');
            } else {
                card_title.parentElement.classList.add('hide_submit-card-button');
                card_title.parentElement.classList.add('hide_delete-card-button');
            }
        } else {
            card_title.parentElement.classList.add('hide_submit-card-button');
            card_title.parentElement.classList.remove('hide_delete-card-button');
        }

        card_title.parentElement.classList.remove('hide_modify-card-button');
    }

    if (focused.classList.contains('new_column-title')) {
        new_column_title = focused;
        if (new_column_title.value.toString() !== '') {
            new_column_title.parentElement.classList.remove('hide_submit-button');
        } else {
            new_column_title.parentElement.classList.add('hide_submit-button');
        }
    }
}

function open_delete_prompt(event, del_btn) {
    if (del_btn.parentElement.classList.contains('verify-delete') === false) {
        event.preventDefault();
        del_btn.parentElement.classList.add('verify-delete');
    }
}

function verify_text_inserted(event, sub_btn) {
    let input_text = sub_btn.prev('input').value.toString();

    if (input_text === '' || input_text === sub_btn.parent().find("h1").innerHTML.toString()) {
        event.preventDefault();
        return false
    }
}

jQuery(document).ready(function($) {

    // {# disabilita il tasto invio per form cambio nome colonna #}
    $('.prevent_submit_on_enter_press').on('keyup keypress', function(e) {
        let keyCode = e.keyCode || e.which;
        if (keyCode === 13) {
            e.preventDefault();
            return false;
        }
    });

    let hide_form_class = 'compressed';

    // smooth scroll quando si aprono form per nuova card e nuova colonna
    $('.new_column-title').on('focus', function(e) {
        e.preventDefault();
        this.scrollIntoView({behavior: 'smooth', block: "end"});
    });

    $('.card-title.new_card').on('focus', function(e) {
        e.preventDefault();
        this.closest("form").classList.remove(hide_form_class);
        this.scrollIntoView({behavior: 'smooth', block: "center"});
    });

    // chiusura form nuova card
    $('.close_new_card_form').on('click', function(e) {
        e.preventDefault();
        this.closest("form").classList.add(hide_form_class);
    });
});