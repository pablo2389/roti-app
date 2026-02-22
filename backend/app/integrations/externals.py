def send_email_alert(to_email: str, subject: str, body: str) -> bool:
    # Simulado: aquí se integrará un servicio de correo real
    print(f"[SIMULADO] Enviando email a {to_email}: {subject}")
    return True


def generar_link_whatsapp(telefono: str, mensaje: str) -> str:
    # Simulado: devuelve link de whatsapp preformateado
    return f"https://wa.me/{telefono}?text={mensaje}"


def generar_prompt_ia(producto: dict) -> str:
    # Simulado: generar prompt para herramienta IA
    return f"Genera una descripción comercial atractiva para el producto: {producto.get('nombre')} - {producto.get('descripcion')} Precio: {producto.get('precio')}"
