const gridContainer = document.getElementById('grid-container');
const importInput = document.getElementById('importInput');
const widthInput = document.getElementById('widthInput');
const heightInput = document.getElementById('heightInput');
const resizeBtn = document.getElementById('resizeBtn');
const exportBtn = document.getElementById('exportBtn');
const importBtn = document.getElementById('importBtn');
const clearBtn = document.getElementById('clearBtn');
const output = document.getElementById('output');
const copyBtn = document.getElementById('copyBtn');
const paletteItems = document.querySelectorAll('.palette-item');
const toolButtons = document.querySelectorAll('.tool-btn');

let currentType = 'X';
let currentTool = 'brush'; // brush, bucket
let isDrawing = false;
let gridWidth = 30;
let gridHeight = 15;

// Keyboard navigation
let selectedX = 0;
let selectedY = 0;

// Initialize
function init() {
    createGrid();
    setupEvents();
    updateSelection();
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
            
            // Mouse events
            cell.addEventListener('mousedown', (e) => {
                isDrawing = true;
                useTool(x, y);
                // Also select this cell
                selectedX = x;
                selectedY = y;
                updateSelection();
            });
            
            cell.addEventListener('mouseenter', (e) => {
                if (isDrawing) {
                    // Only brush supports drag
                    if (currentTool === 'brush') {
                        useTool(x, y);
                    }
                    // Update selection to follow mouse? Optional.
                    // Let's keep selection separate or follow mouse click.
                }
            });

            gridContainer.appendChild(cell);
        }
    }
}

function useTool(x, y) {
    if (x < 0 || x >= gridWidth || y < 0 || y >= gridHeight) return;
    
    if (currentTool === 'brush') {
        const cell = getCell(x, y);
        setCellType(cell, currentType);
    } else if (currentTool === 'bucket') {
        floodFill(x, y, currentType);
    }
}

function getCell(x, y) {
    // Flat index = y * width + x
    const index = y * gridWidth + x;
    return gridContainer.children[index];
}

function setCellType(cell, type) {
    if (!cell) return;
    cell.dataset.type = type;
    cell.className = 'cell'; // Reset classes
    if (x = cell.dataset.x, y = cell.dataset.y) {
       if (parseInt(x) === selectedX && parseInt(y) === selectedY) {
           cell.classList.add('keyboard-selected');
       }
    }

    if (type === ' ') {
        cell.classList.add('type-space');
        cell.textContent = '';
    } else {
        cell.classList.add(`type-${type}`);
        cell.textContent = type; 
    }
}

function floodFill(startX, startY, targetType) {
    const startCell = getCell(startX, startY);
    const startType = startCell.dataset.type;
    
    if (startType === targetType) return; // Already same color
    
    const queue = [[startX, startY]];
    const visited = new Set();
    
    while (queue.length > 0) {
        const [x, y] = queue.pop();
        const key = `${x},${y}`;
        
        if (visited.has(key)) continue;
        visited.add(key);
        
        const cell = getCell(x, y);
        if (!cell) continue;
        
        if (cell.dataset.type === startType) {
            setCellType(cell, targetType);
            
            // Neighbors
            if (x > 0) queue.push([x - 1, y]);
            if (x < gridWidth - 1) queue.push([x + 1, y]);
            if (y > 0) queue.push([x, y - 1]);
            if (y < gridHeight - 1) queue.push([x, y + 1]);
        }
    }
}

function updateSelection() {
    // Remove old selection
    document.querySelectorAll('.keyboard-selected').forEach(c => c.classList.remove('keyboard-selected'));
    
    // Add new
    const cell = getCell(selectedX, selectedY);
    if (cell) {
        cell.classList.add('keyboard-selected');
        // cell.scrollIntoView({ behavior: 'smooth', block: 'center' }); // Optional, might be annoying
    }
}

