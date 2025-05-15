function closeMessage(button) {
    const message = button.parentElement;
    message.classList.add('fade-out');
    setTimeout(() => {
        message.style.display = 'none';
    }, 300);
}