# No arquivo utils.py dentro do diretório do seu aplicativo Django (por exemplo, images/utils.py)

import os
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .models import Imagem, Doenca

def visualizar_e_fazer_download():
    # Obtendo todas as classes disponíveis
    classes = Doenca.objects.all()

    # Criando uma resposta HTTP
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="estrutura_de_classes.txt"'

    # Escrevendo a estrutura de classes no arquivo
    for classe in classes:
        response.write(f'Classe: {classe.nome}\n')

        # Obtendo todas as imagens classificadas para esta classe
        imagens_classificadas = Imagem.objects.filter(classe=classe)

        # Escrevendo os nomes das imagens no arquivo
        for imagem in imagens_classificadas:
            response.write(f'- {imagem.image.name}\n')

        response.write('\n')

    return response
