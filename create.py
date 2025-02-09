import customtkinter as ctk
import qrcode
from services import cadastrar_pet, pegar_dados
from PIL import Image


class Create(ctk.CTkToplevel):
    def __init__(self, id_usuario_logado, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id_usuario_logado = id_usuario_logado
        self.config_tela_create()  # carrega as config da tela registro
        self.widgets_create()  # carrega os widgtes da tela registro

    def config_tela_create(self):
        self.geometry("600x400")  # dimensoes x y da tela
        self.title("Registro")  # titulo que aparece na tela
        self.resizable(False, False)  # nao permite usuario ajustar tela

    def widgets_create(self):
        # ====================================criação de widgets========================================================
        # frames
        tela_frame = ctk.CTkScrollableFrame(self, width=400, height=350, corner_radius=10)
        tela_frame.pack(padx=20, pady=20)
        tela_frame.grid_columnconfigure((0, 1), weight=1)

        # labels
        pet_label = ctk.CTkLabel(tela_frame, text="DADOS DO PET", font=("Roboto", 18), width=300, height=30)
        self.imagem_label = ctk.CTkLabel(tela_frame, text="", width=200, height=200)  # para o qrcode
        self.erro_label = ctk.CTkLabel(tela_frame, text="", font=("Roboto", 12), width=300, height=30)

        # entrys
        self.nome_entry = ctk.CTkEntry(tela_frame, placeholder_text="Nome", font=("Roboto", 14), width=300, height=30)
        self.raca_entry = ctk.CTkEntry(tela_frame, placeholder_text="Raça", font=("Roboto", 14), width=300, height=30)
        self.obs_entry = ctk.CTkEntry(tela_frame, placeholder_text="Observações", font=("Roboto", 14),
                                      width=300, height=30)

        # optionmenu
        sexo_var = ctk.StringVar(value="Sexo")
        self.sexo_optionmenu = ctk.CTkOptionMenu(tela_frame, values=["M", "F"], variable=sexo_var, font=("Roboto", 14),
                                                 width=300, height=30)

        # buttons
        voltar_button = ctk.CTkButton(tela_frame, text="Voltar", command=self.voltartela, font=("Roboto", 14),
                                      width=150, height=30)

        salvar_button = ctk.CTkButton(tela_frame, text="Salvar", command=self.salvar, font=("Roboto", 14),
                                      fg_color="green", width=150, height=30)

        # ==============================================================================================================
        # ===================================definindo lugares dos widgets==============================================
        pet_label.grid(row=0, column=0, pady=20, columnspan=3)
        self.nome_entry.grid(row=1, column=0, pady=10, columnspan=3)
        self.raca_entry.grid(row=2, column=0, pady=10, columnspan=3)
        self.sexo_optionmenu.grid(row=3, column=0, pady=10, columnspan=3)
        self.obs_entry.grid(row=4, column=0, pady=10, columnspan=3)
        voltar_button.grid(row=5, column=0, pady=20, sticky="w", columnspan=3)
        salvar_button.grid(row=5, column=2, pady=20, sticky="w", columnspan=3)
        self.erro_label.grid(row=6, column=0, pady=10, columnspan=3)
        self.imagem_label.grid(row=7, column=0, pady=20, columnspan=3)

    def salvar(self):
        # pegar dados dos campos
        self.nome_pet = self.nome_entry.get()
        self.raca = self.raca_entry.get()
        self.sexo = self.sexo_optionmenu.get()
        self.obs = self.obs_entry.get()

        # verifica se todos os campos estão ocupados
        if not all([self.nome_pet, self.raca, self.sexo, self.obs]):
            self.erro_label.configure(text="Preencha todos os campos")
            return

        # cadastrar usuario no banco de dados pets e observações,
        if cadastrar_pet(self.nome_pet, self.raca, self.sexo, self.obs, self.id_usuario_logado):
            # chama a funcao de gerar qrcode
            self.criar_qrcode()

            # coloca a imagem do qrcode no campo image_label
            img1 = ctk.CTkImage(light_image=Image.open("./" + self.qr_nome),
                                dark_image=Image.open("./" + self.qr_nome),
                                size=(200, 200))
            self.imagem_label.configure(image=img1)
            self.imagem_label = img1

            # limpa o nome do pet para evitar dualidade de dados
            self.nome_entry.delete(0, "end")  # limpa o nome do pet

            # limpa o label de erro se houver
            self.erro_label.configure(text="")
        else:
            print("Erro ao cadastrar pet")

    def criar_qrcode(self):
        # pega o nome e celular do responsavel do pet
        nome_responsavel, celular_formatado = pegar_dados(self.id_usuario_logado)

        # formata sexo do pet para texto
        if self.sexo == "M":
            sexo_format = "Masculino"
        else:
            sexo_format = "Feminino"

        # cria o modelo da mensagem para o whatsapp
        mensagem = f"""
Olá {nome_responsavel} encontrei o {self.nome_pet}%0A
%2ADados do Pet%2A%0A
%2ANome do Pet%3A%2A {self.nome_pet}%0A
%2ARaca do Pet%3A%2A {self.raca}%0A
%2ASexo%3A%2A {sexo_format}%0A
%2AObservacoes%3A%2A {self.obs}%0A"""

        # formatar texto para formato url
        mensagem = mensagem.replace(" ", "%20")

        # cria a URL
        url_whatsapp = f"https://api.whatsapp.com/send?phone={celular_formatado}&text={mensagem}"

        # cria o objeto QRCode
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        # adiciona os dados ao QRCode
        qr.add_data(url_whatsapp)
        qr.make(fit=True)

        # cria a imagem QRCode
        imagem_qrcode = qr.make_image(fill_color="black", back_color="white")

        # salva a imagem QRCode
        self.qr_nome = f"qrcodes/qrcode_cuidador{nome_responsavel}_pet_{self.nome_pet}.png"
        imagem_qrcode.save(self.qr_nome)

    def voltartela(self):
        if self.master:
            self.master.deiconify()
        self.destroy()
