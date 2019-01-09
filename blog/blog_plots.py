import parselmouth

import numpy as np

import bokeh.plotting as bp
import colorcet

sound = parselmouth.Sound("de_noordenwind_en_de_zon_sentence.wav")
detail = sound.extract_part(0.3, 0.35, preserve_times=True)
detail_bis = sound.extract_part(1.95, 2, preserve_times=True)

sound_pre_emphasized = sound.copy()
sound_pre_emphasized.pre_emphasize()
spectrogram = sound_pre_emphasized.to_spectrogram(window_length=0.025)
spectrogram_values = 10 * np.log10(spectrogram.values)
spectrogram_values = np.maximum(spectrogram_values, np.max(spectrogram_values) - 60)


wave_tools = "xpan,xwheel_zoom,xzoom_in,xzoom_out,reset,save"


bp.output_file("wave.html")

fig_wave = bp.figure(plot_width=1000, plot_height=400, tools=wave_tools, active_scroll="xwheel_zoom")
fig_wave.line(sound.xs(), sound.values[0,:])
fig_wave.x_range.bounds = 'auto'
fig_wave.x_range.start = sound.xmin
fig_wave.x_range.end = sound.xmax
fig_wave.title.text = "Geluidsgolven van de zin \"De noordenwind en de zon waren erover aan het redetwisten wie de sterkste was van hun beiden.\""
fig_wave.xaxis.axis_label = "Tijd [s]"
fig_wave.yaxis.axis_label = "Luchtdruk/amplitude"

bp.save(fig_wave)


bp.output_file("wave_detail.html")

fig_wave_detail = bp.figure(plot_width=1000, plot_height=400, tools=wave_tools, active_scroll="xwheel_zoom")
fig_wave_detail.line(detail.xs(), detail.values[0,:])
fig_wave_detail.x_range.bounds = 'auto'
fig_wave_detail.x_range.start = detail.xmin
fig_wave_detail.x_range.end = detail.xmax
fig_wave_detail.title.text = "Detail van de geluidsgolven van de o-klank in \"noordenwind\""
fig_wave_detail.xaxis.axis_label = "Tijd [s]"
fig_wave_detail.yaxis.axis_label = "Luchtdruk/amplitude"

bp.save(fig_wave_detail)


bp.output_file("wave_detail_bis.html")

fig_wave_detail_bis = bp.figure(plot_width=1000, plot_height=400, tools=wave_tools, active_scroll="xwheel_zoom")
fig_wave_detail_bis.line(detail_bis.xs(), detail_bis.values[0,:])
fig_wave_detail_bis.x_range.bounds = 'auto'
fig_wave_detail_bis.x_range.start = detail_bis.xmin
fig_wave_detail_bis.x_range.end = detail_bis.xmax
fig_wave_detail_bis.title.text = "Detail van de geluidsgolven van de o-klank in \"erover\""
fig_wave_detail_bis.xaxis.axis_label = "Tijd [s]"
fig_wave_detail_bis.yaxis.axis_label = "Luchtdruk/amplitude"

bp.save(fig_wave_detail_bis)


bp.output_file("spectrogram.html")

fig_spectrogram = bp.figure(plot_width=1000, plot_height=400, tools=wave_tools, active_scroll="xwheel_zoom")
fig_spectrogram.line(spectrogram.xs(), spectrogram.values[0,:])
fig_spectrogram.image(image=[spectrogram_values], x=spectrogram.x1 + spectrogram.dx / 2, y=spectrogram.y1 + spectrogram.dy / 2, dw=spectrogram.nx * spectrogram.dx, dh=spectrogram.ny * spectrogram.dy, palette=colorcet.fire)
fig_spectrogram.x_range.bounds = 'auto'
fig_spectrogram.x_range.start = spectrogram.xmin
fig_spectrogram.x_range.end = spectrogram.xmax
fig_spectrogram.y_range.start = spectrogram.ymin
fig_spectrogram.y_range.end = spectrogram.ymax
fig_spectrogram.title.text = "Spectrogram van de zin \"De noordenwind en de zon waren erover aan het redetwisten wie de sterkste was van hun beiden.\""
fig_spectrogram.xaxis.axis_label = "Tijd [s]"
fig_spectrogram.yaxis.axis_label = "Frequentie [Hz]"


bp.save(fig_spectrogram)

