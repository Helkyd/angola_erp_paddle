# -*- coding: utf-8 -*-
# Copyright (c) 2016, Helio de Jesus and contributors
# For license information, please see license.txt


#Date Changed: 12/01/2023


from __future__ import unicode_literals

import frappe

from paddleocr import PaddleOCR,draw_ocr

import os
import numpy as np
import re

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

		print ('Opcao CODE')
		#OCR IMAGE
		#ocr = PaddleOCR(lang='en')
		ocr = PaddleOCR(lang='en',show_log=False)
		img_path = filefinal
		result = ocr.ocr(img_path, cls=False)
		'''
		for idx in range(len(result)):
			res = result[idx]
			for line in res:
				print(line)
		'''

		# draw result
		result = result[0]
		boxes = [line[0] for line in result]
		txts = [line[1][0] for line in result]
		scores = [line[1][1] for line in result]
		print ('Textos no file ',txts)
		tmp_matricula = txts

		#RETURNS Vehicle PLATE ....
		matricula_final = 'MATRICULA INVALIDA'
		tmp_matricula_final = ''
		regex = r"^[a-zA-Z]{2}[\\s-]{0,1}[0-9]{2}[\\s-]{0,1}[0-9]{1,2}[\\s-]{0,1}[a-zA-Z]{2}$|^[a-zA-Z]{3}[\\s-]{0,1}[0-9]{2}[\\s-]{0,1}[0-9]{1,2}[\\s-]{0,1}$|^[0-9]{3}[\\s-]{0,1}[a-zA-Z]{2}[\\s-]{0,1}[0-9]{2,3}$|^[a-zA-Z]{2}[\\s-]{0,1}[0-9]{3}[\\s-]{0,1}[0-9]{2}$"

		print ('len tmp_matricula ', len(tmp_matricula))
		print ('tmp_matricula ',tmp_matricula)
		for ttmatr in tmp_matricula:
			print ('ttmatr ',ttmatr)
			if ttmatr.find('Predict time of') == -1:
				#Possible plate
				print (ttmatr.split(',')[0])
				mm = ttmatr.split(',')[0].replace(':','-').replace(' ','') # ttmatr.replace(':','-').replace(',','')
				#Trying to match plate regex
				matches = re.finditer(regex,mm.split()[0])
				for matchNum, match in enumerate(matches, start=1):
					print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
					for groupNum in range(0, len(match.groups())):
						groupNum = groupNum + 1
						print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
					matricula_final = match.group()
			else:
				#Special case when Plate has LD-XX in one line and XX-FF on the second line...
				print ('aqui')
				if len(tmp_matricula) == 2:
					if not matricula_final:
						#Starts with Letters
						if ttmatr.split(',')[0:2].isalpha():
							tmp_matricula_final = ttmatr.split(',')[0]
						elif tmp_matricula_final and ttmatr.split(',')[0:2].isalnum():
							#starts with Numbers like -01 or 12
							if ttmatr.split(',')[0].startswith('-'):
								tmp_matricula_final += ttmatr.split(',')[0]
							else:
								#adds - before
								tmp_matricula_final += '-' + ttmatr.split(',')[0]

			if tmp_matricula_final:
				print ('matricula final tem ', matricula_final)
				print ('tmp matricula final tem ', tmp_matricula_final)
				mm = tmp_matricula_final.split(',')[0].replace(':','-').replace(' ','') # ttmatr.replace(':','-').replace(',','')
				#Trying to match plate regex
				matches = re.finditer(regex,mm.split()[0])
				for matchNum, match in enumerate(matches, start=1):
					print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
					for groupNum in range(0, len(match.groups())):
						groupNum = groupNum + 1
						print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
					matricula_final = match.group()

		print ('Matricula final... ', matricula_final)
		return matricula_final


	else:
		print ('Por fazer....')
		frappe.throw('Por Fazer...')


