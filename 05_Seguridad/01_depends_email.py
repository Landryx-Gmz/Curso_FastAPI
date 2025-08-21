from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated

app = FastAPI()

class EmailService:
    def send_email(self, recipinet:str, message:str):
        print(f"Sendig email to {recipinet}: {message}")

def get_email_service():
    return EmailService()

email_service_dependency = Annotated[EmailService, Depends(get_email_service)]