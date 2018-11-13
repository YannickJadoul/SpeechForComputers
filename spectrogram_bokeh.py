import sound_recorder

import math
import numpy as np
import parselmouth

import bokeh.layouts
import bokeh.models
import bokeh.palettes
import bokeh.plotting
import colorcet

import scipy.ndimage

import time


SAMPLING_FREQUENCY = 16000
BLOCK_SIZE = 100

recorder = sound_recorder.SoundRecorder(sampling_frequency=SAMPLING_FREQUENCY, block_size=BLOCK_SIZE)
recorder.start()


TIME_SLICE = 0.25

wave_source = bokeh.models.ColumnDataSource({'time': [], 'amplitude': []})
spectrum_source = bokeh.models.ColumnDataSource({'frequency': [], 'power_density': []})
spectrogram_source = bokeh.models.ColumnDataSource({'values': [], 'x': [], 'y': [], 'w': [], 'h': []})

TOOLS = 'xpan,xbox_select,xwheel_zoom,hover,reset'

recording = bokeh.models.widgets.Toggle(label="Record", active=True, button_type='success')
gain = bokeh.models.widgets.Slider(start=1, end=20, value=1, step=1, title="Gain")

fig_wave = bokeh.plotting.figure(tools=TOOLS, active_scroll='xwheel_zoom', sizing_mode='scale_height')
fig_wave.plot_width *= 4
fig_wave.line('time', 'amplitude', source=wave_source, line_width=2)
fig_wave.circle('time', 'amplitude', source=wave_source, size=0, color=None, nonselection_color=None)
fig_wave.x_range = bokeh.models.ranges.DataRange1d(range_padding=0) # follow='end', follow_interval=TIME_SLICE, range_padding=0)
fig_wave.y_range = bokeh.models.ranges.Range1d(start=-1, end=1)
fig_wave.hover.mode = "vline"
fig_wave.hover.tooltips = [
    ("time", "@time{0.0[0000]} s"),
    ("amplitude", "@amplitude{0.0000}"),
]

fig_spectrum = bokeh.plotting.figure(tools=TOOLS, active_scroll='xwheel_zoom', sizing_mode='scale_height')
fig_spectrum.plot_width *= 4
fig_spectrum.line('frequency', 'power_density', source=spectrum_source, line_width=2, color='firebrick')
fig_spectrum.x_range = bokeh.models.ranges.DataRange1d(bounds='auto', range_padding=0)
fig_spectrum.y_range = bokeh.models.ranges.Range1d(start=-40, end=80)
fig_spectrum.hover.mode = "vline"
fig_spectrum.hover.tooltips = [
    ("frequency", "@frequency{0.0[0]} Hz"),
    ("power density", "@power_density{0.0000} dB/Hz"),
]

fig_spectrogram = bokeh.plotting.figure(tools=TOOLS, active_scroll='xwheel_zoom', sizing_mode='scale_height')
fig_spectrogram.plot_width *= 4
fig_spectrogram.image(image='values', x='x', y='y', dw='w', dh='h', source=spectrogram_source, palette=list(reversed(colorcet.gray)))
#spectrogram_color_mapper = bokeh.models.LinearColorMapper(palette=list(reversed(colorcet.gray)))
#fig_spectrogram.rect(x='x', y='y', width='w', height='h', color={'field': 'values', 'transform': spectrogram_color_mapper}, source=spectrogram_source)
fig_spectrogram.x_range = bokeh.models.ranges.Range1d(0, 1)
fig_spectrogram.y_range = bokeh.models.ranges.Range1d(0, 1)

widgets = bokeh.layouts.widgetbox(recording, gain, width=400, sizing_mode='fixed')
layout = bokeh.layouts.row(widgets, bokeh.layouts.column(fig_wave, fig_spectrum, fig_spectrogram, sizing_mode='scale_height'), sizing_mode='scale_height')


def update_recording(active):
	recording.button_type = 'success' if active else 'danger'

def get_sound_slice(sound):
	#to_time = int(10 * sound.xmax) / 10
	#sound_slice = sound.extract_part(from_time=to_time - TIME_SLICE, to_time=to_time, preserve_times=True)
	return sound.extract_part(from_time=sound.xmax - TIME_SLICE)


def get_selected_sound_slice(sound_slice):
	if len(wave_source.selected.indices) == 0:
		return sound_slice
	else:
		m, M = np.min(wave_source.selected.indices), np.max(wave_source.selected.indices)
		from_time, to_time = sound_slice.frame_number_to_time(m+1), sound_slice.frame_number_to_time(M+1)
		return sound_slice.extract_part(from_time=from_time, to_time=to_time, preserve_times=True)


def update_wave(sound_slice):	
	sound_slice.values *= gain.value
	wave_source.data = {'time': sound_slice.xs(), 'amplitude': sound_slice.values[0,:]}


def update_spectrum(sound_slice):
	spectrum = sound_slice.to_spectrum()
	spectrum_db = 10 * np.log10(2 * np.sum(np.power(spectrum.values, 2), axis=0) * spectrum.dx / 4.0e-10)
	spectrum_source.data = {'frequency': spectrum.xs(), 'power_density': spectrum_db}

def update():
	t = time.time()

	if not recording.active:
		return

	sound_slice = get_sound_slice(recorder.sound)
	selected_sound_slice = get_selected_sound_slice(sound_slice)

	update_wave(sound_slice)
	update_spectrum(selected_sound_slice)

	# try:
	# 	spectrogram = selected_sound_slice.to_spectrogram(window_length=0.02)

	# 	spectrogram.xmin = selected_sound_slice.xmin
	# 	spectrogram_values = 10 * np.log10(spectrogram.values)
	# 	spectrogram_values = np.maximum(spectrogram_values, np.max(spectrogram_values) - 70)
	# 	#spectrogram_values = scipy.ndimage.zoom(spectrogram_values, 4, order=1, mode='constant', prefilter=False)

	# 	spectrogram_source.data = {'values': [spectrogram_values], 'x': [spectrogram.x1 + spectrogram.dx / 2], 'y': [spectrogram.y1 + spectrogram.dy / 2], 'w': [spectrogram.nx * spectrogram.dx], 'h': [spectrogram.ny * spectrogram.dy]}
	# 	fig_spectrogram.x_range = bokeh.models.ranges.Range1d(sound_slice.xmin, sound_slice.xmax)
	# 	fig_spectrogram.y_range = bokeh.models.ranges.Range1d(spectrogram.ymin, spectrogram.ymax)
	# except parselmouth.PraatError:
	# 	spectrogram_source.data = {'values': [], 'x': [], 'y': [], 'w': [], 'h': []}
	
	#for x in recorded.values[0]:
	#	print(f'{x:.4}', end=' ')

	print(time.time() - t)


def on_wave_selection_changed(attr, old, new):
	sound_slice = get_sound_slice()
	selected_sound_slice = get_selected_sound_slice(sound_slice)
	update_spectrum(selected_sound_slice)


"""def on_start_end_wave_changed(attr, old, new):
	sound_slice = get_sound_slice()
	selected_sound_slice = get_selected_sound_slice(sound_slice)
	update_spectrum(selected_sound_slice)
"""

wave_source.on_change('selected', on_wave_selection_changed)
recording.on_click(update_recording)

doc = bokeh.plotting.curdoc()
doc.add_periodic_callback(update, 100)
doc.add_root(layout)
