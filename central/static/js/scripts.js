
const button = document.querySelector(`#spec`);
const content = document.querySelector(`#spec_text`);

button.addEventListener('click', () => {
    if (content.style.display != 'none') {
        button.textContent = 'Display';
        content.style.display = 'none';
    }
    else {
        button.textContent = 'Hide';
        content.style.display = 'block';
    }
})