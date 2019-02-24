import numpy as np
import pyaudio
import wave
import os

import logging

class Loop_listen(object):
    def __init__(self, pathname='./', filename='temp', rate = 16000, max_seconds=1, threshold=True, threshold_limit = 3, debug=False):
        self.chunk = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = rate
        self.swidth = 2
        self.Threshold = threshold_limit if threshold else -1
        self.Max_Seconds = max_seconds
        self.TimeoutSignal= int(((self.RATE / self.chunk * self.Max_Seconds) + 2))
        self.FileNameTmp = filename
        self.silence = True
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format = self.FORMAT,
                            channels = self.CHANNELS,
                            rate = self.RATE,
                            input = True,
                            output = False,
                            frames_per_buffer = self.chunk)
        self.pathname = pathname
        self.create_path()
        self.debug=debug
        pass

    def create_path(self):
        if(self.pathname != './' or self.pathname != '/'):
            if(not os.path.isdir(self.pathname)):
                os.mkdir(self.pathname)
        path = os.path.join(self.pathname, 'output')
        audio= os.path.join(path, 'audio')
        # img = os.path.join(path, 'img')
        if(not os.path.isdir(path)):
            os.mkdir(path)
            os.mkdir(audio)
            # os.mkdir(img)

        self.pathname=path

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def listen(self):
        if(self.debug): logging.debug("\n...Waiting you speech...\n")
        while self.silence:
            try:
                input_ = self.GetStream(self.chunk)
            except:
                continue
            rms_value = self.rms(input_)
            if (rms_value > self.Threshold):
                self.silence=False
                LastBlock=input_
                if(self.debug): logging.debug("...Recoding...")
                self.KeepRecord(LastBlock)
    
    def GetStream(self,chunk):
        return self.stream.read(chunk)

    def rms(self, frame):
        d = np.frombuffer(frame, np.int16).astype(np.float)
        return int(np.sqrt( np.mean(d**2))/1000)

    def KeepRecord(self, LastBlock):
        all = list()
        all.append(LastBlock)
        for i in range(self.TimeoutSignal):
            try:
                data = self.GetStream(self.chunk)
            except:
                continue
            all.append(data)
        data = b''.join(all)
        
        self.WriteSpeech(data)

    def WriteSpeech(self, WriteData):
        self.closeStream()
        try:
            wf = wave.open(self.getPath('audio'), 'wb')
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(WriteData)
            wf.close()
            if(self.debug): logging.debug("File saved")
        except:
            if(self.debug): logging.warning("I could not save this file")
            pass


    def getPath(self, subfolder):
        if(subfolder == 'audio'):
            ext = '.wav'
        elif(subfolder == 'img'):
            ext = '.png'
        else:
            ext = ''
        return os.path.join(self.pathname, subfolder, self.FileNameTmp+ext)

    def closeStream(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

# i=1
# try:
#     while(True):
#         audio = AudioHandler(filename=str(i), threshold_limit= 3)
#         audio.listen()
#         i+=1
# except KeyboardInterrupt:
#     print('interrupted!')

# print('Finalizado com sucesso')