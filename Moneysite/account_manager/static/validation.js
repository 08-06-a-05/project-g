function isNumeric(value) {
    return /^-?\d+$/.test(value);
}

function validate() { // При нажатии на кнопку отправки форма еще раз проходит валидацию
    var valid=true
    if (!username.value){
        name_line.style.backgroundPosition="100% 0";
        valid = false;
    }
    if (!email.value){
        email_line.style.backgroundPosition="100% 0";
        valid = false;
    } else if (email.validity.typeMismatch){
        email_line.style.backgroundPosition="100% 0";
        valid = false;
        
    }
    if (!password.value || password.validity.tooShort){
        password_line.style.backgroundPosition="100% 0";
        valid = false;
    }
    if (!password_check.value || password.value!=password_check.value){
        password_check_line.style.backgroundPosition="100% 0";
        valid=false;
    }
    return valid;
}


var email = document.getElementById("email"); //email пользователя
var password = document.getElementById("password"); //пароль пользователя
var password_check = document.getElementById("password_check"); // повторно введенный пароль пользователя
var username = document.getElementById("name"); // имя пользователя
var name_line = document.getElementById("name_line"); // валидационная линия под именем
var email_line = document.getElementById("email_line"); // валидационная линия под email
var password_line = document.getElementById("password_line"); // валидационная линия под паролем
var password_check_line = document.getElementById("password_check_line"); // валидационная линия под повторно введенным паролем
var error_message = document.getElementById("error_message"); // предупреждение об ошибке, пока не работает
var error_name_message = document.getElementById("error_name_message");

//Проверка корректности введённого email

email.addEventListener("input", function (event) {
    if (!email.value){
        email_line.style.backgroundPosition="100% 0";
        error_message.textContent="Это обязательное поле";
        error_message.style.visibility="visible";
        error_message.style.opacity="1";
    } else if (email.validity.typeMismatch) {
        email_line.style.backgroundPosition="100% 0";
        error_message.textContent="Такой email не существует";
        error_message.style.visibility="visible";
        error_message.style.opacity="1";
    } else {
        email_line.style.backgroundPosition="50% 0";
        error_message.style.opacity="0";
        error_message.style.visibility="hidden";
    }
});

//Проверка корректности введённого пароля

password.addEventListener("input", function (event) {
    if (!password.value || password.validity.tooShort || isNumeric(password.value)) {
        password_line.style.backgroundPosition="100% 0";
        if (password_check.value==password.value){
            password_check_line.style.backgroundPosition="50% 0";
        }
        else{
            password_check_line.style.backgroundPosition="100% 0";
        }
    } else {
        password_line.style.backgroundPosition="50% 0";
        if (password_check.value==password.value){
            password_check_line.style.backgroundPosition="50% 0";
        }
        else{
            password_check_line.style.backgroundPosition="100% 0";
        }
    }
});

//Проверка, что повторно введенный пароль совпадает

password_check.addEventListener("input", function (event) {
    if (!password_check.value || password.value!=password_check.value) {
        password_check_line.style.backgroundPosition="100% 0";
    } else {
        password_check_line.style.backgroundPosition="50% 0";
    }
});

//Проверка, что введено имя

username.addEventListener("input", function (event) {
    if (!username.value) {
        name_line.style.backgroundPosition="100% 0";
        error_name_message.textContent="Это обязательное поле";
        error_name_message.style.visibility="visible";
        error_name_message.style.opacity="1";
    } else if (username.value=="Jacob"){
        name_line.style.backgroundPosition="100% 0";
        error_name_message.textContent="Ваше имя слишком уродское!";
        error_name_message.style.visibility="visible";
        error_name_message.style.opacity="1";
    } else {
        name_line.style.backgroundPosition="50% 0";
        error_name_message.style.visibility="hidden";
        error_name_message.style.opacity="0";
    }
});