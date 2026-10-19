import asyncio
from pathlib import Path
from datetime import datetime
from plyer import camera
import os

async def record_webcam(duration=10):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # Enregistrement dans le dossier interne de l'application
        final_file = os.path.join(os.getcwd(), f"record_{timestamp}.mp4")
        
        camera.take_video(filename=final_file)
        await asyncio.sleep(duration)
        
        if Path(final_file).exists():
            return final_file
        return "error: file not found"
    except Exception as e:
        return f"error:{e}"

