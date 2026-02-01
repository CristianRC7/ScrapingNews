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
    # Valores por defecto si no existe config.py
    DELAY_BETWEEN_PREFERRED_SITES = (8, 12)
    DELAY_BEFORE_GENERAL_SEARCH = (8, 12)
    DELAY_AFTER_RATE_LIMIT = 20
    MAX_RETRIES_ON_RATE_LIMIT = 1
    MAX_RESULTS_PER_PREFERRED_SITE = 2
    REQUEST_TIMEOUT = 20
    CONTENT_CHAR_LIMIT = 500000
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    ]

def get_random_user_agent():
    """Retorna un User-Agent aleatorio para evitar detección"""
    return random.choice(USER_AGENTS)

def search_in_preferred_site(site_url, query, headers):
    """Busca en un sitio específico - SIMPLIFICADO"""
    results = []
    try:
        # Usar User-Agent aleatorio
        headers = headers.copy()
        headers['User-Agent'] = get_random_user_agent()
        
        # Extraer dominio del sitio
        from urllib.parse import urlparse
        domain = urlparse(site_url).netloc
        if not domain:
            domain = site_url
        
        # Buscar en sitio específico
        search_query = f"site:{domain} {query}"
        encoded_query = urllib.parse.quote_plus(search_query)
        url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
        
        print(f"  Buscando en {domain}...")
        
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        
        # Manejar código 202
        if response.status_code == 202:
            print(f"  ⚠️ Spam detectado (202). Esperando {DELAY_AFTER_RATE_LIMIT}s...")
            time.sleep(DELAY_AFTER_RATE_LIMIT)
            response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
            if response.status_code == 202:
                print(f"  ❌ Sitio bloqueado, saltando...")
                return results
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscar resultados
            for result in soup.find_all('div', class_='result')[:MAX_RESULTS_PER_PREFERRED_SITE]:
                try:
                    link = result.find('a', class_='result__a')
                    if not link:
                        continue
                    
                    title = link.get_text().strip()
                    href = link.get('href', '')
                    
                    # Limpiar URL
                    if href.startswith('//'):
                        href = 'https:' + href
                    
                    # Extraer URL real del redirect de DuckDuckGo
                    if 'uddg=' in href:
                        import re
                        match = re.search(r'uddg=([^&]+)', href)
                        if match:
                            href = urllib.parse.unquote(match.group(1))
                    
                    if href and href.startswith('http'):
                        snippet = result.find('a', class_='result__snippet')
                        description = snippet.get_text().strip() if snippet else ""
                        
                        results.append({
                            'url': href,
                            'title': title[:150],
                            'description': description[:200],
                            'image': 'https://via.placeholder.com/300x200?text=Noticia',
                            'is_preferred': True
                        })
                        print(f"  ✓ {title[:40]}...")
                        
                except Exception as e:
                    print(f"  Error: {e}")
                    continue
                    
    except Exception as e:
        print(f"  Error en sitio: {e}")
    
    return results

def search_news(query, limit=10, preferred_sites=None):
    """
    Busca noticias priorizando sitios preferidos
    GARANTIZA resultados generales siempre que sea posible
    """
    all_results = []
    headers = {'User-Agent': get_random_user_agent()}
    
    print(f"\n{'='*60}")
    print(f"INICIANDO BÚSQUEDA: '{query}' (límite: {limit})")
    print(f"{'='*60}")
    
    # 1. Buscar en sitios preferidos (SI EXISTEN)
    if preferred_sites and len(preferred_sites) > 0:
        print(f"\n--- FASE 1: SITIOS PREFERIDOS ({len(preferred_sites)} sitios) ---\n")
        
        for idx, site in enumerate(preferred_sites, 1):
            site_name = site.get('name', 'Desconocido')
            site_url = site.get('url', '')
            
            print(f"[{idx}/{len(preferred_sites)}] {site_name}")
            
            # DELAY entre sitios (no antes del primero)
            if idx > 1:
                delay = random.uniform(*DELAY_BETWEEN_PREFERRED_SITES)
                print(f"    ⏱️  Esperando {delay:.1f}s...")
                time.sleep(delay)
            
            preferred_results = search_in_preferred_site(site_url, query, headers)
            
            # Agregar nombre del sitio
            for result in preferred_results:
                result['site_name'] = site_name
            
            all_results.extend(preferred_results)
        
        print(f"\n✓ Total preferidos: {len(all_results)} resultados")
    
    # 2. SIEMPRE buscar resultados generales
    remaining_slots = max(1, limit - len(all_results))  # Mínimo 1 resultado general
    
    print(f"\n--- FASE 2: BÚSQUEDA GENERAL ({remaining_slots} resultados) ---\n")
    
    # DELAY si hubo búsquedas preferidas
    if all_results:
        delay = random.uniform(*DELAY_BEFORE_GENERAL_SEARCH)
        print(f"⏱️  Esperando {delay:.1f}s antes de búsqueda general...")
        time.sleep(delay)
    
    try:
        # User-Agent aleatorio
        headers['User-Agent'] = get_random_user_agent()
        
        # Búsqueda general en DuckDuckGo
        encoded_query = urllib.parse.quote_plus(query)
        url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
        
        print(f"🔍 Buscando en DuckDuckGo...")
        
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        
        # Manejar código 202
        if response.status_code == 202:
            print(f"⚠️  Spam detectado (202). Esperando {DELAY_AFTER_RATE_LIMIT}s...")
            time.sleep(DELAY_AFTER_RATE_LIMIT)
            
            # Segundo intento
            headers['User-Agent'] = get_random_user_agent()
            response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
            
            if response.status_code == 202:
                print(f"❌ Búsqueda general bloqueada después de reintentar")
                print(f"   Mostrando solo {len(all_results)} resultados preferidos")
                print(f"\n{'='*60}")
                print(f"RESUMEN: {len(all_results)} resultados totales")
                print(f"{'='*60}\n")
                return all_results
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # URLs ya encontradas
            existing_urls = {result['url'] for result in all_results}
            
            general_count = 0
            
            # Buscar resultados
            for result in soup.find_all('div', class_='result'):
                if len(all_results) >= limit:
                    break
                    
                try:
                    link = result.find('a', class_='result__a')
                    if not link:
                        continue
                    
                    title = link.get_text().strip()
                    href = link.get('href', '')
                    
                    # Limpiar URL
                    if href.startswith('//'):
                        href = 'https:' + href
                    
                    # Extraer URL real
                    if 'uddg=' in href:
                        import re
                        match = re.search(r'uddg=([^&]+)', href)
                        if match:
                            href = urllib.parse.unquote(match.group(1))
                    
                    # Evitar duplicados
                    if href in existing_urls:
                        continue
                    
                    if href and href.startswith('http'):
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
                    print(f"  Error: {e}")
                    continue
            
            print(f"\n✓ Total generales: {general_count} resultados")
            
        else:
            print(f"⚠️  Error {response.status_code} en búsqueda general")
            
    except Exception as e:
        print(f"❌ Error en búsqueda general: {e}")
    
    # Resumen final
    preferred_count = sum(1 for r in all_results if r.get('is_preferred', False))
    general_count = sum(1 for r in all_results if not r.get('is_preferred', False))
    
    print(f"\n{'='*60}")
    print(f"RESUMEN:")
    print(f"  ⭐ Preferidos: {preferred_count}")
    print(f"  🌐 Generales: {general_count}")
    print(f"  📊 TOTAL: {len(all_results)} resultados")
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