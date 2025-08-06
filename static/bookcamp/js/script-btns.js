document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.card-btn');

    buttons.forEach(button => {
        button.addEventListener('click', async function() {
            const buttonId = this.id.match(/^id_(.+)-(\d+)$/);
            service_method = 'POST';
            if (button.className.includes('remove')) {
                service_method = 'DELETE';
            }
            try {
                const response_ok = await sendRequestToServer(service_method, buttonId[1], data={'set_product':buttonId[2]});

                if(response_ok){
                    console.log('id_'+buttonId[1]);
                    card = document.querySelector('#id_'+buttonId[1]);
                    div = card.querySelector('.card-status');
                    if(service_method == 'POST'){
                        div.classList.remove('invisible');
                        select = div.querySelector('select');
                        select.disabled = false;
                        select.value = 1;
                        this.classList.add('remove');
                    }
                    else{
                        div.classList.add('invisible');
                        div.querySelector('select').disabled = true;
                        this.classList.remove('remove');
                    }
                }
            } catch (error) {
                console.log(error)
            }

        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
const selects = document.querySelectorAll('.current_status');
    selects.forEach(select => {
        select.addEventListener('change', async function() {
        try{
            const response_ok = sendRequestToServer('PATCH', this.id.replace(/-status$/, ""), {'status':this.value})
            console.log(this.value)
        }
        catch(error){
            console.log(error)
        }
        });
    });
});

async function sendRequestToServer(service_method, slug = null, data = null) {
    url = window.location.protocol + '//' + window.location.host + '/api/inventory/';
    const baseOptions = {
      method: service_method,
      headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
    };
    if (service_method != 'POST')
    {
        url += slug + '/';
    }

    if (service_method != 'DELETE')
    {
        baseOptions.body = JSON.stringify(data);
    }
    console.log(data)
    const response = await fetch(url, baseOptions);
    return response.ok;
}
function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}