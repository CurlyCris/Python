'''

# EJERCICIO 1

def contar_caracteres(palabra):
    longitud = len(palabra)
    return f'La longitud de la palabra es {longitud}'

resultado = contar_caracteres('hola')
print(resultado)

#EJERCICIO 2

def calcular_promedio(numeros):
    if len(numeros) == 0:
        return "La lista está vacía." 

    promedio = sum(numeros) / len(numeros)
    return (f'El promedio de la lista es {promedio}')

resultado = calcular_promedio([5,10,20,3])
print(resultado)

resultado = calcular_promedio([])
print(resultado)

#EJERCICIO 3

def encontrar_duplicado(lista):
    elementos_vistos = set() #Set se utiliza para conjuntos que almacenan elementos únicos
    for elemento in lista:
        if elemento in elementos_vistos: #Tengo que poner el condicional antes, si lo pongo después de añadir el número al set, siempre me va a devolver el primer elemento porque va a estar en el set
            return elemento
        elementos_vistos.add(elemento)
      
lista = [1, 2, 3, 4, 2, 5, 6]
resultado = encontrar_duplicado(lista)
print(f'Los números duplicados son: {resultado}')  

#EJERCICIO 4

def enmascarado_datos(texto):
    enmascarado = '#' * (len(str(texto))-4) #Multiplica # por el número de carácteres menos los últimos 4
    return enmascarado + str(texto[-4:])

resultado = enmascarado_datos('123456789')
print(resultado)


#EJERCICIO 5

def es_anagrama(palabra1, palabra2):
    if sorted(palabra1)==sorted(palabra2):
        return ('Las dos palabras son anagramas')
    else:
        return ('Las palabras no son anagramas')

resultado = es_anagrama('mora','roma')
print(resultado)



#EJERCICIO 6

def buscar_nombre():
    entrada = input("Ingresa una lista de nombres separados por espacio:")
    lista_nombres = entrada.split()

    nombre = input(f'Ingrese el nombre que quiere buscar: ')
    try:
        if nombre in lista_nombres:  
            print("El nombre que busca SI aparece en la lista")  
        else:
            print("El nombre que busca NO aparece en la lista")
    except ValueError: 
        print("Por favor, ingrese un nombre válido.")
    
buscar_nombre()


#EJERCICIO 7

def fibonacci(n):
    if n==0:
        return 0
    if n==1:
        return 1
    n = fibonacci(n-1) + fibonacci(n-2)
    return n

resultado = fibonacci(4)
print(resultado)



#EJERCICIO 8

def encontrar_puesto_empleado(nombre_completo, empleados):
    for empleado in empleados:
        nombre_completo_empleado = empleado['nombre'] + " " + empleado['apellido']
        if nombre_completo == nombre_completo_empleado:
            return empleado['puesto']
    return 'La persona no trabaja aquí.'

lista_empleados = [{'nombre': "Juan", 'apellido': "García", 'puesto': "Secretario"},
{'nombre': "Mabel", 'apellido': "García", 'puesto': "Product Manager"},
{'nombre': "Isabel", 'apellido': "Martín", 'puesto': "CEO"}]

print(encontrar_puesto_empleado("Juan García", lista_empleados))


#EJERCICIO 9
cubo = lambda x: x ** 3  
print(cubo(5))

#EJERCICIO 10
resto = lambda a, b: a%b 
print(resto(10,3))

#EJERCICIO 11
lista_numeros = 24, 56, 2.3, 19, 1, 0

filtrar_pares = filter(lambda x: x%2==0, lista_numeros)
numeros_pares = list(filtrar_pares)
print(numeros_pares)

#EJERCICIO 12
lista_numeros = 24, 56, 2.3, 19, 1, 0

suma = map (lambda x: x+3, lista_numeros)
numeros_sumados = list(suma)
print(numeros_sumados)

'''

#EJERCICIO 13

lista1 = [1, 4, 5, 6 , 7 , 9]
lista2 = [3, 11, 34, 56]

suma_listas = map(lambda x_y: x_y[0] + x_y[1], zip(lista1, lista2)) #x_y[0]: El primer elemento de la tupla (el primer valor de cada par, que proviene de lista1).
numeros_sumados = list(suma_listas)
print(numeros_sumados)

#EJERCICIO 14

class Arbol:
    def __init__(self):
        self.tronco = 1
        self.ramas = [] 

    def crecer_tronco(self):
        self.tronco += 1
    
    def nueva_rama(self):
        self.ramas.append(1)

    def crecer_ramas(self):
        self.ramas = [rama + 1 for rama in self.ramas]

    def quitar_rama(self, indice):
        self.ramas.pop(indice)

    def info_arbol(self):
        return f"Tronco: {self.tronco}, Ramas: {len(self.ramas)}, Longitudes de ramas: {self.ramas}"
    
mi_arbol = Arbol()
mi_arbol.crecer_tronco()
mi_arbol.nueva_rama()
mi_arbol.crecer_ramas()
mi_arbol.nueva_rama()
mi_arbol.nueva_rama()
mi_arbol.quitar_rama(2)
print(mi_arbol.info_arbol())

#EJERCICIO 15

class UsuarioBanco:
    def __init__(self, nombre, saldo, cuenta_corriente):
        self.nombre = nombre
        self.saldo = saldo
        self.cuenta_corriente = cuenta_corriente

    def retirar_dinero(self, dinero):
        if self.saldo >= dinero:
            self.saldo -= dinero  
        else:
            raise ValueError("El saldo es insuficiente")

    
    def transferir_dinero(self, destinatario, cantidad):
        if self.saldo >= cantidad:
            self.saldo -= cantidad
            destinatario.saldo + cantidad
        else:
            raise ValueError("No tienes suficiente saldo para transferir")

    def agregar_dinero(self, cantidad):
        self.saldo += cantidad
    
alicia = UsuarioBanco("Alicia", 100, True)
bob = UsuarioBanco("Bob", 50, True)

alicia.agregar_dinero(20)

bob.transferir_dinero(alicia, 20)

alicia.retirar_dinero(50)

print(f"Saldo de Alicia: {alicia.saldo}") 
print(f"Saldo de Bob: {bob.saldo}")
        
#EJERCICIO 16

def contar_palabras(texto):
    palabras = texto.split()  
    contador = {}  
    
    for palabra in palabras:
        if palabra in contador:
            contador[palabra] += 1  
        else:
            contador[palabra] = 1  
    
    return contador  


def reemplazar_palabras(texto, palabra_original, palabra_nueva):
    return texto.replace(palabra_original, palabra_nueva) 

def eliminar_palabra(texto, palabra):
    return texto.replace(palabra, "")  

def procesar_texto(opcion, texto, *args):
    if opcion == "contar":
        return contar_palabras(texto)  
    elif opcion == "reemplazar":
        return reemplazar_palabras(texto, args[0], args[1])  
    elif opcion == "eliminar":
        return eliminar_palabra(texto, args[0])  
    else:
        return "Opción no válida"  

texto = "Este es un ejemplo de texto. Este texto contiene palabras repetidas."

print(procesar_texto("contar", texto))  
print(procesar_texto("reemplazar", texto, "texto", "relato"))  
print(procesar_texto("eliminar", texto, "ejemplo"))  




