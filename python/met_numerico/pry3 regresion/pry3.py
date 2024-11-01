import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sympy import *
from ecuacion import Ecuacion
from sis_ecuacion import SistemaEcuacion
from sis_ecuacion import despeje_por_gauss_jordan

def leer_tipo_regresion():
    while True:
        try:
          print("Elija el tipo de Regresión ")
          print("[1] Lineal")
          print("[2] Polinomial Cuadrática")
          print("[3] Lineal Múltiple")
          tipo_regresion = int(input('Opción: ')) # Solicitar el tipo de regresión
          if tipo_regresion in [1, 2, 3]:
              break
          else:
              print("Opción no válida. Por favor, elige 1, 2 o 3.")
        except ValueError:
            print("Entrada inválida. Por favor, introduce una opción válida.") 
   
    return tipo_regresion

def obtener_datos(tipo_regresion):
       
    tuplas = []  # Lista para almacenar los pares de datos
    try:
        while True:
            try:
                n = int(input("¿Cuántas tuplas de datos quieres introducir?: "))  # Solicitar la cantidad de datos
                if (n < 2):
                    print("Entrada inválida. Por favor, introduce una cantidad de datos mayor que 2.")
                else:
                    break
            except ValueError:
                print("Entrada inválida. Por favor, introduce una opción válida.") 
    except:
        print("Entrada inválida. Por favor, introduce números válidos.")
    if tipo_regresion in [1, 2]:
        for i in range(n):
            while True:
                try:
                    # Pedir al usuario que introduzca un par de datos numéricos
                    x = float(input(f"[{i + 1}] Ingrese x: "))
                    y = float(input(f"[{i + 1}] Ingrese y: "))
                    tuplas.append((x, y))  # Almacenar el par 
                    break  # Salir del bucle si la entrada es válida
                except ValueError:
                    print("Entrada inválida. Por favor, introduce números válidos.")
    else:
        for i in range(n):
            while True:
                try:
                    # Pedir al usuario que introduzca un par de datos numéricos
                    x1 = float(input(f"[{i + 1}] Ingrese x1: "))
                    x2 = float(input(f"[{i + 1}] Ingrese x2: "))
                    y = float(input(f"[{i + 1}] Ingrese y: "))
                    tuplas.append((x1, x2, y))  # Almacenar el par 
                    break  # Salir del bucle si la entrada es válida
                except ValueError:
                    print("Entrada inválida. Por favor, introduce números válidos.")
    return tuplas

def regresion_lineal(puntos):
    """
    Calcula los coeficientes de la regresión lineal a partir de una lista de puntos.
    
    :param puntos: Lista de tuplas (x, y)
    :return: Tupla (a0, a1, r2) donde a0 y a1 son las constantes del módelo de regresión y = a0 + a1x y r2 el coeficiente de determinación
    """
    n = len(puntos)
    
    # Calcular las sumas necesarias
    suma_x = sum(x for x, y in puntos)
    suma_y = sum(y for x, y in puntos)
    suma_xy = sum(x * y for x, y in puntos)
    suma_x2 = sum(x ** 2 for x, y in puntos)
    
    eqs = [
        Ecuacion.of([n, suma_x], suma_y),
        Ecuacion.of([suma_x, suma_x2] , suma_xy)
        ]
    
    sistema_eq = SistemaEcuacion(eqs)
    resultado = despeje_por_gauss_jordan(sistema_eq.clone())
    
    a0 = resultado[0]
    a1 = resultado[1]
    
    media_y = suma_y / n
    suma_desviaciones = sum((y - media_y) ** 2 for x, y in puntos)
    sr = sum((y - a0 - a1 * x) ** 2 for x, y in puntos)
    
    r2 = (suma_desviaciones - sr) / suma_desviaciones
    
    return a0, a1, r2


