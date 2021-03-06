from django.shortcuts import render
from django.http import HttpResponse
from taller_1.scrapers import run_spider
import json
from os.path import exists

def index(request):
	return render(request, 'taller_1/taller_1.html')

def traer_facultades(request):
	if request.method == 'POST':
		lista_facultades = {}
		post_text = request.POST.get('valor', 'No data found')
		if post_text == 'TRAER_FACULTADES':
			if not exists('taller_1/flat_files/facultades_items.json'):
				lista_facultades = run_spider.traer_facultades()
				archivo = open('taller_1/flat_files/facultades_items.json', 'w')
				archivo.write(json.dumps(lista_facultades))
				archivo.close()
			else:
				with open('taller_1/flat_files/facultades_items.json') as json_data:
					lista_facultades = json.load(json_data)
					json_data.close()
		return HttpResponse (
			json.dumps(lista_facultades),
			content_type = "application/json"
		)
	else:
		return HttpResponse (
			json.dumps({"Error": "Error en JSON"}),
			content_type = "application/json"
		)
