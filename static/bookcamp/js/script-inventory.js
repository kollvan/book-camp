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

        const urlParams = new URLSearchParams(window.location.search);

        const formData = new FormData(this);
        Array.from(this.elements).forEach(element => {
            if (element.type === 'checkbox') {
                if(element.checked) urlParams.append(element.name, element.value);
            }
            else{
                urlParams.set(element.name, element.value)
            }
        });

        const newUrl = window.location.pathname + '?' + urlParams.toString();

        window.location.href = newUrl;
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.card-btn');
    buttons.forEach(button =>{
        button.addEventListener('click', async function(){
            const buttonId = this.id.match(/^id_(.+)-(\d+)$/);
            try{
                const response_ok = sendRequestDeleteToServer(buttonId[1]);
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

async function sendRequestDeleteToServer(slug) {
    url = window.location.protocol + '//' + window.location.host + '/api/inventory/' + slug + '/';
    const baseOptions = {
      method: 'DELETE',
      headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
    };
    const response = await fetch(url, baseOptions);
    return response.ok;
}
function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}