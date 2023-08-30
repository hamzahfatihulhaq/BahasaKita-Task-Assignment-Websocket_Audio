from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi import UploadFile, File
from bson import ObjectId
from config.db import db
from schemas.audio_schema import get_audio_metadata
from models.audio_model import Audio
import os
from bson.errors import InvalidId

router = APIRouter()

@router.websocket("/ws")
async def audio_websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:       
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: '{data}'")
    except WebSocketDisconnect:
        await websocket.close(code=1000)  # Menutup WebSocket dengan kode penutup 1000
        print("WebSocket connection closed")


@router.post("/upload/")
async def upload_audio(audio_data: UploadFile = File(...)):
    audio_collection = db.db["audio"]
    
    # Simpan file sementara
    file_path = os.path.join("uploads", audio_data.filename)
    with open(file_path, "wb") as f:
        f.write(audio_data.file.read())

    # Baca metadata dari file audio
    metadata = get_audio_metadata(file_path)
    os.remove(file_path)  # Hapus file sementara

    # # Simpan metadata audio ke MongoDB
    audio_metadata = Audio(
        name= metadata["name"], 
        size= metadata["size"], 
        sample_rate= metadata["sample_rate"],
        bit_depth= metadata["bit_depth"],
        duration= metadata["duration"],
        file_type= metadata["file_type"]
        )
    result = audio_collection.insert_one(audio_metadata.to_dict())

    # # Simpan audio ke file di folder "Audiodb"
    audio_id = str(result.inserted_id)
    audio_file_path = os.path.join("Audiodb", str(audio_id) + metadata["file_type"])
    
    # # Menulis data bytes ke file
    with open(audio_file_path, "wb") as file:
        while True:
            audio_chunk = audio_data.file.read(320)  # Baca 320 bit
            if not audio_chunk:
                break
            file.write(audio_chunk)

    return {"message": f"Audio uploaded successfully '{audio_id}'"}



@router.get("/get_audio/{audio_id}/")
async def get_audio(audio_id: str):
    try:
        audio_collection = db.db["audio"]

        audio = audio_collection.find_one({"_id": ObjectId(audio_id)})
        
        serialized_dict = {}
        
        if audio:
            # Memproses kunci '_id'
            if '_id' in audio:
                serialized_dict['_id'] = str(audio['_id'])
            
            # Memproses kunci selain '_id'
            for i in audio:
                if i != '_id':
                    serialized_dict[i] = audio[i]
            
            return {"message": serialized_dict}

        return {"message": "Audio not found"}
    except InvalidId:
        return {"error": "Invalid audio ID format"}
