# -*- coding: utf-8 -*-
# Copyright (c) 2016, Helio de Jesus and contributors
# For license information, please see license.txt


#Date Changed: 27/12/2022


from __future__ import unicode_literals

import frappe

from paddleocr import PaddleOCR,draw_ocr

import os


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
