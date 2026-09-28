"""
Scraper de portafolio — Alan
-----------------------------
Extrae productos (nombre, precio, disponibilidad, link) desde una tienda
online y los guarda en:
  1) un archivo CSV/Excel-friendly (products.csv)
  2) una base de datos SQLite con histórico de precios (products.db)

Este script usa como ejemplo "books.toscrape.com", un sitio público hecho
específicamente para practicar/mostrar web scraping (no tiene restricciones
legales ni técnicas de por medio). La estructura es idéntica a la que
usarías en una tienda real: solo cambiarías los selectores CSS/HTML según
el sitio del cliente.

Cómo adaptarlo a un cliente real:
- Cambia BASE_URL por la URL de la categoría/página del cliente.
- Ajusta los selectores en `parse_product()` según el HTML real del sitio
  (inspecciona con las devtools del navegador: clic derecho > Inspeccionar).
- Respeta siempre robots.txt y los términos de uso del sitio del cliente.

Requisitos:
    pip install requests beautifulsoup4
"""

import csv
import sqlite3
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
TOTAL_PAGINAS = 2          # cuántas páginas de resultados recorrer
CSV_PATH = "products.csv"
DB_PATH = "products.db"
DELAY_SEGUNDOS = 1         # pausa entre requests para no saturar el sitio


def obtener_html(url: str) -> str:
    """Descarga el HTML de una URL con un User-Agent normal."""
    headers = {"User-Agent": "Mozilla/5.0 (compatible; PortfolioScraper/1.0)"}
    respuesta = requests.get(url, headers=headers, timeout=10)
    respuesta.raise_for_status()
    respuesta.encoding = "utf-8"
    return respuesta.text


def parse_pagina(html: str) -> list[dict]:
    """Extrae nombre, precio, disponibilidad y link de cada producto."""
    soup = BeautifulSoup(html, "html.parser")
    productos = []

    for card in soup.select("article.product_pod"):
        nombre = card.select_one("h3 a")["title"].strip()
        precio_txt = card.select_one("p.price_color").get_text(strip=True)
        precio_limpio = "".join(c for c in precio_txt if c.isdigit() or c == ".")
        precio = float(precio_limpio)
        disponible = card.select_one("p.instock.availability").get_text(strip=True)
        link_relativo = card.select_one("h3 a")["href"]
        link = "https://books.toscrape.com/" + link_relativo.replace("../../../", "")

        productos.append({
            "nombre": nombre,
            "precio": precio,
            "disponibilidad": disponible,
            "link": link,
            "fecha_extraccion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })

    return productos


def guardar_csv(productos: list[dict], path: str) -> None:
    """Guarda los productos en un CSV listo para abrir en Excel."""
    if not productos:
        return
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        # Se usa ";" como separador (en vez de ",") porque Excel en
        # configuración regional español/Chile espera ";" para reconocer
        # columnas automáticamente al abrir el archivo con doble clic.
        writer = csv.DictWriter(f, fieldnames=productos[0].keys(), delimiter=";")
        writer.writeheader()
        writer.writerows(productos)
    print(f"CSV generado: {path} ({len(productos)} productos)")


def guardar_sqlite(productos: list[dict], path: str) -> None:
    """
    Guarda los productos en SQLite, permitiendo llevar un histórico de
    precios a lo largo del tiempo (cada corrida agrega una fila nueva por
    producto con su fecha, en vez de sobreescribir).
    """
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS precios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            disponibilidad TEXT,
            link TEXT,
            fecha_extraccion TEXT NOT NULL
        )
    """)
    cur.executemany(
        """INSERT INTO precios (nombre, precio, disponibilidad, link, fecha_extraccion)
           VALUES (:nombre, :precio, :disponibilidad, :link, :fecha_extraccion)""",
        productos,
    )
    conn.commit()
    conn.close()
    print(f"Base de datos actualizada: {path} (+{len(productos)} registros)")


def main():
    todos_los_productos = []

    for pagina in range(1, TOTAL_PAGINAS + 1):
        url = BASE_URL.format(pagina)
        print(f"Descargando página {pagina}...")
        html = obtener_html(url)
        productos = parse_pagina(html)
        todos_los_productos.extend(productos)
        time.sleep(DELAY_SEGUNDOS)

    guardar_csv(todos_los_productos, CSV_PATH)
    guardar_sqlite(todos_los_productos, DB_PATH)


if __name__ == "__main__":
    main()