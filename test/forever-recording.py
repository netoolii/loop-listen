import loop_listen as Loop


i=0
try:
    while(True):
        audio = Loop(filename=str(i), threshold= False, max_seconds=3, rate = 16000, debug=False)
        audio.listen()
        i=+1
except KeyboardInterrupt:
    print('interrupted!')

print('Finalizado com sucesso')