import numpy as np
import parselmouth
import pyaudio
import queue
import time

import matplotlib.pyplot as plt
import seaborn as sns

BLOCK_SIZE = 1600

q = queue.Queue()

def record_callback(in_data, frame_count, time_info, status):
	q.put((np.frombuffer(in_data, dtype=np.float32), frame_count, time_info, status))
	return (None, pyaudio.paContinue)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=16000, input=True, start=False, frames_per_buffer=BLOCK_SIZE, stream_callback=record_callback)

sns.set()

plt.ion()

fig = plt.figure()
ax = fig.add_subplot(111)

BLOCK_COUNT = 10
history = np.zeros(BLOCK_SIZE * BLOCK_COUNT, dtype=np.float32)
#line, = ax.plot(np.arange(len(history)) / 44100, np.zeros(len(history)), 'b-')
#ax.set_ylim([-0.2, 0.2])
line, = ax.plot(np.arange(1 + len(history) // 2) / 16000, np.zeros(1 + len(history) // 2), 'b-')
ax.set_ylim([-40, -5])
fig.tight_layout()

stream.start_stream()

while True:
	i = 0
	while True:
		i += 1
		data, frame_count, time_info, status = q.get()
		if q.empty():
			break
		history[:-BLOCK_SIZE] = history[BLOCK_SIZE:]
		history[-BLOCK_SIZE:] = data
	print(i)

	spectrum = parselmouth.Sound(history, sampling_frequency=16000).to_spectrum()

	#line.set_ydata(history)
	line.set_xdata(spectrum.xs())
	line.set_ydata(np.log(np.sum(np.power(spectrum.values, 2), axis=0)))
	ax.relim()
	ax.autoscale_view()
	fig.canvas.draw()
	fig.canvas.flush_events()
