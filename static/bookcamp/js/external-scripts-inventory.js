document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('change', function(e) {
        if (e.target.type === 'radio' && e.target.classList.contains('value-rank')) {
            div_card = e.target.parentElement;
            data = {
                'rank': e.target.value,
            }
            response = sendRequestToServer('PATCH', div_card.id.split('_')[1], data);
        }
    });
});
document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('change', async function(e){
        if(e.target.name === 'product_status'){
            try{
                const response_ok = sendRequestToServer('PATCH', e.target.id.replace(/-status$/, ""),
                {'status': e.target.value})

            }
            catch(error){
                console.log(error)
            }
        }

    });
});

