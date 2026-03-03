import { sendRequestToServer, sendRequestForWidgets } from './generic.js'

document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('click', async function(e) {

        if(e.target.hasAttribute('data-button-add')){
            const addButton = e.target
            const slug = addButton.dataset.productSlug
            const url = window.location.origin + '/api/inventory/'
            const data = {
                'set_product': addButton.dataset.productId
            }
            const promise = sendRequestToServer(url, 'POST', null, data)
            promise.then(async (value) =>{
                e.target.remove();
                const content = document.querySelector('section');
                const html_response = await sendRequestForWidgets(slug, '/inventory/widgets/user_data/');
                const html_data = await html_response.json()
                content.insertAdjacentHTML('beforeEnd', html_data.user_data);

                const product_title = document.querySelector('[data-product-title]');

                product_title.append( await createProductStatus());

                document.querySelector('[data-list-reviews]').querySelector('details').insertAdjacentHTML(
                    'beforebegin',
                    html_data.review_data
                );
            }).catch((errorData)=>{
                console.log(errorData)
            });
        }

        if(e.target.hasAttribute('data-button-remove')){
            const slug = e.target.dataset.productSlug
            const id = e.target.dataset.productId
            const response = sendRequestToServer(window.location.origin + '/api/inventory/','DELETE', slug)
            response.then(value =>{
                document.querySelector('[data-product-title-status]').remove();
                document.querySelector('[data-user-main-widget]').remove()

                const button_add = document.createElement('button')
                button_add.classList.add('btn-user-data', 'btn-add')
                button_add.dataset.productSlug = slug
                button_add.dataset.productId = id
                button_add.dataset.buttonAdd = ''
                button_add.id = `button-add-${slug}`
                button_add.textContent = 'Добавить'

                document.querySelector('[data-tag-list]').after(button_add)
                document.querySelector('[data-user-review]').remove()
            }).catch((errorData)=>{
                console.log(errorData)
            });
        }
    });
    document.addEventListener('change', async function(e) {
        if (event.target.getAttribute('name') === 'product_status'){
            const textStatus = e.target.options[e.target.selectedIndex].text;
            document.querySelector('[data-product-title-status]').textContent = textStatus
        }
    });
    document.addEventListener('changeReverse', async function(e) {
        if (event.target.hasAttribute('name', 'product_status')){
            const textStatus = e.target.options[e.target.selectedIndex].text;
            document.querySelector('[data-product-title-status]').textContent = textStatus
        }
    });
});

async function createProductStatus(){
    const div_status = document.createElement('div')
    div_status.classList.add('card-status', 'product-status')
    div_status.textContent = 'Добавленно'
    div_status.dataset.productTitleStatus = ''
    console.log(div_status)
    return div_status
}
