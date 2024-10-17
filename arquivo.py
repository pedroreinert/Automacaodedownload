import pyautogui
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import shutil
import datetime

# Configurações do navegador
browser = webdriver.Chrome()

# Acessa o site
browser.get("https://consulta-empresa.netlify.app/")

# Informa login e senha
login_input = browser.find_element(By.ID, "username")
login_input.send_keys("jhonatan")

senha_input = browser.find_element(By.ID, "password")
senha_input.send_keys("12345678")

# Clica no botão de acesso
acessar_button = browser.find_element(By.CLASS_NAME, "btn-lg")
acessar_button.click()

# Espera a tabela carregar
table_loaded = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.ID, "tabelaEmpresas"))
)

# Encontra as empresas na tabela
empresas = browser.find_elements(By.CSS_SELECTOR, "#tabelaEmpresas tr td:nth-child(1)")

# Conjunto para rastrear arquivos renomeados
arquivos_renomeados = set()

# Loop pelas empresas
for empresa in empresas:
    empresa_nome = empresa.text
    print(f"Processando empresa: {empresa_nome}")

    try:
        # Clica no botão de download
        download_button = empresa.find_element(By.XPATH, "../td[3]/button")
        download_button.click()

        # Espera o download concluir
        download_complete = False
        while not download_complete:
            time.sleep(1)  # Aguarda 1 segundo
            arquivos_lista = os.listdir("C:\\Users\\pedro\\Downloads")
            for arquivo in arquivos_lista:
                # Verifica se o arquivo foi baixado e não foi renomeado
                if arquivo.endswith('.pdf') and arquivo not in arquivos_renomeados:
                    download_complete = True
                    arquivo_baixado = arquivo  # Armazena o nome do arquivo baixado
                    break

        # Renomeia o arquivo baixado com um timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        novo_nome = f"{empresa_nome}_{timestamp}.pdf"

        # Tenta renomear o arquivo com tentativas
        tentativas = 5
        while tentativas > 0:
            try:
                # Verifica se o arquivo está disponível e não está sendo usado
                if os.path.exists(os.path.join("C:\\Users\\pedro\\Downloads", arquivo_baixado)):
                    shutil.move(os.path.join("C:\\Users\\pedro\\Downloads", arquivo_baixado), os.path.join("C:\\Users\\pedro\\Downloads", novo_nome))
                    arquivos_renomeados.add(novo_nome)  # Adiciona ao conjunto de arquivos renomeados
                    print(f"Arquivo baixado e renomeado para {novo_nome}.")
                    break  # Sai do loop se renomeou com sucesso
            except PermissionError:
                print(f"Erro de permissão ao renomear {arquivo_baixado}. Tentando novamente em 10 segundos.")
                time.sleep(5)  # Aguarda 5 segundos antes de tentar novamente
                tentativas -= 1  # Diminui o número de tentativas
            except Exception as e:
                print(f"Erro inesperado: {e}. Tentando novamente em 10 segundos.")
                time.sleep(5)  # Aguarda 5 segundos antes de tentar novamente
                tentativas -= 1  # Diminui o número de tentativas

        if tentativas == 0:
            print(f"Falha ao renomear o arquivo {arquivo_baixado} após várias tentativas.")

    except Exception as e:
        print(f"Erro ao processar a empresa {empresa_nome}: {e}")

# Fecha o navegador
browser.quit()