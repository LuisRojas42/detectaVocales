#! /usr/bin/env python
# -*- coding: utf-8 -*-
from scipy.fftpack import fft
from scipy.io import wavfile
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import soundfile as sf
import numpy as np
import pyaudio
import wave
import struct
import time

play = True

A_files_H = ['AR.wav', 'A-L.wav', 'AI.wav']
E_files_H = ['ER.wav', 'E-L.wav', 'EI.wav']
I_files_H = ['I-R.wav', 'I-L.wav', 'II.wav']
O_files_H = ['O-R.wav', 'O-L.wav', 'OI.wav']
U_files_H = ['UR.wav', 'U-L.wav', 'UI.wav']


A_files_M = ['A-M.wav', 'AS.wav']
E_files_M = ['E-M.wav', 'ES.wav']
I_files_M = ['I-M.wav', 'IS.wav']
O_files_M = ['O-M.wav']
U_files_M = ['U-M.wav', 'US.wav']

def get_max(file):

	fs, data = wavfile.read(file)
	#print('Data from file: ' + str(data))

	data_fft = fft(data)
	freqs = np.fft.fftfreq(len(data_fft))
	#print('Data after FFT: ' + str(data_fft))

	ab = np.abs(data_fft)
	idx = np.argmax(ab)

	freq = freqs[idx]
	freq_in_hz = abs(freq * fs)

	#print('Absolute values of data: ' + str(ab))

	#print('Maximum value (' + file + '): ' + str(max(ab)))
	#print('Index of max arg (' + file + '): ' + str(idx))
	print('Frequency in Hz max (' + file + '): ' + str(freq_in_hz))
	#print('Just freq (' + file + '): ' + str(freq))
	#print('Sound Rate (' + file + '): ' + str(fs))
	#print('Index of max value: ' + str(list(ab).index(max(ab))))
	#print('')
	return freq_in_hz




def avg(files):

	if len(files) == 0:
		return 0
	else:
		summ = 0
		for file in files:
			summ = summ + get_max(file)

		avg = summ / len(files)
		print('Average: ' + str(avg))
		return avg


    
def avg_vowels(sex):
	vow = []

	if sex == 'H':
		print('HOMBRE')
		#A
		print('A')
		vow.append(avg(A_files_H))
		print('')
		#E
		print('E')
		vow.append(avg(E_files_H))
		print('')
		#I
		print('I')
		vow.append(avg(I_files_H))
		print('')
		#O
		print('O')
		vow.append(avg(O_files_H))
		print('')
		#U
		print('U')
		vow.append(avg(U_files_H))
		print('')

	else:
		print('MUJER')
		#A
		print('A')
		vow.append(avg(A_files_M))
		print('')
		#E
		print('E')
		vow.append(avg(E_files_M))
		print('')
		#I
		print('I')
		vow.append(avg(I_files_M))
		print('')
		#O
		print('O')
		vow.append(avg(O_files_M))
		print('')
		#U
		print('U')
		vow.append(avg(U_files_M))
		print('')

	return vow



def compare(avgs, value):
	difs = []

	if value > 100 and value < 2500:
		for avg in avgs:
			if avg > value:
				difs.append(avg - value)
			else:
				difs.append(value - avg)

		idx = difs.index(min(difs))

		if idx == 0:
			return 'A'
		elif idx == 1:
			return 'E'
		elif idx == 2:
			return 'I'
		elif idx == 3:
			return 'O'
		else:
			return 'U'
	else:
		return ''

    
def filter(val):
	if val > 100 and val < 2500:
		return val
	else:
		return '.'

    
def getVowel(sex, usrIn):
    averages_H = avg_vowels(sex)
    #averages_M = avg_vowels('M')
    print(averages_H)

    #averages = [732, 398, 215, 516, 290]

    CHUNK = 1024 * 4
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=CHUNK
                )

    global play
    play = True
    while play:
        data = stream.read(CHUNK)
        data_int = struct.unpack(str(2 * CHUNK) + 'B', data)
        data_fft = fft(data_int)

        freqs = np.fft.fftfreq(len(data_fft))

        ab = np.abs(data_fft)
        idx = np.argmax(ab[1:])

        freq = freqs[idx + 1]
        freq_in_hz = abs(freq * RATE)

        #print(compare(averages_H, freq_in_hz*2))
        #label.config(text = compare(averages_H, freq_in_hz*2))
        usrIn.delete('0', 'end')
        usrIn.insert('end',compare(averages_H, freq_in_hz*2))
        usrIn.update()
        #print(freq_in_hz * 2)
        #print(filter(freq_in_hz * 2))

        
class Menu():

    def __init__(self):
        self.raiz = Tk()

        self.xp = BooleanVar()
        self.hp = BooleanVar()

        self.raiz.title("Detectar vocales")
        self.raiz.resizable(0, 0)
        self.raiz.geometry("400x250")
        
        #text = Text(self.raiz, height=10, width=30)
        #text.insert(INSERT, "Hello.....")
        #text.pack(side=ttk.BOTTOM)
        txtVar = StringVar(None)
        self.usrIn = Entry(self.raiz, textvariable = txtVar, width = 50)
        
        self.usrIn.pack(side = 'bottom')
        #usrIn.insert(0,"text")
        #usrIn.insert('end'," AAA")

        self.back = ttk.Frame()

        self.back.config(width="400", height="250")
        miImagen = PhotoImage(file='back2.png')
        Label(self.back, image=miImagen, bg="white", font=(18)).place(x=0, y=0)

        self.g_xp = Checkbutton(self.back, variable=self.xp, onvalue=True, offvalue=False, bg="white")
        self.g_xp.place(x=102, y=45)
        self.g_hp = Checkbutton(self.back, variable=self.hp, onvalue=True, offvalue=False, bg="white")
        self.g_hp.place(x=192, y=45)

        self.play = ttk.Button(self.back, text="Play", command=self.play)
        self.play.place(x=85, y=120)
        self.stop = ttk.Button(self.back, text="Stop", command=self.parar, state=DISABLED)
        self.stop.place(x=205, y=120)

        self.back.pack()

        self.raiz.mainloop()

    def play(self, *args):
        xp = self.xp.get()
        hp = self.hp.get()
        if (xp & hp):
            messagebox.showinfo(message="Solo debe marcar una opción", title="Resultado")
            return;
        if ((not xp) & (not hp)):
            messagebox.showinfo(message="Debe marcar una opción", title="Resultado")
            return;
        if (xp & (not hp)):
            self.play.configure(state=DISABLED)
            self.stop['state'] = 'normal'
            getVowel('H', self.usrIn)
            return;
        if ((not xp) & hp):
            self.play.configure(state=DISABLED)
            self.stop['state'] = 'normal'
            getVowel('M', self.usrIn)
            return;
        
    def parar(self, *args):
        self.stop.configure(state=DISABLED)
        self.play['state'] = 'normal'
        global play
        play = False
        
        
        
def main():
    men = Menu()
    return 0



if __name__ == '__main__':
    main()