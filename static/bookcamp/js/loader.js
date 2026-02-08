export class Loader{

    static initState = {
        text: 'Loading',
        divClassElement: ['container-loader',],
        spanClassElement: ['loader', 'small',],
        dataMainAttribute: 'loader'
    }


    static createLoader(msg){
        const { text, divClassElement, spanClassElement, dataMainAttribute } = this.initState
        const div = document.createElement('div')
        div.dataset[dataMainAttribute] = ''
        div.classList.add(...divClassElement)

        const textSpan = document.createElement('span')
        textSpan.textContent = msg || text
        div.appendChild(textSpan)

        const span = document.createElement('span')
        span.classList.add(...spanClassElement)
        div.appendChild(span)

        this.element = div
        return div;
    }

};

