//google.load('visualization', '1.0', {'packages':['corechart']});
//google.setOnLoadCallback(initialization);
var type='';
var income_data = []
var budget_data = []
var categories_data = []
var category_currency = '';
var income_currency = '';
function initialization(list_income,list_budget,list_categories,list_monthly_outlay, exchanged_list, income_cur, wal_type, cat_cur){
    income_data = list_income;
    budget_data = list_budget;
    categories_data = list_categories;
    exchanged_data = exchanged_list;
    monthly_outlay_data = list_monthly_outlay;
    income_data.unshift(['Дата', 'Доходы/Расходы']);
    budget_data.unshift(['Дата', 'Сумма']);
    categories_data.unshift(['Трата', '%']);
    monthly_outlay_data.unshift(['', '']);
    exchanged_data.unshift(['Валюта','%']);
    income_currency = String(income_cur);
    category_currency = cat_cur
    type = wal_type;
    drawChart();
    drawChart2();
    drawChart3();
    drawChart4();
}

function drawChart4() {
    var data = google.visualization.arrayToDataTable(monthly_outlay_data);
    
    var options = {
        label: 'Прямая линейной регресии',
        title: 'Прямая линейной регресии',
        // width: '400',
        height: '400',
        hAxis: {
            title: 'День',
        },
        vAxis: {
            title: 'Трата',
        },
        legend: {
            position: 'none'
        },
        trendlines: {
            0: {
            visibleInLegend: 'none',
            title: 'Прямая линейной регресии'
            }
        }
    };
  
    var chart = new google.visualization.ScatterChart(document.getElementById('graph4'));
    chart.draw(data, options);
}

function drawChart3() {
    var data3 = google.visualization.arrayToDataTable(categories_data);
    var options3 = {
        title: category_currency,
        is3D: true,
        pieResidueSliceLabel: 'Остальное',
        // width: '400',
        height: '400',
        chartArea: {width: '90%'},
        };
    var chart3 = new google.visualization.PieChart(document.getElementById('graph3'));
    chart3.draw(data3, options3);
};

function drawChart2(){
    var data2 = google.visualization.arrayToDataTable(exchanged_data);
    var options2 = {
    is3D: true,
    title: 'Состояние кошелька',
    // width: '400',
    height: '400',
    legend: 'none',
    chartArea: {width: '90%'},
    };
    var chart2 = new google.visualization.PieChart(document.getElementById('graph2'));
    chart2.draw(data2, options2);
}

function drawChart() {
    var data = google.visualization.arrayToDataTable(income_data);
    var options = {
    title: type,
    hAxis: {title: 'Дата'},
    vAxis: {title: income_currency},
    // width: '400',
    height: '400',
    legend: 'none',
    chartArea: {width: '70%'},
    };
    var chart = new google.visualization.ColumnChart(document.getElementById('graph'));
    chart.draw(data, options);
}
document.addEventListener("DOMContentLoaded", scroll_to_down);

function scroll_to_down(){
    var scroll_top = document.getElementById('scroll-name');
    if (window.location.href.indexOf('scroll-date')!=-1){
        scroll_top.scrollIntoView();
    }
}
