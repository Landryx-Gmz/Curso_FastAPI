from fastapi import FastAPI, BackgroundTasks
import time

app = FastAPI()

def write_notification(email: str, message=""):
    time.sleep(4)
    with open("log.txt", mode="w") as email_file:
        content = f"Notificacion para {email}: { message}"
        email_file.write(content)
    print("Termino la tarea!")

@app.post("/send-notification/{email}")
async def send_notification(email: str, background_task: BackgroundTasks):
    background_task.add_task(write_notification, email, message="Alguna notificacion")
    return {"message": "Tarea mandada al segundo plano"}