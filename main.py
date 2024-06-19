# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 14:30:15 2024

@author: M
"""

from fastapi import FastAPI 
from routers.router import user_router
import gradio as gr
import plotly.graph_objects as go
import shutil
from models import converter 
import subprocess
import gradio as gr
import os

def make_plot():
    labels = ['1 класс','2 класс','3 класс',]
    values = [5, 25, 70]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    
    fig.update_layout(width=400,
    height=200,
    paper_bgcolor = 'black')
    
    return fig

app = FastAPI()

with gr.Blocks() as demo:
    video_file = gr.Video(max_length = 7200)
    upload_button = gr.Button('Обработать')
    reload_button = gr.Button('Новое видео', link = '/')    
    
    with gr.Row(visible=False) as row:
        with gr.Tab('1-я половина урока'):
            with gr.Row():
                with gr.Column():
                    plot = gr.Plot(make_plot, label = "Таматика", container = False)
                with gr.Column():
                    with gr.Accordion("Вопросы:", open=False):
                        q_intro = gr.Textbox(text_align = 'left', lines = 20)
                        
                    with gr.Accordion("Домашнее задание:", open=False):
                        hw_intro = gr.Textbox(text_align = 'left', lines = 20)
            
            intro = gr.Markdown("intro", visible = False)
            transcript_button_intro = gr.Button('Получить расшифровку')
            with gr.Accordion("Display Details", open=False):
                out_intro = gr.Textbox(text_align = 'left', lines = 20)
            
            def read_transcript(name):
                with open(f'./segments_diar/{name}.txt', 'r') as f:
                    data = ''
                    for line in f:
                        data += line 
                with open(f'./segments_diar/{name}_question.txt', 'r') as f:
                    q = ''
                    for line in f:
                        q += line        
                with open(f'./segments_diar/{name}_home_work.txt', 'r') as f:
                    hw = ''
                    for line in f:
                        hw += line 
                    return {
                            transcript_button_intro: gr.Button(visible=False),
                            out_intro: data,
                            q_intro: q,
                            hw_intro: hw
                            }
                
            transcript_button_intro.click(read_transcript, intro,
                                          [transcript_button_intro, out_intro, q_intro, hw_intro])
                
        with gr.Tab('2-я половина урока'):
            with gr.Row():
                with gr.Column():
                    plot = gr.Plot(make_plot, label = "Таматика", container = False)
                with gr.Column():
                    with gr.Accordion("Вопросы:", open=False):
                        q_midle = gr.Textbox(text_align = 'left', lines = 20)
    
            midle = gr.Markdown("midle", visible = False)
            
            transcript_button_midle = gr.Button('Получить расшифровку')
            with gr.Accordion("Display Details", open=False):
                out_midle = gr.Textbox(text_align = 'left', lines = 20)
            
            def read_transcript(name):
                with open(f'./segments_diar/{name}.txt', 'r') as f:
                    data = ''
                    for line in f:
                        data += line 
                with open(f'./segments_diar/{name}_question.txt', 'r') as f:
                    q = ''
                    for line in f:
                        q += line 
                    return {
                            transcript_button_midle: gr.Button(visible=False),
                            out_midle: data,
                            q_midle: q
                            }
                
            transcript_button_midle.click(read_transcript, midle, 
                                          [transcript_button_midle, out_midle, q_midle])
            
        with gr.Tab('3-я половина урока'):
            with gr.Row():
                with gr.Column():
                    plot = gr.Plot(make_plot, label = "Таматика", container = False)
                with gr.Column():
                    with gr.Accordion("Вопросы:", open=False):
                        q_end = gr.Textbox(text_align = 'left', lines = 20)
                        
                    with gr.Accordion("Домашнее задание и анонс:", open=False):
                        hw_end = gr.Textbox(text_align = 'left', lines = 20)
                        
                        
            end = gr.Markdown("end", visible = False)
            
            transcript_button_end = gr.Button('Получить расшифровку')
            with gr.Accordion("Display Details", open=False):
                out_end = gr.Textbox(text_align = 'left', lines = 20)
            
            def read_transcript(name):
                with open(f'./segments_diar/{name}.txt', 'r') as f:
                    data = ''
                    for line in f:
                        data += line 
                with open(f'./segments_diar/{name}_question.txt', 'r') as f:
                    q = ''
                    for line in f:
                        q += line        
                with open(f'./segments_diar/{name}_home_work.txt', 'r') as f:
                    hw = ''
                    for line in f:
                        hw += line 
                    return {
                            transcript_button_end: gr.Button(visible=False),
                            out_end: data,
                            q_end: q,
                            hw_end: hw
                            }
            
            transcript_button_end.click(read_transcript, end,
                                        [transcript_button_end, out_end, q_end, hw_end])
                
            
    def upload_video(input_video):
        if os.path.isfile("./models/full_audio.wav"):
            os.remove("./models/full_audio.wav")
        if os.path.isfile("./segments_diar/intro.wav"):
            os.remove("./segments_diar/intro.wav")
        if os.path.isfile("./segments_diar/midle.wav"):
            os.remove("./segments_diar/midle.wav")
        if os.path.isfile("./segments_diar/end.wav"):
            os.remove("./segments_diar/end.wav")
                    
        run_model = 'python ./models/rnnt.py --model_config ./models/rnnt_model_config.yaml --model_weights ./models/rnnt_model_weights.ckpt --tokenizer_path ./models/tokenizer_all_sets --device cuda --audio_path ./models/full_audio.wav --hf_token <hf_token>'
        path = "../models"
        shutil.copy(input_video, path)
        converter.make_wav(input_video)
        subprocess.call(run_model, shell=True)
        
        return {row: gr.Row(visible=True)}
    
    upload_button.click(upload_video, video_file, row)
    
app = gr.mount_gradio_app(app, demo, path='/gradio') 
app.include_router(router = user_router)
