# -*- coding: utf-8 -*-
# Copyright (c) 2016, Helio de Jesus and contributors
# For license information, please see license.txt


#Date Changed: 27/12/2022


from __future__ import unicode_literals

import frappe

from paddleocr import PaddleOCR,draw_ocr

import os
import numpy as np

@frappe.whitelist(allow_guest=True)
def paddle_ocr_TEST(data,action = "OCR PLATES",tipodoctype = None):
	print ('OCR para Vehicle Plates...')
	if action == "OCR PLATES":
		if os.path.isfile(frappe.get_site_path('public','files') + data.replace('/files','')):
			filefinal = frappe.get_site_path('public','files') + data.replace('/files','')
			print ('filefinal ',filefinal)
			if filefinal.startswith('.'):
				filefinal1 = "/home/frappe/frappe-bench/sites" + filefinal[1:len(filefinal)]
				filefinal = filefinal1
			print ('filefinal1 ',filefinal)

		else:
			filefinal = data

		#OCR IMAGE
		ocr = PaddleOCR(lang='en')
		img_path = filefinal
		result = ocr.ocr(img_path, cls=False)
		for idx in range(len(result)):
			res = result[idx]
			for line in res:
				print(line)

		# draw result
		from PIL import Image
		result = result[0]
		image = Image.open(img_path).convert('RGB')
		boxes = [line[0] for line in result]
		txts = [line[1][0] for line in result]
		scores = [line[1][1] for line in result]

		#im_show = draw_ocr(image, boxes, txts, scores, font_path='/home/frappe/frappe-bench/apps/paddleocr/doc/fonts/simfang.ttf')
		#im_show = Image.fromarray(im_show)
		#im_show.save('./tmp/result.jpg')
		print ('Textos no file ',txts)


	else:
		print ('Por fazer....')
		frappe.throw('Por Fazer...')


@frappe.whitelist(allow_guest=True)
def paddle_ocr(data: str,action = "OCR PLATES",tipodoctype = None):
	print ('OCR para Vehicle Plates...')
	print (data)
	if action == "OCR PLATES":
		if data:
			if os.path.isfile(frappe.get_site_path('public','files') + data.replace('/files','')):
				filefinal = frappe.get_site_path('public','files') + data.replace('/files','')
				print ('filefinal ',filefinal)
				if filefinal.startswith('.'):
					filefinal1 = "/home/frappe/frappe-bench/sites" + filefinal[1:len(filefinal)]
					filefinal = filefinal1
				print ('filefinal1 ',filefinal)

			else:
				filefinal = data

			#OCR IMAGE
			ocr = PaddleOCR(lang='en')
			img_path = filefinal
			result = ocr.ocr(img_path, cls=False)
			for idx in range(len(result)):
				res = result[idx]
				for line in res:
					print(line)

			# draw result
			from PIL import Image
			result = result[0]
			image = Image.open(img_path).convert('RGB')
			boxes = [line[0] for line in result]
			txts = [line[1][0] for line in result]
			scores = [line[1][1] for line in result]

			#im_show = draw_ocr(image, boxes, txts, scores, font_path='/home/frappe/frappe-bench/apps/paddleocr/doc/fonts/simfang.ttf')
			#im_show = Image.fromarray(im_show)
			#im_show.save('./tmp/result.jpg')
			print ('Textos no file ',txts)
			return txts
		else:
			#Image DAta
			print ('DATA imagem ')
			#OCR IMAGE
			ocr = PaddleOCR(lang='en')
			img_path = img
			result = ocr.ocr(img_path, cls=False)
			for idx in range(len(result)):
				res = result[idx]
				for line in res:
					print(line)

			# draw result
			print ('Textos no file ',txts)
			if img:
				return txts
			from PIL import Image
			result = result[0]
			image = Image.open(img_path).convert('RGB')
			boxes = [line[0] for line in result]
			txts = [line[1][0] for line in result]
			scores = [line[1][1] for line in result]

			#im_show = draw_ocr(image, boxes, txts, scores, font_path='/home/frappe/frappe-bench/apps/paddleocr/doc/fonts/simfang.ttf')
			#im_show = Image.fromarray(im_show)
			#im_show.save('./tmp/result.jpg')
			print ('Textos no file ',txts)

	else:
		print ('Por fazer....')
		frappe.throw('Por Fazer...')



@frappe.whitelist()
def ocrpdf_tools(ficheiro,action = "SCRAPE", empresa = None, tipodoctype = None, lugarficheiro = None):
	#FIX 22-10-2022
	# importing required modules
	import PyPDF2
	import requests
	import base64

	headers= {
		'Authorization': "token d10edbec5ca1f72:3eb5598eecfb8e9",
		'Accept': 'application/json'

	}
	'''
	with open(ficheiro, "rb") as image_file3:
		encoded_string = base64.b64encode(image_file3.read())
	'''

	site1 = "https://tools.angolaerp.co.ao/api/method/upload_file"
	#Remove spaces from filename ...
	#REMOVED FOR NOW OTHERWISE NO SCAN WILL BE DONE.. 16-04-2022
	#ficheiro1 = str(unicodedata.normalize('NFKD',ficheiro).encode('ascii','ignore').decode('utf-8'))
	ficheiro1 = ficheiro
	print ('ficheiro ', ficheiro1)
	ficheiro = ficheiro1
	print ('privado ', 'private' in ficheiro)
	if 'private' in ficheiro:
		if ficheiro.startswith('/private') or ficheiro.startswith('private'):
			print (frappe.get_site_path('private','files') + ficheiro.replace('/private/files',''))
			print (os.path.isfile(frappe.get_site_path('private','files') + ficheiro.replace('/private/files','')))
			if os.path.isfile(frappe.get_site_path('private','files') + ficheiro.replace('/private/files','')):
				filefinal = frappe.get_site_path('private','files') + ficheiro.replace('/private/files','')
			else:
				filefinal = ficheiro
		else:
			filefinal = ficheiro
	elif 'public' in ficheiro:
		if ficheiro.startswith('/public') or ficheiro.startswith('public'):
			if os.path.isfile(frappe.get_site_path('public','files') + ficheiro.replace('/public/files','')):
				filefinal = frappe.get_site_path('public','files') + ficheiro.replace('/public/files','')
			else:
				filefinal = ficheiro
		else:
			filefinal = ficheiro

	print ('Fiche Private/Public ', filefinal)
	ficheiro = filefinal
