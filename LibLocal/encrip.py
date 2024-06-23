import os
from cryptography.fernet import Fernet

# Función para generar una clave y guardarla en un archivo
def generar_clave():
    try:
        os.remove('key.key')
    except:
        pass

    ruta='key.key'
    # Genera una nueva clave utilizando Fernet
    clave = Fernet.generate_key()
    # Guarda la clave en un archivo especificado por la ruta en modo escritura binaria ('wb')
    with open(ruta, 'wb') as archivo_clave:
        archivo_clave.write(clave)
    return 'key.key'

# Función para cargar la clave desde un archivo
def cargar_clave(ruta):
    # Lee la clave desde el archivo especificado por la ruta en modo lectura binaria ('rb')
    return open(ruta, 'rb').read()

# Función para cifrar un archivo y guardar el contenido cifrado en un archivo .bin
def cifrar_archivo(ruta_archivo_original, clave):
    try:
        os.remove('archivo_cifrado.bin')
    except:
        pass
    ruta_archivo_bin= 'archivo_cifrado.bin'
    # Crea un objeto Fernet usando la clave proporcionada
    fernet = Fernet(clave)
    # Abre el archivo original en modo lectura binaria ('rb')
    #with open(ruta_archivo_original, 'rb') as archivo_original:
        # Lee todo el contenido del archivo original
    #    contenido = archivo_original.read()
    # Cifra el contenido usando el objeto Fernet
    contenido_cifrado = fernet.encrypt(ruta_archivo_original)
    # Abre o crea un archivo .bin en modo escritura binaria ('wb') y escribe el contenido cifrado
    with open(ruta_archivo_bin, 'wb') as archivo_bin:
        archivo_bin.write(contenido_cifrado)

# Función para descifrar un archivo .bin y guardar el contenido descifrado en su formato original
def descifrar_archivo(ruta_archivo_bin, clave):
    try:
        os.remove('fileCifrado.bin')
    except:
        pass
    ruta_archivo_original= 'fileCifrado.bin'
    # Crea un objeto Fernet usando la clave proporcionada
    fernet = Fernet(clave)
    # Abre el archivo .bin cifrado en modo lectura binaria ('rb')
    #with open(ruta_archivo_bin, 'rb') as archivo_bin:
        # Lee el contenido cifrado del archivo .bin
    #    contenido_cifrado = archivo_bin.read()
    # Descifra el contenido cifrado usando el objeto Fernet
    contenido_descifrado = fernet.decrypt(ruta_archivo_bin)
    # Abre o crea un archivo en modo escritura binaria ('wb') y escribe el contenido descifrado
    with open(ruta_archivo_original, 'wb') as archivo_original:
        archivo_original.write(contenido_descifrado)
