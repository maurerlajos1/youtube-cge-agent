import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# Ensure CUDA DLLs from torch/lib are discoverable on Windows
torch_lib = r"H:\TTS\venv\Lib\site-packages\torch\lib"
if os.path.exists(torch_lib):
    os.add_dll_directory(torch_lib)
    os.environ['PATH'] = torch_lib + os.pathsep + os.environ.get('PATH', '')

os.environ['HF_HOME'] = 'H:/hf_cache'
os.environ['TORCH_HOME'] = 'H:/torch_cache'
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'

import time
import json
from datetime import timedelta
import soundfile as sf
import numpy as np
from faster_whisper import WhisperModel

DOWNLOAD_ROOT = 'H:/hf_cache/whisper'
AUDIO_PATH = 'H:/Youtube agent/audio_16k.wav'
OUTPUT_DIR = 'H:/Youtube agent'

def format_timestamp(seconds: float, srt_format: bool = False) -> str:
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    millis = int((seconds - int(seconds)) * 1000)
    if srt_format:
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    else:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

def main():
    print("=" * 60)
    print("STARTING WHISPER TRANSCRIPTION ON NVIDIA RTX 3090")
    print("=" * 60)
    print(f"Audio file: {AUDIO_PATH}")
    if not os.path.exists(AUDIO_PATH):
        print(f"Error: Audio file not found at {AUDIO_PATH}")
        sys.exit(1)

    t0 = time.time()
    print("Loading audio into memory using soundfile...")
    audio, sr = sf.read(AUDIO_PATH, dtype='float32')
    duration_sec = len(audio) / sr
    print(f"Loaded {len(audio):,} samples ({duration_sec:.1f}s / {format_timestamp(duration_sec)}) at {sr}Hz in {time.time()-t0:.2f}s")

    print(f"Loading faster-whisper large-v3-turbo (FP16 on CUDA)...")
    t_model = time.time()
    model = WhisperModel(
        'large-v3-turbo',
        device='cuda',
        device_index=0,
        compute_type='float16',
        download_root=DOWNLOAD_ROOT
    )
    print(f"Model ready in {time.time() - t_model:.2f}s")

    print(f"Starting transcription (English, beam_size=5, VAD filter enabled)...")
    t_transcribe = time.time()

    segments, info = model.transcribe(
        audio,
        language='en',
        beam_size=5,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500)
    )

    collected_segments = []
    plain_text_lines = []
    timestamped_lines = []
    srt_lines = []

    last_log_time = time.time()
    srt_idx = 1

    for segment in segments:
        seg_data = {
            "id": segment.id,
            "seek": segment.seek,
            "start": round(segment.start, 2),
            "end": round(segment.end, 2),
            "text": segment.text.strip()
        }
        collected_segments.append(seg_data)

        start_str = format_timestamp(segment.start)
        end_str = format_timestamp(segment.end)
        srt_start = format_timestamp(segment.start, srt_format=True)
        srt_end = format_timestamp(segment.end, srt_format=True)

        plain_text_lines.append(segment.text.strip())
        timestamped_lines.append(f"[{start_str} -> {end_str}] {segment.text.strip()}")
        srt_lines.append(f"{srt_idx}\n{srt_start} --> {srt_end}\n{segment.text.strip()}\n")
        srt_idx += 1

        now = time.time()
        if now - last_log_time >= 15:
            pct = (segment.end / duration_sec) * 100
            elapsed = now - t_transcribe
            speed = segment.end / max(elapsed, 0.001)
            eta = (duration_sec - segment.end) / max(speed, 0.001)
            print(f"[{format_timestamp(segment.end)} / {format_timestamp(duration_sec)}] "
                  f"{pct:5.1f}% complete | Speed: {speed:.1f}x real-time | Elapsed: {elapsed/60:.1f}m | ETA: {eta/60:.1f}m")
            last_log_time = now

    total_time = time.time() - t_transcribe
    print("=" * 60)
    print(f"[SUCCESS] TRANSCRIPTION FINISHED in {total_time/60:.2f} minutes ({total_time:.1f} seconds)!")
    print(f"Speed: {duration_sec / total_time:.1f}x real-time | Segments: {len(collected_segments):,}")
    print("=" * 60)

    # 1. Plain text
    txt_path = os.path.join(OUTPUT_DIR, "transcript.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(plain_text_lines))
    print(f"Saved: {txt_path}")

    # 2. Timestamped lines
    ts_path = os.path.join(OUTPUT_DIR, "transcript_timestamped.txt")
    with open(ts_path, "w", encoding="utf-8") as f:
        f.write("\n".join(timestamped_lines))
    print(f"Saved: {ts_path}")

    # 3. SubRip Subtitles (SRT)
    srt_path = os.path.join(OUTPUT_DIR, "transcript.srt")
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_lines))
    print(f"Saved: {srt_path}")

    # 4. JSON
    json_path = os.path.join(OUTPUT_DIR, "transcript.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "language": "en",
            "duration": duration_sec,
            "duration_formatted": format_timestamp(duration_sec),
            "total_segments": len(collected_segments),
            "total_words": sum(len(s['text'].split()) for s in collected_segments),
            "processing_time_seconds": round(total_time, 1),
            "segments": collected_segments
        }, f, indent=2, ensure_ascii=False)
    print(f"Saved: {json_path}")

    print("All transcript files successfully written!")

if __name__ == "__main__":
    main()
