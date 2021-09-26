#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of DRK Impfterminerfassung.

import matplotlib.pyplot as plt
import sys
import numpy as np
from fpdf import FPDF
import time
import os
import os.path
import datetime
import matplotlib.gridspec as gridspec
sys.path.append("..")

Logo = '../utils/logo.png'

FreeSans = '../utils/Schriftart/FreeSans.ttf'
FreeSansBold = '../utils/Schriftart/FreeSansBold.ttf'


class MyPDF(FPDF):

	time='zeit'

	def header(self):
		self.add_font('GNU', '', FreeSans, uni=True)
		self.set_font('GNU', '', 11)
		self.cell(40, 10, 'Impfzentrum des DRK Odenwaldkreis:', ln=1)
		self.image(Logo, x=7, y=10, w=100, h=24, type='PNG')
		self.ln(20)


	def footer(self):
		self.set_y(-15)
		self.add_font('GNU', '', FreeSans, uni=True)
		self.set_font('GNU', '', 11)

		page= 'Seite %s/ {nb}' % self.page_no()

		self.cell(0, 10, page, align='R')


class PDFgenerator:

	def __init__(self, content, date):
		self.content=content
		self.date=date

		# Pie chart, where the slices will be ordered and plotted counter-clockwise:
		self.labels = self.content[0]
		self.sizes = self.content[1]
		self.fig1, self.ax1 = plt.subplots()
		self.ax1.pie(self.sizes, explode=self.explode, labels=self.labels, autopct=lambda p: '{:.2f}%  ({:,.0f})'.format(p, p * sum(self.sizes)/100),
                    shadow=True, startangle=90)
		# Equal aspect ratio ensures that pie is drawn as a circle.
		self.ax1.axis('equal')
		self.ax1.set_title("Gesamtanzahl der Impfungen: %s" % (self.tests), pad=32)
		plt.savefig('tmp/' + str(self.date) + '.png', dpi=(170))

	def generate(self):

		pdf=MyPDF()
		#pdf.time=self.date
		# pdf.name=self.name
		pdf.alias_nb_pages()
		pdf.add_page()
		pdf.set_auto_page_break(True, 25)
		pdf.add_font('GNU', '', FreeSans, uni=True)
		pdf.add_font('GNU', 'B', FreeSansBold, uni=True)

		pdf.set_font('GNU', 'B', 14)

		pdf.cell(20, 10, 'Tagesprotokoll für %s' % (self.date), ln=1)

		pdf.set_font('GNU', '', 14)

		pdf.cell(20, 10, 'Erstellt: {}'.format(datetime.datetime.now().strftime("%Y-%m-%d um %H:%M:%S"), ln=1))
		pdf.set_font('GNU', 'B' , 20)
		pdf.ln(15)
		pdf.set_font('GNU', 'B', 14)
		pdf.cell(35, 10, 'Testzentrum: %s, %s' %(self.station,self.address), 0, 1)

		current_x =pdf.get_x()
		current_y =pdf.get_y()

		pdf.line(current_x, current_y, current_x+190, current_y)
		pdf.ln(20)
		pdf.image('tmp/' + str(self.date) + '.png', w=210, h=160)
		os.remove('tmp/'+str(self.date) + '.png')
		pdf.set_font('GNU', '', 14)
		self.filename = "../../Reports/Tagesreport_Impfzentrum_" + str(self.date) + ".pdf"
		pdf.output(self.filename)
		return self.filename

aux=FPDF('P', 'mm', 'A4')
