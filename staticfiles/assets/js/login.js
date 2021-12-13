//Ejecutando funciones
//document.getElementById("btn-iniciar-sesion").addEventListener("click", iniciarSesion);
//document.getElementById("btn-registrarse").addEventListener("click", register);
window.addEventListener("resize", anchoPage);

//Declarando variables
var formulario_login = document.querySelector(".formulario-login");
var formulario_register = document.querySelector(".formulario-register");
var contenedor_login_register = document.querySelector(".contenedor-login-register");
var trasera_login = document.querySelector(".trasera-login");
var trasera_register = document.querySelector(".trasera-register");

    //FUNCIONES

function anchoPage(){

    if (window.innerWidth > 850){
        trasera_register.style.display = "block";
        trasera_login.style.display = "block";
        formulario_login.style.display = "block";
        contenedor_login_register.style.left = "10px";
        formulario_register.style.display = "none";
        trasera_register.style.opacity = "1";
        trasera_login.style.opacity = "0";
    }else{
        trasera_register.style.display = "block";
        trasera_register.style.opacity = "1";
        trasera_login.style.display = "none";
        formulario_login.style.display = "block";
        contenedor_login_register.style.left = "0px";
        formulario_register.style.display = "none";
        formulario_login.style.display = "block";
        contenedor_login_register.style.left = "0px";
        formulario_register.style.display = "none";
        trasera_register.style.display = "block";
        trasera_login.style.display = "none";   
    }
}

anchoPage();

    