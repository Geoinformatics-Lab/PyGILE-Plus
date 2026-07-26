#!/bin/bash
# Start virtual framebuffer in the background on display :99
Xvfb :99 -screen 0 1024x768x24 &

# Execute the container command (e.g., Jupyter, Bash, Python)
exec "$@"
