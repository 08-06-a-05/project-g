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