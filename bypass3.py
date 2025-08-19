import pyautogui
import time
import random
import string
import pyperclip # Biblioteca para copiar o texto para a área de transferência
import pyotp

# Função para gerar um nickname aleatório
def gerar_nickname_aleatorio(min_tamanho=6, max_tamanho=8):
    tamanho = random.randint(min_tamanho, max_tamanho)
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(tamanho))

# Função para localizar uma imagem com espera adaptativa
def localizar_imagem(imagem_referencia, confidence=0.8, timeout=10):  # Timeout menor
    start_time = time.time()
    localizacao = None
    while localizacao is None and time.time() - start_time < timeout:
        localizacao = pyautogui.locateOnScreen(imagem_referencia, confidence=confidence)
        if localizacao:
            print(f"Imagem encontrada: {imagem_referencia}")
        else:
            time.sleep(0.5)  # Menor tempo de espera entre tentativas
    if not localizacao:
        print(f"Imagem não encontrada: {imagem_referencia}")
    return localizacao

# Função para clicar em uma imagem
def clicar_na_imagem(imagem_referencia, timeout=10):  # Timeout menor
    localizacao = localizar_imagem(imagem_referencia, timeout=timeout)
    if localizacao:
        pyautogui.click(pyautogui.center(localizacao))
        time.sleep(0.2)  # Reduzi o tempo de espera após o clique
    else:
        print(f"Não foi possível clicar na imagem: {imagem_referencia}")

# Função para digitar texto com intervalo reduzido
def digitar_texto(texto):
    pyautogui.write(texto, interval=0.05)  # Intervalo de digitação mais rápido

# Função para pressionar Page Down
def pressionar_pgdown():
    pyautogui.press('pagedown')
    time.sleep(0.3)  # Reduzi o tempo de espera após o Page Down

# Função para pressionar Ctrl + V (colar)
def pressionar_ctrl_v():
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.3)  # Reduzi o tempo de espera após colar

# Função para pressionar Ctrl + C (Copiar)
def pressionar_ctrl_c():
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.3)

# Função para pressionar Enter
def pressionar_ENTER():
    pyautogui.press('enter')
    time.sleep(0.2)  # Reduzi o tempo de espera após pressionar Enter

# Função que simula o registro no site
def realizar_registro():
    clicar_na_imagem("imagens/register.png")
    clicar_na_imagem("imagens/dia.png")
    clicar_na_imagem("imagens/dia3.png")
    clicar_na_imagem("imagens/mes.png")
    clicar_na_imagem("imagens/mes3.png")
    clicar_na_imagem("imagens/ano33.png")
    pressionar_pgdown()
    pressionar_ENTER()
    clicar_na_imagem("imagens/continuar33.png")
    clicar_na_imagem("imagens/concordo3.png")
    clicar_na_imagem("imagens/continuar3.png")
    clicar_na_imagem("imagens/email3.png")
    pressionar_ctrl_v()

    # Captura o texto atual do clipboard (email)
    email = pyperclip.paste()

    # Salvando as informações da conta em um arquivo txt
    with open("rockstar.txt", "a") as arquivo:
        arquivo.write(f"{email}:WolfStore77BR:\n")
    print("Informações da conta salvas com sucesso.")

# Função para preencher o formulário
def preencher_formulario():
    nickname = gerar_nickname_aleatorio()
    clicar_na_imagem("imagens/senha3.png")
    digitar_texto("WolfStore77BR")
    clicar_na_imagem("imagens/nick3.png")
    digitar_texto(nickname)
    pressionar_pgdown()
    clicar_na_imagem("imagens/confirmaemail.png")
    time.sleep(5)  # Reduzi o tempo de espera
    clicar_na_imagem("imagens/codigorockstar.png")
    time.sleep(1.8)  # Reduzi o tempo de espera
    pressionar_ctrl_v()
    clicar_na_imagem("imagens/enviar.png")
    time.sleep(2.5)  # Reduzi o tempo de espera
    clicar_na_imagem("imagens/link.png")
    
    # Copia a URL para a área de transferência e cola
    pyperclip.copy("https://socialclub.rockstargames.com/settings/mfa")
    pressionar_ctrl_v()
    pressionar_ENTER()
    time.sleep(3.8)

    clicar_na_imagem("imagens/configrock.png")
    time.sleep(1)

    # Coordenadas de início e fim
    inicio = (483, 853)
    final = (769, 852)

    # Ir para a posição inicial
    pyautogui.moveTo(inicio[0], inicio[1], duration=0.3)
    time.sleep(0.2)  # Pequena pausa antes de arrastar

    # Pressionar o botão esquerdo do mouse
    pyautogui.mouseDown()

    # Arrastar até a posição final
    pyautogui.moveTo(final[0], final[1], duration=0.5)

    # Copiar o texto desejado
    pressionar_ctrl_c()

    # Captura o texto atual do clipboard (2FA)
    two2fa = pyperclip.paste()

    time.sleep(1)

    # Salvando as informações da conta em um arquivo txt
    with open("rockstar.txt", "a") as arquivo:
        arquivo.write(f"{two2fa}\n")
        arquivo.write("-" * 20 + "\n")

    # Soltar o botão esquerdo do mouse
    pyautogui.mouseUp()

    pressionar_ctrl_v()

    time.sleep(0.5)

    # Coordenada de destino
    destino = (440, 674)

    # Mover o mouse até a posição desejada
    pyautogui.moveTo(destino[0], destino[1], duration=0.3)

    # Pequena pausa antes do clique
    time.sleep(0.2)

    # Realizar o clique com o botão esquerdo
    pyautogui.click()

    pressionar_ctrl_c()

    time.sleep(0.5)

    pressionar_pgdown()

    # Gerar código TOTP (2FA) a partir do segredo
    totp = pyotp.TOTP(two2fa)
    codigo_2fa = totp.now()

    # Copia o código de 6 dígitos para a área de transferência
    pyperclip.copy(codigo_2fa)
    print(f"Código 2FA gerado: {codigo_2fa}")

    clicar_na_imagem("imagens/codeverifrock.png")

    pressionar_ctrl_v()

    clicar_na_imagem("imagens/senharock2.png")

    pyperclip.copy("WolfStore77BR")

    pressionar_ctrl_v()

    clicar_na_imagem("imagens/verificar23.png")

# Função principal
def main():
    time.sleep(1)  # Reduzi a pausa inicial para ajustar a tela
    realizar_registro()
    preencher_formulario()

if __name__ == "__main__":
    main()
