import os
import hashlib
import tkinter as tk
from tkinter import messagebox
from PIL import Image
import io
from PyPDF2 import PdfReader

def calcular_hash(arquivo):
    hash_sha256 = hashlib.sha256()
    if arquivo.lower().endswith(('.png', '.jpeg', '.jpg')):
        with open(arquivo, 'rb') as f:
            img = Image.open(f)
            with io.BytesIO() as img_bytes:
                img.save(img_bytes, format='PNG')
                hash_sha256.update(img_bytes.getvalue())
    elif arquivo.lower().endswith('.pdf'):
        with open(arquivo, 'rb') as f:
            pdf = PdfReader(f)
            for page in pdf.pages:
                with io.BytesIO() as page_bytes:
                    page_bytes.write(page.extract_text().encode('utf-8'))
                    hash_sha256.update(page_bytes.getvalue())
    return hash_sha256.hexdigest()

def verificar_duplicados(caminho_pasta):
    arquivos_verificados = {}
    log_exclusao = []
    
    # Verifica se existem arquivos para processar
    arquivos_encontrados = False
    
    for root, _, arquivos in os.walk(caminho_pasta):
        for nome_arquivo in arquivos:
            if nome_arquivo.lower().endswith(('.pdf', '.png', '.jpeg', '.jpg')):
                arquivos_encontrados = True
                caminho_completo = os.path.join(root, nome_arquivo)
                try:
                    hash_arquivo = calcular_hash(caminho_completo)
                    if hash_arquivo in arquivos_verificados:
                        try:
                            os.remove(caminho_completo)
                            log_exclusao.append(f"Arquivo excluído: {caminho_completo}")
                        except PermissionError:
                            log_exclusao.append(f"Erro: Sem permissão para excluir {caminho_completo}")
                    else:
                        arquivos_verificados[hash_arquivo] = caminho_completo
                except Exception as e:
                    log_exclusao.append(f"Erro ao processar {caminho_completo}: {str(e)}")
    
    if not arquivos_encontrados:
        return "Nenhum arquivo compatível encontrado na pasta especificada."

    # Define o caminho do arquivo de log no mesmo diretório do script
    log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log_exclusao.txt')
    
    try:
        # Tenta criar ou abrir o arquivo de log
        with open(log_path, 'w', encoding='utf-8') as log:
            log.write("=== Log de Exclusão de Arquivos ===\n")
            log.write(f"Data e hora: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            for item in log_exclusao:
                log.write(f"{item}\n")
            log.write("\n=== Fim do Log ===")
        
        return f"Processo concluído. {len([l for l in log_exclusao if 'excluído' in l])} arquivos duplicados encontrados. Log salvo em: {log_path}"
    
    except PermissionError:
        # Tenta criar o log em uma pasta alternativa (Documents)
        try:
            documents_path = os.path.join(os.path.expanduser('~'), 'Documents')
            log_path = os.path.join(documents_path, 'log_exclusao.txt')
            
            with open(log_path, 'w', encoding='utf-8') as log:
                log.write("=== Log de Exclusão de Arquivos ===\n")
                log.write(f"Data e hora: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                for item in log_exclusao:
                    log.write(f"{item}\n")
                log.write("\n=== Fim do Log ===")
            
            return f"Processo concluído. Log salvo em pasta alternativa: {log_path}"
        
        except Exception as e:
            return f"Processo concluído, mas não foi possível salvar o log. Erro: {str(e)}"

def obter_caminho_da_pasta():
    caminho_arquivo = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pex.lic')
    if not os.path.exists(caminho_arquivo):
        raise FileNotFoundError(f"O arquivo {caminho_arquivo} não foi encontrado.")
    with open(caminho_arquivo, 'r') as arquivo:
        caminho_pasta = arquivo.readline().strip()
    return caminho_pasta

def excluir_arquivos_duplicados():
    try:
        caminho = obter_caminho_da_pasta()
        mensagem = verificar_duplicados(caminho)
        messagebox.showinfo("Resultado", mensagem)
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

def main():
    root = tk.Tk()
    root.title("Exclusão de Arquivos Duplicados")
    root.geometry("400x200")
    
    label_copyright = tk.Label(root, text="©2024 Delean Mafra - Todos os direitos reservados")
    label_copyright.pack(pady=10)
    
    btn_executar = tk.Button(
        root, text="Excluir Arquivos Duplicados", command=excluir_arquivos_duplicados
    )
    btn_executar.pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    import datetime
    main()







# # import os
# # import hashlib
# # import tkinter as tk
# # from tkinter import messagebox

# # def calcular_hash(arquivo):
# #     # Calcula o hash SHA-256 de um arquivo para identificar duplicados
# #     hash_sha256 = hashlib.sha256()
# #     with open(arquivo, 'rb') as f:
# #         for chunk in iter(lambda: f.read(4096), b""):
# #             hash_sha256.update(chunk)
# #     return hash_sha256.hexdigest()

# # def verificar_duplicados(caminho_pasta):
# #     # Verifica e exclui arquivos duplicados na pasta especificada
# #     arquivos_verificados = {}
# #     log_exclusao = []

# #     for root, _, arquivos in os.walk(caminho_pasta):
# #         for nome_arquivo in arquivos:
# #             if nome_arquivo.lower().endswith(('.pdf', '.png', '.jpeg', '.jpg')):
# #                 caminho_completo = os.path.join(root, nome_arquivo)
# #                 hash_arquivo = calcular_hash(caminho_completo)

# #                 if hash_arquivo in arquivos_verificados:
# #                     os.remove(caminho_completo)  # Excluir o arquivo duplicado
# #                     log_exclusao.append(caminho_completo)
# #                 else:
# #                     arquivos_verificados[hash_arquivo] = caminho_completo

# #     # Salvar log dos arquivos excluídos
# #     with open('log_exclusao.txt', 'w') as log:
# #         for item in log_exclusao:
# #             log.write(f"{item}\n")
# #     return "Processo concluído. Log salvo em 'log_exclusao.txt'."

# # def obter_caminho_da_pasta():
# #     # Lê o caminho da pasta a partir de um arquivo de texto
# #     with open('pex.lic', 'r') as arquivo:
# #         caminho_pasta = arquivo.readline().strip()
# #     return caminho_pasta

# # def excluir_arquivos_duplicados():
# #     # Executa a função de exclusão de arquivos duplicados e exibe mensagem de conclusão
# #     caminho = obter_caminho_da_pasta()
# #     mensagem = verificar_duplicados(caminho)
# #     messagebox.showinfo("Resultado", f"{mensagem}\nTodos os arquivos duplicados foram excluídos.")

# # def main():
# #     root = tk.Tk()
# #     root.withdraw()  # Oculta a janela principal inicialmente

# #     # Configuração da interface para executar a exclusão de arquivos duplicados
# #     root.deiconify()  # Mostra a janela principal para o botão de execução
# #     root.title("Exclusão de Arquivos Duplicados")
# #     root.geometry("400x200")

# #     # Label de autoria
# #     label_copyright = tk.Label(root, text="©2024 Delean Mafra - Todos os direitos reservados")
# #     label_copyright.pack(pady=10)

# #     # Botão para iniciar o processo de exclusão
# #     btn_executar = tk.Button(
# #         root, text="Excluir Arquivos Duplicados", command=excluir_arquivos_duplicados
# #     )
# #     btn_executar.pack(pady=20)

# #     root.mainloop()

# # if __name__ == "__main__":
# #     main()
