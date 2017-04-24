#!/bin/bash
source ~/.bash_profile
cd ~/manage_chessella/
python chessella_script.py >> chessella_job.log 2>&1
