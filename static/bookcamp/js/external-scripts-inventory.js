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