def regresion_polinomial_cuadratica(puntos):
    """
    Calcula los coeficientes de la regresión polinomial cuadrática a partir de una lista de puntos.
    
    :param puntos: Lista de tuplas (x, y)
    :return: Tupla (a0, a1, a2) donde a0, a1 y a2 son las constantes del módelo de regresión y = a0 + a1x + a2x^2 y r2 el coeficiente de determinación
    """
    n = len(puntos)
    
    # Calcular las sumas necesarias
    suma_x = sum(x for x, y in puntos)
    suma_y = sum(y for x, y in puntos)
    suma_xy = sum(x * y for x, y in puntos)
    suma_x2y = sum(x ** 2 * y for x, y in puntos)
    suma_x2 = sum(x ** 2 for x, y in puntos)
    suma_x3 = sum(x ** 3 for x, y in puntos)
    suma_x4 = sum(x ** 4 for x, y in puntos)
    
    eqs = [
        Ecuacion.of([n, suma_x, suma_x2], suma_y),
        Ecuacion.of([suma_x, suma_x2, suma_x3] , suma_xy),
        Ecuacion.of([suma_x2, suma_x3, suma_x4], suma_x2y)
        ]
    
    sistema_eq = SistemaEcuacion(eqs)
    resultado = despeje_por_gauss_jordan(sistema_eq.clone())
    
    a0 = resultado[0]
    a1 = resultado[1]
    a2 = resultado[2]
    
    media_y = suma_y / n
    suma_desviaciones = sum((y - media_y) ** 2 for x, y in puntos)
    sr = sum((y - a0 - a1 * x - a2 * x ** 2) ** 2 for x, y in puntos)
    
    r2 = (suma_desviaciones - sr) / suma_desviaciones #Cálculo del coeficiente de determinación
    
    return a0, a1, a2, r2

def regresion_lineal_multiple(puntos):
    """
    Calcula los coeficientes de la regresión polinomial cuadrática a partir de una lista de puntos.
    
    :param puntos: Lista de tuplas (x, y)
    :return: Tupla (a0, a1, a2) donde a0, a1 y a2 son las constantes del módelo de regresión y = a0 + a1x_1 + a2x_2 y r2 el coeficiente de determinación
    """
    n = len(puntos)
    
    #Calcular las sumas necesarias
    suma_x1 = sum(x1 for x1, x2, y in puntos)
    suma_x2 = sum(x2 for x1, x2, y in puntos)
    suma_y = sum(y for x1, x2, y in puntos)
    suma_x1cuad = sum(x1 ** 2 for x1, x2, y in puntos)
    suma_x1x2 = sum(x1 * x2 for x1, x2, y in puntos)
    suma_x1y = sum(x1 * y for x1, x2, y in puntos)
    suma_x2cuad = sum(x2 ** 2 for x1, x2, y in puntos)
    suma_x2y = sum(x2 * y for x1, x2, y in puntos)
    
    eqs = [
        Ecuacion.of([n, suma_x1, suma_x2], suma_y),
        Ecuacion.of([suma_x1, suma_x1cuad, suma_x1x2], suma_x1y),
        Ecuacion.of([suma_x2, suma_x1x2, suma_x2cuad], suma_x2y)
        ]
    
    sistema_eq = SistemaEcuacion(eqs)
    resultado = despeje_por_gauss_jordan(sistema_eq.clone())
    
    a0 = resultado[0]
    a1 = resultado[1]
    a2 = resultado[2]
    
    media_y = suma_y / n
    suma_desviaciones = sum((y - media_y) ** 2 for x1, x2, y in puntos)
    sr = sum((y - a0 - a1 * x1 - a2 * x2) ** 2 for x1, x2, y in puntos)
    r2 = (suma_desviaciones - sr) / suma_desviaciones #Cálculo del coeficiente de determinación
    
    return a0, a1, a2, r2
 
def grafica_dispersion_2d(datos):
    # Datos que lleva el gráfico
    x = [x for x, y in datos]
    y = [y for x, y in datos]

    # Crear la gráfica de dispersión
    plt.scatter(x, y, color='blue', marker='o')

    # Añadir título y etiquetas
    plt.title('Gráfica de Dispersión')
    plt.xlabel('Eje X')
    plt.ylabel('Eje Y')

    # Mostrar la gráfica
    plt.grid()
    plt.show()
    
