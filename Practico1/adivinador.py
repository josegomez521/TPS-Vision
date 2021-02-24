import random

def adivina(intentos2):
    num1 = random.randint(0, 100)
    print(num1)
    contador = 0
    while True:
        if contador == intentos2:
            print('\nSe acabaron los intentos')
            break
        else:
            contador += 1
            num2 = int(input('Ingrese un número: '))
            if num1 == num2:
                print(f'Adivinaste el número en {contador} intentos')
                break
            else:
                print('No adivinaste el número')

intentos1 = 3
print('Adivina el número entre 0 y 100')
adivina(intentos1)