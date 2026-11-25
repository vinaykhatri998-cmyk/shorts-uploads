#!/usr/bin/env bash
# One-time setup on a fresh Ubuntu cloud container (about 5 minutes).
set -e
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq --no-install-recommends blender xvfb ffmpeg >/dev/null
python3 -m venv /opt/shorts-venv
/opt/shorts-venv/bin/pip install -q pillow kokoro-onnx soundfile numpy
mkdir -p /opt/kokoro
cd /opt/kokoro
[ -f kokoro-v1.0.onnx ] || curl -sSL -o kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
[ -f voices-v1.0.bin ] || curl -sSL -o voices-v1.0.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
echo "setup ok"
