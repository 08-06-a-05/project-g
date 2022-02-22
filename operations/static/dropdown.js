var add_category = document.getElementById("new_category");
var category = document.getElementById("category");
var swap_button = document.getElementById('swap-category');
var exist_category = document.getElementById('id_category');
var new_category = document.getElementById('new-category');
swap_button.addEventListener("click", function (event) {
    if (swap_button.textContent == "Добавить категорию"){
        category.style.display = "none";
        add_category.style.display = "flex";
        swap_button.textContent="Выбрать из уже существующих";
        swap_button.style.width = "60%";
        exist_category.value="";
    } else {
        category.style.display = "flex";
        add_category.style.display = "none";
        swap_button.textContent="Добавить категорию";
        swap_button.style.width = "40%";
        new_category.value="";
    }
});

var select_currency= document.getElementById("select_currency");

var operations_date = document.getElementById("operations_date");
operations_date.addEventListener("change",function(){
    if (operations_date.value){
        operations_date.style.color="#444";
    } else {
        operations_date.style.color="#999";
    }
});

function show_operation_information(category, amount, currency, description, date){
    var root = document.getElementById("root");
    root.style="filter:blur(15px); pointer-events: none";
    var operation_details = document.getElementById('operation_information');
    var operation_date = document.getElementById('operation_information_date');
    var operation_currency = document.getElementById('operation_information_currency');
    var operation_category = document.getElementById('operation_information_category');
    var operation_amount = document.getElementById('operation_information_amount');
    var operation_description = document.getElementById('operation_information_description');
    operation_date.textContent = "Дата:"+date;
    operation_amount.textContent = "Сумма:"+amount;
    operation_category.textContent = "Категория:"+category;
    operation_description.textContent = "Описание:"+description;
    operation_currency.textContent = "Валюта:"+currency;
    operation_details.style.display = "flex";
};
function close_information(){
    var operation_details = document.getElementById('operation_information');
    operation_details.style.display = "none";
    var root = document.getElementById("root");
    root.style="filter:none; pointer-events: auto";
}