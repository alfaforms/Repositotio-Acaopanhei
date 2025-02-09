import customtkinter as ctk
from services import autenticar_usuario
import main
import register


class Hello(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # inicializa tela App
        self.config_tela()  # carrega as config da tela App
        self.widgets_tela()  # carrega os widgtes da tela App
        self.toplevel_window = None  # definindo variavel para carregar outras telas

    def config_tela(self):
        self._set_appearance_mode("System")  # tema escuro do app
        self.title("Login")  # titulo que aparece na tela
        self.geometry("600x400")  # dimensoes x y da tela
        self.resizable(False, False)  # nao permite usuario ajustar tela

    def widgets_tela(self):
        # ====================================criação de widgets========================================================
        # labels
        fraselogin_label = ctk.CTkLabel(self, text="Sistema de Login", font=("Roboto", 24), width=300, height=30)
        naotemconta_label = ctk.CTkLabel(self, text="Se não tem uma conta", font=("Roboto", 12), width=150, height=30)
        self.errologin_label = ctk.CTkLabel(self, text="", text_color="red", font=("Roboto", 12), width=150, height=30)

        # entrys
        self.login_entry = ctk.CTkEntry(self, placeholder_text="Nome de usuario", font=("Roboto", 14),
                                        width=300, height=30)
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Insira a senha", font=("Roboto", 14), show="*",
                                           width=300, height=30)

        # buttons
        logar_button = ctk.CTkButton(self, text="Login", command=self.carregar_tela_usuario, font=("Roboto", 14),
                                     width=300, height=30)
        registrar_button = ctk.CTkButton(self, text="Cadastre-se", command=self.registrar, font=("Roboto", 12),
                                         fg_color="green", width=150, height=30)

        # ==============================================================================================================
        # ===================================definindo lugares dos widgets==============================================

        # labels
        fraselogin_label.place(x=150, y=15)
        naotemconta_label.place(x=138, y=295)
        self.errologin_label.place(x=90, y=210)

        # entrys
        self.login_entry.place(x=150, y=120)
        self.password_entry.place(x=150, y=170)

        # buttons
        logar_button.place(x=150, y=250)
        registrar_button.place(x=300, y=295)

    def carregar_tela_usuario(self):
        # definindo variaveis das entradas
        self.login = self.login_entry.get()
        self.password = self.password_entry.get()

        # chama função autenticar usuario dentro de services.py e retorna o id usuario logado e a lista de pets que
        # esse usuario tem
        self.id_usuario_logado, self.lista_pets_logado = autenticar_usuario(self.login, self.password)

        try:  # verifica se login e senha batem com banco de dados
            if not (self.id_usuario_logado is None):
                # tratativa da tela
                self.toplevel_window = main.Main(self.id_usuario_logado, self.lista_pets_logado)
                self.withdraw()  # esconde a tela App
                self.toplevel_window.focus()  # focar tela
                self.errologin_label.configure(text="")  # tira a mensagem de erro de login se tiver
                self.login_entry.delete(0, "end")  # limpa campo login
                self.password_entry.delete(0, "end")  # limpa compo password
            else:
                self.errologin_label.configure(text="Login ou senha incorreto")
                self.errologin_label.place(x=142, y=210)

        except:
            self.errologin_label.configure(text="Login ou senha incorreto")
            self.errologin_label.place(x=142, y=210)

    def registrar(self):
        self.toplevel_window = register.TelaRegistro(self)  # chama a Tela de Registro
        self.withdraw()  # esconde a tela
        self.toplevel_window.focus()  # focar tela
        self.login_entry.delete(0, "end")  # limpa campo login
        self.password_entry.delete(0, "end")  # limpa compo password


app = Hello()  # define app para classe App
app.mainloop()  # mantem app em loop para a tela ficar ligada
