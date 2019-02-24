import loop_listen as Loop


i=5
try:
    for i in range(i):
        audio = Loop(filename=str(i), threshold_limit= 5, max_seconds=3, debug=False)
        audio.listen()
except KeyboardInterrupt:
    print('interrupted!')

print('Finalizado com sucesso')