function setupEvents() {
    // Resize
    resizeBtn.addEventListener('click', () => {
        if (confirm("Resizing will clear the current grid. Continue?")) {
            createGrid();
            selectedX = 0;
            selectedY = 0;
            updateSelection();
        }
    });

    // Tools
    document.getElementById('toolBrush').addEventListener('click', () => setTool('brush'));
    document.getElementById('toolBucket').addEventListener('click', () => setTool('bucket'));

    function setTool(tool) {
        currentTool = tool;
        toolButtons.forEach(btn => btn.classList.remove('active'));
        if (tool === 'brush') document.getElementById('toolBrush').classList.add('active');
        if (tool === 'bucket') document.getElementById('toolBucket').classList.add('active');
    }

    // Clear
    clearBtn.addEventListener('click', () => {
        if (confirm("Clear entire grid?")) {
            for (let i = 0; i < gridContainer.children.length; i++) {
                setCellType(gridContainer.children[i], ' ');
            }
        }
    });

    // Palette
    paletteItems.forEach(item => {
        item.addEventListener('click', () => {
            paletteItems.forEach(i => i.classList.remove('active'));
            item.classList.add('active');
            currentType = item.dataset.type;
        });
    });

    // Mouse up
    document.addEventListener('mouseup', () => isDrawing = false);

    // Keyboard Navigation
    document.addEventListener('keydown', (e) => {
        // Prevent scrolling with arrows
        if(["ArrowUp","ArrowDown","ArrowLeft","ArrowRight", "Space"].indexOf(e.code) > -1) {
            e.preventDefault();
        }

        switch(e.code) {
            case 'ArrowUp':
                if (selectedY > 0) selectedY--;
                break;
            case 'ArrowDown':
                if (selectedY < gridHeight - 1) selectedY++;
                break;
            case 'ArrowLeft':
                if (selectedX > 0) selectedX--;
                break;
            case 'ArrowRight':
                if (selectedX < gridWidth - 1) selectedX++;
                break;
            case 'Space':
                useTool(selectedX, selectedY);
                break;
        }
        updateSelection();
    });

    // Export
    exportBtn.addEventListener('click', exportLevel);
    importBtn.addEventListener('click', importLevel);

    // Copy
    copyBtn.addEventListener('click', () => {
        output.select();
        document.execCommand('copy');
    });
}

function exportLevel() {
    let pyCode = "NEW_LEVEL = [\n";
    for (let y = 0; y < gridHeight; y++) {
        let rowStr = '    "';
        for (let x = 0; x < gridWidth; x++) {
            const cell = getCell(x, y);
            rowStr += cell.dataset.type || ' ';
        }
        rowStr += '",';
        pyCode += rowStr + "\n";
    }
    pyCode += "]";
    output.value = pyCode;
}

function importLevel() {
    const raw = importInput.value;
    if (!raw.trim()) {
        alert("Paste Python list code into the 'Import Level' box and click Import.");
        return;
    }

    try {
        // Simple parse: find content between brackets and quotes
        // Remove variable assignment etc, just get lines
        // Improve regex to capture strings inside list
        const rows = raw.match(/"([^"]*)"/g);
        
        if (!rows || rows.length === 0) {
            throw new Error("No string rows found");
        }
        
        // Clean quotes
        const cleanRows = rows.map(r => r.replace(/"/g, ''));
        
        const newHeight = cleanRows.length;
        const newWidth = cleanRows[0].length;
        
        // Resize grid
        widthInput.value = newWidth;
        heightInput.value = newHeight;
        createGrid(); // resets grid
        
        // Fill grid
        for (let y = 0; y < newHeight; y++) {
            const rowStr = cleanRows[y];
            for (let x = 0; x < newWidth; x++) {
                if (x < rowStr.length) {
                    const char = rowStr[x];
                    const cell = getCell(x, y);
                    setCellType(cell, char);
                }
            }
        }
        
        alert("Level imported successfully!");

    } catch (e) {
        alert("Import failed: " + e.message + "\nMake sure to paste a valid Python list of strings.");
    }
}

// Start
init();
