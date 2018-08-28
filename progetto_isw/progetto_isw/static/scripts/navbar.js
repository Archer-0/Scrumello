function manage_board_modifications(e) {
    let focused = document.activeElement;
    let board_title;
    let new_board_title;
    let edit_board;
    let discard_changes;

    if (focused.classList.contains('start_change_board_name')) {
        edit_board = focused;
        edit_board.parentElement.classList.remove('hide_board_name_input');
        edit_board.parentElement.classList.remove('hide_delete-button');
        edit_board.parentElement.classList.add('hide_board_name_link');
    }

    if (focused.classList.contains('discard_board_name_modifications')) {
        discard_changes = focused;
        discard_changes.parentElement.classList.remove('hide_board_name_link');
        discard_changes.parentElement.classList.add('hide_board_name_input');
        discard_changes.parentElement.classList.add('hide_submit-button');
        discard_changes.parentElement.classList.add('hide_delete-button');
        discard_changes.parentElement.classList.remove('verify-delete');
    }

    if (focused.classList.contains('board-title') &&
        focused.classList.contains('input-field')) {

        board_title = focused;
        if (board_title.value.toString() !== '') {
            board_title.parentElement.classList.remove('prevent_submit_on_enter_press');
            if (board_title.defaultValue.toString() !== board_title.value.toString()) {
                board_title.parentElement.classList.remove('hide_submit-button');
                board_title.parentElement.classList.add('hide_delete-button');
            } else {
                board_title.parentElement.classList.add('hide_submit-button');
                board_title.parentElement.classList.add('hide_delete-button');
            }
        } else {
            board_title.parentElement.classList.add('prevent_submit_on_enter_press');
            board_title.parentElement.classList.add('hide_submit-button');
            board_title.parentElement.classList.remove('hide_delete-button');
        }
    }

    if (focused.classList.contains('new_board-title')) {
        new_board_title = focused;
        if (new_board_title.value.toString() !== '') {
            new_board_title.parentElement.classList.remove('hide_submit-button');
        } else {
            new_board_title.parentElement.classList.add('hide_submit-button');
        }
    }
}

function open_delete_board_prompt(event, del_btn){
    if (del_btn.parentElement.classList.contains('verify-delete') === false) {
        event.preventDefault();
        del_btn.parentElement.classList.add('verify-delete');
    }
}

function verify_board_text_inserted(event, sub_btn) {
    if (sub_btn.prev().value === '') {
        event.preventDefault();
    }
}

$(document).ready(function() {
    var wasScrolled = false;

    window.scrollTo(0, 0);

    // {# disabilita il tasto invio per form cambio nome colonna #}
    $('.prevent_submit_on_enter_press').on('keyup keypress', function(e) {
        let keyCode = e.keyCode || e.which;
        if (keyCode === 13) {
            e.preventDefault();
            return false;
        }
    });

    $(window).on('scroll', function () {
        // {# quando si raggiunge il valore indicato di scroll la nav bar si contrae #}
        if (Math.round($(window).scrollTop()) > 50) {
            $('.navbar').addClass('scrolled');
            wasScrolled = true;
        }
        // {# la nav bar torna grande solo quando si torna in testa alla pagina #}
        if (Math.round($(window).scrollTop()) <= 1) {
            $('.navbar').removeClass('scrolled');
            if (wasScrolled === true) {
                window.scrollTo(0, 0);
                wasScrolled = false;
            }
        }
    });
});