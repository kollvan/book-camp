import { sendRequestToServer } from './generic.js'

document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('click', async function(event) {
        if (event.target.hasAttribute('data-mini-button-add')){
            const btnAddElement = event.target
            const slug = btnAddElement.dataset.productSlug
            const id = btnAddElement.dataset.productId
            const promise = sendRequestToServer( window.location.origin + '/api/inventory/',
                'POST',
                null,
                {'set_product': id}
            )
           promise.then( async (successData)=>{
                if(!successData.ok)
                    throw Error(successData)
                const productStatusElement = document.querySelector(`[data-card-id="${id}"]`);
                productStatusElement.parentElement.classList.remove('invisible');
                productStatusElement.disabled = false;
                productStatusElement.value = 1;
                btnAddElement.classList.add('remove');
                btnAddElement.dataset.miniButtonRemove = ''
                btnAddElement.removeAttribute('data-mini-button-add')
            }).catch( async (errorData)=>{
                console.log(errorData)
            })
        }
        if (event.target.hasAttribute('data-mini-button-remove')){
            const btnRemoveElement = event.target
            const slug = btnRemoveElement.dataset.productSlug
            const id = btnRemoveElement.dataset.productId
            const promise = sendRequestToServer(
                window.location.origin + '/api/inventory/',
                'DELETE',
                slug,
            );
            promise.then( async (successData)=>{
                if(!successData.ok)
                    throw Error(successData)
                const productStatusElement = document.querySelector(`[data-card-id="${id}"]`);
                productStatusElement.parentElement.classList.add('invisible');
                btnRemoveElement.classList.remove('remove');
                btnRemoveElement.dataset.miniButtonAdd = ''
                btnRemoveElement.removeAttribute('data-mini-button-remove')
            }).catch( async (errorData)=>{
                console.log(errorData)
            })
        }
//        if (event.target.hasAttribute('data-mini-button')){
//            const slug = event.target.productSlug
//            const id = event.target.productId
//
//            let method = undefained
//            let data = undefained
//            if (event.target.hasAttribute('data-mini-button-remove')){
//                method = 'DELETE'
//            }else{
//                method = 'POST'
//                data={'set_product': id}
//            }
//
//            const promise = sendRequestToServer(
//                window.location.origin + '/api/inventory/',
//                method
//                slug,
//                data
//            );
//            promise.then( async (successData)=>{
//                if(!successData.ok)
//                    throw Error(successData)
//                const productStatusElement = document.querySelector(`[data-card-id="${id}"]`);
//                productStatusElement.classList.toggle('invisible');
//                const selectElement = productStatusElement.querySelector('select')
//                const isDisabled = selectElement.disabled
//                selectElement.disabled = !isDisabled;
//                if (method === 'POST')
//                    selectElement.value = 1
//                event.target.classList.toggle('remove');
//            }).catch( async (errorData)=>{
//                console.log(errorData)
//            })
//        }
//        const buttonId = this.id.match(/^id_(.+)-(\d+)$/);
//        service_method = 'POST';
//        if (button.className.includes('remove')) {
//            service_method = 'DELETE';
//        }
//        try {
//            const response_ok = await sendRequestToServer(service_method, buttonId[1], data={'set_product':buttonId[2]});
//
//            if(response_ok){
//                if(service_method == 'POST'){
//
//                }
//                else{
//
//                }
//            }
//        } catch (error) {
//            console.log(error)
//        }

    });
});

