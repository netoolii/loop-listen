from loop_listen.loop_listen  import Loop_listen as Loop


i=0
try:
    while(True):
        audio = Loop(filename=str(i), threshold= False, max_seconds=3, rate = 16000)
        audio.listen()
        i=+1
except KeyboardInterrupt:
    print('interrupted!')

print('Finalizado com sucesso')