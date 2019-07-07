$(function () {
    $('.save-putt-button').click(function () {
        $.ajax({
            url: '/save_putt',
            data: {
                'putt-form': $('.save-putt-form').serialize(),
                'no_putts': $('.putts-made').val(),
                'distance': $('.distance').val(),
                'cur-dist': $('.cur-dist').val()
            },
            type: 'POST',
            success: function (response) {
                // console.log(response)
                $('.putts-made').val(0)
                $('.distance').val(9)

                parsed_response = JSON.parse(response)
                if (parsed_response['distance']) {
                    $('.cur-dist').text(parsed_response['distance'] + "'")
                }

                if (parsed_response['save_code']) {
                    $('.putt-save-container').css('background', '#009900')
                    $('.putt-save-success').css('display', 'block')
                    $('.putt-save-success').css('width', '150px')

                    $('.save-putt-form').css('display', 'none')



                    setTimeout(function () {
                        $('.save-putt-form').css('display', 'flex')

                        $('.putt-save-container').css('background', 'none')
                        $('.putt-save-success').css('display', 'none')
                    }, 2000)
                }

                /* ########################## */
                /* THIS UPDATES THE AVERAGES */
                avgsContainer = document.querySelector('.putt-avgs-inner-container')
                avgsContainer.classList.remove('hide-avgs-container');
                while (avgsContainer.firstChild) {
                    avgsContainer.removeChild(avgsContainer.firstChild)
                }

                var todayAvgs = parsed_response['today_avgs']
                for (var puttAvg of Object.entries(todayAvgs)) {
                    console.log(puttAvg)
                    puttAvgContainer = document.createElement('div')
                    puttAvgContainer.classList.add('putt-avg-container')

                    h5 = document.createElement('h5')
                    h5.innerText = puttAvg[0] + "'"

                    p = document.createElement('p')
                    p.innerText = puttAvg[1] + '%'

                    puttAvgContainer.appendChild(h5)
                    puttAvgContainer.appendChild(p)
                    avgsContainer.appendChild(puttAvgContainer)
                /* ########################## */
                }
            },
            error: function (error) {
                console.log(error)
            }
        });
    });
});