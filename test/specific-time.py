from loop_listen.loop_listen  import Loop_listen as Loop



i=5
try:
    for i in range(i):
        audio = Loop(filename=str(i), threshold=False, max_seconds=3)
        audio.listen()
except KeyboardInterrupt:
    print('interrupted!')

print('Finalizado com sucesso')