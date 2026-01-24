// static/script.js
let searchResults = [];
let selectedUrls = [];

document.getElementById('searchBtn').addEventListener('click', performSearch);
document.getElementById('generateBtn').addEventListener('click', generateBlog);
document.getElementById('downloadBtn').addEventListener('click', downloadBlog);

async function performSearch() {
    const query = document.getElementById('searchQuery').value.trim();
    const limit = document.getElementById('limitPages').value;
    
    if (!query) {
        alert('Por favor escribe un título de noticia');
        return;
    }
    
    document.getElementById('loading').style.display = 'block';
    document.getElementById('results').innerHTML = '';
    document.getElementById('selectedSection').style.display = 'none';
    document.getElementById('blogSection').style.display = 'none';
    selectedUrls = [];
    
    try {
        const response = await fetch('/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query, limit })
        });
        
        searchResults = await response.json();
        displayResults(searchResults);
    } catch (error) {
        alert('Error al realizar la búsqueda: ' + error.message);
    } finally {
        document.getElementById('loading').style.display = 'none';
    }
}

function displayResults(results) {
    const resultsDiv = document.getElementById('results');
    
    if (results.length === 0) {
        resultsDiv.innerHTML = '<p>No se encontraron resultados</p>';
        return;
    }
    
    results.forEach((result, index) => {
        const resultItem = document.createElement('div');
        resultItem.className = 'result-item';
        resultItem.innerHTML = `
            <input type="checkbox" id="result-${index}" data-url="${result.url}">
            <div class="result-image">
                <img src="${result.image}" alt="${result.title}" onerror="this.src='https://via.placeholder.com/300x200?text=Sin+Imagen'">
            </div>
            <div class="result-content">
                <label for="result-${index}">
                    <h4>${result.title}</h4>
                    ${result.description ? `<p class="description">${result.description}</p>` : ''}
                    <a href="${result.url}" target="_blank" class="result-url">${result.url}</a>
                </label>
            </div>
        `;
        
        const checkbox = resultItem.querySelector('input[type="checkbox"]');
        checkbox.addEventListener('change', updateSelection);
        
        resultItem.addEventListener('click', (e) => {
            if (e.target.tagName !== 'A' && e.target.tagName !== 'INPUT') {
                checkbox.checked = !checkbox.checked;
                updateSelection.call(checkbox);
            }
        });
        
        resultsDiv.appendChild(resultItem);
    });
}

function updateSelection() {
    const checkboxes = document.querySelectorAll('.result-item input[type="checkbox"]');
    selectedUrls = Array.from(checkboxes)
        .filter(cb => cb.checked)
        .map(cb => cb.dataset.url);
    
    document.getElementById('selectedCount').textContent = selectedUrls.length;
    
    if (selectedUrls.length > 0) {
        document.getElementById('selectedSection').style.display = 'block';
    } else {
        document.getElementById('selectedSection').style.display = 'none';
    }
    
    // Actualizar visualización
    checkboxes.forEach(cb => {
        const item = cb.closest('.result-item');
        if (cb.checked) {
            item.classList.add('selected');
        } else {
            item.classList.remove('selected');
        }
    });
}

async function generateBlog() {
    if (selectedUrls.length === 0) {
        alert('Selecciona al menos una página');
        return;
    }
    
    const query = document.getElementById('searchQuery').value;
    const generateBtn = document.getElementById('generateBtn');
    
    generateBtn.disabled = true;
    generateBtn.textContent = 'Generando blog...';
    
    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                urls: selectedUrls,
                topic: query
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            document.getElementById('blogContent').textContent = result.blog;
            document.getElementById('blogSection').style.display = 'block';
            document.getElementById('blogSection').scrollIntoView({ behavior: 'smooth' });
        } else {
            alert('Error al generar el blog: ' + result.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        generateBtn.disabled = false;
        generateBtn.textContent = 'Generar Blog';
    }
}

function downloadBlog() {
    const content = document.getElementById('blogContent').textContent;
    
    const blob = new Blob([content], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'blog.txt';
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
}