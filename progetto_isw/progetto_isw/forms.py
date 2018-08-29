from django import forms
from models import Board, Column, Card


class LoginForm(forms.Form):
    login_username = forms.CharField(
        label="Username",
        max_length=32,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'forms_field-input',
                   'placeholder': 'Username',
                   'required': 'true',
                   'autofocus': 'true'}
        )
    )

    login_password = forms.CharField(
        label="Password",
        max_length=32,
        required=True,
        widget=forms.PasswordInput(
            attrs={'class': 'forms_field-input',
                   'placeholder': 'Password',
                   'required': 'true'}
        )
    )


class SignupForm(forms.Form):
    signup_username = forms.CharField(
        label="Username",
        max_length=32,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'forms_field-input',
                   'placeholder': 'Username',
                   'required': 'true',
                   'autofocus': 'true'}
        )
    )

    signup_password = forms.CharField(
        label="Password",
        max_length=32,
        required=True,
        widget=forms.PasswordInput(
            attrs={'class': 'forms_field-input',
                   'placeholder': 'Password',
                   'required': 'true'}
        )
    )

    signup_password_confirm = forms.CharField(
        label="Repeat Password",
        max_length=32,
        widget=forms.PasswordInput(
            attrs={'class': 'forms_field-input',
                   'placeholder': 'Repeat Password',
                   'required': 'true'}
        )
    )


class BoardCreationForm(forms.Form):
    board_name = forms.CharField(
        label="Board Name",
        max_length=512,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form_popup_field-input',
                   'placeholder': 'New board name',
                   'title': 'Choose a name for the new board.',
                   'required': 'true',
                   'autofocus': 'true'}
        )
    )


class BoardNameModificationForm(forms.Form):
    new_board_name = forms.CharField(
        label="Board Name",
        max_length=512,
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'board-title input-field',
                   'placeholder': 'New board name',
                   'title': 'Choose a new name for the board.',
                   'autofocus': 'true',
                   'onkeyup': 'manage_board_modifications(this);'}
        )
    )


class ColumnCreationForm(forms.Form):
    column_name = forms.CharField(
        label="Column Name",
        max_length=512,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'new_column-title',
                   'placeholder': '+ New Column',
                   'title': 'Choose a name for the new column.',
                   'onkeyup': 'show_button(this)'}
        )
    )


class ColumnNameModificationForm(forms.Form):
    new_column_name = forms.CharField(
            label="Column name",
            max_length=512,
            required=False,
            widget=forms.TextInput(
                attrs={'class': 'column-title input-field',
                       'placeholder': 'New Column Name',
                       'title': 'Choose a new name for this column.',
                       'onkeyup': 'show_button(this)'}
            )
        )


class CardCreationForm(forms.Form):
    new_card_title = forms.CharField(
            label="New Card Title",
            max_length=512,
            required=True,
            widget=forms.TextInput(
                attrs={'class': 'card-title new_card prevent_submit_on_enter_press',
                       'onkeyup': 'show_button(this)',
                       'onclick': 'show_button(this)',
                       'placeholder': 'New Card Title',
                       'title': 'Insert a title for the new card.'}
            )
        )

    new_card_description = forms.CharField(
        label="New Card Description",
        max_length=8048,
        required=True,
        widget=forms.Textarea(
            attrs={'class': 'new_card_description_input',
                   'placeholder': 'New Card Description',
                   'title': 'Insert a description for the new card.'}
        )
    )

    new_card_expire_date = forms.DateField(
        label="New Card Expire Date",
        required=True,
        widget=forms.DateInput(
            attrs={'class': 'new_card_expire_date_input prevent_submit_on_enter_press',
                   'type': 'date',
                   'value': '1996-06-03',
                   'title': 'Choose an expire date for the new card.'}
        )
    )

    new_card_story_points = forms.IntegerField(
        label="New Card Story Points",
        required=True,
        widget=forms.NumberInput(
            attrs={'class': 'new_card_story_points_input prevent_submit_on_enter_press',
                   'type': 'number',
                   'placeholder': 'Be optimistic, but not too much...',
                   'title': 'Choose a story point value for the new card.'}
        )
    )


# Funzione utilizzata per ottenere la lista di tuple (id, nome) di cards in una board.
# Se viene passato anche l'ID di una colonna come secondo parametro, per rendere la lista piu' user friendly,
# salvera' il nome della colonna con ID == ID_fornito come 'Invariato'
def get_available_columns_choices(board_id, current_mother_column=None):
    board = Board.objects.get(pk=board_id)
    available_columns = Column.objects.all().filter(mother_board=board)

    choices = [(column.id, "Unchanged" if current_mother_column is not None and column.id == current_mother_column else column.name) for column in available_columns]
    # print('mother column ' + current_mother_column.__str__())

    return choices


class CardModificationForm(forms.Form):
    def __init__(self, board_id, card_id, *args, **kwargs):
        super(CardModificationForm, self).__init__(*args, **kwargs)

        # cerca la card in modo da popolare i form con i dati gia' registrati
        this_card = Card.objects.get(pk=card_id)

        self.fields['new_card_title'] = forms.CharField(
            label="New Card Title",
            max_length=512,
            required=False,
            widget=forms.TextInput(
                attrs={'class': 'card-title prevent_submit_on_enter_press',
                       'value': this_card.title,
                       'title': 'Maybe this card deserve a better title.'}
            )
        )

        self.fields['new_card_description'] = forms.CharField(
            label="New Card Description",
            max_length=8048,
            initial='%s' % this_card.description,
            required=False,
            widget=forms.Textarea(
                attrs={'class': 'card_description_input',
                       'title': 'Change the description for this card.'}
            )
        )

        self.fields['new_card_expire_date'] = forms.DateField(
            label="New Card Expire Date",
            required=False,
            widget=forms.DateInput(
                attrs={'class': 'card_expire_date_input prevent_submit_on_enter_press',
                       'type': 'date',
                       'value': this_card.expire_date,
                       'title': 'Do you need more time?'}
            )
        )

        self.fields['new_card_story_points'] = forms.IntegerField(
            label="New Card Story Points",
            required=False,
            widget=forms.NumberInput(
                attrs={'class': 'card_story_points_input prevent_submit_on_enter_press',
                       'type': 'number',
                       'value': this_card.story_points,
                       'title': 'Choose a story point value for the new card.'}
            )
        )

        # ottengo la lista di colonne disponibili nella board e cerco quella in cui e' la carta che si sta modificando
        available_columns = get_available_columns_choices(board_id, this_card.mother_column.id)
        this_column_position_in_columns_list = 0

        for i, (a, b) in enumerate(available_columns):
            print (str('a: ' + a.__str__() + ', b: ' + b))
            if a == this_card.mother_column.id:
                this_column_position_in_columns_list = i

        self.fields['new_card_mother_column'] = forms.ChoiceField(
            choices=available_columns,
            initial=available_columns[this_column_position_in_columns_list],
            label="New mother Column",
            widget=forms.Select(
                attrs={'class': 'select-column',
                       'placeholder': 'New Card Title',
                       'title': 'Where do you want to put this card?'}
            )
        )


class SearchUserForm(forms.Form):
    user_name = forms.CharField(
        label="User name",
        max_length=512,
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'add_user_input',
                   'onkeyup': 'search_user();',
                   'placeholder': 'Search for users...',
                   'title': 'Search users to add.'}
        )
    )