document.addEventListener('DOMContentLoaded', function() {
    const selectElements = document.querySelectorAll('.inventory-search');
    const handleSelectChange = function() {
        const urlParams = new URLSearchParams(window.location.search);

        selectElements.forEach(select => {
          if (select.value) {
            urlParams.set(select.name, select.value);
          } else {
            urlParams.delete(select.name);
          }
        });

        const newUrl = window.location.pathname + '?' + urlParams.toString();
        window.location.href = newUrl;
    };
    selectElements.forEach(select => {
        select.addEventListener('change', handleSelectChange);
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('#filter-form');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const fieldNames = new Set();

        for (let i = 0; i < form.elements.length; i++) {
            const element = form.elements[i];
            if (element.name) {
                fieldNames.add(element.name);
            }
        }
        const searchParams = new URLSearchParams(window.location.search);
        for (let [key, value] of searchParams.entries()) {
            if(!fieldNames.has(key))
            {
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = key;
                input.value = value;
                form.appendChild(input);
            }
        }
        form.submit()
    });

});


document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.card-btn');
    buttons.forEach(button =>{
        button.addEventListener('click', async function(){
            const buttonId = this.id.match(/^id_(.+)-(\d+)$/);
            try{
                const response_ok = sendRequestToServer('DELETE', buttonId[1]);
                if(response_ok){
                    let card_good = this.closest('.card');
                    card_good.remove();
                }
            }catch(error){
                console.log(error)
            }
        });
    });
});


