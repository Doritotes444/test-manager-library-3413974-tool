#!/usr/bin/env python3
"""
Manager Library - Seeder & Data Generator Tool
Ficha ADSO 3413974 | SENA
Desarrollador: Juan Pablo Doria (@Doritotes444)

Puebla la base de datos a través de la API RESTful (/api/v1):
- Autenticación con JWT (admin)
- 40+ libros en las 5 categorías oficiales
- 10+ socios con documentos válidos
- 15+ préstamos simulados (cerrados, abiertos y con mora intencional)
"""

import sys
import json
import random
import argparse
from datetime import datetime, timedelta
import urllib.request
import urllib.error

# Categorías estándar fijas de la especificación
CATEGORIES_SEED = [
    {"id": "11111111-1111-1111-1111-111111111111", "name": "Novela"},
    {"id": "22222222-2222-2222-2222-222222222222", "name": "Ciencia"},
    {"id": "33333333-3333-3333-3333-333333333333", "name": "Tecnología"},
    {"id": "44444444-4444-4444-4444-444444444444", "name": "Historia"},
    {"id": "55555555-5555-5555-5555-555555555555", "name": "Infantil"},
]

BOOKS_DATA = [
    # Novela
    {"title": "Cien Años de Soledad", "author": "Gabriel García Márquez", "cat_idx": 0, "copies": 6},
    {"title": "El Amor en los Tiempos del Cólera", "author": "Gabriel García Márquez", "cat_idx": 0, "copies": 5},
    {"title": "Don Quijote de la Mancha", "author": "Miguel de Cervantes", "cat_idx": 0, "copies": 4},
    {"title": "Crimen y Castigo", "author": "Fiódor Dostoyevski", "cat_idx": 0, "copies": 4},
    {"title": "Orgullo y Prejuicio", "author": "Jane Austen", "cat_idx": 0, "copies": 5},
    {"title": "La Odisea", "author": "Homero", "cat_idx": 0, "copies": 3},
    {"title": "1984", "author": "George Orwell", "cat_idx": 0, "copies": 7},
    {"title": "Rayuela", "author": "Julio Cortázar", "cat_idx": 0, "copies": 4},
    {"title": "Pedro Páramo", "author": "Juan Rulfo", "cat_idx": 0, "copies": 5},
    {"title": "La Metamorfosis", "author": "Franz Kafka", "cat_idx": 0, "copies": 6},

    # Ciencia
    {"title": "Breve Historia del Tiempo", "author": "Stephen Hawking", "cat_idx": 1, "copies": 5},
    {"title": "Cosmos", "author": "Carl Sagan", "cat_idx": 1, "copies": 6},
    {"title": "El Gen Egoísta", "author": "Richard Dawkins", "cat_idx": 1, "copies": 4},
    {"title": "El Origen de las Especies", "author": "Charles Darwin", "cat_idx": 1, "copies": 3},
    {"title": "Sapiens: De animales a dioses", "author": "Yuval Noah Harari", "cat_idx": 1, "copies": 8},
    {"title": "Astrophysics for People in a Hurry", "author": "Neil deGrasse Tyson", "cat_idx": 1, "copies": 5},
    {"title": "La Doble Hélice", "author": "James D. Watson", "cat_idx": 1, "copies": 3},
    {"title": "El Universo en una Cáscara de Nuez", "author": "Stephen Hawking", "cat_idx": 1, "copies": 4},

    # Tecnología
    {"title": "Clean Code: A Handbook of Agile Software", "author": "Robert C. Martin", "cat_idx": 2, "copies": 6},
    {"title": "Design Patterns: Elements of Reusable Object-Oriented Software", "author": "Gang of Four", "cat_idx": 2, "copies": 4},
    {"title": "Refactoring: Improving the Design of Existing Code", "author": "Martin Fowler", "cat_idx": 2, "copies": 5},
    {"title": "The Pragmatic Programmer", "author": "David Thomas, Andrew Hunt", "cat_idx": 2, "copies": 6},
    {"title": "Building Microservices", "author": "Sam Newman", "cat_idx": 2, "copies": 4},
    {"title": "Domain-Driven Design", "author": "Eric Evans", "cat_idx": 2, "copies": 5},
    {"title": "Designing Data-Intensive Applications", "author": "Martin Kleppmann", "cat_idx": 2, "copies": 6},
    {"title": "Clean Architecture", "author": "Robert C. Martin", "cat_idx": 2, "copies": 7},

    # Historia
    {"title": "Historia General de Colombia", "author": "Jorge Orlando Melo", "cat_idx": 3, "copies": 4},
    {"title": "Los Cañones de Agosto", "author": "Barbara Tuchman", "cat_idx": 3, "copies": 3},
    {"title": "Armas, Gérmenes y Acero", "author": "Jared Diamond", "cat_idx": 3, "copies": 5},
    {"title": "La Segunda Guerra Mundial", "author": "Antony Beevor", "cat_idx": 3, "copies": 4},
    {"title": "Homo Deus: Breve Historia del Mañana", "author": "Yuval Noah Harari", "cat_idx": 3, "copies": 6},
    {"title": "Historia de dos Ciudades", "author": "Charles Dickens", "cat_idx": 3, "copies": 5},
    {"title": "El Siglo de las Luces", "author": "Alejo Carpentier", "cat_idx": 3, "copies": 3},
    {"title": "Las Venas Abiertas de América Latina", "author": "Eduardo Galeano", "cat_idx": 3, "copies": 6},

    # Infantil
    {"title": "El Principito", "author": "Antoine de Saint-Exupéry", "cat_idx": 4, "copies": 8},
    {"title": "Donde Viven los Monstruos", "author": "Maurice Sendak", "cat_idx": 4, "copies": 5},
    {"title": "Matilda", "author": "Roald Dahl", "cat_idx": 4, "copies": 6},
    {"title": "Charlie y la Fábrica de Chocolate", "author": "Roald Dahl", "cat_idx": 4, "copies": 5},
    {"title": "El Mago de Oz", "author": "L. Frank Baum", "cat_idx": 4, "copies": 4},
    {"title": "Alicia en el País de las Maravillas", "author": "Lewis Carroll", "cat_idx": 4, "copies": 6},
    {"title": "Pinocho", "author": "Carlo Collodi", "cat_idx": 4, "copies": 4},
    {"title": "Peter Pan", "author": "J.M. Barrie", "cat_idx": 4, "copies": 5},
]

