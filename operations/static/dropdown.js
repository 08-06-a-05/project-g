var add_category = document.getElementById("new_category");
var category = document.getElementById("category");
var swap_button = document.getElementById('swap-category');
var new_category = document.getElementById('new-category');
var operations_category = document.getElementById('operations_category');
swap_button.addEventListener("click", function (event) {
    console.log(operations_category.options[operations_category.selectedIndex].text)
    if (swap_button.textContent == "Добавить категорию"){
        //operations_category.value = "";
        category.style.display = "none";
        add_category.style.display = "flex";
        swap_button.textContent="Выбрать из уже существующих";
        swap_button.style.width = "60%";
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
/*
amount.addEventListener("blur", function (event) {
    if (!email.value){
        error_email_message.textContent="Пожалуйста, введите email";
        perekras(email_line,error_email_message,false);
    } else {
        send_JSON();
    }
});*/

function perekras(err_mes,type){
    if (!type){
        err_mes.style.visibility = "visible";
        err_mes.style.opacity = "1";
    } else {
        err_mes.style.visibility = "hidden";
        err_mes.style.opacity = "0";
    }
}

function validation(){
    var add_amount = document.getElementById('id_amount');
    var error_amount_message=document.getElementById('error_amount_message')
    //var choose_or_add_category = document.getElementById('operations_category')
    if (!add_amount.value){

        return false;
    }
    else {
        val = add_amount.value
        if (!isNaN(val)){
            val = parseFloat(val);
            add_amount.value = val.toFixed(2);
            perekras(error_amount_message,true)
            return true;
        } else {
            error_amount_message.textContent = "Пожалуйста, введите число";
            perekras(error_amount_message,false)
            return false;
        }
    }
}/*
operations_category.addEventListener("blur", function (event) {
    if (!operations_category.value){
        error_category_message.textContent="Пожалуйста, введите email";
        perekras(error_category_message,false);
    } else if (){
    }
});
*/
//var operations_category = document.getElementById('operations_category')
var errors = [];
var error_type_message = document.getElementById('error_type_message');
var error_currency_message = document.getElementById('error_currency_message');
var error_datetime_message = document.getElementById('error_datetime_message');
var error_category_message = document.getElementById('error_category_message');
var error_new_category_message = document.getElementById('error_new_category_message');
var error_description_message = document.getElementById('error_description_message');
function initialization(errors_list){
    errors = errors_list
    for (let i = 0; i < errors.length; i++) {
        if (errors[i]['code']=='invalid_category'){
            error_category_message.textContent = errors[i]['message']
            perekras(error_category_message, false)
        }
    }
}
