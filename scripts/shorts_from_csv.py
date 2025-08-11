#!/usr/bin/env python3
# Generates simple vertical shorts (1080x1920) from topics.csv using ffmpeg + espeak (no external APIs)
import os, csv, argparse, subprocess, random

ROOT = os.path.dirname(os.path.dirname(__file__))
DATA = os.path.join(ROOT, "data", "topics.csv")
OUT_DIR = os.path.join(ROOT, "output", "shorts")
os.makedirs(OUT_DIR, exist_ok=True)

def tts(text, wav_path):
    cmd = ["espeak", "-v", "fr", "-s", "150", text, "-w", wav_path]
    subprocess.check_call(cmd)

def make_video(title, tips, out_path):
    caption = "\\n\\n".join([title, "Astuce: " + tips[0], "Rappel: " + tips[1]]).replace(":", "\\:")
    audio = os.path.join(OUT_DIR, "tmp.wav")
    tts(" ".join([title, tips[0], tips[1]]), audio)
    filter_text = f"drawtext=text='{caption}':x=(w-text_w)/2:y=(h-text_h)/2:fontsize=48:fontcolor=white:box=1:boxcolor=black@0.5:boxborderw=24"
    cmd = [
        "ffmpeg","-y",
        "-f","lavfi","-i","color=size=1080x1920:duration=8:rate=30:color=#111111",
        "-i", audio,
        "-shortest",
        "-vf", filter_text,
        "-c:v","libx264","-pix_fmt","yuv420p","-c:a","aac","-b:a","128k",
        out_path
    ]
    subprocess.check_call(cmd)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=1)
    args = ap.parse_args()
    rows = list(csv.DictReader(open(DATA, "r", encoding="utf-8")))
    random.shuffle(rows)
    made = 0
    for r in rows[:args.count]:
        title = r["title"]
        tips = [
            "commence léger, progresse chaque semaine",
            "privilégie la technique avant la charge"
        ]
        out = os.path.join(OUT_DIR, r['slug'] + ".mp4")
        make_video(title, tips, out)
        made += 1
    print(f"Generated {made} short(s) in {OUT_DIR}")

if __name__ == "__main__":
    main()
