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
from models.regression import process_topic
import subprocess
import os


def split_list(input_list, chunk_size):
    return [' '.join(input_list[i : i + chunk_size]) for i in range(0, len(input_list), chunk_size)]

def make_plot(classes, part):
    labels = ['Рефлексия','Практика','Другая тематика']
    class_0_counter = 0
    class_1_counter = 0
    class_2_counter = 0
    classes_len = 0
    for item in classes:
        if item == 0:
            class_0_counter += 1
        elif item == 1:
            class_1_counter += 1
        else:
            class_2_counter += 1
    classes_len = class_0_counter + class_1_counter + class_2_counter   
    values = [class_0_counter/classes_len*100,
              class_1_counter/classes_len*100,
              class_2_counter/classes_len*100]
    
    if part == 'midle':
        with open(f'./segments_diar/{part}_practise_metric.txt', 'w') as f:
            f.write(f'{class_1_counter/classes_len*100}')
    else:
        pass
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    
    fig.update_layout(width=400,
    height=200,
    paper_bgcolor = 'black')
    print("done plot")
    
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
                    #graph = gr.Button('график')
                    plot_intro = gr.Plot(label = "Таматика", container = False, visible = True)
                with gr.Column():
                    with gr.Accordion("Вопросы:", open=False):
                        q_intro = gr.Textbox(label = '',text_align = 'left', lines = 20)
                        
                    with gr.Accordion("Домашнее задание:", open=False):
                        hw_intro = gr.Textbox(label = '',text_align = 'left', lines = 20)
                        
                    with gr.Accordion("Похвала", open=False):
                        gw_intro = gr.Textbox(label = '',text_align = 'left', lines = 20)  
                    
            
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
                with open(f'./segments_diar/{name}_good_work.txt', 'r') as f:
                    gw = ''
                    for line in f:
                        gw += line 
                    
                    return {
                            transcript_button_intro: gr.Button(visible=False),
                            out_intro: data,
                            q_intro: q,
                            hw_intro: hw,
                            gw_intro: gw
                      }
                
            transcript_button_intro.click(read_transcript, intro,
                                          [transcript_button_intro, out_intro, 
                                           q_intro, hw_intro, gw_intro])
            def classificate(name):
                with open(f'./segments_diar/{name}.txt', 'r') as f:
                    data_for_classifier = []
                    for line in f:
                        chunks = split_list(line[21:].split(), 5)
                        data_for_classifier.extend(chunks)
                classes = process_topic(data_for_classifier)
                print(classes)
                figure_to_draw = make_plot(classes, 'intro')
                return figure_to_draw
                
            
            demo.load(classificate, intro, plot_intro)
            #graph.click(classificate, intro, plot_intro)
                
        with gr.Tab('2-я половина урока'):
            with gr.Row():
                with gr.Column():
                    plot_midle = gr.Plot(label = "Таматика", container = False, visible = True)
                with gr.Column():
                    with gr.Accordion("Вопросы:", open=False):
                        q_midle = gr.Textbox(label = '',text_align = 'left', lines = 20)
                    with gr.Accordion("Похвала", open=False):
                        gw_midle = gr.Textbox(label = '',text_align = 'left', lines = 20)
    
            midle = gr.Markdown("midle", visible = False)
            
            transcript_button_midle = gr.Button('Получить расшифровку')
            with gr.Accordion("Display Details", open=False):
                out_midle = gr.Textbox(label = '',text_align = 'left', lines = 20)
            
            def read_transcript(name):
                with open(f'./segments_diar/{name}.txt', 'r') as f:
                    data = ''
                    for line in f:
                        data += line
                with open(f'./segments_diar/{name}_question.txt', 'r') as f:
                    q = ''
                    for line in f:
                        q += line
                with open(f'./segments_diar/{name}_good_work.txt', 'r') as f:
                    gw = ''
                    for line in f:
                        gw += line 
                    return {
                            transcript_button_midle: gr.Button(visible=False),
                            out_midle: data,
                            q_midle: q,
                            gw_midle: gw 
                            }
                
            transcript_button_midle.click(read_transcript, midle, 
                                          [transcript_button_midle, out_midle,
                                           q_midle, gw_midle])
            def classificate(name):
                with open(f'./segments_diar/{name}.txt', 'r') as f:
                    data_for_classifier = []
                    for line in f:
                        chunks = split_list(line[21:].split(), 5)
                        data_for_classifier.extend(chunks)
                classes = process_topic(data_for_classifier)
                print(classes)
                figure_to_draw = make_plot(classes, 'midle')
                return figure_to_draw
                
            
            demo.load(classificate, midle, plot_midle)
            
        with gr.Tab('3-я половина урока'):
            with gr.Row():
                with gr.Column():
                    plot_end = gr.Plot(label = "Таматика", container = False, visible = True)
                with gr.Column():
                    with gr.Accordion("Вопросы:", open=False):
                        q_end = gr.Textbox(label = '',text_align = 'left', lines = 20)     
                    with gr.Accordion("Домашнее задание и анонс:", open=False):
                        hw_end = gr.Textbox(label = '',text_align = 'left', lines = 20)
                    with gr.Accordion("Похвала", open=False):
                        gw_end = gr.Textbox(label = '',text_align = 'left', lines = 20)
                        
                        
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
                with open(f'./segments_diar/{name}_good_work.txt', 'r') as f:
                    gw = ''
                    for line in f:
                        gw += line 
                    return {
                            transcript_button_end: gr.Button(visible=False),
                            out_end: data,
                            q_end: q,
                            hw_end: hw,
                            gw_end: gw
                            }
            
            transcript_button_end.click(read_transcript, end,
                                        [transcript_button_end, out_end, q_end,
                                         hw_end, gw_end])
            def classificate(name):
                with open(f'./segments_diar/{name}.txt', 'r') as f:
                    data_for_classifier = []
                    for line in f:
                        chunks = split_list(line[21:].split(), 5)
                        data_for_classifier.extend(chunks)
                classes = process_topic(data_for_classifier)
                print(classes)
                figure_to_draw = make_plot(classes, 'end')
                return figure_to_draw
                
            
            demo.load(classificate, end, plot_end)
            
        with gr.Tab('Summary'):
            with gr.Row():
                with gr.Column():
                    emot_refl = gr.Textbox(label = 'Эмоциональная рефлексия',text_align='left', interactive=True)
                    logic_refl =  gr.Textbox(label = 'Логическая рефлексия',text_align='left', interactive=True)
                    practise = gr.Textbox(label = 'Практическая часть',text_align='left', interactive=True)
                    homework =  gr.Textbox(label = 'Домашнее задание',text_align='left', interactive=True)
                    goodwork = gr.Textbox(label = 'Похвала',text_align='left', interactive=True)
                with gr.Column():
                    positive_feedback = gr.Textbox(label = 'Позитивная обратная связь',text_align='left', interactive=True)
                    negative_feedback = gr.Textbox(label = 'Комментарии',text_align='left', interactive=True)
                    output = gr.TextArea(label = 'Отчет', text_align='left', interactive=True, show_copy_button = True)
                    
            summary = gr.Markdown("end", visible = False)
            transcript_button_summary = gr.Button('Рассчитать метрики')
            summaryze_button = gr.Button('Отобразить отчет')
            
            def make_summary(name):
                
                # рефлексия
                # обработка классификатором эмоц - 0 логист - 1 
                e_refl = '0/3'
                log_refl = '0/3'
                
                print('start')
                with open('./segments_diar/midle_practise_metric.txt', 'r') as f:
                    prac_metric = f.read()
                # midle урок - 1
                if int(float(prac_metric)) >= 30:
                    prac = '1/3'
                    print(prac_metric)
                else:
                    print(prac_metric)
                    prac = '0/3'
                                
                with open('./segments_diar/intro_home_work.txt', 'r') as f:
                    hw = ''
                    for line in f:
                        hw += line[20:]
                    if hw == '':
                        intro_hw = 0
                    else: 
                        intro_hw = 1
                with open('./segments_diar/end_home_work.txt', 'r') as f:
                    hw = ''
                    for line in f:
                        hw += line[20:]
                    if hw == '':
                        end_hw = 0
                    else: 
                        end_hw = 2    
                
                good_work = 0
                parts = ['intro', 'midle', 'end']
                for name in parts:
                    counter = 0
                    with open(f'./segments_diar/{name}_good_work.txt', 'r') as f:
                        gw = ''
                        for line in f:
                            gw += line[20:]
                        if gw == '':
                            counter += 0
                        else: 
                            counter += 1
                     
                    good_work += counter
                    
                hw_summary = f'{intro_hw + end_hw}/3'
                gw_summary = f'{good_work}/3'
                
                return {
                        transcript_button_summary: gr.Button(visible=False),
                        emot_refl: e_refl,
                        logic_refl: log_refl,
                        practise:prac,
                        homework:hw_summary,
                        goodwork:gw_summary
                    }
                
            transcript_button_summary.click(make_summary, summary,
                                            [transcript_button_summary, 
                                             emot_refl, logic_refl,
                                             practise, homework, goodwork])
            
            def otchet(emot_refl, logic_refl,
                       practise, homework, goodwork, positive_feedback, negative_feedback):
            
                out = f'Эмоциональная рефлексия: {emot_refl}\n' + \
                        f'Логическая рефлексия: {logic_refl}\n' + \
                        f'Практическая часть: {practise}\n' + \
                        f'Домашняя работа: {homework}\n' + \
                        f'Похвала: {goodwork}\n' + \
                        f'Положительная обратная связь: {positive_feedback}\n'+ \
                        f'Комменатрии: {negative_feedback}'
                               
                return{
                        output: out
                    }
            
            summaryze_button.click(otchet, [emot_refl, logic_refl,
                                           practise, homework, goodwork,positive_feedback,
                                           negative_feedback], 
                                           [output])
            
    def upload_video(input_video):
        if os.path.isfile("./models/full_audio.wav"):
            os.remove("./models/full_audio.wav")
        if os.path.isfile("./segments_diar/intro.wav"):
            os.remove("./segments_diar/intro.wav")
        if os.path.isfile("./segments_diar/midle.wav"):
            os.remove("./segments_diar/midle.wav")
        if os.path.isfile("./segments_diar/end.wav"):
            os.remove("./segments_diar/end.wav")
                    
        run_model = 'python ./models/rnnt.py --model_config ./models/rnnt_model_config.yaml --model_weights ./models/rnnt_model_weights.ckpt --tokenizer_path ./models/tokenizer_all_sets --device cuda --audio_path ./models/full_audio.wav --hf_token <token>'
        path = "../models"
        shutil.copy(input_video, path)
        converter.make_wav(input_video)
        subprocess.call(run_model, shell=True)
        
        
        
        return {row: gr.Row(visible=True)}
    
    upload_button.click(upload_video, video_file, row)
    

    
app = gr.mount_gradio_app(app, demo, path='/gradio') 
app.include_router(router = user_router)
