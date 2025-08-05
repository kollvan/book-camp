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
                const response_ok = await sendRequestToServer(buttonId, service_method);

                if(response_ok){
                    console.log('id_'+buttonId[1])
                    card = document.querySelector('#id_'+buttonId[1])
                    div = card.querySelector('.card-status')
                    if(service_method == 'POST'){
                        div.classList.remove('invisible')
                        div.textContent = 'Добавленно'
                        this.classList.add('remove')
                    }
                    else{
                        div.classList.add('invisible')
                        this.classList.remove('remove');
                    }
                }
            } catch (error) {
                console.log(error)
            }

        });
    });

    async function sendRequestToServer(buttonId, service_method) {
        url = window.location.protocol + '//' + window.location.host + '/api/inventory/';
        product_id = buttonId[2]
        const baseOptions = {
          method: service_method,
          headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
        };
        if (service_method == 'DELETE'){
            product_id = buttonId[1]
            url += product_id + '/'
        }
        else
        {
            baseOptions.body = JSON.stringify({ 'set_product': product_id })
        }
        const response = await fetch(url, baseOptions);
        return response.ok;
    }
    function getCookie(name) {
      let matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
      ));
      return matches ? decodeURIComponent(matches[1]) : undefined;
    }
});