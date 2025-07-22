import pygame, os, mutagen
from mutagen.id3 import ID3, APIC
from PIL import Image, ImageTk
import customtkinter as ctk
import io

app = ctk.CTk()
app.geometry("250x350")

# Criando ordem de leitura das musicas
# Cria uma lista onde é adicionado tudo dentro de musica/ que termina com .mp3
lista_de_musica = [os.path.join("./musica/", f) for f in os.listdir("./musica/") if f.endswith(".mp3")] 
indice_musica_atual = 0 # contador começa na primeira musica
pygame.mixer.init()

# Criação dos frames
FrameSuperior = ctk.CTkFrame(app)
FrameSuperior.pack(fill='x', padx=10)

#Imagem da caoa da musica
label_capa = ctk.CTkLabel(FrameSuperior, text="", width=200, height=200)
label_capa.pack(pady=10)

# Label para mostrar nome musica
label_nomeMusica = ctk.CTkLabel(app, text="")
label_nomeMusica.pack(pady=10)

# Criação dos Botões
botoes_frame = ctk.CTkFrame(app)
botoes_frame.pack(pady=5, side="bottom")

botaoAnterior = ctk.CTkButton(botoes_frame, text="<<", command=lambda: TrocarMusica(-1), width=30)
botaoAnterior.pack(side="left", padx=5)

botaoPlay = ctk.CTkButton(botoes_frame, text="play", command=lambda: PlayMusica(), width=50, height=50, corner_radius=25, font=("Arial", 20))
botaoPlay.pack(padx=5, side="left")

botaoProximo = ctk.CTkButton(botoes_frame, text=">>", command=lambda: TrocarMusica(1), width=30)
botaoProximo.pack(side="left", padx=5)

def extrair_capa(musica_path):
    try:
        audio = ID3(musica_path)
        for tag in audio.values():
            if isinstance(tag, APIC):
                image_data = tag.data
                image = Image.open(io.BytesIO(image_data))
                return image
    except:
        return None
    return None

def atualizar_capa(musica_path):
    capa = extrair_capa(musica_path)
    if capa:
        # Redimensionar a imagem para caber no label
        capa = capa.resize((330, 300), Image.LANCZOS)
        photo = ctk.CTkImage(light_image=capa, size=(220, 170))
        label_capa.configure(image=photo)
        label_capa.image = photo  # Manter uma referência
    else:
        # Se não houver capa, exibir uma imagem padrão ou limpar
        label_capa.configure(image='')
        label_capa.image = None

def PlayMusica():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        botaoPlay.configure(text="Play")
    else:
        if not pygame.mixer.music.get_busy():
            carregar_musica()
        pygame.mixer.music.unpause()
        botaoPlay.configure(text="Pause")

def carregar_musica():
    if lista_de_musica:
        musica_path = lista_de_musica[indice_musica_atual]
        pygame.mixer.music.load(musica_path)
        pygame.mixer.music.play()
        nome_musica = os.path.basename(musica_path)
        label_nomeMusica.configure(text=nome_musica)
        botaoPlay.configure(text="Pause")
        atualizar_capa(musica_path)

def TrocarMusica(direcao):
    global indice_musica_atual

    if not lista_de_musica:
        return
    
    indice_musica_atual += direcao

    # verifica os limites da lista
    if indice_musica_atual >= len(lista_de_musica):
        indice_musica_atual = 0
    elif indice_musica_atual < 0:
        indice_musica_atual = len(lista_de_musica) - 1
    
    carregar_musica()

app.mainloop()
