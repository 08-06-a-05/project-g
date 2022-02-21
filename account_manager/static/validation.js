function isNumeric(value) {
    return /^-?\d+$/.test(value);
}


function send_JSON() {
    var url = window.location.origin+'/abra/';
    xhr.open("POST",url,true);
    xhr.setRequestHeader("X-CSRFToken",token,"Content-Type","application/json");
    var data=JSON.stringify({"email":email.value});
    xhr.send(data);
}


function validate() { // При нажатии на кнопку отправки форма еще раз проходит валидацию
    if (!username.value){
        error_name_message.textContent="Пожалуйста, введите имя";
        perekras(name_line,error_name_message,false);
        valid = false;
    }
    if (!email.value){
        error_email_message.textContent="Пожалуйста, введите email";
        perekras(email_line,error_email_message,false);
        valid=false;
    } else if (email.validity.typeMismatch){
        error_email_message.textContent="Такой email не существует";
        perekras(email_line,error_email_message,false);
        valid = false;
    }
    if (!password.value){
        error_password_message.textContent="Пожалуйста, введите пароль";
        perekras(password_line,error_password_message,false);
        valid = false;
    }
    else if (password.validity.tooShort){
        error_password_message.textContent="Пароль должен содержать как минимум 8 символов";
        perekras(password_line,error_password_message,false);
        valid = false;
    } else if (isNumeric(password.value)) {
        error_password_message.textContent="Пароль не может состоять только из цифр";
        perekras(password_line,error_password_message,false);
        valid=false;
    }
    if (!password_check.value){
        error_password_check_message.textContent="Пожалуйста, введите пароль повторно";
        perekras(password_check_line,error_password_check_message,false);
        valid=false;
    } else if (password.value!=password_check.value){
        error_password_check_message.textContent="Подтверждение не совпадает с паролем";
        perekras(password_check_line,error_password_check_message,false);
        valid=false;
    }
    return valid;
}


function perekras(err_line,err_mes,type){
    if (!type){
        err_line.style.backgroundPosition = "100% 0";
        err_mes.style.visibility = "visible";
        err_mes.style.opacity = "1";
    } else {
        err_line.style.backgroundPosition = "50% 0";
        err_mes.style.visibility = "hidden";
        err_mes.style.opacity = "0";
    }
}

var emails=document.getElementById("emails");
var email = document.getElementById("email"); //email пользователя
var password = document.getElementById("password"); //пароль пользователя
var password_check = document.getElementById("password_check"); // повторно введенный пароль пользователя
var username = document.getElementById("name"); // имя пользователя
var name_line = document.getElementById("name_line"); // валидационная линия под именем
var email_line = document.getElementById("email_line"); // валидационная линия под email
var password_line = document.getElementById("password_line"); // валидационная линия под паролем
var password_check_line = document.getElementById("password_check_line"); // валидационная линия под повторно введенным паролем
var error_email_message = document.getElementById("error_email_message"); // предупреждение об ошибке, при вводе email
var error_name_message = document.getElementById("error_name_message"); // предупреждение об ошибке, при вводе имени
var error_password_message = document.getElementById("error_password_message"); // предупреждение об ошибке, при вводе пароля
var error_password_check_message = document.getElementById("error_password_check_message"); // предупреждение об ошибке, при повторном вводе пароля

//Проверка корректности введённого email

var token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
var result;
var xhr = new XMLHttpRequest();
var valid=true;


email.addEventListener("blur", function (event) {
    if (!email.value){
        error_email_message.textContent="Пожалуйста, введите email";
        perekras(email_line,error_email_message,false);
    } else {
        send_JSON();
    }
});

xhr.onreadystatechange = function (){
    if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
        var answer = JSON.parse(this.responseText);
        if (answer.is_exist=="false"){
            error_email_message.textContent="Такой email не существует";
            perekras(email_line,error_email_message,false);
            valid = false;
        }
        else if (answer.is_registered=='true') {
            error_email_message.textContent="Этот email уже занят";
            perekras(email_line,error_email_message,false);
            valid = false;
        } else {
            perekras(email_line,error_email_message,true);
            valid = true;
        }
        can_use = true;
    }
}

//Проверка корректности введённого пароля

password.addEventListener("blur", function (event) {
    if (!password.value){
        error_password_message.textContent="Пожалуйста, введите пароль";
        perekras(password_line,error_password_message,false);
        if (password_check.value==password.value){
            perekras(password_check_line,error_password_check_message,true);
        }
        else{
            error_password_check_message.textContent="Подтверждение не совпадает с паролем"
            perekras(password_check_line,error_password_check_message,false);
        }
    } else if (password.validity.tooShort || isNumeric(password.value)) { 
        if (password.validity.tooShort){
            error_password_message.textContent="Пароль должен содержать как минимум 8 символов";
            perekras(password_line,error_password_message,false);
            if (password_check.value==password.value){
                perekras(password_check_line,error_password_check_message,true);
            }
            else{
                error_password_check_message.textContent="Подтверждение не совпадает с паролем"
                perekras(password_check_line,error_password_check_message,false);
            }
        }
        if (isNumeric(password.value)) {
            error_password_message.textContent="Пароль не может состоять только из цифр";
            perekras(password_line,error_password_message,false);
            if (password_check.value==password.value){
                perekras(password_check_line,error_password_check_message,true);
            }
            else{
                error_password_check_message.textContent="Подтверждение не совпадает с паролем"
                perekras(password_check_line,error_password_check_message,false);
            }
        }
    } else {
        perekras(password_line,error_password_message,true);
        if (password_check.value==password.value){
            perekras(password_check_line,error_password_check_message,true);
        }
        else{
            error_password_check_message.textContent="Подтверждение не совпадает с паролем"
            perekras(password_check_line,error_password_check_message,false);
        }
    }
});

//Проверка, что повторно введенный пароль совпадает

password_check.addEventListener("blur", function (event) {
    if (!password_check.value) {
        error_password_check_message.textContent="Пожалуйста, введите пароль повторно";
        perekras(password_check_line,error_password_check_message,false);
    } else if ( password.value!=password_check.value) {
        error_password_check_message.textContent="Подтверждение не совпадает с паролем";
        perekras(password_check_line,error_password_check_message,false);
    } else {
        perekras(password_check_line,error_password_check_message,true);
    }
});

//Проверка, что введено имя

username.addEventListener("blur", function (event) {
    if (!username.value) {
        error_name_message.textContent="Пожалуйста, введите имя";
        perekras(name_line,error_name_message,false);
    } else if (username.value=="Георгий"){
        error_name_message.textContent="Ваше имя слишком красивое!";
        perekras(name_line,error_name_message,false);
    } else {
        perekras(name_line,error_name_message,true);
    }
});