def calcular (dias):
    semanas = dias / 7
    print(f'En {dias} dias han pasado {semanas} semanas')



def decorador(func):
    def inner():
        print('AHora se desplegarán los primeros del 0 al 1000')
        func()
        print('Fin de la iteración')
    return inner

# Forma 1
#primos_decorados = decorador(primos)
#primos_decorados()

# Forma 2
@decorador
def primos():
    for number in range (0, 20):  
        if number > 1:  
            for i in range (2, number):  
                if (number % i) == 0:  
                    break  
            else:  
                print (number) 

primos()

