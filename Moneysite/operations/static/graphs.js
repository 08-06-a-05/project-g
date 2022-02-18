google.load("visualization", "1", {packages:["corechart"]});
var type='Доходы';
var income_data = []
var outlay_data = []
var budget_data = []
var categories_data = []
function initialization(list_income,list_outlay,list_budget,list_categories,list_monthly_outlay,list_line_dots){
    income_data = list_income;
    outlay_data = list_outlay;
    budget_data = list_budget;
    categories_data = list_categories;
    monthly_outlay_data = list_monthly_outlay;
    line_dots_data = list_line_dots;
    income_data.unshift(['Дата', 'Доходы']);
    outlay_data.unshift(['Дата', 'Расходы']);
    budget_data.unshift(['Дата', 'Сумма']);
    categories_data.unshift(['Трата', '%']);
    monthly_outlay_data.unshift(['День', 'Количество'])
    drawChart();
    drawChart2();
    drawChart3();
    drawChart4();
}
/*[
        ['Трата', '%'],
        ['Рестораны',     9],
        ['Такси', 10],
        ['Магазины одежды',    30],
        ['Продуктовые магазины', 20],
        ['Продуктовые магазины', 20],
        ['Коммунальные платежы', 11]
        ]);*/

var use = 0;
var button = document.getElementById('type');

function drawChart4() {
    var scatter = google.visualization.arrayToDataTable(monthly_outlay_data)
    var line = new google.visualization.DataView(scatter);
    line.setColumns([100, 200, {
        type: 'number',
        calc: function (dt, row) {
            console.log(dt, row)
          return dt.getValue(row, 0)
        }
    }]);

    var options4 = {
        title: 'Прогноз месячных расходов',
        width: '400',
        height: '400',

        hAxis: {minValue: 1, maxValue: 30},
        vAxis: {minValue: 1, maxValue: 30},

        seriesType: 'scatter',
        series: {
            1: {
                type: 'line'
            }
        }
    };

    var chart4 = new google.visualization.ComboChart(document.getElementById('graph4'));
    chart4.draw(line, options4);
};

function drawChart3() {
    var data3 = google.visualization.arrayToDataTable(categories_data);
    var options3 = {
        is3D: true,
        pieResidueSliceLabel: 'Остальное',
        width: '400',
        height: '400',
        chartArea: {width: '90%'},
        };
    var chart3 = new google.visualization.PieChart(document.getElementById('graph3'));
    chart3.draw(data3, options3);
};

function drawChart2(){
    var data2 = google.visualization.arrayToDataTable(budget_data);
    var options2 = {
    title: 'Состояние кошелька',
    hAxis: {title: 'День'},
    vAxis: {title: 'USD($)'},
    width: '400',
    height: '400',
    legend: 'none',
    chartArea: {width: '70%'},
    };
    var chart2 = new google.visualization.LineChart(document.getElementById('graph2'));
    chart2.draw(data2, options2);
}

function drawChart() {
    if (use == 0){
        var data = google.visualization.arrayToDataTable(income_data);
    } else {
        var data = google.visualization.arrayToDataTable(outlay_data);
    }
    var options = {
    title: type,
    hAxis: {title: 'Месяц'},
    vAxis: {title: 'USD($)'},
    width: '400',
    height: '400',
    legend: 'none',
    chartArea: {width: '70%'},
    };
    var chart = new google.visualization.ColumnChart(document.getElementById('graph'));
    chart.draw(data, options);
}


button.addEventListener("change", function (event) {
    if (button.value=='Доходы'){
        use = 0;
        type='Доходы';
    } else {
        use = 1;
        type='Расходы';
    }
    drawChart();
});