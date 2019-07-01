$(function () {
    $('.save-putt-button').click(function () {

        $.ajax({
            url: '/save_putt',
            data: {
                'putt-form': $('.save-putt-form').serialize(),
                'no_putts': $('.putts-made').val(),
                'cur-dist': $('.cur-dist').val()
            },
            type: 'POST',
            success: function (response) {
                // console.log(response)
                parsed_response = JSON.parse(response)
                $('.cur-dist').text(parsed_response['distance'] + "'")
                if (parsed_response['save_code']) {
                    $('.putt-save-container').css('background', '#009900')
                    $('.putt-save-success').css('display', 'block')
                    $('.putt-save-success').css('width', '150px')

                    setTimeout(function () {
                        $('.putt-save-container').css('background', 'none')
                        $('.putt-save-success').css('width', '0px')
                        setTimeout(function() {
                            $('.putt-save-success').css('display', 'none')
                        }, 150)
                    }, 2000)
                }
            },
            error: function (error) {
                console.log(error)
            }
        });
    });
});