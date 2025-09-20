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
