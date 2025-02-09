import customtkinter as ctk
from services import RegisterService


class TelaRegistro(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_tela_registro()  # carrega as config da tela registro
        self.widgets_tela_registro()  # carrega os widgtes da tela registro

    def config_tela_registro(self):
        self.geometry("600x400")  # dimensoes x y da tela
        self.title("Registro")  # titulo que aparece na tela
        self.resizable(False, False)  # nao permite usuario ajustar tela

    def widgets_tela_registro(self):
        # ====================================criação de widgets========================================================
        # scroll frame
        cadastro_frame = ctk.CTkScrollableFrame(self, width=330, height=350, corner_radius=10)
        cadastro_frame.pack(padx=20, pady=20)
        cadastro_frame.grid_columnconfigure((0, 1), weight=1)

        # labels
        fraseregistro_label = ctk.CTkLabel(cadastro_frame, text="Sistema de Registro", font=("Roboto", 24),
                                           width=300, height=30)
        jatemconta_label = ctk.CTkLabel(cadastro_frame, text="Se já tem uma conta", font=("Roboto", 12),
                                        width=150, height=30)
        self.erroregistro_label = ctk.CTkLabel(cadastro_frame, text="", text_color="red", font=("Roboto", 12),
                                               width=150, height=30)

        # entrys
        self.login_entry = ctk.CTkEntry(cadastro_frame, placeholder_text="Defina o nome de usuario",
                                        font=("Roboto", 14), width=300, height=30)
        self.nome_entry = ctk.CTkEntry(cadastro_frame, placeholder_text="Digite seu nome completo", font=("Roboto", 14),
                                       width=300, height=30)
        self.ddd_entry = ctk.CTkEntry(cadastro_frame, placeholder_text="DDD", font=("Roboto", 14),
                                      width=100, height=30)
        self.celular_entry = ctk.CTkEntry(cadastro_frame, placeholder_text="Digite seu telefone",
                                          font=("Roboto", 14), width=200, height=30)
        self.password_entry = ctk.CTkEntry(cadastro_frame, placeholder_text="Define a senha", font=("Roboto", 14),
                                           show="*", width=300, height=30)
        self.con_password_entry = ctk.CTkEntry(cadastro_frame, placeholder_text="Confirme a senha", font=("Roboto", 14),
                                               show="*", width=300, height=30)

        # buttons
        registrar_button = ctk.CTkButton(cadastro_frame, text="Registrar", command=self.registrar_usuario,
                                         font=("Roboto", 14), fg_color="green", width=300, height=30)
        voltar_button = ctk.CTkButton(cadastro_frame, text="Voltar", command=self.voltartela, font=("Roboto", 12),
                                      width=150, height=30)

        # ==============================================================================================================
        # ===================================definindo lugares dos widgets==============================================
        fraseregistro_label.grid(row=0, column=0, pady=10, columnspan=2)
        self.erroregistro_label.grid(row=1, column=0, pady=10, columnspan=2)
        self.login_entry.grid(row=2, column=0, pady=10, columnspan=2)
        self.nome_entry.grid(row=3, column=0, pady=10, columnspan=2)
        self.ddd_entry.grid(row=5, column=0, pady=10, columnspan=1)
        self.celular_entry.grid(row=5, column=1, pady=10, columnspan=1)
        self.password_entry.grid(row=6, column=0, pady=10, columnspan=2)
        self.con_password_entry.grid(row=7, column=0, pady=10, columnspan=2)
        registrar_button.grid(row=8, column=0, pady=10, columnspan=2)
        jatemconta_label.grid(row=9, column=0, pady=10, columnspan=1)
        voltar_button.grid(row=9, column=1, pady=10, columnspan=1)

    def registrar_usuario(self):
        # Coleta os dados e envia para o RegisterService para validar e registrar
        login = self.login_entry.get()
        password = self.password_entry.get()
        con_password = self.con_password_entry.get()
        nome = self.nome_entry.get()
        ddd = self.ddd_entry.get()
        celular = self.celular_entry.get()

        # Validações
        if not all([login, password, nome, ddd, celular]):
            self.erroregistro_label.configure(text="Preencha todos os campos!")
            return

        if password != con_password:
            self.erroregistro_label.configure(text="Senhas não coincidem!")
            return

        if RegisterService.verificar_login_existente(login):
            self.erroregistro_label.configure(text="Login já cadastrado!")
            return

        # Tenta cadastrar o usuário
        if RegisterService.cadastrar_usuario(login, password, nome, ddd, celular):
            self.voltartela()
        else:
            self.erroregistro_label.configure(text="Erro ao registrar usuário.")

    def voltartela(self):
        if self.master:
            self.master.deiconify()
        self.destroy()
