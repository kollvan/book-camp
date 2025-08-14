
async function sendRequestToServer(service_method, slug = null, data = null) {
    url = window.location.protocol + '//' + window.location.host + '/api/inventory/';
    const baseOptions = {
      method: service_method,
      headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
    };
    if (service_method != 'POST')
    {
        url += slug + '/';
    }

    if (service_method != 'DELETE')
    {
        baseOptions.body = JSON.stringify(data);
    }
    console.log(data)
    const response = await fetch(url, baseOptions);
    return response.ok;
}
function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}