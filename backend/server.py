from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json
import os
from backend.utils import write_md_to_pdf, write_md_to_word
from preprocessing.frame_extractor import VideoKeyFrameExtractor
from preprocessing.transcribe_audio import transcribe_audio
from key_frames.model import mainGPT
from backend.websocket_manager import WebSocketManager
import base64
from dotenv import load_dotenv
load_dotenv()


class ResearchRequest(BaseModel):
    task: str
    report_type: str
    agent: str


app = FastAPI()

app.mount("/site", StaticFiles(directory="./frontend"), name="site")
app.mount("/static", StaticFiles(directory="./frontend/static"), name="static")

templates = Jinja2Templates(directory="./frontend")

manager = WebSocketManager()


@app.on_event("startup")
def startup_event():
    if not os.path.isdir("inputs"):
        os.makedirs("inputs")
    app.mount("/inputs", StaticFiles(directory="inputs"), name="inputs")
    if not os.path.isdir("outputs"):
        os.makedirs("outputs")
    app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")
    if not os.path.isdir("uploads"):
        os.makedirs("uploads")
    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse('index.html', {"request": request, "report": None})


async def generate_chat(filename: str, upload: str, websocket: WebSocket):

    await websocket.send_json({"type": "logs", "output": "Generating keyframes..."})
    extractor = VideoKeyFrameExtractor(
        f'uploads/{filename}', f"inputs/{upload}/frames")
    extractor.process_video()
    await websocket.send_json({"type": "logs", "output": "Keyframes generated!"})

    await websocket.send_json({"type": "logs", "output": "Transcribing audio..."})
    with open(f"inputs/{upload}/transcript.txt", "w") as f:
        f.write(transcribe_audio(f'uploads/{filename}'))
    await websocket.send_json({"type": "logs", "output": "Audio transcribed!"})

    chat = mainGPT(f"inputs/{upload}",
                   "Please provide a summary of the video content.", os.environ["OPENAI_API_KEY"])
    print(chat)
    await websocket.send_json({"type": "logs", "output": "Report ready!"})
    await websocket.send_json({"type": "report", "output": chat['message'] if 'message' in chat else chat})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data.startswith("start"):
                json_data = json.loads(data[6:])
                input = base64.b64decode(json_data.get("input"))
                filename = json_data.get("name")
                upload = filename.split(".")[0]
                if input and filename:
                    if not os.path.isdir(f"inputs/{upload}"):
                        os.makedirs(f"inputs/{upload}")
                        os.makedirs(f"inputs/{upload}/frames")
                    with open(f"uploads/{filename}", "wb") as video_file:
                        video_file.write(input)
                    await generate_chat(filename, upload, websocket)
                # print(input)
                # if task and report_type:
                #     report = await manager.start_streaming(task, report_type, websocket)
                #     # Saving report as pdf
                #     # pdf_path = await write_md_to_pdf(report)
                #     # Saving report as docx
                #     docx_path = await write_md_to_word(report)
                #     # Returning the path of saved report files
                #     await websocket.send_json({"type": "path", "output": {"pdf": '', "docx": docx_path}})
                # else:
                #     print("Error: not enough parameters provided.")

    except WebSocketDisconnect:
        await manager.disconnect(websocket)
