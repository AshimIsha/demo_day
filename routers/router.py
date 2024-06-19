# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 14:59:03 2024

@author: M
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse
import shutil
from models import converter 
import subprocess
import gradio as gr

user_router = APIRouter()

@user_router.get('/login')
async def upload_form():
    
    
    return 

@user_router.get('/auth')
async def process_video(request: Request):
    

    
    return RedirectResponse(url='/gradio')






