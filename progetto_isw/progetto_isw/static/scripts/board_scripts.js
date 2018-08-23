// gestione pulsanti nome colonna e cards
function show_button() {
    let focused = document.activeElement;
    let column_title;
    let card_title;
    let new_column_title;

    if (focused.classList.contains('column-title')) {
        column_title = focused;
        if (column_title.value.toString() !== '') {
            if (column_title.defaultValue.toString() !== column_title.value.toString()) {
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

    if (focused.classList.contains('card-title')) {
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
        focused.closest("li").classList.add('shadowed');
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