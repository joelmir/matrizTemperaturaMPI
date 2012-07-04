# -*- coding: utf-8 -*-
from mpi4py import MPI
import sys, copy


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

alfa = 0.2
#Monta 5 matrizes
for m in range(5):
    matriz=[]
    for passo in range(10):
        
        if rank == 0:
            #se for o primeiro passo, le a matriz, senão mantém a matriz atualizada
            if passo == 0:
                try:
                    with open('matriz'+str(m)+'.txt','r') as arq:
                        matriz = eval(arq.read())
                        if type(matriz) != list:
                            print 'O arquivo esta errado'
                except IOError:
                    print 'O arquivo não pode ser lido'
                    sys.exit()
                except SyntaxError:
                    print 'O arquivo não está no formato correto'
                    sys.exit()
                
            for r in range(size):
                comm.send(matriz, dest=r, tag=1)
                           

        data = comm.recv(source=0, tag=1)
        interv = len(data)/size
        quebrado = len(data)%size

        if interv == 0 and rank >= len(data):
            #A matriz não atingiu o numero de colunas referentes ao numero de processos
            pass
        else:
           
            inicio = 0
            #calcula o inicio da posição do processo    
            for r in range(rank):
                if r < quebrado:
                    inicio += (interv+1)
                else:
                    inicio += interv

            if rank < quebrado:
                interv += 1    
            #Calcula a posicao 
            #print rank,interv,inicio
            #data1 = data
            data1 = copy.deepcopy(data)
            for p in range(interv):
                i = inicio+p
                for j in range(len(data[i])):
                    #Temos i,j da matriz
                    
                    #somente calcula se não for uma borda
                    if i != 0 and j != 0 and i < (len(data)-1) and j < (len(data[i])-1):
                        valor = data1[i-1][j]
                        valor += data1[i+1][j]
                        valor += data1[i][j-1]
                        valor += data1[i][j+1]
                        
                        #Calcula a temperatura no proximo instante
                        #print rank,valor,data[i][j], (valor - 4*data[i][j]), alfa
                        data[i][j] += alfa*(valor - 4*data1[i][j])
        #envia a nova matriz para o processo zero            
        comm.send(data, dest=0, tag=1)

        if rank == 0:
            for r in range(size):
                data = comm.recv(source=r, tag=1)
                #print data
                interv = len(data)/size
                quebrado = len(data)%size
                #print r,data
                if interv == 0 and r >= len(data) and False:
                    #A matriz não atingiu o numero de colunas referentes ao numero de processos
                    #Não atualiza os dados desse processo
                    pass
                else:
                   
                    inicio = 0
                    #calcula o inicio da posição do processo    
                    for r in range(r):
                        if r < quebrado:
                            inicio += (interv+1)
                        else:
                            inicio += interv

                    if r < quebrado:
                        interv += 1    
                    #Calcula a posicao 
                    for p in range(interv):
                        matriz[p+inicio] = data[p+inicio]
            for rr in matriz:
                print rr
            #print matriz
            #Se for o ultimo passo, grava uma imagem da matriz
            if passo == 9:
                with open('matriz'+str(m+1)+'.txt','w') as arq:
                    arq.write(str(matriz))
            '''
            else:
                with open('matriz'+str(m)+'.txt','w') as arq:
                    arq.write(str(matriz))
            '''
        
