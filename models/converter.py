# -*- coding: utf-8 -*-
"""
Created on Fri May 31 15:02:32 2024

@author: M
"""

import subprocess
import math
import re 

def format_time(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    full_seconds = int(seconds)
    milliseconds = int((seconds - full_seconds) * 100)

    if hours > 0:
        return f"{hours:02}:{minutes:02}:{full_seconds:02}:{milliseconds:02}"
    else:
        return f"{minutes:02}:{full_seconds:02}:{milliseconds:02}"
    
    
def search_question_regexp(expression):
    question_patterns = [   'как' ,	
                            'что' ,	
                            'сколько',	
                            'где'	,
                            'какой' ,	
                            'кто' 	,
                            'когда' ,	
                            'почему',	
                            'чем' 	,
                            'чего' 	,
                            'куда' 	,
                            'который', 	
                            'кому' 	,
                            'зачем' ,	
                            'откуда', 	
                            'чей' 	,
                            'чья' 	,
                            'каков' ,	
                            'отчего' 	]
    
    for pattern in question_patterns:
        if re.search(pattern, expression):
            return True
        else:
            return False      

def search_homework(expression):
    anouncement_patterns = [ 'домашн\w+',
                 'дамашн\w+',
                 'следующ\w+'       
        
        ]
    for pattern in anouncement_patterns:
        if re.search(pattern, expression):
            return True
        else:
            return False

def save_transcript(transc, name):
    
    with open(f'./segments_diar/{name}.txt', 'w') as f:
        for key, item in transc.items():
            f.write(f'{key} - {item}\n')
            
            
    with open(f'./segments_diar/{name}_question.txt', 'w+') as f:
        print('start searchin questions')
        for key, item in transc.items():
            if search_question_regexp(item):
                f.write(f'{key} - {item}\n')
        print("end_searching_questions")
    
    if name == 'end' or name == 'intro':
        with open(f'./segments_diar/{name}_home_work.txt', 'w+') as f:
            print('start searchin questions')
            for key, item in transc.items():
                if search_homework(item):
                    f.write(f'{key} - {item}\n')
            print("end_searching_questions")

        

def make_wav(file_name):
    ffmpeg_convert_comand = f'ffmpeg -i {file_name} -ab 16k -ac 1 -ar 16000 -vn ./models/full_audio.wav'
    subprocess.call(ffmpeg_convert_comand, shell=True)
    

def cut_video(transcriptions, boundaries):
    
    intro_dict = {}
    midle_dict = {}
    end_dict = {}
    
    start_of_lesson = boundaries[0][0]
    
    end_of_lesson = boundaries[-1][1] # end of speech in seconds
    
    end_of_intro = end_of_lesson / 10
    
    end_of_lesson_sec = end_of_lesson - (end_of_lesson / 5)
    
    max_intro_time = 0
    max_midle_time = 0
    
    
    for transcription, boundary in zip(transcriptions, boundaries):
        if max_intro_time <= end_of_intro:
            max_intro_time = boundary[1]
            intro_dict[f'[{str(format_time(boundary[0]))}-{str(format_time(boundary[1]))}]'] = transcription
            
        elif boundary[0] > max_intro_time and boundary[1] <= end_of_lesson_sec:
            max_midle_time = boundary[1]
            midle_dict[f'[{str(format_time(boundary[0]))}-{str(format_time(boundary[1]))}]'] = transcription
           
        elif boundary[0] > end_of_lesson_sec:
            end_dict[f'[{str(format_time(boundary[0]))}-{str(format_time(boundary[1]))}]'] = transcription
    
    save_transcript(intro_dict, 'intro')
    
    save_transcript(midle_dict, 'midle') 
    
    save_transcript(end_dict, 'end')   
    
    
    ffmpeg_cut_intro = f'ffmpeg -ss {start_of_lesson} -i ./models/full_audio.wav -t {max_intro_time} -c copy ./segments_diar/intro.wav'
    ffmpeg_cut_midle = f'ffmpeg -ss {max_intro_time} -i ./models/full_audio.wav -t {max_midle_time - max_intro_time} -c copy ./segments_diar/midle.wav'
    ffmpeg_cut_end = f'ffmpeg -ss {max_midle_time} -i ./models/full_audio.wav -t {end_of_lesson_sec} -c copy ./segments_diar/end.wav'
   
    subprocess.call(ffmpeg_cut_intro, shell=True)
    subprocess.call(ffmpeg_cut_midle, shell=True)
    subprocess.call(ffmpeg_cut_end, shell=True)
    
    