@frappe.whitelist(allow_guest=True)
def paddle_ocr(data,opcao='batch',action = "OCR PLATES",tipodoctype = None):
	''' opcao pode ser batch to execute RUN or code to run via code '''

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

			if opcao == "batch":
				print ('Teste usando SHELL')
				from subprocess import run

				#ENG
				run_ppocr = 'python3 /home/frappe/frappe-bench/apps/paddleocr/tools/infer/predict_system.py --det_model_dir="/home/frappe/frappe-bench/apps/paddleocr/en_PP-OCRv3_det_infer/" ' \
				'--cls_model_dir="/home/frappe/frappe-bench/apps/paddleocr/ch_ppocr_mobile_v2.0_cls_infer/" ' \
				'--rec_model_dir="/home/frappe/frappe-bench/apps/paddleocr/en_PP-OCRv3_rec_infer/" ' \
				'--rec_char_dict_path="/home/frappe/frappe-bench/apps/paddleocr/ppocr/utils/en_dict.txt" --rec_image_shape="3,32,320" ' \
				'--image_dir=' + filefinal1

				#CHIN
				run_ppocr = 'cd /home/frappe/frappe-bench/apps/paddleocr && python3 /home/frappe/frappe-bench/apps/paddleocr/tools/infer/predict_system.py --det_model_dir="/home/frappe/frappe-bench/apps/paddleocr/ch_ppocr_server_v2.0_det_infer/" ' \
				'--cls_model_dir="/home/frappe/frappe-bench/apps/paddleocr/ch_ppocr_mobile_v2.0_cls_infer/" ' \
				'--rec_model_dir="/home/frappe/frappe-bench/apps/paddleocr/ch_ppocr_server_v2.0_rec_infer/" ' \
				'--rec_image_shape="3,32,320" ' \
				'--image_dir=' + filefinal1

				print ('run_ppocr ',run_ppocr)
				dados = run(run_ppocr,capture_output=True,shell=True)
				print ('dados.stdout')
				print (dados.stdout)
				print ('dados.stderr')
				print (dados.stderr)
				print (len(dados.stdout.decode('utf-8').split('ppocr DEBUG:')))
				print (dados.stdout.decode('utf-8').split('ppocr DEBUG:'))

				tmp_matricula = dados.stdout.decode('utf-8').split('ppocr DEBUG:')[len(dados.stdout.decode('utf-8').split('ppocr DEBUG:'))-2], dados.stdout.decode('utf-8').split('ppocr DEBUG:')[len(dados.stdout.decode('utf-8').split('ppocr DEBUG:'))-1]

			else:
				print ('Opcao CODE')
				#OCR IMAGE
				#ocr = PaddleOCR(lang='en')
				#ocr = PaddleOCR(lang='en',show_log=False)
				#ocr = PaddleOCR(lang='en',show_log=False,rec_image_shape='3,32,320')
				ocr = PaddleOCR(lang='ch',show_log=False)
				img_path = filefinal
				result = ocr.ocr(img_path, cls=False)
				'''
				for idx in range(len(result)):
					res = result[idx]
					for line in res:
						print(line)
				'''

				# draw result
				result = result[0]
				boxes = [line[0] for line in result]
				txts = [line[1][0] for line in result]
				scores = [line[1][1] for line in result]
				print ('Textos no file ',txts)
				tmp_matricula = txts

			#RETURNS Vehicle PLATE ....
			matricula_final = 'MATRICULA INVALIDA'
			tmp_matricula_final = ''
			regex = r"^[a-zA-Z]{2}[\\s-]{0,1}[0-9]{2}[\\s-]{0,1}[0-9]{1,2}[\\s-]{0,1}[a-zA-Z]{2}$|^[a-zA-Z]{3}[\\s-]{0,1}[0-9]{2}[\\s-]{0,1}[0-9]{1,2}[\\s-]{0,1}$|^[0-9]{3}[\\s-]{0,1}[a-zA-Z]{2}[\\s-]{0,1}[0-9]{2,3}$|^[a-zA-Z]{2}[\\s-]{0,1}[0-9]{3}[\\s-]{0,1}[0-9]{2}$"

			print ('len tmp_matricula ', len(tmp_matricula))
			print ('tmp_matricula ',tmp_matricula)
			for ttmatr in tmp_matricula:
				print ('ttmatr ',ttmatr)
				if ttmatr.find('Predict time of') == -1:
					#Possible plate
					print ('MM ', ttmatr.split(',')[0])
					mm = ttmatr.split(',')[0].replace(':','-').replace(' ','').replace('·','-') # ttmatr.replace(':','-').replace(',','')

					#Exception if ends with -LETTER+5(might be Z)
					if mm.endswith('5'):
						mm1 = mm[:len(mm)-1]
						mm = mm1 + 'Z'

					#Trying to match plate regex
					matches = re.finditer(regex,mm.split()[0])
					for matchNum, match in enumerate(matches, start=1):
						print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
						for groupNum in range(0, len(match.groups())):
							groupNum = groupNum + 1
							print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
						matricula_final = match.group()

					#Special case when Plate has LD-XX in one line and XX-FF on the second line...
					print ('aqui')
					if len(tmp_matricula) == 2:
						if matricula_final == 'MATRICULA INVALIDA':
							#Starts with Letters
							tt = ttmatr.split(',')[0]
							if tt[0:2].isalpha():
								tmp_matricula_final = ttmatr.split(',')[0]
							elif tmp_matricula_final and tt[0:2].isalnum():
								#starts with Numbers like -01 or 12
								if ttmatr.split(',')[0].startswith('-'):
									tmp_matricula_final += ttmatr.split(',')[0]
								else:
									#adds - before
									tmp_matricula_final += '-' + ttmatr.split(',')[0]

			if tmp_matricula_final:
				print ('matricula final tem ', matricula_final)
				print ('tmp matricula final tem ', tmp_matricula_final)
				mm = tmp_matricula_final.split(',')[0].replace(':','-').replace(' ','') # ttmatr.replace(':','-').replace(',','')
				#Trying to match plate regex
				matches = re.finditer(regex,mm.split()[0])
				for matchNum, match in enumerate(matches, start=1):
					print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
					for groupNum in range(0, len(match.groups())):
						groupNum = groupNum + 1
						print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
					matricula_final = match.group()

			print ('Matricula final... ', matricula_final)
			return matricula_final

			#return (dados.stdout.decode('utf-8').split('ppocr DEBUG:')[len(dados.stdout.decode('utf-8').split('ppocr DEBUG:'))-2], dados.stdout.decode('utf-8').split('ppocr DEBUG:')[len(dados.stdout.decode('utf-8').split('ppocr DEBUG:'))-1])


			#OCR IMAGE
			#ocr = PaddleOCR(lang='en')
			ocr = PaddleOCR(lang='en',show_log=False)
			img_path = filefinal
			result = ocr.ocr(img_path, cls=False)
			'''
			for idx in range(len(result)):
				res = result[idx]
				for line in res:
					print(line)
			'''

			# draw result
			result = result[0]
			boxes = [line[0] for line in result]
			txts = [line[1][0] for line in result]
			scores = [line[1][1] for line in result]
			print ('Textos no file ',txts)
			return (txts)

			#from PIL import Image
			#image = Image.open(img_path).convert('RGB')

			#im_show = draw_ocr(image, boxes, txts, scores, font_path='/home/frappe/frappe-bench/apps/paddleocr/doc/fonts/simfang.ttf')
			#im_show = Image.fromarray(im_show)
			#im_show.save('./tmp/result.jpg')
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

			print ('Textos no file000 ',txts)

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

