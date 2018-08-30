hamb = $('.hambbutton a');

hamb.on('click', function(e) {
    e.preventDefault();
    $(this).toggleClass('animate');
    $('span').toggleClass('back');
    $('.toolbar').toggleClass('hidden');
    $('.toolbar-container').toggleClass('expanded');
});

// {# quando si clicca un elemento della toolbox essa si chiude #}
$('.toolbar-item').on('click', function (e) {
    $(this).toggleClass('animate');
    $('span').toggleClass('back');
    $('.toolbar').toggleClass('hidden');
    $('.toolbar-container').toggleClass('expanded');
});