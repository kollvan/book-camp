function delay_remove(elem, delay){
    if (elem){
        setTimeout(function() {
            elem.remove();
        }, delay);
    }
};

 setTimeout(function(){
     const popupMenu = document.querySelector('#popup-message.fade-out')
    if(popupMenu){
        popupMenu.classList.add('hidden');
        delay_remove(popupMenu, 2000);
    }
 }, 1000);

document.addEventListener('DOMContentLoaded', function(){
    const closeBtn = document.querySelector('.close-btn')
    const popupMenu = document.getElementById('popup-message')
    closeBtn.addEventListener('click', function() {
        popupMenu.remove()
    });
});
