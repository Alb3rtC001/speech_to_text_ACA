#This file is design for run in jupyter
import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt
import time
from scipy.fftpack import fft
from tkinter import TclError

#Uncomment this
#%matplotlib tk

CHUNK = 1024 * 2           #Cuanto audio se va a procesar por frame
FORMAT = pyaudio.paInt16   #El formato va a ser de 16bits
CHANNELS = 1               #Indica que va a ser mono el audio
RATE = 44100               #kHz audio por segundo 

#Creación de los ejes de la gráfica
fig, (ax, ax2) = plt.subplots(2, figsize=(15, 8))

#Instanciamos el pyaudio para que reconozca el microfono y el audio
p = pyaudio.PyAudio()

stream = p.open(
    format = FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input = True,
    output = True,
    frames_per_buffer=CHUNK
)

#Variabnle for X de la gráfica
x = np.arange(0, 2*CHUNK, 2)
#Rango de frecuancia
x_fft = np.linspace(0, RATE, CHUNK)

#Crea una linea con datos random
line, = ax.plot(x, np.random.rand(CHUNK), '-', lw=2)
#Transforma la linea en un resultado semilog
line_fft, =ax2.semilogx(x_fft, np.random.rand(CHUNK), '-', lw=2)

#Formateando los ejes de la gráfica
ax.set_title('AUDIO WAVEFROM')
ax.set_xlabel('audio')
ax.set_ylabel('volumen')
ax.set_ylim(0, 255)
ax.set_xlim(0, 2 * CHUNK)
plt.setp(ax, xticks=[0, CHUNK, 2 * CHUNK], yticks=[0, 128, 255])

ax2.set_xlim(20, RATE / 2)

#Muestra la gráfica sin pararla
plt.show(block=False)

print('steam started')

#Medir frame ratio
frame_count = 0
start_time = time.time()

#Bucle optimizado para mostrar la gráfica
#URL: Basti's Scratchpad on the internet Spedding up Matplotlib
while True:
    #Data en binario
    data = stream.read(CHUNK)
    
    #Convierte data en enteros, haciendolo un array con np y con un offset en Y de 127
    data_int = struct.unpack(str(2 * CHUNK) + 'B', data)
    
    #Crea un array np con otro offset de 128
    data_np = np.array(data_int, dtype='b')[::2] + 128
    
    line.set_ydata(data_np)
    
    #Reescalarlo para normalizarlo en una línea
    y_fft = fft(data_int)
    line_fft.set_ydata(np.abs(y_fft[0:CHUNK]) * 2 / (256 * CHUNK))
    
    #Actualiza el cambas de la gráfica
    try:
        fig.canvas.draw()
        fig.canvas.flush_events()
        frame_count += 1
        
    except TclError:
        
        #Calcula la media de ratio frames
        frame_rate = frame_count / (time.time() - start_time)
        
        print('stream stoped')
        print('media de ratio frames = {:.0f} FPS'.format(frame_rate))
        break