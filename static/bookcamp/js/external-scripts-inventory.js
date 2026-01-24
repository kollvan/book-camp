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
    document.getElementById('form-review').addEventListener('submit', async function(e){
        e.preventDefault();
        const form = e.target;
        const formData = new FormData(form);
        const slug = form.dataset.productSlug;
        url = window.location.protocol + '//' + window.location.host + '/api/inventory/' + slug + '/';
        console.log(url)
        const data = Object.fromEntries(formData.entries());
        const response = await fetch(url, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            alert('Данные обновлены!');
            submit_button = document.getElementById('button-submit-review')
            reset_button = document.getElementById('button-reset-review')

            change_button = document.createElement('button')
            change_button.textContent = 'Изменить'
            change_button.type = 'button'
            change_button.id = 'button-change-review'
            change_button.dataset.productSlug = form.dataset.productSlug

            submit_button.parentElement.appendChild(change_button)
            submit_button.remove()
            reset_button.remove()

            document.getElementById(form.dataset.productSlug + '_review').disabled = true
        }
    });
    document.getElementById('button-change-review').addEventListener('click', async function(e){
        const button_change = e.target;
        const div = button_change.parentElement;
        const textarea = document.getElementById(button_change.dataset.productSlug + '_review')
        textarea.removeAttribute('disabled')

        save_button = document.createElement('button')
        save_button.textContent = 'Сохранить'
        save_button.type = 'submit'
        save_button.id = 'button-submit-review'
        div.appendChild(save_button)
        reset_button = document.createElement('button')
        reset_button.textContent = 'Сбросить'
        reset_button.type = 'reset'
        reset_button.id = 'button-reset-review'
        div.appendChild(reset_button)
        button_change.remove()
    });
    document.getElementById('link-show-more').addEventListener('click', async function(e){
        const link = e.target
        console.log(link.dataset.reviewsUrl)
        const response = await fetch(window.location.protocol + '//' + window.location.host + link.dataset.reviewsUrl, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        dataReviews = await response.json()
        const bottomListReview = document.querySelector('.bottom-list-reviews')
        dataReviews.reviews.forEach((review)=>{
            newContainer = createReviewContainer(
                review.user__username,
                review.rank,
                review.review
            )
            bottomListReview.before(newContainer)
        });
        if (!dataReviews.next)
            bottomListReview.remove();
        else
            link.dataset.reviewsUrl = dataReviews.next;
    })
});
function createReviewContainer(username, rank, review){
    const div = document.createElement('div')
    div.classList.add('review-container')
    const title = document.createElement('p')
    title.classList.add('review-title')
    if (rank >= 3) {
        title.classList.add('good-review')
    } else if (rank > 0){
        title.classList.add('bad-review')
    }
    title.textContent = username
    div.appendChild(title)
    const content = document.createElement('p')
    content.classList.add('review-content')
    content.textContent = review
    div.appendChild(content)
    const rank_review = document.createElement('div')
    rank_review.classList.add('card-rank-product')
    rank_review.classList.add('rank-review')
    rank_review.textContent = 'Рейтинг: ' + rank
    div.appendChild(rank_review)

    return div;
};

