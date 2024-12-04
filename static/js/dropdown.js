function toggleDropdown(event, button) {
    event.preventDefault();
    const dropdown = button.parentElement;
    const content = dropdown.querySelector('.content');

    // Toggle dropdown visibility
    if (content.style.display === 'none' || content.style.display === '') {
        content.style.display = 'block';
        button.classList.add('active');

        // Close dropdown if clicked outside
        document.addEventListener('click', handleOutsideClick);
    } else {
        content.style.display = 'none';
        button.classList.remove('active');

        // Remove event listener when dropdown closes
        document.removeEventListener('click', handleOutsideClick);
    }

    // Event handler for closing dropdown when clicking outside
    function handleOutsideClick(e) {
        // Check if the click is outside the dropdown
        if (!dropdown.contains(e.target)) {
            content.style.display = 'none';
            button.classList.remove('active');
            document.removeEventListener('click', handleOutsideClick);
        }
    }

    // Close dropdown if a button inside it is clicked
    content.querySelectorAll('button').forEach((dropdownButton) => {
        dropdownButton.addEventListener('click', () => {
            content.style.display = 'none';
            button.classList.remove('active');
            document.removeEventListener('click', handleOutsideClick);
        });
    });
}