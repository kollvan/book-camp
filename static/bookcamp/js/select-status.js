document.addEventListener('DOMContentLoaded', function() {
const selects = document.querySelectorAll('.current_status');
    selects.forEach(select => {
        select.addEventListener('change', async function() {
        try{
            const response_ok = sendRequestToServer('PATCH', this.id.replace(/-status$/, ""), {'status':this.value})

        }
        catch(error){
            console.log(error)
        }
        });
    });
});
