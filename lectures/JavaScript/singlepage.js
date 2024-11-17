function showPage(page) {
    document.querySelectorAll('div').forEach(div => {
        div.style.display = 'none'
    })

    console.log(page)
    document.querySelector(`#${page}`).style.display = 'block';
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('button').forEach(button => {
        button.onclick = function() {
            showPage(this.dataset.page)
        }
    })
})

// voltar pagina que estava
window.onpopstate = function(event) {
    console.log(event.state.section)
    showSection(event.state.section)
}