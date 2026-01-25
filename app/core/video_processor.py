import asyncio
import os
import re
import subprocess
from typing import Dict, Any

async def get_video_info(file_path: str) -> Dict[str, Any]:
    try:
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        process = await asyncio.create_subprocess_exec(
            "ffmpeg", "-i", file_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            startupinfo=startupinfo
        )
        _, stderr = await process.communicate()
        output = stderr.decode('utf8', errors='ignore')

        duration_match = re.search(r"Duration: (\d{2}):(\d{2}):(\d{2}\.\d{2})", output)
        duration = 0.0
        if duration_match:
            h, m, s = duration_match.groups()
            duration = float(h) * 3600 + float(m) * 60 + float(s)

        res_match = re.search(r"Video:.*?, (\d{3,5})x(\d{3,5})", output)
        width, height = 0, 0
        if res_match:
            width, height = map(int, res_match.groups())

        if duration == 0 and width == 0:
            return {"error": "Video bilgileri okunamadı. Lütfen geçerli bir video dosyası seçin."}

        return {
            "width": width,
            "height": height,
            "duration": duration,
            "size": os.path.getsize(file_path)
        }
    except FileNotFoundError:
        return {"error": "FFmpeg sistemde bulunamadı. Lütfen yüklü olduğundan emin olun."}
    except Exception as e:
        return {"error": f"Hata: {str(e)}"}

async def compress_video(
    input_path: str, 
    output_path: str, 
    crf: int = 23, 
    resolution: str = None,
    progress_callback = None
) -> Dict[str, Any]:
    try:
        cmd = ["ffmpeg", "-i", input_path]
        
        filters = []
        if resolution:
            filters.append(f"scale={resolution}")
        
        if filters:
            cmd.extend(["-vf", ",".join(filters)])
            
        cmd.extend([
            "-vcodec", "libx264",
            "-crf", str(crf),
            "-preset", "slow",
            "-c:a", "aac",
            "-b:a", "48k",
            "-strict", "-2",
            "-y",
            output_path
        ])
        
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            startupinfo=startupinfo
        )
        
        total_duration = 0
        stderr_lines = []
        
        while True:
            line = await process.stderr.readline()
            if not line:
                break
            
            line_str = line.decode('utf8', errors='ignore')
            stderr_lines.append(line_str)
            
            if "Duration" in line_str and total_duration == 0:
                duration_match = re.search(r"Duration: (\d{2}):(\d{2}):(\d{2}\.\d{2})", line_str)
                if duration_match:
                    h, m, s = duration_match.groups()
                    total_duration = float(h) * 3600 + float(m) * 60 + float(s)
            
            if "time=" in line_str and total_duration > 0 and progress_callback:
                time_match = re.search(r"time=(\d{2}):(\d{2}):(\d{2}\.\d{2})", line_str)
                if time_match:
                    h, m, s = time_match.groups()
                    current_time = float(h) * 3600 + float(m) * 60 + float(s)
                    percentage = (current_time / total_duration)
                    progress_callback(percentage)

        await process.wait()
        
        if process.returncode == 0 and os.path.exists(output_path):
            new_size = os.path.getsize(output_path)
            return {"status": "success", "output_path": output_path, "new_size": new_size}
        else:
            error_msg = "".join(stderr_lines[-20:])
            return {"status": "error", "message": f"FFmpeg Hatası:\n{error_msg}"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

async def trim_video(
    input_path: str, 
    output_path: str, 
    start_time: float, 
    end_time: float,
    progress_callback = None
) -> Dict[str, Any]:
    try:
        cmd = [
            "ffmpeg",
            "-ss", str(start_time),
            "-i", input_path,
            "-to", str(end_time),
            "-c", "copy",
            "-y",
            output_path
        ]
        
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            startupinfo=startupinfo
        )
        
        total_duration = end_time - start_time
        
        while True:
            line = await process.stderr.readline()
            if not line:
                break
            
            line_str = line.decode('utf8', errors='ignore')
            
            if "time=" in line_str and total_duration > 0 and progress_callback:
                time_match = re.search(r"time=(\d{2}):(\d{2}):(\d{2}\.\d{2})", line_str)
                if time_match:
                    h, m, s = time_match.groups()
                    current_time_val = float(h) * 3600 + float(m) * 60 + float(s)
                    percentage = (current_time_val / total_duration)
                    progress_callback(percentage)

        await process.wait()
        
        if process.returncode == 0 and os.path.exists(output_path):
            return {"status": "success", "output_path": output_path}
        else:
             return {"status": "error", "message": "Kesme işlemi başarısız."}

    except Exception as e:
        return {"status": "error", "message": str(e)}
