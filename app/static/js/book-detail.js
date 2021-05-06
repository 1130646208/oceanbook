

$(document).on('confirmation', '.remodal', function () {
    var book_id = $('#book-id').text()
    window.location.href='/gifts/book/' + book_id
});