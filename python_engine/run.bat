@echo off
set SDL_VIDEODRIVER=dummy
set SDL_AUDIODRIVER=null
set PYGAME_HIDE_SUPPORT_PROMPT=1
set DYAD_DISABLE_DASH=1
py -3.11 python_engine/dyad_field_v7.py pause