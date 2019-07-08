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
                todayAvgsContainer = document.querySelector('.today-avg-container')
                while (todayAvgsContainer.firstChild) {
                    todayAvgsContainer.removeChild(todayAvgsContainer.firstChild)
                }

                allTimeAvgsContainer = document.querySelector('.all-time-avg-container')
                while (allTimeAvgsContainer.firstChild) {
                    allTimeAvgsContainer.removeChild(allTimeAvgsContainer.firstChild)
                }

                var todayAvgs = parsed_response['today_avgs'],
                    allTimeAvgs = parsed_response['all_time_avgs'];

                for (var puttAvg of Object.entries(todayAvgs)) {
                    // console.log(puttAvg)
                    puttAvgTodayContainer = document.createElement('div')
                    puttAvgTodayContainer.classList.add('putt-avg-container')

                    puttAvgOuterContainer = document.createElement('div')
                    puttAvgOuterContainer.classList.add('putt-avg-outer-container')

                    h5 = document.createElement('h5')
                    h5.innerText = puttAvg[0] + "'"

                    p = document.createElement('p')
                    p.innerText = puttAvg[1] + '%'

                    puttAvgTodayContainer.appendChild(h5)
                    puttAvgTodayContainer.appendChild(p)
                    puttAvgOuterContainer.appendChild(puttAvgTodayContainer)
                    todayAvgsContainer.appendChild(puttAvgOuterContainer)
                /* ########################## */
                }

                for (var puttAvg of Object.entries(allTimeAvgs)) {
                    // console.log(puttAvg)
                    puttAvgContainer = document.createElement('div')
                    puttAvgContainer.classList.add('putt-avg-container')

                    puttAvgOuterContainer = document.createElement('div')
                    puttAvgOuterContainer.classList.add('putt-avg-outer-container')

                    h5 = document.createElement('h5')
                    h5.innerText = puttAvg[0] + "'"

                    p = document.createElement('p')
                    p.innerText = puttAvg[1] + '%'

                    puttAvgContainer.appendChild(h5)
                    puttAvgContainer.appendChild(p)
                    puttAvgOuterContainer.appendChild(puttAvgContainer)
                    allTimeAvgsContainer.appendChild(puttAvgOuterContainer)
                /* ########################## */
                }
            },
            error: function (error) {
                console.log(error)
            }
        });
    });
});