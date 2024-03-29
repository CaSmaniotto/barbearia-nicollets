// timer do alerta
setTimeout(function () {
    document.getElementById("alerta").style.visibility = "hidden";
}, 4000);

setTimeout(function(){ 
    document.getElementById("alerta").style.opacity='0';
}, 1000);


// opções de acessibilidade
const changeSize = () => {
    const elements = document.querySelectorAll('*');

    elements.forEach(element => {
        element.classList.toggle('changeFont');
    });

    // Verifica se a classe de fonte foi ativada e armazena o estado no localStorage
    const isFontChanged = elements[0].classList.contains('changeFont');
    localStorage.setItem('fontChanged', isFontChanged);

    const btnSize = document.getElementById('btnSize');

    btnSize.classList.toggle('active');
}

function toggleDarkMode() {
    var element = document.body;
    element.classList.toggle("dark"); 
    
    const darkMode = element.classList.contains('dark');
    localStorage.setItem('darkMode', darkMode);

    const btnContraste = document.getElementById('btnContraste');
    btnContraste.classList.toggle('active');
}

// Obtém o estado da classe de fonte do localStorage ao carregar a página
document.addEventListener('DOMContentLoaded', () => {
    const fontChanged = localStorage.getItem('fontChanged');
    const darkMode = localStorage.getItem('darkMode');

    if (fontChanged === 'true') {
        changeSize();
    }

    if (darkMode === 'true') {
        toggleDarkMode()
    }

});