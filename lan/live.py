import asyncio, os, time, datetime
from pathlib import Path
import subprocess

async def record_screen_with_audio(duree=10):
    base = datetime.datetime.now().strftime('%H-%M-%S')
    # Utilisation du répertoire courant de l'app pour éviter les erreurs de permission Android 10+
    final = os.path.join(os.getcwd(), f"screen_{base}.mp4")
    
    try:
        cmd = ["screenrecord", "--time-limit", str(duree), final]
        await asyncio.to_thread(subprocess.run, cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        if Path(final).exists():
            return final
    except Exception as e:
        pass
    return ""

def screen_shoot():
    date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nom = f"screen_{date}.png"
    # Stockage dans le dossier privé de l'application (pas de blocage Scoped Storage)
    chemin = os.path.join(os.getcwd(), nom)
    
    try:
        subprocess.run(["screencap", "-p", chemin], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if os.path.exists(chemin):
            return chemin
    except:
        pass
    return None

