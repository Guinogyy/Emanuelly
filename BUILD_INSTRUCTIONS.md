# Como criar o APK (Android) para o BTS To-Do List

Este guia explica como transformar seu aplicativo Flet em um arquivo `.apk` para instalar no Android.

## Pré-requisitos

1.  **Python 3.8+** instalado.
2.  **SDK do Flutter** instalado (o Flet usa o Flutter por baixo dos panos).
3.  **SDK do Android** (via Android Studio ou command-line tools).

## Passo a Passo

1.  **Instale o Flet Mobile Tools**:
    Abra seu terminal e rode:
    ```bash
    pip install flet
    ```

2.  **Organize os Arquivos**:
    Certifique-se de que a estrutura do projeto está assim:
    ```
    /seu-projeto
      main.py
      data_manager.py
      theme_manager.py
      resources/
        foto.jfif
        success.mp3
        confetti.gif
      assets/ (opcional, se quiser ícone do app)
        icon.png
    ```

3.  **Compile para APK**:
    No terminal, dentro da pasta do projeto, execute:
    ```bash
    flet build apk
    ```
    *Dica: Se quiser um ícone personalizado, adicione `--product "BTS To-Do"` e coloque um `icon.png` na pasta `assets`.*

4.  **Localize o APK**:
    Após o processo terminar (pode demorar alguns minutos na primeira vez), o arquivo estará em:
    `build/apk/app-release.apk`

5.  **Instale no Celular**:
    Envie esse arquivo `.apk` para o celular da sua amiga (via WhatsApp, Drive, USB) e instale! (Lembre-se de ativar "Fontes Desconhecidas" nas configurações do Android).

## Solução de Problemas Comuns

*   **"Assets not found"**: Verifique se a pasta `resources` está na mesma pasta que `main.py`.
*   **App fecha ao abrir**: Conecte o celular via USB e rode `flet run --android` para ver os logs de erro no terminal.
