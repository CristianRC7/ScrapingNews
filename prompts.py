# Almacena los prompts para la generación de contenido con IA

BLOG_GENERATION_PROMPT = """Eres un periodista profesional. Basándote ÚNICAMENTE en la siguiente información extraída de noticias, escribe un artículo de blog completo y profesional sobre "{topic}".

INFORMACIÓN DE LAS NOTICIAS:
{content}

INSTRUCCIONES:
- Escribe un artículo completo con introducción, desarrollo y conclusión
- Usa un tono profesional y periodístico
- Estructura el contenido de manera clara
- NO inventes información que no esté en las fuentes
- Mínimo 500 palabras

ARTÍCULO:"""

def get_blog_prompt(topic, content):
    """
    Genera el prompt para crear un blog
    
    Args:
        topic: Tema del blog
        content: Contenido extraído de las noticias
    
    Returns:
        str: Prompt formateado
    """
    return BLOG_GENERATION_PROMPT.format(topic=topic, content=content)