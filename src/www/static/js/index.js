/**
 * Created by Javier on 03/05/2017.
 */

function insertElements(data) {
    var collections = $('#collections');
    var buttons = $('#buttons');
    buttons.empty();
    if (data.previous) {
         var prev = $('<a type="button" class="btn btn-primary" href="#">Prev</a>')
             .click({'url': data.previous}, onClickButton);
         buttons.append(prev);
    }
    if (data.next) {
        var next = $('<a type="button" class="btn btn-primary" href="#">Next</a>')
            .click({'url': data.next}, onClickButton);
        buttons.append(next);
    }
    collections.html(JSON.stringify(data.results, undefined, 2));
}

function onClickSideVar(event) {
    $.get('/api/v1/extract/data/?collection=' + event.data.collection, insertElements);
}

function onClickButton(event) {
    $.get(event.data.url, insertElements);
}

$.get('/api/v1/extract/data/', function (data) {
    for (var i = 0; i < data.length; i++) {
        var element = $('<li><a href="#">' + data[i] + '</a></li>')
            .click({'collection': data[i]}, onClickSideVar);
        $('#sidebar').append(element);
    }
});
