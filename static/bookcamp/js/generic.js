export async function sendRequestToServer(url, service_method='POST', slug = null, data = null) {
    const baseOptions = {
      method: service_method,
      headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
    };
    if (slug)
        url += `${slug}/`;
    if (data)
        baseOptions.body = JSON.stringify(data);

    return fetch(url, baseOptions);
}

function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}

export async function sendRequestForWidgets(pk, service){
    const url = window.location.origin + service + pk + '/';

    const baseOptions = {
      method: 'GET',
      headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
    };
    const html_response = await fetch(url, baseOptions)
    return html_response
}