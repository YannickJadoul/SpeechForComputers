import numpy as np
import parselmouth
import pyaudio

from functools import partial

class SoundPlayer:

	def _play_callback(self, in_data, frame_count, time_info, status):
		data = self._sound.values[:,self._sound_i:self._sound_i+frame_count].astype('float32').tobytes('F')
		self._sound_i = min(self._sound_i + frame_count, len(self._sound))

		return (data, pyaudio.paContinue if self._sound_i < len(self._sound) else pyaudio.paComplete)

	def __init__(self, block_size=200):
		self._block_size = block_size

		self._pyaudio = pyaudio.PyAudio()
		self._stream = None

	def play(self, sound):
		if self._stream and self._stream.is_active():
			self._stream.stop_stream()

		self._sound = sound
		self._sound_i = 0
		self._stream = self._pyaudio.open(format=pyaudio.paFloat32, channels=sound.n_channels, rate=int(sound.sampling_frequency), output=True, frames_per_buffer=self._block_size, stream_callback=self._play_callback)

	def stop(self):
		if self._stream and self._stream.is_active():
			self._stream.stop_stream()

	def close(self):
		if self._pyaudio:
			self._pyaudio.terminate()

	@property
	def t(self):
		if not self._stream or not self._stream.is_active():
			return None
		else:
			return self._sound.frame_number_to_time(self._sound_i + 1)
