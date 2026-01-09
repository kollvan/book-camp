function changeValue(direction, input) {
    let currentValue = parseInt(input.value) || parseInt(input.min) || 0;
    const min = parseInt(input.min) || 0;
    const max = parseInt(input.max) || 3000;
    const step = parseInt(input.step) || 1;

    let newValue = direction === 'up' ? currentValue + step : currentValue - step;

    if (newValue < min) input.value = min
    else if (newValue > max) input.value = max
    else input.value = newValue;

    input.dispatchEvent(new Event('input', { bubbles: true }));
    input.dispatchEvent(new Event('change', { bubbles: true }));

    input.dispatchEvent(new CustomEvent('valueChanged', {
        detail: { value: newValue, direction: direction }
    }));
}
document.addEventListener('DOMContentLoaded', function(){
    const inputFrom = document.querySelector('#from-year-publication');
    const inputTo = document.querySelector('#to-year-publication');
    const buttonFromUp = document.querySelector('#button-from-up');
    const buttonFromDown = document.querySelector('#button-from-down');
    const buttonToUp = document.querySelector('#button-to-up');
    const buttonToDown = document.querySelector('#button-to-down');

    buttonFromUp.addEventListener('click', () => changeValue('up', inputFrom));
    buttonFromDown.addEventListener('click', () => changeValue('down', inputFrom));
    buttonToUp.addEventListener('click', () => changeValue('up', inputTo));
    buttonToDown.addEventListener('click', () => changeValue('down', inputTo));
});
