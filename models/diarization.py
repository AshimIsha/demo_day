# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 01:15:16 2024

@author: M
"""

import argparse
import torch
from pyannote.audio import Pipeline
from rnnt import format_time

def get_speakers(s_0, s_1, part):
    
    overall = s_0 + s_1
    
    s_0_percent = s_0 / overall * 100
    s_1_percent = s_1 / overall * 100
    
    with open(f'../gradio_ui/{part}.txt', 'w') as f:
        print('Writing file trancsript...')
        f.write('\n'.join(s_0_percent))
        f.write('\n'.join(s_1_percent))
        print('File write_successfully')
    
     

def diarize(name, pipeline):
    count_speaker_1 = 0
    count_speaker_0 = 0
    
    print('pipeline')
    diarization = pipeline(f"../segments_diar/{name}.wav", num_speakers=2, 
                               min_speakers = 1, max_speakers = 2)
    print(f'end_pipeline for {name}')    
# print the result
        
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        if speaker == 'SPEAKER_00':
            count_speaker_0 += 1
        else:
            count_speaker_1 += 1
            
        print(f"start={format_time(turn.start)}s stop={format_time(turn.end)}s speaker_{speaker}")
    
            
    return count_speaker_0, count_speaker_1
    

def main(device, hf_token):
    pipeline = Pipeline.from_pretrained(
      "pyannote/speaker-diarization-3.1",
      use_auth_token=hf_token)
    
    pipeline = pipeline.to(torch.device(device))
    
    print('start_diar')

    intro_s_0, intro_s_1 = diarize('intro', pipeline)
    mid_s_0, mid_s_1 = diarize('midle', pipeline)
    end_s_0, end_s_1 = diarize('end', pipeline)
    
    get_speakers(intro_s_0, intro_s_1, 'intro')
    get_speakers(mid_s_0, mid_s_1, 'midle')
    get_speakers(end_s_0, end_s_1, 'end')
    
    
def _parse_args():
    parser = argparse.ArgumentParser(
        description="pyannotate-diarization checkpoint"
    )
    
    parser.add_argument(
        "--hf_token", help="HuggingFace token for using pyannote Pipeline"
    )
    
    parser.add_argument("--device", help="Device: cpu / cuda")
    
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()

    main(
        
        device = args.device,
        hf_token = args.hf_token,
    )









