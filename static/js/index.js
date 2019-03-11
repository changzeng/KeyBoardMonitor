function applyKeyboardData(){
// keyUsageData from https://codepen.io/Siilwyn/pen/RrNNvN.js

    /*
      Helper functions
    */
// Takes date object and returns string in YYYY-MM-DD format
    var getFormattedDate = function (date) {
        var yyyy = date.getFullYear().toString();
        var mm = (date.getMonth() + 1).toString();
        var dd = date.getDate().toString();
        if (mm.length == 1)
            mm = "0" + mm;
        if (dd.length == 1)
            dd = "0" + dd;

        var res = yyyy + '-' + mm + '-' + dd;
        return res;
    };

// Find the highest amount of keystrokes
// takes date object and JSON data
    var maxKeystrokes = function (date, data) {
        return d3.max(d3.values(data[date]));
    };

    /*
      Core
    */
// Fills in keys on keyboard figure in DOM
// takes date object and JSON data
    var mapDataToKeyboard = function (date, data) {
        date = getFormattedDate(date);

        var keyboard = d3.select('[data-keyboard]');
        var keys = keyboard.selectAll('div');
        var keyUsageDataDay = d3.entries(data[date]);

        // Set the correct scale to display range of colors
        var colorScale = d3.scale.linear()
            .domain([0, 10, maxKeystrokes(date, data)])
            .range(['#abb6dd', '#5775dd', '#0829dd']);

        keys.data(keyUsageDataDay, function (d) {
            // Bind the correct key to the data using the key text
            return (d && d.key) || this.getAttribute("key");
        })
            .style('background', function (d) {
                return colorScale(d.value);
            })
            .on('mouseover', function (d) {
                this.classList.add('key-is-active');
                this.txt = this.textContent;
                this.textContent = d.value;
            })
            .on('mouseout', function (d) {
                this.classList.remove('key-is-active');
                this.textContent = this.txt;
            });
    };

    /*
      Date selection
    */
    var nextDateButton = document.querySelector('[data-next-date]');
    var prevDateButton = document.querySelector('[data-prev-date]');

    var changeDate = function (operator) {
        var newDate = new Date(currentDate);

        newDate.setDate(operator(currentDate));

        if (keyUsageData[getFormattedDate(newDate)]) {

            currentDate = newDate;

            dateDisplay.textContent = getFormattedDate(currentDate);
            mapDataToKeyboard(currentDate, keyUsageData);
        }
    };

    prevDateButton.addEventListener('click', function () {
        changeDate(function (currentDate) {
            return currentDate.getDate() - 1;
        });
    });

    nextDateButton.addEventListener('click', function () {
        changeDate(function (currentDate) {
            return currentDate.getDate() + 1;
        });
    });

    /*
      Init
    */
    var currentDate = new Date()
    var dateDisplay = document.querySelector('[data-date]');
    dateDisplay.textContent = getFormattedDate(currentDate);
    mapDataToKeyboard(currentDate, keyUsageData);
}
