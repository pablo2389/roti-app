"""
IA Integration Service - Supports OpenAI, Anthropic, Cohere
"""
import os
from typing import Optional

IA_PROVIDER = os.getenv("IA_PROVIDER", "")
IA_API_KEY = os.getenv("IA_API_KEY", "")

def generar_contenido_ia(producto: dict) -> str:
    """Generate product description using configured IA provider."""
    if not IA_PROVIDER or not IA_API_KEY:
        # Fallback to simulated prompt
        return generar_prompt_ia(producto)
    
    if IA_PROVIDER == "openai":
        return _openai_generate(producto)
    elif IA_PROVIDER == "anthropic":
        return _anthropic_generate(producto)
    elif IA_PROVIDER == "cohere":
        return _cohere_generate(producto)
    else:
        # Unknown provider, fallback to simulated
        return generar_prompt_ia(producto)


def _openai_generate(producto: dict) -> str:
    """Generate using OpenAI API."""
    try:
        import openai
        openai.api_key = IA_API_KEY
        
        prompt = f"""Genera una descripción comercial atractiva y breve (máx 150 palabras) para este producto de rotisería:
Nombre: {producto.get('nombre')}
Descripción: {producto.get('descripcion', 'N/A')}
Precio: ${producto.get('precio')}

Responde solo con la descripción, sin explicaciones adicionales."""
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI error: {e}")
        return generar_prompt_ia(producto)


def _anthropic_generate(producto: dict) -> str:
    """Generate using Anthropic (Claude) API."""
    try:
        from anthropic import Anthropic
        client = Anthropic()
        
        prompt = f"""Genera una descripción comercial atractiva y breve (máx 150 palabras) para este producto de rotisería:
Nombre: {producto.get('nombre')}
Descripción: {producto.get('descripcion', 'N/A')}
Precio: ${producto.get('precio')}

Responde solo con la descripción, sin explicaciones adicionales."""
        
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text.strip()
    except Exception as e:
        print(f"Anthropic error: {e}")
        return generar_prompt_ia(producto)


def _cohere_generate(producto: dict) -> str:
    """Generate using Cohere API."""
    try:
        import cohere
        co = cohere.Client(IA_API_KEY)
        
        prompt = f"""Genera una descripción comercial atractiva para este producto:
{producto.get('nombre')} - ${producto.get('precio')}
{producto.get('descripcion', 'N/A')}

Respuesta breve (máx 150 palabras):"""
        
        response = co.generate(
            prompt=prompt,
            max_tokens=200,
            temperature=0.7
        )
        return response.generations[0].text.strip()
    except Exception as e:
        print(f"Cohere error: {e}")
        return generar_prompt_ia(producto)


def generar_prompt_ia(producto: dict) -> str:
    """Generate prompt that user can copy-paste to ChatGPT/Claude manually."""
    return f"""Genera una descripción comercial atractiva y breve (máx 150 palabras) para este producto de rotisería:
Nombre: {producto.get('nombre')}
Descripción actual: {producto.get('descripcion', 'N/A')}
Precio: ${producto.get('precio')}

[NOTA: Este es un prompt simulado. Para usar IA real, configura IA_PROVIDER y IA_API_KEY en .env]"""


def send_email_alert(to_email: str, subject: str, body: str) -> bool:
    """Simulado. Para implementar con SMTP, configura SMTP_* en .env"""
    print(f"[SIMULADO] Email a {to_email}: {subject}")
    return True


def generar_link_whatsapp(telefono: str, mensaje: str) -> str:
    """Genera link de WhatsApp (simulado)."""
    return f"https://wa.me/{telefono}?text={mensaje}"
