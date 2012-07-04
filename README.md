matrizTemperaturaMPI
====================

Matriz de calculo de temperatura com MPI (Python)

Execicio com a utilização de MPI com Python.
Matriz de temperatura, calcula a propagação da temperatura matriz

dependencias:
    python
    mpi4py

para rodar:
$ mpirun -n [numero de processos] python mpi.py

#### Melhorias ###
Alterar a troca de mensagens, não passar a matriz inteira,
somente a parte que cada processo vai usar.
Implimentar a troca de mensagens entre os processos.

(getter e scatter)
