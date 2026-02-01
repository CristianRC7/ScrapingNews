let searchResults = [];
let selectedUrls = [];
let preferredSites = [];

// Constantes para localStorage
const STORAGE_KEY = 'preferred_sites';
const TOGGLE_STATE_KEY = 'preferred_toggle_state';

// Cargar sitios preferidos desde localStorage al iniciar
document.addEventListener('DOMContentLoaded', function() {
    loadPreferredSites();
    loadToggleState();
});

document.getElementById('addSiteBtn').addEventListener('click', addPreferredSite);
document.getElementById('searchBtn').addEventListener('click', performSearch);
document.getElementById('generateBtn').addEventListener('click', generateBlog);
document.getElementById('downloadBtn').addEventListener('click', downloadBlog);
document.getElementById('togglePreferredBtn').addEventListener('click', togglePreferredSection);

// ====================================
// SISTEMA DE BLOQUEO DE BOTONES
// ====================================

function disableAllButtons() {
    const searchBtn = document.getElementById('searchBtn');
    const generateBtn = document.getElementById('generateBtn');
    
    searchBtn.disabled = true;
    searchBtn.style.opacity = '0.5';
    
    generateBtn.disabled = true;
    generateBtn.style.opacity = '0.5';
}

function enableAllButtons() {
    const searchBtn = document.getElementById('searchBtn');
    const generateBtn = document.getElementById('generateBtn');
    
    searchBtn.disabled = false;
    searchBtn.style.opacity = '1';
    
    generateBtn.disabled = false;
    generateBtn.style.opacity = '1';
}

// ====================================
// TOGGLE MOSTRAR/OCULTAR
// ====================================

function togglePreferredSection() {
    const content = document.getElementById('preferredContent');
    const btn = document.getElementById('togglePreferredBtn');
    
    if (content.style.display === 'none') {
        // Mostrar
        content.style.display = 'block';
        btn.textContent = '▼ Ocultar';
        localStorage.setItem(TOGGLE_STATE_KEY, 'shown');
    } else {
        // Ocultar
        content.style.display = 'none';
        btn.textContent = '▶ Mostrar';
        localStorage.setItem(TOGGLE_STATE_KEY, 'hidden');
    }
}

function loadToggleState() {
    const state = localStorage.getItem(TOGGLE_STATE_KEY);
    const content = document.getElementById('preferredContent');
    const btn = document.getElementById('togglePreferredBtn');
    
    if (state === 'hidden') {
        content.style.display = 'none';
        btn.textContent = '▶ Mostrar';
    } else {
        content.style.display = 'block';
        btn.textContent = '▼ Ocultar';
    }
}

// ====================================
// FUNCIONES DE LOCALSTORAGE
// ====================================

function saveToLocalStorage() {
    try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(preferredSites));
        console.log('✓ Sitios guardados en localStorage');
    } catch (error) {
        console.error('Error guardando en localStorage:', error);
        alert('No se pudieron guardar los sitios. Verifica que tu navegador permita localStorage.');
    }
}

function loadFromLocalStorage() {
    try {
        const stored = localStorage.getItem(STORAGE_KEY);
        if (stored) {
            preferredSites = JSON.parse(stored);
            console.log(`✓ Cargados ${preferredSites.length} sitios desde localStorage`);
        } else {
            preferredSites = [];
            console.log('No hay sitios preferidos guardados');
        }
    } catch (error) {
        console.error('Error cargando desde localStorage:', error);
        preferredSites = [];
    }
}

function loadPreferredSites() {
    loadFromLocalStorage();
    displayPreferredSites();
}

// ====================================
// GESTIÓN DE SITIOS PREFERIDOS
// ====================================

function addPreferredSite() {
    const name = document.getElementById('siteName').value.trim();
    const url = document.getElementById('siteUrl').value.trim();
    
    if (!name || !url) {
        alert('Por favor completa el nombre y la URL del sitio');
        return;
    }
    
    // Validar URL
    let validUrl = url;
    if (!validUrl.startsWith('http://') && !validUrl.startsWith('https://')) {
        validUrl = 'https://' + validUrl;
    }
    
    // Verificar duplicados
    if (preferredSites.some(site => site.url === validUrl)) {
        alert('Este sitio ya está en la lista de preferencias');
        return;
    }
    
    // Agregar nuevo sitio
    const newSite = {
        id: Date.now(),
        name: name,
        url: validUrl
    };
    
    preferredSites.push(newSite);
    saveToLocalStorage();
    displayPreferredSites();
    
    document.getElementById('siteName').value = '';
    document.getElementById('siteUrl').value = '';
    
    console.log('✓ Sitio agregado:', newSite);
}

function deletePreferredSite(siteId) {
    if (!confirm('¿Eliminar este sitio de preferencias?')) {
        return;
    }
    
    preferredSites = preferredSites.filter(site => site.id !== siteId);
    saveToLocalStorage();
    displayPreferredSites();
    
    console.log('✓ Sitio eliminado:', siteId);
}

