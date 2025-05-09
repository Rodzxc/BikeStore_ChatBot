from langchain.tools import Tool

# ==== Traduccion de subcategorias ====
Traductor_subcategory = {
    "bicicletas de montaña": "Mountain Bikes",
    "bicicletas de ruta": "Road Bikes",
    "bicicletas de turismo": "Touring Bikes",
    "bici": "Bike",
    "manubrios": "Handlebars",
    "ejes de centro": "Bottom Brackets",
    "frenos": "Brakes",
    "cadenas": "Chains",
    "bielas": "Cranksets",
    "desviadores": "Derailleurs",
    "horquillas": "Forks",
    "juego de dirección": "Headsets",
    "cuadros de montaña": "Mountain Frames",
    "cuadros de bicicletas de montaña": "Mountain Frames",
    "pedales": "Pedals",
    "cuadros de ruta": "Road Frames",
    "cuadros de bicicletas de ruta": "Road Frames",
    "asientos": "Saddles",
    "sillines": "Saddles",
    "cuadros de turismo": "Touring Frames",
    "ruedas": "Wheels",
    "pantalones con tirantes": "Bib-Shorts",
    "gorras": "Caps",
    "guantes": "Gloves",
    "camisetas de ciclismo": "Jerseys",
    "pantalones cortos": "Shorts",
    "medias": "Socks",
    "calcetines": "Socks",
    "mallas": "Tights",
    "chalecos": "Vests",
    "portabicicletas": "Bike Racks",
    "soportes para bicicleta": "Bike Stands",
    "botellas y portabotellas": "Bottles and Cages",
    "limpiadores": "Cleaners",
    "guardabarros": "Fenders",
    "cascos": "Helmets",
    "mochilas de hidratación": "Hydration Packs",
    "luces": "Lights",
    "candados": "Locks",
    "alforjas": "Panniers",
    "bombas de aire": "Pumps",
    "llantas y cámaras": "Tires and Tubes"
}

# ==== Traductor de subcategorias ====
def translator_subcategory_es_en(categoria_es):
    return Traductor_subcategory.get(categoria_es.lower(), categoria_es)

description="""
              Translate product subcategory names from Spanish to English.
              Use it when the user speaks in Spanish and the data is in English.
              It is also useful for performing searches by subcategory (productsubcategory).
            """

translator_subcategory_es_en_tool= Tool(
    name="translator_subcategory_es_en",
    func=translator_subcategory_es_en,
    description=description
)