# config.py
# Configuración del sistema de scraping

# ====================================
# CONFIGURACIÓN ANTI-SPAM
# ====================================

# Delays entre búsquedas (en segundos)
# Aumenta estos valores si sigues recibiendo error 202
DELAY_BETWEEN_PREFERRED_SITES = (10, 15)  # (mínimo, máximo) segundos aleatorios
DELAY_BEFORE_GENERAL_SEARCH = (10, 15)    # Delay antes de búsqueda general
DELAY_AFTER_RATE_LIMIT = 20              # Espera después de recibir 202

# Número de reintentos después de 202
MAX_RETRIES_ON_RATE_LIMIT = 1

# ====================================
# CONFIGURACIÓN DE BÚSQUEDA
# ====================================

# Número máximo de resultados por sitio preferido
MAX_RESULTS_PER_PREFERRED_SITE = 2

# Timeout para requests (en segundos)
REQUEST_TIMEOUT = 20

# Límite de caracteres extraídos por página
CONTENT_CHAR_LIMIT = 500000

# ====================================
# USER AGENTS
# ====================================

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
]
# ====================================