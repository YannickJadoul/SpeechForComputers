import sound_player
import sound_recorder
import ui

import math
import numpy as np
import parselmouth

import bokeh.layouts
import bokeh.plotting

import matplotlib.pyplot as plt
import scipy.ndimage

import subprocess
import time

from functools import partial


SAMPLING_FREQUENCY = 16000
BLOCK_SIZE = 100

RECODING_SLICE = 0.25
RECORDED_SLICE = 10
SPECTROGRAM_WINDOW_LENGTH = {'start': 0.005, 'end': 0.05, 'value': 0.02, 'step': 0.005}


player = sound_player.SoundPlayer(block_size=BLOCK_SIZE)
recorder = sound_recorder.SoundRecorder(sampling_frequency=SAMPLING_FREQUENCY, block_size=BLOCK_SIZE)
recorder.start()

extra_sounds = {"De noordenwind en de zon": parselmouth.Sound("de_noordenwind_en_de_zon_sentence.wav"),
                "Yanny of Laurel":          parselmouth.Sound("yanny_laurel.wav")}


sound_selection = ui.SoundSelectionButtons(extra_sounds.keys())

wave_plot = ui.WavePlot()
spectrum_plot = ui.SpectrumPlot()
spectrogram_plot = ui.SpectrogramPlot()
play_indicator = ui.PlayIndicator([wave_plot.fig, spectrogram_plot.fig])
ui.link_ranges(wave_plot.fig.x_range, spectrogram_plot.fig.x_range)

window_length_slider = bokeh.models.widgets.Slider(**SPECTROGRAM_WINDOW_LENGTH, format="0.000", title="Spectrogram window")
play_button = bokeh.models.widgets.Button(label="\u25b6 Play")
print_button = bokeh.models.widgets.Button(label="Print")

widgets = bokeh.layouts.widgetbox(*sound_selection.buttons, ui.hr(), window_length_slider, ui.hr(), play_button, print_button, width=400, sizing_mode='fixed')
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
			spectrogram = sound_slice.to_spectrogram(window_length=window_length_slider.value)

			spectrogram_values = 10 * np.log10(spectrogram.values)
			spectrogram_values = np.maximum(spectrogram_values, np.max(spectrogram_values) - 70)
			spectrogram_values = scipy.ndimage.zoom(spectrogram_values, 4, order=1, mode='constant', prefilter=False)

			spectrogram_plot.source.data = {'values': [spectrogram_values], 'x': [spectrogram.x1 - spectrogram.dx / 2], 'y': [spectrogram.y1 - spectrogram.dy / 2], 'w': [spectrogram.nx * spectrogram.dx], 'h': [spectrogram.ny * spectrogram.dy]}
		except:
			spectrogram_plot.source.data = {'values': [], 'x': [], 'y': [], 'w': [], 'h': []}


def update_play_indicator():
	play_indicator.x = player.t


previous_blocks_recorded = 0

def print_samples(sound_slice):
	global previous_blocks_recorded
	blocks_recorded = recorder.blocks_recorded
	values = sound_slice.values[0,-BLOCK_SIZE * (blocks_recorded - previous_blocks_recorded):]
	for x in values:
		print(f'{x:.4}', end=' ') 
	previous_blocks_recorded = recorder.blocks_recorded


def update(manual=False):
	t = time.time()

	update_play_indicator()

	if manual or sound_selection.is_recording:
		sound = get_sound()
		highlighted_sound = get_highlighted_sound(sound)

		update_wave(sound)
		update_spectrum(highlighted_sound)
		update_spectrogram(None if sound_selection.is_recording else highlighted_sound)

	#print_samples(sound)

	#print(time.time() - t)

def update_spectrum_of_wave_selection(attr, old, new):
	sound = get_sound()
	highlighted_sound = get_highlighted_sound(sound)
	update_spectrum(highlighted_sound)
	update_spectrogram(None if sound_selection.is_recording else highlighted_sound)


def update_spectrogram_window_length(attr, old, new):
	sound = get_sound()
	highlighted_sound = get_highlighted_sound(sound)
	update_spectrogram(None if sound_selection.is_recording else highlighted_sound)


def play_sound():
	if not sound_selection.is_recording:
		sound = get_sound()
		highlighted_sound = get_highlighted_sound(sound)
		player.play(highlighted_sound)



def do_print():
	sound = get_sound()
	highlighted_sound = get_highlighted_sound(sound)
	t = highlighted_sound.xs()
	y = highlighted_sound.values[0,:]
	
	plt.clf()
	plt.figure(figsize = (6, 3.543), clear=True) # width, height in inches (14.8 x 9 cm)
	
	plt.subplot(211)
	plt.plot(t, y, 'k', linewidth = 1)
	plt.ylabel("amplitude")
	plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
	
	plt.tight_layout()
	
	plt.subplot(212)
	plt.specgram(y, Fs = SAMPLING_FREQUENCY, cmap=plt.get_cmap("plasma"))
	plt.xlabel("tijd (sec)")
	plt.ylabel("frequentie (Hz)")
	plt.ylim(0, 4000)
	plt.tight_layout()
	
	plt.savefig("wave.png", dpi=600, format="png", transparent=True)
	
	process = subprocess.Popen("./print_wave.sh", shell=True)


wave_plot.source.selected.on_change('indices', update_spectrum_of_wave_selection)

sound_selection.on_change(start_stop_recorder)
sound_selection.on_change(partial(update, True))

window_length_slider.on_change('value', update_spectrogram_window_length)
play_button.on_click(play_sound)
print_button.on_click(do_print)

doc = bokeh.plotting.curdoc()
doc.add_periodic_callback(update, 100)
doc.add_root(layout)

def on_session_destroyed(session_context):
	recorder.close()
	player.close()
