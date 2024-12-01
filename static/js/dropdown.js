function toggleDropdown(event, button) {
    event.preventDefault();
    const dropdown = button.parentElement;
    const content = dropdown.querySelector('.content');

    if (content.style.display === 'none' || content.style.display === '') {
        content.style.display = 'block';
        button.classList.add('active');
    } else {
        content.style.display = 'none';
        button.classList.remove('active');
    }
}
