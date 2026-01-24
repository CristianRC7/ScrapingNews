import requests
from bs4 import BeautifulSoup
import urllib.parse

def extract_image_from_url(url, headers):
    """Extrae la imagen principal de una URL"""
    try:
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Buscar Open Graph image (la más común en noticias)
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'):
            return og_image['content']
        
        # Buscar Twitter Card image
        twitter_image = soup.find('meta', attrs={'name': 'twitter:image'})
        if twitter_image and twitter_image.get('content'):
            return twitter_image['content']
        
        # Buscar la primera imagen en article
        article = soup.find('article')
        if article:
            img = article.find('img')
            if img and img.get('src'):
                img_src = img['src']
                if img_src.startswith('//'):
                    return 'https:' + img_src
                elif img_src.startswith('/'):
                    from urllib.parse import urljoin
                    return urljoin(url, img_src)
                return img_src
        
        # Buscar cualquier imagen grande
        for img in soup.find_all('img'):
            src = img.get('src', '')
            if src and ('width' in str(img.attrs) or 'height' in str(img.attrs)):
                try:
                    width = img.get('width', '0')
                    if isinstance(width, str):
                        width = width.replace('px', '').strip()
                    if width and int(width) > 200:
                        if src.startswith('//'):
                            return 'https:' + src
                        elif src.startswith('/'):
                            from urllib.parse import urljoin
                            return urljoin(url, src)
                        return src
                except:
                    continue
        
        return None
        
    except Exception as e:
        print(f"  Error extrayendo imagen: {e}")
        return None

def search_news(query, limit=10):
    results = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        # Usar DuckDuckGo HTML
        encoded_query = urllib.parse.quote_plus(query)
        url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
        
        print(f"Buscando en DuckDuckGo: {query}")
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscar todos los resultados
            for result in soup.find_all('div', class_='result'):
                if len(results) >= limit:
                    break
                    
                try:
                    # Obtener link
                    link = result.find('a', class_='result__a')
                    if not link:
                        continue
                    
                    title = link.get_text().strip()
                    href = link.get('href', '')
                    
                    # Limpiar URL de DuckDuckGo
                    if href.startswith('//'):
                        href = 'https:' + href
                    
                    # Extraer URL real del redirect de DuckDuckGo
                    if 'uddg=' in href:
                        import re
                        match = re.search(r'uddg=([^&]+)', href)
                        if match:
                            href = urllib.parse.unquote(match.group(1))
                    
                    if href and href.startswith('http'):
                        # Intentar extraer descripción
                        snippet = result.find('a', class_='result__snippet')
                        description = snippet.get_text().strip() if snippet else ""
                        
                        # Intentar extraer imagen
                        print(f"  Extrayendo imagen de: {title[:40]}...")
                        image_url = extract_image_from_url(href, headers)
                        
                        results.append({
                            'url': href,
                            'title': title[:150],
                            'description': description[:200],
                            'image': image_url or 'https://via.placeholder.com/300x200?text=Sin+Imagen'
                        })
                        print(f"✓ Encontrado: {title[:50]}... {'[con imagen]' if image_url else '[sin imagen]'}")
                        
                except Exception as e:
                    print(f"Error procesando resultado: {e}")
                    continue
            
            print(f"Total encontrados: {len(results)} resultados")
            
        else:
            print(f"Error: código {response.status_code}")
            
    except Exception as e:
        print(f"Error en búsqueda: {e}")
    
    return results

def scrape_content(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        print(f"Extrayendo contenido de: {url}")
        response = requests.get(url, timeout=15, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Eliminar elementos no deseados
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside', 'iframe', 'form']):
            element.decompose()
        
        # Buscar contenido principal
        content = ""
        
        # Intentar con article primero
        article = soup.find('article')
        if article:
            paragraphs = article.find_all('p')
            content = ' '.join([p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 20])
        
        # Si no, buscar en main
        if not content:
            main = soup.find('main')
            if main:
                paragraphs = main.find_all('p')
                content = ' '.join([p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 20])
        
        # Si no, todos los párrafos
        if not content:
            paragraphs = soup.find_all('p')
            content = ' '.join([p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 20])
        
        # Limpiar espacios extras
        content = ' '.join(content.split())
        
        print(f"✓ Extraídos {len(content)} caracteres")
        
        # Limitar a 5000 caracteres
        return content[:5000] if content else "No se pudo extraer contenido de esta página."
        
    except Exception as e:
        print(f"✗ Error extrayendo de {url}: {e}")
        return f"Error al extraer contenido: {str(e)}"