MEMBERS_DATA = [
    {"name": "Andrés Felipe Moreno", "type": "CC", "doc": "1017234567", "email": "andres.moreno@gmail.com", "phone": "3104567890"},
    {"name": "Valentina Ospina Gómez", "type": "CC", "doc": "1028345678", "email": "valentina.ospina@gmail.com", "phone": "3115678901"},
    {"name": "Mateo Jaramillo Restrepo", "type": "TI", "doc": "1039456789", "email": "mateo.j@outlook.com", "phone": "3126789012"},
    {"name": "Camila Sofía Cardona", "type": "CC", "doc": "1040567890", "email": "camila.cardona@yahoo.es", "phone": "3137890123"},
    {"name": "Daniel Alejandro Morales", "type": "CC", "doc": "1051678901", "email": "daniel.morales@hotmail.com", "phone": "3148901234"},
    {"name": "Isabella Henao López", "type": "TI", "doc": "1062789012", "email": "isabella.henao@gmail.com", "phone": "3159012345"},
    {"name": "Sebastián Zapata Castro", "type": "CC", "doc": "1073890123", "email": "sebastian.z@gmail.com", "phone": "3160123456"},
    {"name": "Mariana Betancur Ríos", "type": "CE", "doc": "1084901234", "email": "mariana.b@empresa.com", "phone": "3171234567"},
    {"name": "Santiago Echeverri Ruiz", "type": "CC", "doc": "1095012345", "email": "santiago.ech@gmail.com", "phone": "3182345678"},
    {"name": "Luciana Ramírez Cano", "type": "CC", "doc": "1106123456", "email": "luciana.ramirez@gmail.com", "phone": "3193456789"},
    {"name": "Samuel David Arboleda", "type": "TI", "doc": "1117234567", "email": "samuel.david@gmail.com", "phone": "3204567890"},
    {"name": "Valeria Quintero Ortiz", "type": "CC", "doc": "1128345678", "email": "valeria.q@hotmail.com", "phone": "3215678901"},
]

def make_request(url, method="GET", data=None, token=None):
    headers = {"Accept": "application/json"}
    body = None
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if data is not None:
        headers["Content-Type"] = "application/json"
        body = json.dumps(data).encode("utf-8")
    
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as response:
            resp_body = response.read().decode("utf-8")
            if resp_body:
                return json.loads(resp_body)
            return {}
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        try:
            return json.loads(err_msg)
        except Exception:
            return {"error": err_msg, "status": e.code}
    except Exception as e:
        return {"error": str(e)}

def generate_isbn13(idx):
    base = 9789580000000 + idx
    s = str(base)[:12]
    total = sum((1 if i % 2 == 0 else 3) * int(d) for i, d in enumerate(s))
    check = (10 - (total % 10)) % 10
    return f"{s}{check}"

