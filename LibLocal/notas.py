import json,random
import string
try:
    from LibLocal import config
except ImportError:
    import config

# Abre el archivo JSON y carga los datos
def getNotas():
    data_dict = {}

    try:
        with open(config.configDB['notaPatch']) as jsonData:
            try:
                data = json.load(jsonData)
            except json.JSONDecodeError as e:
                print(f"Error al decodificar JSON: {e}")
                return data_dict  # Devuelve un diccionario vacío en caso de error

            # Verifica si el JSON es un objeto único o una lista de objetos
            if isinstance(data, dict):  # Si es un solo objeto JSON
                item_id = data.get("id")
                if item_id is not None:
                    data_dict[item_id] = [data]  # Almacena el objeto en un diccionario
            elif isinstance(data, list):  # Si es una lista de objetos JSON
                for item in data:
                    if isinstance(item, dict):
                        item_id = item.get("id")
                        if item_id is not None:
                            if item_id not in data_dict:
                                data_dict[item_id] = []
                            data_dict[item_id].append(item)
                    else:
                        print(f"Advertencia: El elemento {item} no es un diccionario válido.")
            else:
                print("Advertencia: El archivo JSON no contiene un formato válido.")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {config.configDB['notaPatch']}.")

    return data_dict
def generar_uid():
    numeros = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  # Lista con dígitos del 0 al 9
    uid = ''.join(str(random.choice(numeros)) for _ in range(10))  # Genera un UID de 10 dígitos aleatorios
    return uid

def createNota(nombre, fecha, data):
    id_nota = generar_uid()
    url = f"/nota/{id_nota}"
    dataJson = {
        "id": id_nota,
        "nombre": nombre,
        "fecha": fecha,
        "data": data,
        "url": url
    }
    
    try:
        # Intenta cargar el archivo JSON existente si existe
        with open(config.configDB['notaPatch'], 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        # Si el archivo no existe, inicializa data como una lista vacía
        data = []
    except json.JSONDecodeError:
        print(f"Error al decodificar JSON en {config.configDB['notaPatch']}")
        return False
    
    # Agrega la nueva nota al final de la lista
    data.append(dataJson)
    
    # Escribe el JSON en el archivo específico con formato indentado
    with open(config.configDB['notaPatch'], 'w') as json_file:
        json.dump(data, json_file, indent=4)
    
    return True

a=getNotas()
print(a)
