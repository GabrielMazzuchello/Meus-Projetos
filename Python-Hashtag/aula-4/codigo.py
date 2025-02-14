import flet as ft

def main(pagina):
    texto = ft.Text("Hashzap")

    chat = ft.Column()

    nome_usuario = ft.TextField(label="Escreva seu nome")

    def enviar_mensagem_tunel(mensagem):
        tipo = mensagem["tipo"]
        if tipo == "mensagem":
            texto_mensagem = mensagem["texto"]
            usuario_mensagem = mensagem["usuario"]
            # adicionar a mensagem no chat
            chat.controls.append(ft.Text(f"{usuario_mensagem}: {texto_mensagem}"))
        else:
            usuario_mensagem = mensagem["usuario"]
            chat.controls.append(ft.Text(f"{usuario_mensagem} entrou no chat", 
                                         size=12, italic=True, color=ft.colors.ORANGE_500))
        pagina.update()

    pagina.pubsub.subscribe(enviar_mensagem_tunel)

    def enviar_mensagem(evento):
        pagina.pubsub.send_all({"texto": campo_mensagem.value, "usuario": nome_usuario.value,
                                "tipo": "mensagem"})
        # limpar o campo de mensagem
        campo_mensagem.value = ""
        pagina.update()

    campo_mensagem = ft.TextField(label="Digite uma mensagem", on_submit=enviar_mensagem)
    botao_enviar_mensagem = ft.ElevatedButton("Enviar", on_click=enviar_mensagem)

    def entrar_popup(evento):
        if nome_usuario.value:  # Garantir que o nome do usuário não esteja vazio
            pagina.pubsub.send_all({"usuario": nome_usuario.value, "tipo": "entrada"})
            # adicionar o chat
            pagina.add(chat)
            # remover o botão iniciar chat e o texto
            pagina.remove(botao_iniciar)
            pagina.remove(texto)
            # adicionar o campo de mensagem do usuário
            # adicionar o botão de enviar mensagem
            pagina.add(ft.Row([campo_mensagem, botao_enviar_mensagem]))
            # fechar o container de entrada
            pagina.remove(popup)
            pagina.update()

    # Container que simula o popup de entrada
    popup = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Bem-vindo ao Hashzap"),
                nome_usuario,
                ft.ElevatedButton("Entrar", on_click=entrar_popup),
            ]
        ),
        alignment=ft.alignment.center,
        padding=20,
        border_radius=10,
        bgcolor=ft.colors.LIGHT_BLUE_50
    )

    def entrar_chat(evento):
        # Exibir o "popup" (container) na tela
        pagina.add(popup)
        pagina.update()

    botao_iniciar = ft.ElevatedButton("Iniciar chat", on_click=entrar_chat)

    # Adicionando o título e o botão de iniciar chat na página
    pagina.add(texto)
    pagina.add(botao_iniciar)

ft.app(target=main, view=ft.WEB_BROWSER, port=8000)
