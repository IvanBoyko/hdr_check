# This script checks multiple YouTube video IDs for HDR processing status every 30 minutes.
# 
# 1. Install dependencies:
#   python3 -m pip install yt-dlp --break-system-packages
#   python3 -m pip install yt-dlp-ejs --break-system-packages
#   brew install deno
# 2. Add your IDs: Paste the Video IDs into the VIDEO_IDS list.
# 3. Run it in the background: python3 check_hdr.py &
# 

import yt_dlp
import time
import os

# Configuration
VIDEO_IDS = ["eSsmKQaOiBA", "b_FudzkB-qs", "R60bdY3gy2s", "5-7-pgHwx8I", "5pxCl9kFS2c", "O4El_cwuZeo", "XESuvDl5EXQ"]  # Put your multiple version IDs here
CHECK_INTERVAL = 1800  # Check every 30 minutes (1800 seconds)

def notify_mac(title, text):
    os.system(f"""osascript -e 'display notification "{text}" with title "{title}"'""")

def is_hdr_processed(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        'quiet': True,
        'noplaylist': True,
        'remote_components': ['ejs:github'],
        'js_runtimes': {'deno': {}},
    }

    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            
            # Check for the specific 10-bit HDR codec signatures
            # vp09.02 = VP9 Profile 2 (HDR)
            # av01...10 = AV1 10-bit (HDR)
            for f in formats:
                vcodec = f.get('vcodec', '')
                note = f.get('format_note', '').lower()
                
                if 'hdr' in note or vcodec.startswith('vp09.02') or (vcodec.startswith('av01') and '.10' in vcodec):
                    return True
            return False
        except Exception as e:
            print(f"Error checking {video_id}: {e}")
            return False

print("Starting HDR Monitoring Service...")
active_checks = list(VIDEO_IDS)

while active_checks:
    for vid in list(active_checks):
        print(f"[{time.strftime('%H:%M:%S')}] Checking {vid}...")
        if is_hdr_processed(vid):
            msg = f"HDR is LIVE for video {vid}!"
            print(f"SUCCESS: {msg}")
            notify_mac("YouTube HDR Alert", msg)
            active_checks.remove(vid)
        else:
            print(f"Status: Still SDR.")
            
    if active_checks:
        time.sleep(CHECK_INTERVAL)

print("All videos processed. Service stopping.")
