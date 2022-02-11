var add_category = document.getElementById("new_category");
var category = document.getElementById("category");
var swap_button = document.getElementById('swap-category')
swap_button.addEventListener("click", function (event) {
    if (swap_button.textContent == "Добавить категорию"){
        category.style.display = "none";
        add_category.style.display = "flex";
        swap_button.textContent="Выбрать из уже существующих";
        swap_button.style.width = "60%";'

    } else {
        category.style.display = "flex";
        add_category.style.display = "none";
        swap_button.textContent="Добавить категорию";
        swap_button.style.width = "40%";
    }
});