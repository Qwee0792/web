import json

# Cargar el archivo JSON
with open('config.json') as config_file:
    config = json.load(config_file)

# Crear el diccionario configDB con las variables
configDB = {
    "flask_key": config['secrets']['hey'][0]['flask_key'],
    "template_folder": config['patch']['template_folder'],
    "static_folder": config['patch']['static_folder'],
    "host": config['runParametros']['host'],
    "port": config['runParametros']['port'],
    "debug": config['runParametros']['debug'],
    "disco": config['patch']['patch_discos'],
    "admins": config['UsersAdmins'],
    "notaPatch": config['patch']['notasPatch']
}