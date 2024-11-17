document.addEventListener('DOMContentLoaded', function() {
    
    document.querySelector('select').onchange = function() {
        document.querySelector('#hello').style.color = this.value;  
        const li = document.createElement('li');
        li.innerHTML = this.value;
        document.querySelector('#list').append(li)

    };

    document.querySelectorAll('button').forEach((button) => {
        button.onclick = function() {
            document.querySelector('#hello').style.color = button.dataset.color;
            console.log(button.dataset.color);  
        }
    });

})