google.load("visualization", "1", {packages:["corechart"]});
var type='Доходы';
var list=[['Месяц', 'Доходы'],
            ['сентябрь', 1200],
            ['октябрь', 2000],
            ['ноябрь', 1210]];
var button = document.getElementById('type');
google.setOnLoadCallback(drawChart);

function drawChart() {
    var data = google.visualization.arrayToDataTable(list);
    var options = {
    title: type,
    hAxis: {title: 'Месяц'},
    vAxis: {title: 'USD($)'},
    width: '400',
    height: '400',
    legend: 'none',
    };
    var chart = new google.visualization.ColumnChart(document.getElementById('graph'));
    chart.draw(data, options);
}


button.addEventListener("change", function (event) {
    if (button.value=='Доходы'){
        list=[
            ['Месяц', 'Доходы'],
            ['сентябрь', 1200],
            ['октябрь', 2000],
            ['ноябрь', 1210]
            ];
        type='Доходы';
    } else {
        list=[
            ['Месяц', 'Расходы'],
            ['сентябрь', 32200],
            ['октябрь', 232000],
            ['ноябрь', 12410]
            ];
        type='Расходы';
    }
    drawChart();
});