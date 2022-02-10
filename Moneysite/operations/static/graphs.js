google.load("visualization", "1", {packages:["corechart"]});
var type='Доходы';
var list=[['Месяц', 'Доходы'],
            ['сентябрь', 1200],
            ['октябрь', 2000],
            ['ноябрь', 1210]];
var list2=[['День', 'Сумма'],
            ['01.03.2021', 12200],
            ['02.03.2021', -2000],
            ['07.03.2021', 5210]];
var button = document.getElementById('type');
google.setOnLoadCallback(drawChart);
google.setOnLoadCallback(drawChart2);
google.setOnLoadCallback(drawChart3);


function drawChart3() {
    var data3 = google.visualization.arrayToDataTable([
        ['Трата', '%'],
        ['Рестораны',     9],
        ['Такси', 10],
        ['Магазины одежды',    30],
        ['Продуктовые магазины', 20],
        ['Продуктовые магазины', 20],
        ['Коммунальные платежы', 11]
        ]);
    var options3 = {
        is3D: true,
        pieResidueSliceLabel: 'Остальное',
        width: '400',
        height: '400',
        chartArea: {width: '100%'},
        };
    var chart3 = new google.visualization.PieChart(document.getElementById('graph3'));
    chart3.draw(data3, options3);
};

function drawChart2(){
    var data2 = google.visualization.arrayToDataTable(list2);
    var options2 = {
    title: 'Состояние кошелька',
    hAxis: {title: 'День'},
    vAxis: {title: 'USD($)'},
    width: '400',
    height: '400',
    legend: 'none',
    chartArea: {width: '100%'},
    };
    var chart2 = new google.visualization.ColumnChart(document.getElementById('graph2'));
    chart2.draw(data2, options2);
}

function drawChart() {
    var data = google.visualization.arrayToDataTable(list);
    var options = {
    title: type,
    hAxis: {title: 'Месяц'},
    vAxis: {title: 'USD($)'},
    width: '400',
    height: '400',
    legend: 'none',
    chartArea: {width: '100%'},
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