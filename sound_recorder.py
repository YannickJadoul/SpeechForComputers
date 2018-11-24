import numpy as np
import parselmouth
import pyaudio
import queue


class SoundRecorder:

	def _record_callback(self, in_data, frame_count, time_info, status):
		self._queue.put(np.frombuffer(in_data, dtype=np.float32))
		return (None, pyaudio.paContinue)

	def __init__(self, *, sampling_frequency=16000, block_size=200):
		self._blocks_count = 0
		self._queue = queue.Queue()
		self._sampling_frequency = sampling_frequency

		self._pyaudio = pyaudio.PyAudio()
		self._stream = self._pyaudio.open(format=pyaudio.paFloat32, channels=1, rate=sampling_frequency, input=True, start=False, frames_per_buffer=block_size, stream_callback=self._record_callback)

		self._sound = None

	def start(self):
		self._stream.start_stream()

	def stop(self, clear=False):
		self._stream.stop_stream()
		if clear:
			self.clear()

	@property
	def active(self):
		return self._stream.is_active()

	def clear(self):
		self._sound = None

	def close(self):
		if self._pyaudio:
			self._pyaudio.terminate()

	@property
	def sound(self):
		recorded = []
		while not self._queue.empty():
			recorded.append(self._queue.get())
			self._blocks_count += 1

		if recorded:
			recorded_sound = parselmouth.Sound(np.hstack(recorded), sampling_frequency=self._sampling_frequency)

			if self._sound is None:
				self._sound = recorded_sound
				return self._sound
			else:
				self._sound = parselmouth.Sound.concatenate([self._sound, recorded_sound])

		return self._sound

	@property
	def blocks_recorded(self):
		return self._blocks_count
