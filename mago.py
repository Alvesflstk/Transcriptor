from customtkinter import *
import tkinter as tk
import PIL.Image
import requests
import time
import shutil
import os

base_url = "https://api.assemblyai.com/v2"
mychaveApi = 'f3b9760bcd8b4cb48ca164bc47ff7961'

global content

def sendArchive(path,label_config):
    headers = {"authorization": f"{mychaveApi}"}

    # criando endpoint de upload

    with open(f"{path}", "rb") as f:
        response = requests.post(base_url + "/upload",
                            headers=headers,
                            data=f)

    upload_url = response.json()["upload_url"]


    data = {
        "audio_url": upload_url ,
        "language_code": "pt",
        
    }
    
    # criando endpoint de transcricao
    url = base_url + "/transcript"
    response = requests.post(url, json=data, headers=headers)
    
    # obtendo resposta >>>>> 
    transcript_id = response.json()['id']
    polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

    
    # se o audio for maior que 60 min ele espera até acabar e busca por id 
    while True:
        transcription_result = requests.get(polling_endpoint, headers=headers).json()

        if transcription_result['status'] == 'completed':
            print(transcription_result['text'])
            label_config.configure(text='')
            label_config.configure(text=transcription_result['text'])
            break

        elif transcription_result['status'] == 'error':
            raise RuntimeError(f"Transcription failed: {transcription_result['error']}")

        else:
            time.sleep(3)

    

class mago:
    def __init__(self):
        self.path = None
        self.mago = CTk()
        self.mago.geometry("500x600")
        self.mago.title("Mago")
        self.mago.resizable(False, False)
        self.container = tk.Frame(self.mago,bg='#2B2B2B')
        self.container.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self. imagens = self.conjurar_imagens()
        self.body()
        self.prompt()
        self.mago.mainloop()

    def selecionar_arquivo(self):
        
        arquivo_path = filedialog.askopenfilename()
        if arquivo_path:
            
            nome_arquivo = os.path.basename(arquivo_path)
            print(f"Arquivo selecionado: {nome_arquivo}")
            
            
            pasta_destino = "./audios"
            if not os.path.exists(pasta_destino):
                os.makedirs(pasta_destino)
            
            
            novo_path = os.path.join(pasta_destino, nome_arquivo).replace("\\", "/")
            
            shutil.copy(arquivo_path, novo_path)
            sendArchive(novo_path,self.text_trancript)
            print(f"Arquivo salvo em: {novo_path}")
            
    def transcrever_audio(self):
        
        self.container_response = CTkScrollableFrame(self.container, width=250, height=250)

        self.text_trancript = CTkLabel(self.container_response,text='',wraplength=230)
        self.container_response.place(x=200,y=50)
        self.text_trancript.pack()
    

    def conjurar_imagens(self):
        self.list_images = [CTkImage(light_image=PIL.Image.open("./images/Província I.png"),size=(226,341), dark_image=PIL.Image.open("./images/Província I.png"))]

        return self.list_images
    def prompt(self):
        self.transcrever_audio()
        self.prompt = CTkFrame(self.container, width=340, height=46)
        self.labelArquivo = CTkLabel(self.prompt, text="arquivo conjurado:",font=("Roboto Medium", 12))
        self.buttonConjurar = CTkButton(self.container, text="Conjurar",bg_color='#00afb9',height=46,width=100,command=self.selecionar_arquivo)


        self.prompt.place(x=10,y=530)
        self.buttonConjurar.place(x=370,y=530)
        self.labelArquivo.place(x=10,y=10)

    def body(self):
        self.bodyMago = CTkLabel(self.container, text="",image=self.imagens[0])
        self.ballonMago = CTkFrame(self.container,width=250,height=46)
        self.ballonMagoText = CTkLabel(self.ballonMago,text='Eu transcreverei o que voce me mandar')

        self.bodyMago.place(x=10,y=10)
        self.ballonMago.place(x=200,y=60)
        self.ballonMagoText.place(x=10,y=10)
        
        

if __name__ == "__main__":
    mago = mago()
