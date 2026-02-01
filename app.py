from flask import Flask, render_template, request, jsonify, send_file
from scraper import search_news, scrape_content
from prompts import get_blog_prompt
import requests
import json
from io import BytesIO

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    query = data.get('query')
    limit = int(data.get('limit', 10))
    preferred_sites = data.get('preferred_sites', [])
    
    urls = data.get('manual_urls', [])
    
    if urls:
        results = []
        for url in urls:
            results.append({
                'url': url.strip(),
                'title': url.strip()
            })
        return jsonify(results)
    else:
        results = search_news(query, limit, preferred_sites if preferred_sites else None)
        return jsonify(results)

@app.route('/generate', methods=['POST'])
def generate_blog():
    data = request.json
    selected_urls = data.get('urls', [])
    topic = data.get('topic', '')
    
    print(f"\n{'='*50}")
    print(f"Generando blog sobre: {topic}")
    print(f"URLs seleccionadas: {len(selected_urls)}")
    print(f"{'='*50}\n")
    
    # Extraer contenido de las URLs seleccionadas
    contents = []
    for idx, url in enumerate(selected_urls, 1):
        print(f"\n[{idx}/{len(selected_urls)}] Procesando: {url}")
        content = scrape_content(url)
        if content:
            contents.append(content)
    
    if not contents:
        return jsonify({'success': False, 'error': 'No se pudo extraer contenido de las URLs'})
    
    # Usar el prompt desde prompts.py
    combined_content = "\n\n---\n\n".join(contents)
    prompt = get_blog_prompt(topic, combined_content)

    print(f"\n{'='*50}")
    print("Enviando a Ollama...")
    print(f"{'='*50}\n")
    
    # Llamar a Ollama
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "llama3:latest",
                "prompt": prompt,
                "stream": False
            },
            timeout=120000
        )
        
        if response.status_code == 200:
            result = response.json()
            blog_text = result.get('response', '')
            
            print(f"\n{'='*50}")
            print("✓ Blog generado exitosamente")
            print(f"Longitud: {len(blog_text)} caracteres")
            print(f"{'='*50}\n")
            
            return jsonify({'success': True, 'blog': blog_text})
        else:
            error_msg = f"Error {response.status_code}: {response.text}"
            print(f"✗ {error_msg}")
            return jsonify({'success': False, 'error': error_msg})
            
    except requests.exceptions.Timeout:
        return jsonify({'success': False, 'error': 'Timeout: Ollama tardó demasiado. ¿Está corriendo?'})
    except requests.exceptions.ConnectionError:
        return jsonify({'success': False, 'error': 'No se pudo conectar a Ollama. Verifica que esté corriendo en http://localhost:11434'})
    except Exception as e:
        print(f"✗ Error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    content = data.get('content', '')
    
    buffer = BytesIO()
    buffer.write(content.encode('utf-8'))
    buffer.seek(0)
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name='blog.txt',
        mimetype='text/plain'
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)