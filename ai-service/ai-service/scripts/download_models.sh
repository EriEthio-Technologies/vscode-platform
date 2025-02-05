#!/bin/bash
# ai-service/scripts/download_models.sh

# Install Git LFS
git lfs install

# Download DeepSeek model
git clone https://huggingface.co/deepseek-ai/deepseek-coder-33b-instruct /app/models/deepseek

# Download Qwen model
git clone https://huggingface.co/Qwen/Qwen1.5-72B-Chat /app/models/qwen

# Download Kimi model
git clone https://huggingface.co/SUDA-Research/Kimi-Chat-8x22B /app/models/kimi
