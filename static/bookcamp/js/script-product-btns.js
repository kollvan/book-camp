document.addEventListener('DOMContentLoaded', function() {
        document.addEventListener('click', function(e) {

            if(e.target.classList.contains('btn-add')){
                product_info = e.target.id.match(/^id_(.+)_(\d*)$/)

                data = {
                    'set_product': product_info[2]
                }
                response = sendRequestToServer('POST', slug=null, data=data)
                response.then(async value =>{

                    e.target.remove();
                    const content = document.querySelector('.content');
                    html_response = await sendRequestForWidgets(product_info[1], '/inventory/widgets/user_data/');
                    const html_data = await html_response.json()
                    content.insertAdjacentHTML('beforeEnd', html_data.user_data);

                    createProductStatus()
                });

            }

            if(e.target.classList.contains('btn-remove')){
                console.log('huiii')
                product_info = e.target.id.match(/^id_(.+).*$/)
                response = sendRequestToServer('DELETE', slug=product_info[1])
                response.then(value =>{
                    product_status = document.querySelector('.card-status')
                    div = document.querySelector('.user-data')
                    product_status.remove();
                    div.remove()
                    button_add = document.createElement('button')
                    button_add.classList.add('btn-user-data', 'btn-add')
                    button_add.id = 'id_' + document.querySelector('.card-btn').id
                    button_add.textContent = 'Добавить'
                    tag_list = document.querySelector('.tag-list')
                    tag_list.after(button_add)
                });

            }
    });
});

async function createProductStatus(){
    const product_title = document.querySelector('.product-title');
    div_status = document.createElement('div')
    div_status.classList.add('card-status', 'product-status')
    div_status.textContent = 'Добавленно'
    product_title.after(div_status)
}

document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('change', function(e) {
        if (e.target.type === 'radio' && e.target.classList.contains('value-rank')) {
            div_card = e.target.parentElement;
            data = {
                'rank': e.target.value,
            }
            try{
                response_ok = sendRequestToServer('PATCH', div_card.id.split('_')[1], data)
            }
            catch(error){
                console.log(error)
            }
        }
    });
});