# Web Scraper Portfolio — Python + SQL

Script de extracción de datos web (web scraping) que descarga información de productos desde un sitio, la limpia y la entrega en dos formatos:

- **CSV** listo para abrir en Excel
- **Base de datos SQLite** con histórico de precios (cada ejecución agrega un registro nuevo, permitiendo trackear cambios de precio en el tiempo)

## Tecnologías usadas
- Python 3
- `requests` — descarga de páginas web
- `BeautifulSoup` — extracción y parseo de datos HTML
- `sqlite3` — almacenamiento con histórico

## Características
- Manejo de errores HTTP
- Pausa entre solicitudes para no saturar el sitio (buenas prácticas de scraping)
- Codificación de caracteres corregida (soporta símbolos especiales sin errores)
- CSV compatible con Excel en configuración regional español (separador `;`)

## Adaptable a cualquier sitio o cliente
El script fue construido como base reutilizable: cambiando la URL y los selectores HTML, se puede adaptar a cualquier tienda online, en cualquier moneda, en pocos minutos. Ideal para monitoreo de precios de competencia, extracción de catálogos, o generación de reportes automáticos.

---
*Proyecto de portafolio — disponible para servicios freelance de extracción y automatización de datos.*