@frappe.whitelist(allow_guest=True)
def paddle_ocr_PING():
	print ('CHEGOU AQu......')

	print ('Teste usando SHELL')
	from subprocess import run

	run_ppocr = 'python3 /home/frappe/frappe-bench/apps/paddleocr/tools/infer/predict_system.py --det_model_dir="/home/frappe/frappe-bench/apps/paddleocr/en_PP-OCRv3_det_infer/" ' \
	'--cls_model_dir="/home/frappe/frappe-bench/apps/paddleocr/ch_ppocr_mobile_v2.0_cls_infer/" ' \
	'--rec_model_dir="/home/frappe/frappe-bench/apps/paddleocr/en_PP-OCRv3_rec_infer/" ' \
	'--rec_char_dict_path="/home/frappe/frappe-bench/apps/paddleocr/ppocr/utils/en_dict.txt" ' \
	'--image_dir="/home/frappe/frappe-bench/sites/paddle.angolaerp.co.ao/public/files/1672239685486673.png"'

	print ('run_ppocr ',run_ppocr)
	dados = run(run_ppocr,capture_output=True,shell=True)
	print ('dados.stdout')
	print (dados.stdout)
	print ('dados.stderr')
	print (dados.stderr)
	print (len(dados.stdout.decode('utf-8').split('ppocr DEBUG:')))
	print (dados.stdout.decode('utf-8').split('ppocr DEBUG:'))
	print ('RETURN SREA')
	print (dados.stdout.decode('utf-8').split('ppocr DEBUG:')[len(dados.stdout.decode('utf-8').split('ppocr DEBUG:'))-2], dados.stdout.decode('utf-8').split('ppocr DEBUG:')[len(dados.stdout.decode('utf-8').split('ppocr DEBUG:'))-1])

	return (dados.stdout.decode('utf-8').split('ppocr DEBUG:')[len(dados.stdout.decode('utf-8').split('ppocr DEBUG:'))-2], dados.stdout.decode('utf-8').split('ppocr DEBUG:')[len(dados.stdout.decode('utf-8').split('ppocr DEBUG:'))-1])

	return "PONG"
