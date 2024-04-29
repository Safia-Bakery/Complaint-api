#!/bin/bash
# Start FastAPI in the background
uvicorn main:app --host 0.0.0.0 --port 8000 &

# Start the bot script
python bot/Complaintbot/complaint_bot.py &

python bot/Hrbot/hr_bot.py 

