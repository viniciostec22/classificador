from django.shortcuts import render, redirect
from . models import Imagem
from django.utils import timezone
from django.http import HttpResponse, FileResponse
from django.contrib.messages import constants
from django.contrib import messages
from .models import Imagem, Doenca, Analise
import os
from django.db.models import Count
import tempfile
import zipfile
from django.http import HttpResponse
import shutil
from django.contrib.auth.decorators import login_required

@login_required
def images(request):
    if request.method == "GET":
        return render(request, 'upload_images.html')
    elif request.method == "POST":
        imagens = request.FILES.getlist('image')
        
        if imagens:
            for imagem in imagens:
                nova_imagem = Imagem.objects.create(
                    image=imagem,
                    data_criacao=timezone.now(),
                    usuario=request.user
                )
            messages.add_message(request, constants.SUCCESS, "Imagens salvas com sucesso")
            return redirect('/images/new_images/')
        else:
            # Tratar caso em que não há imagem enviada na requisição
            messages.add_message(request, constants.ERROR, "Nenhuma imagem enviada")
            return redirect('/images/new_images/')
@login_required
def galeria(request):
    images = Imagem.objects.filter(classe=False)
    classes = Doenca.objects.all()
    if request.method == "GET":
        return render(request, 'galeria_images.html',{'images':images, 'classes':classes})
    elif request.method == "POST":
        imagem_id = request.POST.get('image_id')  
        classe_id = request.POST.get('classe_id')  
        # comentarios = request.POST.get('comentarios')
        
        # Supondo que você tenha o especialista (usuário logado) disponível na request
        especialista = request.user
        
        #Crie uma instância da classe Analise com os dados fornecidos
        imagem = Imagem.objects.get(pk=imagem_id)  # Obter a imagem com base no ID fornecido
        analise = Analise(
            imagem_id=imagem_id,
            doenca_id=classe_id,
            especialista=especialista,
            # comentarios=comentarios
        )
               
        analise.save()
        imagem.classe = True
        imagem.save()
        messages.add_message(request, constants.SUCCESS, "Imagem Classificada")
        return redirect('/images/galeria/')
    else:
        messages.add_message(request, constants.ERROR, "ERROR: error interno do sistema")
        return redirect('/images/galeria/')
@login_required
def dashboard(request):
  # Agrupa as análises por doença e conta o número de análises para cada doença
  dados = Analise.objects.values('doenca__nome').annotate(total_analises=Count('id'))

  # Cria um array com as informações para cada doença
  info_doenca = []
  for dado in dados:
    info_doenca.append({
      'nome': dado['doenca__nome'],
      'total_analises': dado['total_analises'],
    })

  # Obtém os nomes das classes de doenças
  categorias = [dado['nome'] for dado in info_doenca if 'nome' in dado]


  return render(request, 'dashboard.html', {'categorias': categorias, 'info_doenca': info_doenca})
@login_required
def download(request):
    if request.method == 'GET':
        # Recuperar todas as análises do banco de dados
        analises = Analise.objects.all()

        # Criar um dicionário para armazenar a contagem de imagens por classe
        contagem_por_classe = {}

        # Contar as imagens por classe
        for analise in analises:
            classe = analise.doenca.nome
            if classe not in contagem_por_classe:
                contagem_por_classe[classe] = 0
            contagem_por_classe[classe] += 1

        return render(request, 'download.html', {'contagem_por_classe': contagem_por_classe})
    elif request.method == "POST":
        # Recuperar todas as análises do banco de dados
        analises = Analise.objects.all()

        # Criar um dicionário para armazenar as imagens agrupadas por classe
        imagens_por_classe = {}

        # Agrupar as imagens por classe
        for analise in analises:
            classe = analise.doenca.nome
            imagem = analise.imagem.image
            if classe not in imagens_por_classe:
                imagens_por_classe[classe] = []
            imagens_por_classe[classe].append(imagem)

        # Criar um arquivo ZIP temporário
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            with zipfile.ZipFile(temp_file, 'w') as zip_file:
                # Adicionar cada imagem ao arquivo ZIP
                for classe, imagens in imagens_por_classe.items():
                    # Criar um subdiretório temporário para cada classe
                    with tempfile.TemporaryDirectory() as temp_dir:
                        for imagem in imagens:
                            caminho_imagem = imagem.path  # Supondo que "imagem" seja um objeto FileField
                            nome_arquivo = os.path.basename(caminho_imagem)
                            caminho_destino = os.path.join(temp_dir, nome_arquivo)
                            shutil.copy(caminho_imagem, caminho_destino)  # Copiar a imagem para o subdiretório temporário

                        # Adicionar o subdiretório temporário ao arquivo ZIP
                        for root, _, files in os.walk(temp_dir):
                            for file in files:
                                caminho_completo = os.path.join(root, file)
                                caminho_relativo = os.path.relpath(caminho_completo, temp_dir)
                                zip_file.write(caminho_completo, arcname=os.path.join(classe, caminho_relativo))

        # Ler o conteúdo do arquivo ZIP temporário
        with open(temp_file.name, 'rb') as zip_data:
            zip_content = zip_data.read()

        # Configurar a resposta HTTP para o arquivo ZIP
        response = HttpResponse(zip_content, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="imagens_por_classe.zip"'
        return response

