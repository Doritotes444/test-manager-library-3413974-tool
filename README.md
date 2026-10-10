# Manager Library - Herramienta de Sembrado de Datos (CLI Tool)

> **Servicio Nacional de Aprendizaje (SENA) &bull; ADSO 3413974**  
> **Desarrollador:** Juan Pablo Doria ([`@Doritotes444`](https://github.com/Doritotes444))  
> **Tecnología:** Python 3 (CLI nativo sin dependencias obligatorias)  

---

## 🎯 Propósito de la Herramienta

Esta herramienta de utilidad (`seeder`) puebla de forma masiva y coherente el catálogo de libros, los registros de socios y el historial de circulación de la biblioteca interactuando **exclusivamente a través de los endpoints RESTful de la API (`/api/v1`)**.

Garantiza que todas las transacciones respeten las reglas del dominio y genera datos realistas para facilitar las demostraciones durante la feria técnica.

---

## 📦 Características Técnicas

- **Cero Dependencias Obligatorias:** Implementado usando la librería estándar de Python (`urllib.request`, `json`, `datetime`), lo que permite ejecutarlo en cualquier máquina sin necesidad de `pip install`.
- **Autenticación Automática:** Solicita token JWT mediante `POST /auth/login` con credenciales de administrador antes de ejecutar las operaciones protegidas.
- **Validación de Invariantes:** Registra libros con códigos ISBN-13 válidos con dígito de verificación y respeta las 5 categorías oficiales.
- **Simulación de Circulación:** Genera préstamos de 1 y 2 libros, y realiza devoluciones inmediatas para demostrar la reincorporación automática de stock.

---

## 💻 Ejecución Local

```bash
# 1. Asegúrate de tener la API corriendo en el puerto 8000
python seed.py --api-url http://localhost:8000/api/v1
```

Opciones disponibles:
```text
--api-url       URL base de la API (por defecto: http://localhost:8000/api/v1)
--admin-user    Usuario administrador (por defecto: admin)
--admin-pass    Contraseña de administrador (por defecto: admin123)
```

---

## 🐳 Ejecución con Docker

```bash
# Construir la imagen del tool
docker build -t manager-library-tool .

# Ejecutar conectado a la red de Docker Compose
docker run --network ml-network manager-library-tool --api-url http://api:8000/api/v1
```
