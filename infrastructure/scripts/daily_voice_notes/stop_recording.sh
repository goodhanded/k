#!/usr/bin/env bash

PID_DIR="/Users/keith/VoiceMemos"
PID_FILE="$PID_DIR/ffmpeg_pid"
LOG_FILE="$PID_DIR/stop_recording.log"

# Sample PID file:
# 1234
# /path/to/recording.wav

if [ -f "$PID_FILE" ]; then
  # FFMPEG_PID=$(cat "$PID_FILE")
  RECORDING_PATH=$(tail -n 1 "$PID_FILE")
  echo "Recording path: $RECORDING_PATH" >> "$LOG_FILE"
  FFMPEG_PID=$(head -n 1 "$PID_FILE")
  kill "$FFMPEG_PID"
  rm "$PID_FILE"
  echo "Recording stopped." >> "$LOG_FILE"
else
  echo "No recording PID file found. Is ffmpeg running?" >> "$LOG_FILE"
fi

# Change working directory to k
cd /Users/keith/Projects/k || exit

# Run the Python script to transcribe and assimilate the voice memo
/Users/keith/Projects/k/.env/bin/python /Users/keith/Projects/k/k.py assimilate "$RECORDING_PATH" >> "$LOG_FILE" 2>&1
