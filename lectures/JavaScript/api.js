
document.addEventListener('DOMContentLoaded', function() {
    fetch('https://api.exchangeratesapi.io/latest?base=USD')
    .then(response => response.json())
    .then(data => {
        /*
        const currency = document.querySelector('#currency').value.toUpperCase();
        const rate = data.rates.[currency];
        if (rate != undefined) {
            document.querySelector('body').innerHTML = `1 USD is ${rate.toFixed(3)}.`
        } else {
            document.querySelector('body').innerHTML = "not possible to find this currency" 
        }

        .catch(erro => {
            console.log('error', erro)
        });
        */
        console.log(data);
    })
});
