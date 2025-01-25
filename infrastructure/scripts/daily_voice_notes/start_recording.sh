#!/usr/bin/env bash

# Where to store recordings
YEAR=$(date +%Y)
MONTH=$(date +%m)
DAY=$(date +%d)
RECORDINGS_DIR="/Users/keith/VoiceMemos/$YEAR/$MONTH/$DAY"
PID_DIR="/Users/keith/VoiceMemos"
mkdir -p "$RECORDINGS_DIR"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
FILENAME="daily_note_${TIMESTAMP}.wav"
OUTPUT_FILE="$RECORDINGS_DIR/$FILENAME"

# Adjust the input parameters as needed
# Example for macOS:
# DEVICE=":0"
# Example for Linux:
# DEVICE="default"
# Example for Windows (replace with actual device name):
# DEVICE="audio=Microphone (Your Device Name)"

# For demonstration, let's assume Linux with PulseAudio default:
DEVICE=":1"

/opt/homebrew/bin/ffmpeg -y -f avfoundation -i "$DEVICE" -ac 1 -ar 44100 "$OUTPUT_FILE" > /dev/null 2>&1 &
# output to log file for debugging
# /opt/homebrew/bin/ffmpeg -y -f avfoundation -i "$DEVICE" -ac 1 -ar 44100 "$OUTPUT_FILE" > /Users/keith/VoiceMemos/ffmpeg.log 2>&1 &

FFMPEG_PID=$!

#echo $FFMPEG_PID > "$PID_DIR/ffmpeg_pid"
# Sample PID file:
# 1234
# /path/to/recording.wav
echo "$FFMPEG_PID" > "$PID_DIR/ffmpeg_pid"
echo "$OUTPUT_FILE" >> "$PID_DIR/ffmpeg_pid"
echo "Recording started: $OUTPUT_FILE"