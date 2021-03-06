window.onload = function() {
    var rawWorkoutItems = [];
    var workoutsByName = {};
    var workoutsNames = [];

    $.getJSON("/api/workout-item", function(data) {
        $.each(data, function(key, val) {
            val.forEach(function(valItem) {
                console.log(valItem);
                rawWorkoutItems.push(valItem);
                var workoutName = valItem["name"];
                console.log(workoutName);
                if (workoutsByName.hasOwnProperty(workoutName)) {
                    workoutsByName[workoutName].push(valItem["iterations_count"]);
                    console.log("add iterations_count");
                } else {
                    workoutsByName[workoutName] = [valItem["iterations_count"]];
                    workoutsNames.push(workoutName);
                    console.log("add workout name + iterations_count");
                }
            });
        });

        var axisYConfigs = [];
        var dataConfigs = [];
        var colors = ["#369EAD", "#C24642", "#7F6084"]
        workoutsNames.forEach(function(item, ind) {
            var newColor = colors[ind % 3];

            axisYConfigs.push({
                title: item,
                lineColor: newColor,
                tickColor: newColor,
                labelFontColor: newColor,
                titleFontColor: newColor,
                includeZero: true
            });

            var specifiedExerciseData = [];
            workoutsByName[item].forEach(function(workoutItem, workoutInd) {
                specifiedExerciseData.push({
                    x: workoutInd,
                    y: workoutItem
                });
            });
            dataConfigs.push({
                type: "line",
                name: item,
                color: newColor,
                showInLegend: true,
                axisYIndex: ind - 1,
                dataPoints: specifiedExerciseData
            });
        });

        console.log(workoutsByName);
        console.log(workoutsNames);

        var chart = new CanvasJS.Chart("chartContainer", {
            title: {
                text: "Workouts By Exercise Type"
            },
            axisY: axisYConfigs,
            toolTip: {
                shared: true
            },
            legend: {
                cursor: "pointer",
                itemclick: toggleDataSeries
            },
            data: dataConfigs
        });
        chart.render();
    });

    function toggleDataSeries(e) {
        if (typeof(e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
            e.dataSeries.visible = false;
        } else {
            e.dataSeries.visible = true;
        }
        e.chart.render();
    }

}
