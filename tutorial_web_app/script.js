document.addEventListener('DOMContentLoaded', () => {
    const toggles = document.querySelectorAll('.btn-toggle');

    toggles.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = btn.getAttribute('data-target');
            const codeBlock = document.getElementById(targetId);
            
            if (codeBlock.classList.contains('visible')) {
                codeBlock.classList.remove('visible');
                btn.textContent = 'Show Solution';
            } else {
                codeBlock.classList.add('visible');
                btn.textContent = 'Hide Solution';
            }
        });
    });
});
