window.onload = function (ev) {
    $.get("/keyboard_usage_data", function (data) {
        pageData = data;
        // keyUsageData = data["daily_log_time"];
        keyUsageData = data["daily_press_time"];
        applyKeyboardData();
        // $(".loading").css("display", "none");
        $(".loading").animate({"opacity": 0}, 500, function () {
            $(this).css("display", "none");
            $(".content").css("display", "block").animate({"opacity": 1});
        });
    })
}