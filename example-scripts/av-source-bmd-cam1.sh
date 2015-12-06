#!/bin/sh
ffmpeg -y \
	-f decklink \
	-i 'DeckLink Mini Recorder (1)@10' \
	-c:v rawvideo -c:a pcm_s16le \
	-pix_fmt uyvy422 \
	-f matroska \
	tcp://localhost:10000
