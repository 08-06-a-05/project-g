//google.load('visualization', '1.0', {'packages':['corechart']});
//google.setOnLoadCallback(initialization);
var type='Доходы';
var income_data = []
var budget_data = []
var categories_data = []

function initialization(list_income,list_budget,list_categories,list_monthly_outlay,list_coefficients){
    income_data = list_income;
    budget_data = list_budget;
    categories_data = list_categories;
    monthly_outlay_data = list_monthly_outlay;
    coefficients = list_coefficients
    income_data.unshift(['Дата', 'Доходы']);
    budget_data.unshift(['Дата', 'Сумма']);
    categories_data.unshift(['Трата', '%']);
    monthly_outlay_data.unshift(['', ''])
    //drawChart();
    drawChart3();
    drawChart4();
}

function drawChart4() {
    var data = google.visualization.arrayToDataTable(monthly_outlay_data);
    
    var options = {
        label: 'Прямая линейной регресии',
        title: 'Прямая линейной регресии',
        width: '400',
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
    if (window.location.href.indexOf('category-currency=')!=-1){
        var category_currency = window.location.href.substr(window.location.href.indexOf('category-currency=')+18,3)
    } else {
        var category_currency = 'RUB'
    }
    var data3 = google.visualization.arrayToDataTable(categories_data);
    var options3 = {
        title: category_currency,
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
    if (window.location.href.indexOf('type=Расходы')!=-1){
        type = 'Расходы';
    } else {
        type = 'Доходы';
    }
    if (window.location.href.indexOf('wallet-currency=')!=-1){
        var wallet_currency = window.location.href.substr(window.location.href.indexOf('wallet-currency=')+16,3)
    } else {
        var wallet_currency = 'RUB'
    }
    var data = google.visualization.arrayToDataTable(income_data);
    var options = {
    title: type,
    hAxis: {title: 'Месяц'},
    vAxis: {title: wallet_currency},
    width: '400',
    height: '400',
    legend: 'none',
    chartArea: {width: '70%'},
    };
    var chart = new google.visualization.ColumnChart(document.getElementById('graph'));
    chart.draw(data, options);
}
var scroll = document.getElementById('percent-scroll');
var scroll_label = document.getElementById('scroll-label');
scroll.addEventListener("change", function() {
    scroll_label.textContent = scroll.value+"%";
});