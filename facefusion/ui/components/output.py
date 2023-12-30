from typing import Tuple, Optional
import gradio

import facefusion.globals
from facefusion import wording
from facefusion.core import limit_resources, conditional_process
from facefusion.ui.core import get_ui_component
from facefusion.ui.typing import Update
from facefusion.normalizer import normalize_output_path
from facefusion.filesystem import is_image, is_video, clear_temp

OUTPUT_IMAGE : Optional[gradio.Image] = None
OUTPUT_VIDEO : Optional[gradio.Video] = None
OUTPUT_START_BUTTON : Optional[gradio.Button] = None
OUTPUT_CLEAR_BUTTON : Optional[gradio.Button] = None


def render() -> None:
	global OUTPUT_IMAGE
	global OUTPUT_VIDEO
	global OUTPUT_START_BUTTON
	global OUTPUT_CLEAR_BUTTON

	OUTPUT_IMAGE = gradio.Image(
		label = wording.get('output_image_or_video_label'),
		visible = False
	)
	OUTPUT_VIDEO = gradio.Video(
		label = wording.get('output_image_or_video_label')
	)
	OUTPUT_START_BUTTON = gradio.Button(
		value = wording.get('start_button_label'),
		variant = 'primary',
		size = 'sm'
	)
	OUTPUT_CLEAR_BUTTON = gradio.Button(
		value = wording.get('clear_button_label'),
		size = 'sm'
	)


def listen() -> None:
	output_path_textbox = get_ui_component('output_path_textbox')
	if output_path_textbox:
		OUTPUT_START_BUTTON.click(start, inputs = output_path_textbox, outputs = [ OUTPUT_IMAGE, OUTPUT_VIDEO ])
	OUTPUT_CLEAR_BUTTON.click(clear, outputs = [ OUTPUT_IMAGE, OUTPUT_VIDEO ])


def start(output_path : str) -> Tuple[gradio.Image, gradio.Video]:
	print(f'start >> source paths : {facefusion.globals.source_paths}')
	print(f'start >> target path : {facefusion.globals.target_path}')
	print(f'start >> output path : {facefusion.globals.output_path}')
	facefusion.globals.output_path = normalize_output_path(facefusion.globals.source_paths, facefusion.globals.target_path, output_path)
	limit_resources()
	conditional_process()
	if is_image(facefusion.globals.output_path):
		return gradio.update(value = facefusion.globals.output_path, visible = True), gradio.update(value = None, visible = False)
	if is_video(facefusion.globals.output_path):
		return gradio.update(value = None, visible = False).update(), gradio.update(value = facefusion.globals.output_path, visible = True)
	return gradio.update(), gradio.update()


def clear() -> Tuple[Update, Update]:
	if facefusion.globals.target_path:
		clear_temp(facefusion.globals.target_path)
	return gradio.update(value = None), gradio.update(value = None)
