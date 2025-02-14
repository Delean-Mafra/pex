import os
import hashlib
import time
import sys  # Importa o módulo sys
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

def hash_file(file_path):
    # Gera um hash SHA-256 para um arquivo
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def find_duplicates(folder_path):
    # Encontra e exclui arquivos duplicados em uma pasta e registra os nomes dos arquivos excluídos
    file_hashes = {}
    deleted_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.pdf', '.png', '.jpeg', '.jpg')):
                file_path = os.path.join(root, file)
                file_hash = hash_file(file_path)
                if file_hash in file_hashes:
                    print(f"Arquivo duplicado encontrado e excluído: {file_path}")
                    os.remove(file_path)
                    deleted_files.append(file)
                else:
                    file_hashes[file_hash] = file_path
    return deleted_files

def create_log_file(deleted_files, folder_path):
    # Cria um arquivo de log com os nomes dos arquivos excluídos
    log_file_path = os.path.join(folder_path, 'deleted_files_log.txt')
    with open(log_file_path, 'w') as log_file:
        for file in deleted_files:
            log_file.write(f"{file}\n")
    return log_file_path

def read_license_file(license_file_path):
    # Lê o caminho da pasta dos arquivos duplicados do arquivo de licença
    try:
        with open(license_file_path, 'r') as file:
            folder_path = file.read().strip()
            if folder_path and os.path.exists(folder_path):
                return folder_path
    except Exception as e:
        print(f"Erro ao ler arquivo de licença: {e}")
    return None

def write_license_file(license_file_path, folder_path):
    # Escreve o caminho da pasta dos arquivos duplicados no arquivo de licença
    with open(license_file_path, 'w') as file:
        file.write(folder_path)

class ExcluiArquivosDuplicados(App):
    def build(self):
        if getattr(sys, 'frozen', False):
            # Executando como .exe
            self.license_file_path = os.path.join(sys._MEIPASS, 'delean.lic.txt')
        else:
            # Executando como script Python
            self.license_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'delean.lic.txt')
        
        self.title = 'Exclui Arquivos Duplicados'
        self.layout = BoxLayout(orientation='vertical')
        
        self.label = Label(text='Clique no botão para encontrar e excluir arquivos duplicados')
        self.layout.add_widget(self.label)
        
        button = Button(text='Executar')
        button.bind(on_press=self.on_button_press)
        self.layout.add_widget(button)
        
        copyright_label = Label(text='Copyright ©2024 | Delean Mafra, todos os direitos reservados.')
        self.layout.add_widget(copyright_label)
        
        return self.layout

    def on_button_press(self, instance):
        folder_path = read_license_file(self.license_file_path)
        if folder_path:
            self.execute_process(folder_path)
        else:
            self.show_password_popup()

    def show_password_popup(self):
        self.password_input = TextInput(password=True, multiline=False)
        popup_content = BoxLayout(orientation='vertical')
        popup_content.add_widget(Label(text='Digite a senha:'))
        popup_content.add_widget(self.password_input)
        popup_button = Button(text='OK')
        popup_button.bind(on_press=self.check_password)
        popup_content.add_widget(popup_button)
        self.popup = Popup(title='Senha Necessária', content=popup_content, size_hint=(0.5, 0.5))
        self.popup.open()

    def check_password(self, instance):
        if self.password_input.text == 'Deus é fiel':
            self.popup.dismiss()
            self.show_folder_path_popup()
        else:
            self.password_input.text = ''
            self.password_input.hint_text = 'Senha incorreta. Tente novamente.'

    def show_folder_path_popup(self):
        self.folder_path_input = TextInput(multiline=False)
        popup_content = BoxLayout(orientation='vertical')
        popup_content.add_widget(Label(text='Informe o caminho da pasta dos arquivos duplicados:'))
        popup_content.add_widget(self.folder_path_input)
        popup_button = Button(text='OK')
        popup_button.bind(on_press=self.save_folder_path)
        popup_content.add_widget(popup_button)
        self.popup = Popup(title='Caminho da Pasta', content=popup_content, size_hint=(0.5, 0.5))
        self.popup.open()

    def save_folder_path(self, instance):
        folder_path = self.folder_path_input.text
        if os.path.exists(folder_path):
            write_license_file(self.license_file_path, folder_path)
            self.popup.dismiss()
            self.execute_process(folder_path)
        else:
            self.folder_path_input.text = ''
            self.folder_path_input.hint_text = 'Caminho inválido. Tente novamente.'

    def execute_process(self, folder_path):
        deleted_files = find_duplicates(folder_path)
        log_file_path = create_log_file(deleted_files, folder_path)
        self.label.text = 'Processo concluído!'
        time.sleep(3)
        os.startfile(log_file_path)

if __name__ == '__main__':
    ExcluiArquivosDuplicados().run()
