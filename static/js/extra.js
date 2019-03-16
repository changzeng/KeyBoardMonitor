function echarts_plot() {
    var my_chart = echarts.init(document.getElementById("press-time-visualization"));
    var xAxisData = [];
    var data1 = [];
    var data2 = [];
    var daily_press_time = pageData["daily_press_time"];
    var daily_log_time = pageData["daily_log_time"]
    for (var i = 0; i < daily_press_time.length; i++) {
        xAxisData.push(daily_press_time[i][0]);
        data1.push(daily_press_time[i][1]);
        data2.push(daily_log_time[i][1])
    }
    option = {
        title: {
            text: '键盘数据统计(天)'
        },
        legend: {
            data: ['键盘按压总时间(s)', '键盘按压总次数'],
            align: 'left'
        },
        toolbox: {
            feature: {
                magicType: {
                    type: ['stack', 'tiled']
                },
                dataView: {},
                saveAsImage: {
                    pixelRatio: 2
                }
            }
        },
        tooltip: {},
        xAxis: {
            data: xAxisData,
            silent: false,
            splitLine: {
                show: false
            }
        },
        yAxis: {
        },
        series: [
            {
                name: '键盘按压总时间(s)',
                type: 'bar',
                data: data1,
                animationDelay: function (idx) {
                    return idx * 10;
                }
            },
            {
                name: '键盘按压总次数',
                type: 'bar',
                data: data2,
                animationDelay: function (idx) {
                    return idx * 10;
                }
            }
        ],
        animationEasing: 'elasticOut',
        animationDelayUpdate: function (idx) {
            return idx * 5;
        }
    };
    my_chart.setOption(option);
}

function render_data() {
    // 绘制echarts可视化图形
    echarts_plot()
}

window.onload = function (ev) {
    $.get("/keyboard_usage_data", function (data) {
        pageData = data;
        // keyUsageData = data["daily_log_time"];
        keyUsageData = data["daily_press_time_each_key"];
        applyKeyboardData();
        // $(".loading").css("display", "none");
        $(".loading").animate({"opacity": 0}, 500, function () {
            $(this).css("display", "none");
            $(".content").css("display", "block").animate({"opacity": 1});
            render_data();
        });
    })
}