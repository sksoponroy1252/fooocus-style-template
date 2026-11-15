@echo off
if not exist .venv (
  py -m venv .venv
)
call .venv\Scripts\activate
python app.py
