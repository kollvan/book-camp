import { Loader } from './loader.js'
import { sendRequestToServer } from './generic.js'

const createSaveButton = async function(){
    const save_button = document.createElement('button')
    save_button.textContent = 'Сохранить'
    save_button.type = 'submit'
    save_button.id = 'button-submit-review'
    return save_button
};
const createResetButton = async function(){
    const reset_button = document.createElement('button')
    reset_button.textContent = 'Сбросить'
    reset_button.type = 'reset'
    reset_button.id = 'button-reset-review'
    return reset_button
};
const createChangeButton = async function(slug){
    const change_button = document.createElement('button')
    change_button.textContent = 'Изменить'
    change_button.type = 'button'
    change_button.id = 'button-change-review'
    change_button.dataset.productSlug = slug
    change_button.setAttribute('data-button-change-inventory', '')
    return change_button
};
const createRemoveButton = async function(slug){
    const remove_button = document.createElement('button')
    remove_button.textContent = 'Удалить'
    remove_button.type = 'button'
    remove_button.id = 'button-remove-review'
    remove_button.dataset.productSlug = slug
    remove_button.setAttribute('data-button-change-inventory', '')
    return remove_button
};
const buttonReviewChange = async function(e){
    const button_change = e.target;
    const div = button_change.parentElement;
    const textarea = document.getElementById(button_change.dataset.productSlug + '_review')
    textarea.removeAttribute('disabled')

    div.appendChild(await createSaveButton())

    div.appendChild(await createResetButton())
    button_change.remove()
    document.querySelector('#button-remove-review').remove()
};
const reviewFormSubmit = async function(e){
    e.preventDefault();
    const form = e.target;
    const divElement = document.querySelector('[data-review-buttons]')
    const slug = form.dataset.productSlug;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    const url = window.location.origin + '/api/inventory/';

    divElement.append(Loader.createLoader())
    const response = await sendRequestToServer(url, 'PATCH', slug, data)

    if (response.ok) {
        const submit_button = document.getElementById('button-submit-review')
        const reset_button = document.getElementById('button-reset-review')

        submit_button.parentElement.appendChild(await createChangeButton(slug))
        submit_button.parentElement.appendChild(await createRemoveButton(slug))
        submit_button.remove()
        reset_button.remove()

        document.getElementById(slug + '_review').disabled = true
    }
    divElement.querySelector('[data-loader]')?.remove();
};
const showMoreClick = async function(e){
    const link = e.target
    const url = window.location.origin + link.dataset.reviewsUrl;

    const bottomListReviews = document.querySelector('[data-more-reviews]')
    bottomListReviews.classList.add('invisible')

    bottomListReviews.before(Loader.createLoader())

    const promise = sendRequestToServer(url, 'GET')
    promise.then(async (successData) => {
        if (!successData.ok)
            throw new Error(`HTTP error! status: ${response.status}`);
        const dataReviews = await successData.json();
        dataReviews.reviews.forEach((review)=>{
            const newContainer = createReviewContainer(
                review.user__username,
                review.rank,
                review.review
            )
            bottomListReviews.before(newContainer)
        });
        if (!dataReviews.next)
            bottomListReviews.remove();
        else
            link.dataset.reviewsUrl = dataReviews.next;
    }).finally( async () => {
        document.querySelector('[data-reviews-list] [data-loader]')?.remove();
        bottomListReviews.classList.remove('invisible');
    });
};
const buttonRemoveClick = async function(e){
    const slug = e.target.dataset.productSlug;
    const url = `${window.location.origin}/api/inventory/`
    const divElement = e.target.parentElement;
    const data = {
        'review': null
    }
    divElement.append(Loader.createLoader())

    const promise = sendRequestToServer(url, 'PATCH', slug, data)
        promise.then(async (successData) => {
        if (!successData.ok)
            throw new Error(`HTTP error! status: ${response.status}`);

        const ownReviewElement = document.querySelector(`#${slug}_review`)
        ownReviewElement.value = ''
        ownReviewElement.disabled = false
        document.querySelector('#button-change-review').remove()
        const div = e.target.parentElement;
        div.appendChild(await createSaveButton())

        div.appendChild(await createResetButton())
        e.target.remove()
    }).catch(error => {
        console.error('Ошибка при Удалении:', error);

    }).finally(()=>{
        divElement.querySelector('[data-loader]')?.remove();
    });
};

document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('change', function(e) {
        const url = window.location.origin + '/api/inventory/'
        if (e.target.hasAttribute('data-value-rank')) {
            const div_card = e.target.parentElement;
            const data = {
                'rank': e.target.value,
            }
            const promise = sendRequestToServer(url, 'PATCH', div_card.dataset.productSlug, data);
            promise.then((successData)=>{
                if (!successData.ok)
                    throw Error(successData)
                e.target.checked = true
            }).catch((errorData)=>{
                div_card.querySelector('[checked]').checked = true
            })
        }
        else if(e.target.name === 'product_status'){
            const data = {'status': e.target.value}
            const promise = sendRequestToServer(url, 'PATCH', e.target.dataset.productSlug, data);
            promise.then((successData)=>{
                if (!successData.ok)
                    throw Error(successData)
                console.log(e.target.value)
            }).catch((errorData)=>{
                e.target.querySelector('[selected]').selected = true
                e.target.dispatchEvent(new Event('changeReverse', { bubbles: true }))
            })
        }
    });
    document.addEventListener('submit', async (event)=>{
        if (event.target.id === 'form-review'){
            await reviewFormSubmit(event)
        }
    });
    document.addEventListener('click', async (event)=>{

        if (event.target.closest('#link-show-more')){
            await showMoreClick(event)
        }else if (event.target.id === 'button-remove-review'){
            await buttonRemoveClick(event);
        }else if(event.target.id === 'button-change-review'){
            await buttonReviewChange(event)
        }
    });
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



