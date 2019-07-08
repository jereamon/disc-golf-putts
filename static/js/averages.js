var avgSelectors = document.querySelectorAll('.putt-avgs-selection p'),
    todayAvgContainer = document.querySelector('.today-avg-container'),
    allTimeAvgContainer = document.querySelector('.all-time-avg-container');

avgSelectors.forEach(function (avgSelector) {
    avgSelector.addEventListener('click', function () {
        avgSelectors.forEach(function (avgSelector) {
            avgSelector.classList.remove('active-avg-selection')
        })
        this.classList.add('active-avg-selection');

        if (this.innerText.indexOf("Today's") >= 0) {
            todayAvgContainer.classList.remove('hidden-avg-container')
            allTimeAvgContainer.classList.add('hidden-avg-container')
        } else {
            todayAvgContainer.classList.add('hidden-avg-container')
            allTimeAvgContainer.classList.remove('hidden-avg-container')
        }
    })
})