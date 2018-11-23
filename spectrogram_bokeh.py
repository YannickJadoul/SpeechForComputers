import sound_recorder
import ui

import math
import numpy as np
import parselmouth

import bokeh.layouts
import bokeh.plotting

import scipy.ndimage

import time

from functools import partial


SAMPLING_FREQUENCY = 16000
BLOCK_SIZE = 100

RECODING_SLICE = 0.25
RECORDED_SLICE = 10
SPECTROGRAM_WINDOW_LENGTH = 0.02 # Turn into slider widget?


recorder = sound_recorder.SoundRecorder(sampling_frequency=SAMPLING_FREQUENCY, block_size=BLOCK_SIZE)
recorder.start()

extra_sounds = {"De noordenwind en de zon": parselmouth.Sound("de_noordenwind_en_de_zon_sentence.wav"),
                "Yanny of Laurel":          parselmouth.Sound("yanny_laurel.wav")}


sound_selection = ui.SoundSelectionButtons(extra_sounds.keys())

wave_plot = ui.WavePlot()
spectrum_plot = ui.SpectrumPlot()
spectrogram_plot = ui.SpectrogramPlot()
ui.link_ranges(wave_plot.fig.x_range, spectrogram_plot.fig.x_range)

widgets = bokeh.layouts.widgetbox(*sound_selection.buttons, width=400, sizing_mode='fixed')
layout = bokeh.layouts.row(widgets, bokeh.layouts.column(wave_plot.fig, spectrum_plot.fig, spectrogram_plot.fig, sizing_mode='scale_height'), sizing_mode='scale_height')


def start_stop_recorder():
	if sound_selection.selected == ui.SoundSelectionButtons.RECORDING:
		if sound_selection.is_recording and not recorder.active:
			recorder.clear()
			recorder.start()
		else:
			recorder.stop()
	else:
		if recorder.active:
			recorder.stop()


def get_sound_slice(sound, length):
	if sound is None or sound.duration <= length:
		return sound
	else:
		return sound.extract_part(from_time=sound.xmax - length)


def get_sound():
	if sound_selection.selected == ui.SoundSelectionButtons.RECORDING:
		return get_sound_slice(recorder.sound, RECODING_SLICE)
	elif sound_selection.selected == ui.SoundSelectionButtons.RECORDED:
		return get_sound_slice(recorder.sound, RECORDED_SLICE)
	else:
		return extra_sounds[sound_selection.selected]


def get_highlighted_sound(sound_slice):
	if sound_slice is None:
		return None
	if len(wave_plot.source.selected.indices) == 0:
		return sound_slice
	else:
		m, M = np.min(wave_plot.source.selected.indices), np.max(wave_plot.source.selected.indices)
		from_time, to_time = sound_slice.frame_number_to_time(m+1), sound_slice.frame_number_to_time(M+1)
		return sound_slice.extract_part(from_time=from_time, to_time=to_time, preserve_times=True)


def update_wave(sound_slice):
	if sound_slice is None:
		wave_plot.source.data = {'time': [], 'amplitude': []}
	else:
		wave_plot.source.data = {'time': sound_slice.xs(), 'amplitude': sound_slice.values[0,:]}


def update_spectrum(sound_slice):
	if sound_slice is None:
		spectrum_plot.source.data = {'frequency': [], 'power_density': []}
	else:
		spectrum = sound_slice.to_spectrum()
		spectrum_db = 10 * np.log10(2 * np.sum(np.power(spectrum.values, 2), axis=0) * spectrum.dx / 4.0e-10)
		spectrum_plot.source.data = {'frequency': spectrum.xs(), 'power_density': spectrum_db}


def update_spectrogram(sound_slice):
	if sound_slice is None:
		spectrogram_plot.source.data = {'values': [], 'x': [], 'y': [], 'w': [], 'h': []}
	else:
		try:
			spectrogram = sound_slice.to_spectrogram(window_length=SPECTROGRAM_WINDOW_LENGTH)

			spectrogram_values = 10 * np.log10(spectrogram.values)
			spectrogram_values = np.maximum(spectrogram_values, np.max(spectrogram_values) - 70)
			spectrogram_values = scipy.ndimage.zoom(spectrogram_values, 4, order=1, mode='constant', prefilter=False)

			spectrogram_plot.source.data = {'values': [spectrogram_values], 'x': [spectrogram.x1 - spectrogram.dx / 2], 'y': [spectrogram.y1 - spectrogram.dy / 2], 'w': [spectrogram.nx * spectrogram.dx], 'h': [spectrogram.ny * spectrogram.dy]}
		except:
			spectrogram_plot.source.data = {'values': [], 'x': [], 'y': [], 'w': [], 'h': []}


previous_blocks_recorded = 0

def print_samples(sound_slice):
	global previous_blocks_recorded
	blocks_recorded = recorder.blocks_recorded
	values = sound_slice.values[0,-BLOCK_SIZE * (blocks_recorded - previous_blocks_recorded):]
	for x in values:
		print(f'{x:.4}', end=' ') 
	previous_blocks_recorded = recorder.blocks_recorded


def update(manual=False):
	if not manual and not sound_selection.is_recording:
		return

	t = time.time()

	sound = get_sound()
	highlighted_sound = get_highlighted_sound(sound)

	update_wave(sound)
	update_spectrum(highlighted_sound)
	update_spectrogram(None if sound_selection.is_recording else sound)

	#print_samples(sound)

	#print(time.time() - t)

def update_spectrum_of_wave_selection(attr, old, new):
	sound = get_sound()
	highlighted_sound = get_highlighted_sound(sound)
	update_spectrum(highlighted_sound)


wave_plot.source.selected.on_change('indices', update_spectrum_of_wave_selection)

sound_selection.on_change(start_stop_recorder)
sound_selection.on_change(partial(update, True))


doc = bokeh.plotting.curdoc()
doc.add_periodic_callback(update, 100)
doc.add_root(layout)
