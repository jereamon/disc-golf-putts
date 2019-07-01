$(function() {
    $('.test-ajax-button').click(function() {
        var putts_made = $('#no_putts').val();

        $.ajax({
            url: '/save_putt',
            data: $('.ajax-test-form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response)
            },
            error: function(error) {
                console.log(error)
            }
        });
    });
});