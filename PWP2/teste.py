import pyautogui
import pydirectinput
import time

time.sleep(3)

# Encontra todas as ocorrências da imagem
botoes = list(pyautogui.locateAllOnScreen("botao_coletar_1.png", confidence=0.8))

# Verifica se encontrou pelo menos 3
if len(botoes) >= 3:
    terceiro_botao = botoes[3]
    centro = pyautogui.center(terceiro_botao)

    # Corrigido: separa os valores x e y
    pydirectinput.moveTo(centro[0], centro[1])
    time.sleep(0.3)
    pydirectinput.click()
    print(botoes)
else:
    print("Não foi possível localizar os 3 botões.")









# import time, pyautogui

# time.sleep(4)
# print(pyautogui.position())