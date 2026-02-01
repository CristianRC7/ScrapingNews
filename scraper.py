import requests
from bs4 import BeautifulSoup
import urllib.parse
import time
import random

try:
    from config import (
        DELAY_BETWEEN_PREFERRED_SITES,
        DELAY_BEFORE_GENERAL_SEARCH,
        DELAY_AFTER_RATE_LIMIT,
        MAX_RETRIES_ON_RATE_LIMIT,
        MAX_RESULTS_PER_PREFERRED_SITE,
        REQUEST_TIMEOUT,
        CONTENT_CHAR_LIMIT,
        USER_AGENTS
    )
except ImportError:
    DELAY_BETWEEN_PREFERRED_SITES = (2, 4)
    DELAY_BEFORE_GENERAL_SEARCH = (3, 5)
    DELAY_AFTER_RATE_LIMIT = 20
    MAX_RETRIES_ON_RATE_LIMIT = 1
    MAX_RESULTS_PER_PREFERRED_SITE = 3
    REQUEST_TIMEOUT = 20
    CONTENT_CHAR_LIMIT = 500000
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    ]

def get_random_user_agent():
    """Retorna un User-Agent aleatorio"""
    return random.choice(USER_AGENTS)

def search_directly_in_site(site_url, query):
    """
    Busca DIRECTAMENTE en el sitio web (sin DuckDuckGo)
    Esto evita completamente el spam
    """
    results = []
    try:
        from urllib.parse import urlparse
        domain = urlparse(site_url).netloc
        if not domain:
            domain = site_url
        
        # Construir URL de búsqueda del sitio (común en muchos sitios)
        # Intentar varios formatos comunes
        search_urls = [
            f"{site_url}/search?q={urllib.parse.quote_plus(query)}",
            f"{site_url}/buscar?q={urllib.parse.quote_plus(query)}",
            f"{site_url}/?s={urllib.parse.quote_plus(query)}",
        ]
        
        headers = {'User-Agent': get_random_user_agent()}
        
        print(f"  Buscando directamente en {domain}...")
        
        # Intentar con cada formato de URL
        for search_url in search_urls:
            try:
                response = requests.get(search_url, headers=headers, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Buscar enlaces que contengan el query
                    links = soup.find_all('a', href=True)
                    found = 0
                    
                    for link in links:
                        if found >= MAX_RESULTS_PER_PREFERRED_SITE:
                            break
                        
                        href = link.get('href', '')
                        title = link.get_text().strip()
                        
                        # Validar que sea un enlace válido
                        if not href or not title or len(title) < 10:
                            continue
                        
                        # Convertir a URL absoluta
                        if href.startswith('/'):
                            href = site_url.rstrip('/') + href
                        elif not href.startswith('http'):
                            continue
                        
                        # Verificar que sea del mismo dominio
                        if domain not in href:
                            continue
                        
                        results.append({
                            'url': href,
                            'title': title[:150],
                            'description': f"Resultado de {domain}",
                            'image': 'https://via.placeholder.com/300x200?text=Noticia',
                            'is_preferred': True
                        })
                        found += 1
                        print(f"  ✓ {title[:40]}...")
                    
                    if results:
                        break  # Si encontró resultados, no seguir probando
                        
            except Exception as e:
                continue
        
        if not results:
            print(f"  ⚠️ No se encontraron resultados en {domain}")
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    return results

def search_news(query, limit=10, preferred_sites=None):
    """
    Búsqueda optimizada
    Estrategia:
    1. Si NO hay sitios preferidos → Solo búsqueda general
    2. Si HAY sitios preferidos → Busca directo en esos sitios (sin DuckDuckGo) + general
    """
    all_results = []
    headers = {'User-Agent': get_random_user_agent()}
    
    print(f"\n{'='*60}")
    print(f"BÚSQUEDA: '{query}' (límite: {limit})")
    print(f"{'='*60}")
    
    # ESTRATEGIA 1: Sitios preferidos (búsqueda DIRECTA, no por DuckDuckGo)
    if preferred_sites and len(preferred_sites) > 0:
        print(f"\n--- SITIOS PREFERIDOS ({len(preferred_sites)}) ---")
        print("Buscando directamente en cada sitio (sin intermediarios)\n")
        
        for idx, site in enumerate(preferred_sites, 1):
            site_name = site.get('name', 'Desconocido')
            site_url = site.get('url', '')
            
            print(f"[{idx}/{len(preferred_sites)}] {site_name}")
            
            # Delay corto entre sitios (no es DuckDuckGo, podemos ser más rápidos)
            if idx > 1:
                delay = random.uniform(1, 2)
                print(f"    ⏱️ Esperando {delay:.1f}s...")
                time.sleep(delay)
            
            # Buscar DIRECTAMENTE en el sitio
            preferred_results = search_directly_in_site(site_url, query)
            
            for result in preferred_results:
                result['site_name'] = site_name
            
            all_results.extend(preferred_results)
        
        print(f"\n✓ Preferidos: {len(all_results)} resultados")
    
    # ESTRATEGIA 2: Búsqueda general en DuckDuckGo
    remaining_slots = limit - len(all_results)
    
    if remaining_slots > 0:
        print(f"\n--- BÚSQUEDA GENERAL ({remaining_slots} resultados) ---\n")
        
        # Delay solo si hubo preferidos
        if all_results:
            delay = random.uniform(*DELAY_BEFORE_GENERAL_SEARCH)
            print(f"⏱️ Esperando {delay:.1f}s...")
            time.sleep(delay)
        
        try:
            headers['User-Agent'] = get_random_user_agent()
            encoded_query = urllib.parse.quote_plus(query)
            url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
            
            print(f"🔍 Buscando en DuckDuckGo...")
            
            response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
            
            # Manejar 202
            if response.status_code == 202:
                print(f"⚠️ Rate limit (202). Esperando {DELAY_AFTER_RATE_LIMIT}s...")
                time.sleep(DELAY_AFTER_RATE_LIMIT)
                
                headers['User-Agent'] = get_random_user_agent()
                response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
                
                if response.status_code == 202:
                    print(f"❌ Bloqueado. Mostrando {len(all_results)} resultados")
                    return all_results
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                existing_urls = {result['url'] for result in all_results}
                general_count = 0
                
                for result in soup.find_all('div', class_='result'):
                    if len(all_results) >= limit:
                        break
                    
                    try:
                        link = result.find('a', class_='result__a')
                        if not link:
                            continue
                        
                        title = link.get_text().strip()
                        href = link.get('href', '')
                        
                        if href.startswith('//'):
                            href = 'https:' + href
                        
                        if 'uddg=' in href:
                            import re
                            match = re.search(r'uddg=([^&]+)', href)
                            if match:
                                href = urllib.parse.unquote(match.group(1))
                        
                        if href in existing_urls or not href.startswith('http'):
                            continue
                        
                        snippet = result.find('a', class_='result__snippet')
                        description = snippet.get_text().strip() if snippet else ""
                        
                        all_results.append({
                            'url': href,
                            'title': title[:150],
                            'description': description[:200],
                            'image': 'https://via.placeholder.com/300x200?text=Noticia',
                            'is_preferred': False
                        })
                        existing_urls.add(href)
                        general_count += 1
                        print(f"  ✓ {title[:50]}...")
                        
                    except Exception as e:
                        continue
                
                print(f"\n✓ Generales: {general_count} resultados")
            else:
                print(f"⚠️ Error {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Resumen
    preferred_count = sum(1 for r in all_results if r.get('is_preferred', False))
    general_count = sum(1 for r in all_results if not r.get('is_preferred', False))
    
    print(f"\n{'='*60}")
    print(f"RESUMEN:")
    print(f"  ⭐ Preferidos: {preferred_count}")
    print(f"  🌐 Generales: {general_count}")
    print(f"  📊 TOTAL: {len(all_results)}")
    print(f"{'='*60}\n")
    
    return all_results

def scrape_content(url):
    """Extrae contenido de una URL"""
    try:
        headers = {'User-Agent': get_random_user_agent()}
        
        print(f"Extrayendo: {url}")
        response = requests.get(url, timeout=REQUEST_TIMEOUT, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Eliminar elementos no deseados
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside', 'iframe', 'form']):
            element.decompose()
        
        content = ""
        
        # Intentar con article
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
        
        # Limpiar
        content = ' '.join(content.split())
        
        print(f"✓ Extraídos {len(content)} caracteres")
        
        return content[:CONTENT_CHAR_LIMIT] if content else "No se pudo extraer contenido."
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return f"Error al extraer contenido: {str(e)}"