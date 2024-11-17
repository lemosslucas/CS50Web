const url = document.querySelector("#pdf-view").getAttribute('data-pdf-url');
const pdfjsLib = window['pdfjsLib'];

let pdfDoc = null;
let selectedText = "";
let translatedText = "";
let currentPage = 1;

const contextMenu = document.querySelector(".context-menu");
contextMenu.style.display = 'none';

// Função para carregar e exibir o texto de cada página
function loadTextFromPage(pageNum) {
    pdfDoc.getPage(pageNum).then(function(page) {
        page.getTextContent().then(function(textContent) {
            let text = "";

            if (pageNum === 1) {
                coverImg = `<img src="${imageURL}" alt="${altContent}"></img>`
                document.querySelector(".pdf-page").innerHTML = coverImg;
            } else {
                textContent.items.forEach(function(item) {  
                    if (item.str != " " && item.str != '' && item.str.length > 1) {
                        if (item.str === item.str.toUpperCase()) {
                            text += `<strong>${item.str}</strong>` + "<br/>";
                        } else  {
                            text += item.str + " ";
                        }
                    }
                });
    
                const textContainer = document.querySelector(".pdf-page");
                textContainer.innerHTML = text;
            }
            document.querySelector("#ind-page").innerHTML =  `Page ${pageNum} / ${pdfDoc.numPages}\n`
        });
    });
}

let chosenLanguage = "";
const valueLanguage = document.getElementById("valueLanguage");
    valueLanguage.addEventListener("change", function() {
        chosenLanguage = valueLanguage.value;
        console.log(chosenLanguage);
});

function captureSelectedText() {
    const selection = window.getSelection().toString().trim();
    if (selection) {
        selectedText = selection;
        console.log("Texto selecionado:", selectedText);
        contextMenu.style.display = 'flex';
    }
}

function translateText() {
    fetch(
        `https://api.mymemory.translated.net/get?q=${encodeURIComponent(selectedText)}&langpair=${encodeURIComponent(bookLanguage)}|${encodeURIComponent(chosenLanguage)}`
    ).then(response => response.json())
    .then((data) => {
        translatedText = data.responseData.translatedText;
        document.querySelector("#translated-text").innerHTML = "Translated text: " + translatedText;
    })
}

function saveText() {
    const data = {
        word_source: selectedText,
        source_language: bookLanguage,
        target_language: document.querySelector("#valueLanguage").value,
        target_word: translatedText,
    }

    fetch("/save_word", {
        method:"POST",
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify(data),
    }).then(response => response.json())
    .then(data => console.log("Word save: ", data))
    .catch(error => console.error("Error to save:", error));
}

document.addEventListener("mouseup", captureSelectedText);

pdfjsLib.getDocument(url).promise.then(function(pdfDoc_) {
    pdfDoc = pdfDoc_;
    loadTextFromPage(currentPage);
    
    document.querySelector('#next-page').addEventListener('click', function(){
        if (currentPage < pdfDoc.numPages) {
            currentPage++;
            loadTextFromPage(currentPage);
        }
    })

    document.querySelector('#previous-page').addEventListener('click', function(){
        if(currentPage > 1) {
            currentPage--;
            loadTextFromPage(currentPage);
        }
    })

}).catch(function(error) {
    console.error("Erro ao carregar o PDF: ", error);
});

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

//standart start closed
document.querySelector('.container-words').style.display = "none";

document.querySelector("#open-button").addEventListener("click", () => {
    document.querySelector('.container-words').style.display = "block";
});

document.querySelector("#close-button").addEventListener("click", () => {
    document.querySelector('.container-words').style.display = "none";
});