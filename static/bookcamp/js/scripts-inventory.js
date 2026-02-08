import { sendRequestToServer } from "./generic.js";
import { PopupWindow } from "./popup-window.js";

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

document.addEventListener('click', async (event) => {
    const url = window.location.origin.toString() + '/api/inventory/';
    if (event.target.hasAttribute('data-btn-remove')){

        const promise = sendRequestToServer(url, 'DELETE', event.target.dataset.productSlug)

        promise
        .then((successData)=>{
            console.log(successData)
            if (!successData.ok)
                throw Error('Something went wrong.')
            event.target.closest('.card').remove()})
        .catch((errorData)=>{
            const popup = new PopupWindow()
            popup.initState.messageLevel = 0
            popup.initState.divClassElement.push('center-message')
            const popupElement = popup.createElement(errorData)
            document.body.append(popupElement)
            setTimeout(popup.getHandlerDisappearance(), 2000, popupElement)})
    }
});


