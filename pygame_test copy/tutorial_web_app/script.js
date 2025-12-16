document.addEventListener('DOMContentLoaded', () => {
    // 1. Handle Toggle Buttons
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

    // 2. Inject Copy Buttons
    const codeBlocks = document.querySelectorAll('.code-solution');
    codeBlocks.forEach(block => {
        const copyBtn = document.createElement('button');
        copyBtn.className = 'btn-copy';
        copyBtn.textContent = 'Copy';
        
        copyBtn.addEventListener('click', () => {
            const codeText = block.querySelector('pre').innerText;
            navigator.clipboard.writeText(codeText).then(() => {
                copyBtn.textContent = 'Copied!';
                setTimeout(() => {
                    copyBtn.textContent = 'Copy';
                }, 2000);
            });
        });

        block.insertBefore(copyBtn, block.firstChild);
    });
});