function displayPreferredSites() {
    const listDiv = document.getElementById('preferredSitesList');
    
    if (preferredSites.length === 0) {
        listDiv.innerHTML = '<p class="no-sites">No hay sitios preferidos. Agrega algunos para priorizarlos en las búsquedas.</p>';
        return;
    }
    
    listDiv.innerHTML = preferredSites.map(site => `
        <div class="preferred-site-item">
            <div class="site-info">
                <strong>⭐ ${site.name}</strong>
                <span class="site-url">${site.url}</span>
            </div>
            <button class="delete-site-btn" onclick="deletePreferredSite(${site.id})">🗑️</button>
        </div>
    `).join('');
}

// ====================================
// BÚSQUEDA DE NOTICIAS
// ====================================

async function performSearch() {
    const query = document.getElementById('searchQuery').value.trim();
    const limit = document.getElementById('limitPages').value;
    
    if (!query) {
        alert('Por favor escribe un título de noticia');
        return;
    }
    
    const searchBtn = document.getElementById('searchBtn');
    const originalBtnText = searchBtn.textContent;
    
    // BLOQUEAR TODOS LOS BOTONES
    disableAllButtons();
    searchBtn.textContent = '🔄 Buscando...';
    searchBtn.style.cursor = 'not-allowed';
    
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
            body: JSON.stringify({ 
                query, 
                limit,
                preferred_sites: preferredSites
            })
        });
        
        searchResults = await response.json();
        displayResults(searchResults);
    } catch (error) {
        alert('Error al realizar la búsqueda: ' + error.message);
        console.error('Error en búsqueda:', error);
    } finally {
        document.getElementById('loading').style.display = 'none';
        
        // REHABILITAR TODOS LOS BOTONES
        enableAllButtons();
        searchBtn.textContent = originalBtnText;
        searchBtn.style.cursor = 'pointer';
    }
}

function displayResults(results) {
    const resultsDiv = document.getElementById('results');
    
    if (results.length === 0) {
        resultsDiv.innerHTML = '<p class="no-results">No se encontraron resultados</p>';
        return;
    }
    
    const preferredResults = results.filter(r => r.is_preferred);
    const generalResults = results.filter(r => !r.is_preferred);
    
    let html = '';
    
    if (preferredResults.length > 0) {
        html += '<h3 class="results-section-title">⭐ Resultados de Sitios Preferidos</h3>';
        html += renderResults(preferredResults, true);
    }
    
    if (generalResults.length > 0) {
        html += '<h3 class="results-section-title">🌐 Resultados Generales</h3>';
        html += renderResults(generalResults, false);
    }
    
    resultsDiv.innerHTML = html;
    
    document.querySelectorAll('.result-item input[type="checkbox"]').forEach(checkbox => {
        checkbox.addEventListener('change', updateSelection);
    });
    
    document.querySelectorAll('.result-item').forEach(item => {
        item.addEventListener('click', (e) => {
            if (e.target.tagName !== 'A' && e.target.tagName !== 'INPUT') {
                const checkbox = item.querySelector('input[type="checkbox"]');
                checkbox.checked = !checkbox.checked;
                updateSelection.call(checkbox);
            }
        });
    });
}

function renderResults(results, isPreferred) {
    let startIndex = isPreferred ? 0 : searchResults.filter(r => r.is_preferred).length;
    
    return results.map((result, index) => {
        const actualIndex = startIndex + index;
        const badgeClass = isPreferred ? 'preferred-badge' : '';
        const badge = isPreferred ? `<span class="${badgeClass}">⭐ ${result.site_name || 'Preferido'}</span>` : '';
        
        return `
            <div class="result-item ${isPreferred ? 'preferred-result' : ''}">
                <input type="checkbox" id="result-${actualIndex}" data-url="${result.url}">
                <div class="result-content">
                    <label for="result-${actualIndex}">
                        ${badge}
                        <h4>${result.title}</h4>
                        ${result.description ? `<p class="description">${result.description}</p>` : ''}
                        <a href="${result.url}" target="_blank" class="result-url">${result.url}</a>
                    </label>
                </div>
            </div>
        `;
    }).join('');
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
    
    checkboxes.forEach(cb => {
        const item = cb.closest('.result-item');
        if (cb.checked) {
            item.classList.add('selected');
        } else {
            item.classList.remove('selected');
        }
    });
}

// ====================================
// GENERACIÓN DE BLOG
// ====================================

async function generateBlog() {
    if (selectedUrls.length === 0) {
        alert('Selecciona al menos una página');
        return;
    }
    
    const query = document.getElementById('searchQuery').value;
    const generateBtn = document.getElementById('generateBtn');
    const originalBtnText = generateBtn.textContent;
    
    // BLOQUEAR TODOS LOS BOTONES
    disableAllButtons();
    generateBtn.textContent = '⏳ Generando blog...';
    generateBtn.style.cursor = 'not-allowed';
    
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
        console.error('Error en generación:', error);
    } finally {
        // REHABILITAR TODOS LOS BOTONES
        enableAllButtons();
        generateBtn.textContent = originalBtnText;
        generateBtn.style.cursor = 'pointer';
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