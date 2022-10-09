const simboloSoma = "+";
const simboloSubtracao = "-";
const simboloDivisao = "/";
const simboloMultiplicacao = "*";

var resultado = 0;

const elementoSimbolo = document.getElementById("simbolo");
const elementoResultado = document.getElementById("resultado");

function somar() {
    resultado = parseInt(document.getElementById("operando1").value) + parseInt(document.getElementById("operando2").value);
    elementoSimbolo.value = simboloSoma;
    elementoResultado.value = resultado;
}

function subtracao() {
    resultado = parseInt(document.getElementById("operando1").value) - parseInt(document.getElementById("operando2").value);
    elementoSimbolo.value = simboloSubtracao;
    elementoResultado.value = resultado;
}

function divisao() {
    resultado = parseInt(document.getElementById("operando1").value) / parseInt(document.getElementById("operando2").value);
    elementoSimbolo.value = simboloDivisao;
    elementoResultado.value = resultado; 
}

function multiplicacao() {
    resultado = parseInt(document.getElementById("operando1").value) * parseInt(document.getElementById("operando2").value);
    elementoSimbolo.value = simboloMultiplicacao;
    elementoResultado.value = resultado;
}