def grafica_dispersion_3d(datos):
    # Datos que lleva la gráfica
    x1 = [x1 for x1, x2, y in datos]
    x2 = [x2 for x1, x2, y in datos]
    y = [y for x1, x2, y in datos]

    # Crear la figura y el eje 3D
    fig = plt.figure(figsize = (6,6))
    ax = fig.add_subplot(projection='3d')

    # Crear la gráfica de dispersión
    ax.scatter(x1, x2, y, color='blue')

    # Añadir título y etiquetas
    ax.set_title('Gráfica de Dispersión 3D')
    ax.set_xlim(xmin = 0)
    ax.set_ylim(ymin = 0)
    ax.set_zlim(zmin = 0)
    ax.set_xlabel('Eje X1')
    ax.set_ylabel('Eje X2')
    ax.set_zlabel('Eje Y')

    ax.view_init(elev=20., azim=-35)
    # Mostrar la gráfica
    plt.tight_layout()
    plt.show()

def pronostico_una_variable(expr):
    while True:
        try:
            print("¿Desea pronosticar algún valor?: ")
            print("[1] Sí")
            print("[0] No")
            pronosticar = int(input("Opción: "))
   
            match pronosticar:
                case 1:
                    valor_a_pronosticar = float(input("Valor x a pronosticar: ")) # Solicitar el valor a Pronosticar
                    print(f"y({valor_a_pronosticar}) = {expr.subs(x, valor_a_pronosticar)}")
                case 0:
                    print("<<Se ha finalizado el prónostico.>>")
                    break
                case _:
                    print("Elija una opción válida")
        except ValueError:
            print("Entrada inválida. Por favor, introduce un valor numérico.")    

def pronostico_dos_variable(expr):
    while True:
        try:
            print("¿Desea pronosticar algún valor?: ")
            print("[1] Sí")
            print("[0] No")
            pronosticar = int(input('Opción: '))
            
            match pronosticar:
                case 1:
                    x1_a_pronosticar = float(input("Valor x1 a pronosticar: "))
                    x2_a_pronosticar = float(input("Valor x2 a pronosticar: "))
                    resultado = expr.subs([(x1, x1_a_pronosticar), (x2, x2_a_pronosticar)])
                    print(f"y({x1_a_pronosticar}, {x2_a_pronosticar}) = {resultado}")
                case 0:
                    print("<<Se ha finalizado el pronóstico.>>")  
                    break
                case _:
                    print("Elija una opción válida")
        except ValueError:
            print("Entrada inválida. Por favor, introduce un valor numérico.")

            
if __name__ == "__main__":
    tipo_regresion = leer_tipo_regresion()
    datos = obtener_datos(tipo_regresion)
    
    print("Los datos introducidos son:")
    for dato in datos:
        print(dato)
    
    if tipo_regresion == 1:
        a0, a1, r2 = regresion_lineal(datos)
        print("Coeficientes: ")
        print(f"a0 = {a0}")
        print(f"a1 = {a1}")
        
        print("Modelo de regresión lineal:")
        x, y = symbols('x y')
        expr = a0 + a1 * x
        print(f"y = {expr}")
        print(f"Coeficiente de determinación = {r2}")
        
        grafica_dispersion_2d(datos)
        
        pronostico_una_variable(expr)
    
    if tipo_regresion == 2:
        a0, a1, a2, r2 = regresion_polinomial_cuadratica(datos)
        print("Coeficientes: ")
        print(f"a0 = {a0}")
        print(f"a1 = {a1}")
        print(f"a2 = {a2}")
        
        print("Modelo de regresión polinomial cuadrática:")
        x, y = symbols('x y')
        expr = a0 + a1 * x + a2 * x ** 2
        print(f"y = {expr}")
        print(f"Coeficiente de determinación = {r2}")
        
        grafica_dispersion_2d(datos)
        
        pronostico_una_variable(expr)
        
    if tipo_regresion == 3:
        a0, a1, a2, r2 = regresion_lineal_multiple(datos)
        print("Coeficientes: ")
        print(f"a0 = {a0}")
        print(f"a1 = {a1}")
        print(f"a2 = {a2}")
        
        print("Modelo de regresión lineal múltiple:")
        x1, x2, y = symbols('x1 x2 y')
        expr = a0 + a1 * x1 + a2 * x2
        print(f"y = {expr}")
        print(f"Coeficiente de determinación = {r2}")
        
        grafica_dispersion_3d(datos)
        
        pronostico_dos_variable(expr)