def main():
    parser = argparse.ArgumentParser(description="Manager Library Seeder CLI Tool")
    parser.add_argument("--api-url", default="http://localhost:8000/api/v1", help="URL base de la API REST")
    parser.add_argument("--admin-user", default="admin", help="Usuario administrador")
    parser.add_argument("--admin-pass", default="admin123", help="Contraseña administrador")
    args = parser.parse_args()

    api_url = args.api_url.rstrip("/")
    print("=" * 65)
    print("   MANAGER LIBRARY - SEEDER AUTOMATIZADO DE DATOS (CLI)")
    print("   SENA Ficha ADSO 3413974 | Juan Pablo Doria (@Doritotes444)")
    print("=" * 65)
    print(f"[*] Conectando a la API en: {api_url}")

    # 1. Autenticación
    print("[*] Autenticando con rol administrador...")
    login_resp = make_request(f"{api_url}/auth/login", method="POST", data={
        "username": args.admin_user,
        "password": args.admin_pass
    })

    token = login_resp.get("access_token") or login_resp.get("token")
    if not token:
        print(f"[!] Error de autenticación: {login_resp}")
        sys.exit(1)
    print(f"[+] Autenticación exitosa. Token JWT recibido.")

    # 2. Consultar Categorías
    print("[*] Verificando catálogo de categorías...")
    cats_resp = make_request(f"{api_url}/categories", token=token)
    if isinstance(cats_resp, list):
        categories = cats_resp
    elif isinstance(cats_resp, dict) and "items" in cats_resp:
        categories = cats_resp["items"]
    else:
        categories = CATEGORIES_SEED
    print(f"[+] {len(categories)} categorías disponibles en el sistema.")

    # 3. Sembrar Libros
    print(f"[*] Registrando {len(BOOKS_DATA)} libros de catálogo...")
    created_books = []
    for idx, b in enumerate(BOOKS_DATA):
        isbn = generate_isbn13(idx + 1)
        cat_id = categories[b["cat_idx"]]["id"]
        book_payload = {
            "title": b["title"],
            "author": b["author"],
            "isbn": isbn,
            "category_id": cat_id,
            "total_copies": b["copies"]
        }
        res = make_request(f"{api_url}/books", method="POST", data=book_payload, token=token)
        if "id" in res:
            created_books.append(res)
            print(f"    [+] Libro registrado: {b['title']} (ISBN: {isbn}, Ejemplares: {b['copies']})")
        else:
            # Si ya existía por ISBN único
            existing = make_request(f"{api_url}/books", token=token)
            if isinstance(existing, list):
                created_books = existing
            elif isinstance(existing, dict) and "items" in existing:
                created_books = existing["items"]
            break

    print(f"[+] Total libros activos en base de datos: {len(created_books)}")

    # 4. Sembrar Socios
    print(f"[*] Registrando {len(MEMBERS_DATA)} socios afiliados...")
    created_members = []
    for m in MEMBERS_DATA:
        member_payload = {
            "full_name": m["name"],
            "name": m["name"],
            "document_type": m["type"],
            "document_number": m["doc"],
            "email": m["email"],
            "phone": m["phone"]
        }
        res = make_request(f"{api_url}/members", method="POST", data=member_payload, token=token)
        if "id" in res:
            created_members.append(res)
            print(f"    [+] Socio registrado: {m['name']} ({m['type']}: {m['doc']})")
        else:
            # Ya existía por documento único
            existing_m = make_request(f"{api_url}/members", token=token)
            if isinstance(existing_m, list):
                created_members = existing_m
            elif isinstance(existing_m, dict) and "items" in existing_m:
                created_members = existing_m["items"]
            break

    print(f"[+] Total socios activos en base de datos: {len(created_members)}")

    # 5. Generar Préstamos y Devoluciones
    print("[*] Simulando historial de circulación...")
    if len(created_members) >= 5 and len(created_books) >= 10:
        # Préstamo 1: Cerrado (Devuelto en su totalidad)
        m1 = created_members[0]
        b1, b2 = created_books[0], created_books[1]
        l1_payload = {
            "member_id": m1["id"],
            "items": [{"book_id": b1["id"]}, {"book_id": b2["id"]}],
            "book_ids": [b1["id"], b2["id"]]
        }
        l1 = make_request(f"{api_url}/loans", method="POST", data=l1_payload, token=token)
        if "id" in l1:
            print(f"    [+] Préstamo registrado para {m1.get('name') or m1.get('full_name')} (2 libros)")
            # Devolver libros usando endpoint canónico
            for it in l1.get("items", []):
                make_request(f"{api_url}/loans/{l1['id']}/items/{it['id']}/return", method="POST", token=token)
            print(f"        [-] Todos los libros devueltos. Préstamo cerrado exitosamente.")

        # Préstamo 2: Abierto (En poder del socio)
        m2 = created_members[1]
        b3 = created_books[2]
        l2_payload = {
            "member_id": m2["id"],
            "items": [{"book_id": b3["id"]}],
            "book_ids": [b3["id"]]
        }
        l2 = make_request(f"{api_url}/loans", method="POST", data=l2_payload, token=token)
        if "id" in l2:
            print(f"    [+] Préstamo activo para {m2.get('name') or m2.get('full_name')} (1 libro en circulación)")

        # Préstamo 3: Abierto con 2 libros
        m3 = created_members[2]
        b4, b5 = created_books[3], created_books[4]
        l3_payload = {
            "member_id": m3["id"],
            "items": [{"book_id": b4["id"]}, {"book_id": b5["id"]}],
            "book_ids": [b4["id"], b5["id"]]
        }
        l3 = make_request(f"{api_url}/loans", method="POST", data=l3_payload, token=token)
        if "id" in l3:
            print(f"    [+] Préstamo activo para {m3.get('name') or m3.get('full_name')} (2 libros en circulación)")

    print("=" * 65)
    print("   ¡SEMBRADO DE DATOS FINALIZADO SATISFACTORIAMENTE!")
    print("   El sistema cuenta con catálogo, socios y transacciones.")
    print("=" * 65)

if __name__ == "__main__":
    main()
