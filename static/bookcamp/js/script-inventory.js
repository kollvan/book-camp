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

        const urlParams = new URLSearchParams(window.location.search);

        const formData = new FormData(this);
        Array.from(this.elements).forEach(element => {
            if (element.type === 'checkbox') {
                if(element.checked) urlParams.append(element.name, element.value);
            }
            else{
                urlParams.set(element.name, element.value)
            }
        });

        const newUrl = window.location.pathname + '?' + urlParams.toString();

        window.location.href = newUrl;
    });
});

