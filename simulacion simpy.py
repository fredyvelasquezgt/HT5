import simpy
import random
import math
#Fredy Velasquez - Mariana David


# name: identificador del proceso
# Ram_need: cantidad de ram necesitado
# cinstrucciones: cantidad de instrucciones


def process(env, name, Ram_need, cinstrucciones, CPU, wait_time, RAM, banderallegada):
    global cuentafinal
    cuentafinal = 0 #Inicio en 0
    yield env.timeout(banderallegada)
    llegada = env.now #Me indica que esta pasando en la actualidad
    run = True #Para el while
    while run: #While que corre todo
        yield RAM.get(Ram_need)
        print(' %s esta listo para empezar - INICIANDO PROCESO, con un tiempo de %s, ram = %s' % (
            name, env.now,  Ram_need)) #Imprimo mis params
        while cinstrucciones > 0:

            with CPU.request() as req: #Tomado de los recursos simpy

                yield req
                yield env.timeout(1)
                cinstrucciones = cinstrucciones - 3  # Valor de instrucciones por unidad de tiempo
                if(cinstrucciones < 0):
                    cinstrucciones = 0
                print(' %s Hace 3 procesos, con un tiempo de %s y queda con %s estan en espera (pendientes)' %
                      (name, env.now, cinstrucciones))
            # En caso de ir a espera
            irespera = random.randint(1, 2)
            if(irespera == 1):
                with wait_time.request() as req: #Tomado de los recursos simpy
                    yield req #Return
                    yield env.timeout(1) #Tiemp
                    print(' %s entra a espera, con un tiempo de %s' % (
                        name, env.now))
        RAM.put(Ram_need)  #Vuelve a RAM 
        tiempo = env.now - llegada #Calculo el tiempo con el actual y con el de llegada
        print(' %s FINALIZADO, finaliza con un tiempo de %s' %
              (name, tiempo))
        cuentafinal = cuentafinal + tiempo #A la cuenta final anterior la suma la nueva ademas del tiempo
        run = False

RAM = simpy.Container(env, init=100, capacity=100)  # Atributos basicos de la RAM
env = simpy.Environment()  # Crea el ambiente de simulacion - 'linea de tiempo'
CPU = simpy.Resource(env, capacity=1)  # cantidad de CPU'S

#------------COLA----------------#
#Lista de esperas de la cola
wait = simpy.Resource(env, capacity=3) #Capacidad de 3
cantidadpro = 50  #Numero de procesos
random.seed(10)  #Seed de Random

for i in range(cantidadpro): #For con formulas respecticas
    #Cantidad de Instrucciones por proceso
    Cantint = (random.randint(1, 10))

    Ram_need = (random.randint(1, 10))  # cantidad de ram x proceso

    timepollega = (random.expovariate(1/10)) #Definir tiempo de llegada

    env.process(process(env, 'Proceso %d' %  #Round para reducir los decs
                        i, round(Ram_need), round(Cantint), CPU, wait, RAM, timepollega))

env.run() #Ejecuto
print('Tiempo promedio ', cuentafinal/cantidadpro) #Imprimo el tiempo promedio - Graficar - Este sera para cada proceso de la cola