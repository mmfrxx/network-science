#!/bin/sh
pip install -r requirements.txt
python3 generate_LFR.py
python3 main.py
python3 draw_graphics.py