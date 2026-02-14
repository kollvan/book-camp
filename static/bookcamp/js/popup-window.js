export class PopupWindow{

    #classLevel = {
        25: 'success-message',
        20: 'info-message',
        0: 'error-message'
    }

    #textLevel = {
        25: 'Success',
        20: 'Info',
        30: 'Warning',
        0: 'Error'
    }

    initState = {
        messageLevel: 20,
        divClassElement: ['pop-up-message', 'fade-out'],
        divTitleClassElement: ['popup-title',],
        divContentClassElement: ['popup-content'],
        btnClassElement: ['close-btn'],
        animationTime: 3000,
    }

    _getMessageLevel(){
        if (!this.#classLevel[this.initState.messageLevel])
            return 0
        return this.initState.messageLevel
    }

    _createTitle(){
        const { divTitleClassElement, btnClassElement} = this.initState
        const messageLevel = this._getMessageLevel()

        const titleElement = document.createElement('div')
        titleElement.classList.add(...divTitleClassElement)
        titleElement.classList.add(this.#classLevel[messageLevel])
        const textElement = document.createElement('div')
        textElement.innerText = this.#textLevel[messageLevel]

        const btnElement = document.createElement('div')
        btnElement.classList.add(...btnClassElement)

        titleElement.append(textElement)
        titleElement.append(btnElement)

        return titleElement
    }

    getHandlerDisappearance(){
        const { animationTime } = this.initState
        return function(elem){
            elem.classList.add('hidden')
            setTimeout((elem) => {elem.remove()}, animationTime + 200, elem)
        }
    }

    _createContent(msg){
        const { divContentClassElement } = this.initState
        const contentElement = document.createElement('div')
        contentElement.classList.add(...divContentClassElement)
        contentElement.textContent = msg
        return contentElement
    }


    createElement(msg){
        const { divClassElement} = this.initState
        const containerElement = document.createElement('div')
        containerElement.id='popup-message'
        containerElement.classList.add(...divClassElement)


        containerElement.append(this._createTitle())
        containerElement.append(this._createContent(msg))

        return containerElement
    }

    getHandlerClose(){
        return (elem)=>{ 
            elem.target.closest('#popup-message').remove() 
        }
    }
}
