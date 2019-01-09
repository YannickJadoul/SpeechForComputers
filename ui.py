import utils

import bokeh.layouts
import bokeh.models
import colorcet

from functools import partial


GRAPH_ASPECT_RATION = 4


class SoundSelectionButtons:

	RECORDING = "Record"
	RECORDED = "Recorded"

	@utils.no_recursion
	def _update_buttons(self, clicked, active):
		for button in self.buttons:
			if button is not clicked:
				button.active = False
			elif clicked is not self._recording_button:
				button.active = True

		changed = clicked is not self._last_clicked or clicked is self._recording_button
		self._last_clicked = clicked
		if changed:
			for f in self._on_change:
				f()

	def _update_recording_button(self, active):
		self._recording_button.button_type = 'success' if active else 'danger'

	def __init__(self, sounds):
		self._sounds = sounds

		self.buttons = [bokeh.models.widgets.Toggle(label=self.RECORDING, active=True, button_type='success'),
		                bokeh.models.widgets.Toggle(label=self.RECORDED, active=False, button_type='primary')]
		self.buttons.extend([bokeh.models.widgets.Toggle(label=sound, active=False, button_type='primary') for sound in sounds])
		self._recording_button = self.buttons[0]
		self._recorded_button = self.buttons[1]
		self._last_clicked = self._recording_button

		for button in self.buttons:
			button.on_click(partial(self._update_buttons, button))
		self._recording_button.on_click(self._update_recording_button)

		self._on_change = []

	@property
	def selected(self):
		return self._last_clicked.label

	@property
	def is_recording(self):
		return self._recording_button.active

	def on_change(self, f):
		self._on_change.append(f)


class WavePlot:

	def __init__(self):
		self.source = bokeh.models.ColumnDataSource({'time': [], 'amplitude': []})

		self.fig = bokeh.plotting.figure(tools='xpan,xbox_select,xbox_zoom,xwheel_zoom,xzoom_in,xzoom_out,hover,reset', active_drag='xbox_select', active_scroll='xwheel_zoom', sizing_mode='scale_height')
		self.fig.plot_width *= GRAPH_ASPECT_RATION
		self.fig.line('time', 'amplitude', source=self.source, line_width=2)
		self.fig.circle('time', 'amplitude', source=self.source, size=0, color=None, nonselection_color=None)
		self.fig.x_range = bokeh.models.ranges.DataRange1d(range_padding=0, min_interval=0.1)
		self.fig.y_range = bokeh.models.ranges.Range1d(start=-1, end=1)
		self.fig.hover.mode = "vline"
		self.fig.hover.tooltips = [
	    	("time", "@time{0.0[0000]} s"),
	    	("amplitude", "@amplitude{0.0000}"),
		]


class SpectrumPlot:

	def __init__(self):
		self.source = bokeh.models.ColumnDataSource({'frequency': [], 'power_density': []})

		self.fig = bokeh.plotting.figure(tools='xpan,xwheel_zoom,xzoom_in,xzoom_out,hover,reset', active_scroll='xwheel_zoom', sizing_mode='scale_height')
		self.fig.plot_width *= GRAPH_ASPECT_RATION
		self.fig.line('frequency', 'power_density', source=self.source, line_width=2, color='firebrick')
		self.fig.x_range = bokeh.models.ranges.DataRange1d(range_padding=0)
		self.fig.y_range = bokeh.models.ranges.Range1d(start=-40, end=80)
		self.fig.hover.mode = "vline"
		self.fig.hover.tooltips = [
		    ("frequency", "@frequency{0.0[0]} Hz"),
		    ("power density", "@power_density{0.0000} dB/Hz"),
		]


class SpectrogramPlot:

	def __init__(self):
		self.source = bokeh.models.ColumnDataSource({'values': [], 'x': [], 'y': [], 'w': [], 'h': []})

		self.fig = bokeh.plotting.figure(tools='hover', sizing_mode='scale_height')
		self.fig.plot_width *= 4
		self.fig.image(image='values', x='x', y='y', dw='w', dh='h', source=self.source, palette=list(reversed(colorcet.gray)))
		#spectrogram_color_mapper = bokeh.models.LinearColorMapper(palette=list(reversed(colorcet.gray)))
		#self.fig.rect(x='x', y='y', width='w', height='h', color={'field': 'values', 'transform': spectrogram_color_mapper}, source=spectrogram_source)
		self.fig.x_range = bokeh.models.ranges.Range1d(0, 1)
		self.fig.y_range = bokeh.models.ranges.Range1d(0, 4000)
		self.fig.hover.tooltips = [
	    	("time", "$x{0.0[0000]} s"),
		    ("frequency", "$y{0.0[0]} Hz"),
		]


class PlayIndicator:

	def __init__(self, figures):
		self.spans = []

		for fig in figures:
			span = bokeh.models.Span(location=None, dimension='height', line_color='firebrick', line_width=3)
			fig.add_layout(span)
			self.spans.append(span)


	@property
	def x(self):
		return self.spans[0].location

	@x.setter
	def x(self, value):
		for span in self.spans:
			span.location = value
	


def link_ranges(source, target):
	@utils.no_recursion
	def set_target(attr, old, new):
		setattr(target, attr, new)

	source.on_change('start', set_target)
	source.on_change('end', set_target)


def hr():
	return bokeh.models.widgets.Div(text='<hr />')
