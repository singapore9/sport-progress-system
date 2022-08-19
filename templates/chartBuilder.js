function onlyDate(datetime) {
    datetime.setMilliseconds(0);
    datetime.setSeconds(0);
    datetime.setMinutes(0);
    datetime.setHours(0);
}

function tabataChart(sinceDate, workoutItemsData, toggleFunction) {
    let workouts = [];
    let exerciseName = "tabata";
    let color = "#369EAD";

    $.each(workoutItemsData, function(key, val) {
        if (val['name'] !== exerciseName) {
            return;
        }
        workouts.push([
            val["iterations_count"],
            val["timestamp"]
        ]);
    });

    let specifiedExerciseData = [];
    workouts.forEach(function(workoutItem, workoutInd) {
        let itemDate = new Date(1000 * workoutItem[1]);
        if (itemDate > sinceDate) {
            onlyDate(itemDate);
            specifiedExerciseData.push({
                x: itemDate,
                y: 1
            });
        }
    });
    specifiedExerciseData.sort((a, b) => a['x'] - b['x']);

    dataConfigs = [{
        type: "column",
        name: exerciseName,
        color: color,
        showInLegend: true,
        axisYIndex: -1,
        dataPoints: specifiedExerciseData
    }];

    let axisYConfigs = [{
        includeZero: true
    }];
    let chart = new CanvasJS.Chart("tabataChartContainer", {
        title: {
            text: "Tabata by Day"
        },
        axisY: axisYConfigs,
        toolTip: {
            shared: true
        },
        legend: {
            cursor: "pointer",
            itemclick: toggleFunction
        },
        data: dataConfigs
    });
    chart.render();
}

function calculateAvgMaxSum(sinceDate, workoutItemsData, exerciseName) {
    let workoutsByDate = {};
    let filteredWorkoutItems = [];
    let dates = [];
    let calculationsByDate = {};

    $.each(workoutItemsData, function(key, val) {
        if (val['name'] !== exerciseName) {
            return;
        }
        workoutItemDate = new Date(1000 * val['timestamp']);
        onlyDate(workoutItemDate);
        let workoutTimestamp = String(workoutItemDate.getTime());

        if (workoutsByDate.hasOwnProperty(workoutTimestamp)) {
            workoutsByDate[workoutTimestamp].push(
                val["iterations_count"]
            );
        } else {
            workoutsByDate[workoutTimestamp] = [
                val["iterations_count"]
            ];
            dates.push(workoutTimestamp);
        }
    });

    dates.forEach(function(item, ind) {
        let iterationsArray = workoutsByDate[item];
        let iterationsSum = iterationsArray.reduce((partialSum, a) => partialSum + a, 0);
        let iterationsMax = Math.max(...iterationsArray);
        let iterationsAvg = iterationsSum / iterationsArray.length;
        calculationsByDate[item] = [iterationsAvg, iterationsMax, iterationsSum];
    });
    return calculationsByDate;
}

function makeExerciseDetailedChart(exerciseName, exerciseDisplayName, chartId, sinceDate, workoutItemsData, toggleFunction) {
    let calculationsByDate = calculateAvgMaxSum(sinceDate, workoutItemsData, exerciseName);
    let colors = ["#369EAD", "#C24642", "#7F6084"];
    let prefixes = ["Average ", "Max ", "Total "];

    let axisYConfigs = [];
    let dataConfigs = [];
    let maxY = 0;

    colors.forEach(function(item, ind) {
        let title = prefixes[ind] + exerciseDisplayName;

        let specifiedExerciseData = [];
        for (const property in calculationsByDate) {
            let date = new Date(Number(property))
            specifiedExerciseData.push({
                'x': date,
                'y': calculationsByDate[property][ind]
            });
            if (calculationsByDate[property][ind] > maxY) {
                maxY = calculationsByDate[property][ind];
            }
        }

        specifiedExerciseData.sort((a, b) => a['x'] - b['x']);
        dataConfigs.push({
            type: "line",
            name: title,
            color: item,
            showInLegend: true,
            axisYIndex: ind - 1,
            dataPoints: specifiedExerciseData
        });
    });

    axisYConfigs = [{
        includeZero: true,
        maximum: maxY * 1.1
    }];
    dataConfigs[1].visible = false;

    let chart = new CanvasJS.Chart(chartId, {
        title: {
            text: "Detailed " + exerciseDisplayName
        },
        axisY: axisYConfigs,
        toolTip: {
            shared: true
        },
        legend: {
            cursor: "pointer",
            itemclick: toggleFunction
        },
        data: dataConfigs
    });
    chart.render();
}

function pullupsChart(sinceDate, workoutItemsData, toggleFunction) {
    let exerciseName = "pull-ups";
    let exerciseDisplayName = "Pull Ups";
    let chartId = "pullupsChartContainer";
    makeExerciseDetailedChart(exerciseName, exerciseDisplayName, chartId, sinceDate, workoutItemsData, toggleFunction);
}


function legsraisesChart(sinceDate, workoutItemsData, toggleFunction) {
    let exerciseName = "legs_raises";
    let exerciseDisplayName = "Legs Raises";
    let chartId = "legsraisesChartContainer";
    makeExerciseDetailedChart(exerciseName, exerciseDisplayName, chartId, sinceDate, workoutItemsData, toggleFunction);

}

window.onload = function() {
    let monthAgo = new Date();
    monthAgo.setMonth(monthAgo.getMonth() - 1);
    let userFilter = location.search.slice(1);
    let filteredWorkoutItems = [];

    $.getJSON("/api/workout-item", function(data) {
        $.each(data, function(key, val) {
            val.forEach(function(valItem) {
                if (valItem['user_id'] !== userFilter) {
                    return;
                }
                filteredWorkoutItems.push(valItem);
            })
        });
        tabataChart(monthAgo, filteredWorkoutItems, toggleDataSeries);
        pullupsChart(monthAgo, filteredWorkoutItems, toggleDataSeries);
        legsraisesChart(monthAgo, filteredWorkoutItems, toggleDataSeries);
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
