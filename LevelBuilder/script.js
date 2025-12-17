const gridContainer = document.getElementById('grid-container');
const widthInput = document.getElementById('widthInput');
const heightInput = document.getElementById('heightInput');
const resizeBtn = document.getElementById('resizeBtn');
const exportBtn = document.getElementById('exportBtn');
const clearBtn = document.getElementById('clearBtn');
const output = document.getElementById('output');
const copyBtn = document.getElementById('copyBtn');
const paletteItems = document.querySelectorAll('.palette-item');

let currentType = 'X';
let isDrawing = false;
let gridWidth = 30;
let gridHeight = 15;

// Initialize
function init() {
    createGrid();
    setupEvents();
}

function createGrid() {
    gridWidth = parseInt(widthInput.value);
    gridHeight = parseInt(heightInput.value);

    gridContainer.style.gridTemplateColumns = `repeat(${gridWidth}, 25px)`;
    gridContainer.innerHTML = '';

    for (let y = 0; y < gridHeight; y++) {
        for (let x = 0; x < gridWidth; x++) {
            const cell = document.createElement('div');
            cell.classList.add('cell');
            cell.dataset.x = x;
            cell.dataset.y = y;
            cell.dataset.type = ' '; // Default empty
            
            cell.addEventListener('mousedown', (e) => {
                isDrawing = true;
                setCellType(cell);
            });
            
            cell.addEventListener('mouseenter', (e) => {
                if (isDrawing) {
                    setCellType(cell);
                }
            });

            gridContainer.appendChild(cell);
        }
    }
}

function setCellType(cell) {
    cell.dataset.type = currentType;
    cell.className = 'cell'; // Reset classes
    
    // Add specific class for color
    if (currentType === ' ') {
        cell.classList.add('type-space');
    } else {
        cell.classList.add(`type-${currentType}`);
        cell.textContent = currentType; // Show letter
    }
    
    if (currentType === ' ') cell.textContent = '';
}

function setupEvents() {
    // Resize
    resizeBtn.addEventListener('click', () => {
        if (confirm("Resizing will clear the current grid. Continue?")) {
            createGrid();
        }
    });

    // Clear
    clearBtn.addEventListener('click', () => {
        if (confirm("Clear entire grid?")) {
            document.querySelectorAll('.cell').forEach(cell => {
                currentType = ' ';
                setCellType(cell);
            });
            // Reset to previous tool or keep eraser? Let's reset tool to space or X? 
            // Actually, just clearing doesn't change tool.
        }
    });

    // Palette Selection
    paletteItems.forEach(item => {
        item.addEventListener('click', () => {
            paletteItems.forEach(i => i.classList.remove('active'));
            item.classList.add('active');
            currentType = item.dataset.type;
        });
    });

    // Stop drawing on mouseup anywhere
    document.addEventListener('mouseup', () => {
        isDrawing = false;
    });

    // Export
    exportBtn.addEventListener('click', exportLevel);

    // Copy
    copyBtn.addEventListener('click', () => {
        output.select();
        document.execCommand('copy'); // Legacy but works widely
        // Navigator clipboard API
        if (navigator.clipboard) {
            navigator.clipboard.writeText(output.value).then(() => {
                const originalText = copyBtn.textContent;
                copyBtn.textContent = "Copied!";
                setTimeout(() => copyBtn.textContent = originalText, 1500);
            });
        }
    });
}

function exportLevel() {
    let pyCode = "NEW_LEVEL = [\n";
    
    const cells = Array.from(document.querySelectorAll('.cell'));
    
    for (let y = 0; y < gridHeight; y++) {
        let rowStr = '    "';
        for (let x = 0; x < gridWidth; x++) {
            // Formula to find cell index in flat array: y * width + x
            const index = y * gridWidth + x;
            const cell = cells[index];
            rowStr += cell.dataset.type || ' ';
        }
        rowStr += '",';
        pyCode += rowStr + "\n";
    }
    
    pyCode += "]";
    output.value = pyCode;
}

// Start
init();
