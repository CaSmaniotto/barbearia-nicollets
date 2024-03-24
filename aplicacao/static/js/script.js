const btnMostrar = document.getElementsByClassName("m-mostrar")[0]; // Selecionando o primeiro elemento
const listaItens = document.getElementsByClassName("itens")[0]; // Selecionando o primeiro elemento
const btnSeta = document.getElementsByClassName("rotate")[0];

btnMostrar.addEventListener('click', () => {
    listaItens.classList.toggle('v');
    btnSeta.classList.toggle('rotate');
});
