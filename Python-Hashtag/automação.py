import time, pyautogui, pandas

link = "https://dlp.hashtagtreinamentos.com/python/intensivao/login"
pyautogui.PAUSE = 0.5

# abre o navegador e o site
pyautogui.press("win")
pyautogui.write("Vivaldi")
pyautogui.press("enter")
pyautogui.click(x=241, y=61)
pyautogui.write(link)
pyautogui.press("enter")

time.sleep(5) # espera o sistema abrir

# faz o loguin 
pyautogui.click(x=714, y=399)
pyautogui.write("gabriel@gmail.com")
pyautogui.press("tab")
pyautogui.write("12345678")
pyautogui.press("tab")
pyautogui.press("enter")

# tempo para carregar o sistema corretamente
time.sleep(2)
tabela = pandas.read_csv(r"C:\Users\gabri\Documents\Repositorios\Meus-Projetos\Python-Hashtag\produtos.csv")




for linha in tabela.index:
    pyautogui.click(x=718, y=283)

    # codigo
    codigo = str(tabela.loc[linha, "codigo"])
    pyautogui.write(codigo)
    pyautogui.press("tab")

    # produto
    marca = str(tabela.loc[linha, "marca"])
    pyautogui.write(marca)
    pyautogui.press("tab")

    # tipo
    tipo = str(tabela.loc[linha, "tipo"])
    pyautogui.write(tipo)
    pyautogui.press("tab")

    # categoria
    categoria = str(tabela.loc[linha, "categoria"])
    pyautogui.write(categoria)
    pyautogui.press("tab")

    # preço
    preco = str(tabela.loc[linha, "preco_unitario"])
    pyautogui.write(preco)
    pyautogui.press("tab")

    # custo do produto
    custo = str(tabela.loc[linha, "custo"])
    pyautogui.write(custo)
    pyautogui.press("tab")

    # obs
    obs = str(tabela.loc[linha, "obs"])
    if obs != "nan":
        pyautogui.write(obs)
    pyautogui.press("tab")

    # botão de enviar
    pyautogui.press("enter")
    pyautogui.scroll(5000)
    