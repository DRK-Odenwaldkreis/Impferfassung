#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of DRK Testzentrum.

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
		self.cell(40, 10, 'Impfzentrum DRK KV Odenwaldkreis e.V.:', ln=1)
		self.image(Logo, x=7, y=10, w=100, h=24, type='PNG')
		self.ln(20)


	def footer(self):
		self.set_y(-15)
		self.add_font('GNU', '', FreeSans, uni=True)
		self.set_font('GNU', '', 11)

		page= 'Seite %s/ {nb}' % self.page_no()

		self.cell(0, 10, page, align='R')


class PDFgenerator:

	def __init__(self, doses, booster, ages, waiting, noshow, extra, vaccine, date):
		self.doses = doses
		self.vaccine  = vaccine
		self.booster = booster
		self.ages = ages
		self.waiting = waiting
		self.noshow = noshow
		self.extra = extra
		self.date = date
	
		self.fig, self.ax = plt.subplots(3,2)
		plt.subplots_adjust(wspace=0.4,hspace=1.5,left=0.11,top=0.95, bottom=0.2)

		# bar chart vaccine doses per station
		try:
			self.station = []
			self.amount = []
			self.totalAmount = 0
			for i in self.doses:
				self.station.append(i[1])
				self.amount.append(i[0])
				self.totalAmount+=i[0]

			self.labels = self.station
			self.height = np.arange(len(self.labels)) 
			self.sizes = np.array(self.amount)
			self.bar = self.ax[0,0].bar(self.labels, self.sizes)
			self.ax[0,0].set_title("Impfungen: %s" % (self.totalAmount))
			self.ax[0,0].set_ylabel("Anzahl")
			self.ax[0,0].axis(ymin=0,ymax=np.max(self.sizes)*1.5)
			self.ax[0,0].set_xticklabels(self.labels, rotation=30, ha='right',fontsize=6)
			for bar in self.bar:
				height = bar.get_height()
				label_x_pos = bar.get_x() + bar.get_width() / 2
				self.ax[0,0].text(label_x_pos, height, s=f'{height} ({round(height/(self.totalAmount)*100,1)}%)', ha='center',va='bottom',fontsize=6)
		except:
			pass
	
		# Pie chart booster
		try:
			self.sizes = []
			self.labels = []
			for i in self.booster:
				if i[1] == 0:
					self.labels.append("Basis")
					self.sizes.append(i[0])
				if i[1] == 1:
					self.labels.append("Booster")
					self.sizes.append(i[0])	
			self.sizes = np.array(self.sizes)
			self.ax[0,1].pie(self.sizes, labeldistance=2.0,pctdistance=3.5,labels=self.labels, autopct=lambda p: '{:.2f}%  ({:,.0f})'.format(p, p * sum(self.sizes)/100),shadow=False, startangle=90)		
		except:
			self.sizes = [0,0]
			self.labels = ["Basis","Booster"]
			self.ax[0,1].pie(self.sizes, labeldistance=2.0,pctdistance=3.5,labels=self.labels, autopct=lambda p: '{:.2f}%  ({:,.0f})'.format(p, p * sum(self.sizes)/100),shadow=False, startangle=90)		


		# Histogram Altersverteilung
		try:
			self.ageArray = np.array(self.ages)
			self.ax[1,0].hist(self.ageArray, 10, color = "green")
			self.ax[1,0].set_xlabel("Alter")
			self.ax[1,0].set_ylabel("Anzahl")
			self.ax[1,0].set_title("Altersschnitt: %s Jahre" %(int(self.ageArray.mean())))
		except:
			self.ax[1,0].set_xlabel("Alter")
			self.ax[1,0].set_ylabel("Anzahl")
			self.ax[1,0].set_title("Altersschnitt: ")

			# Histogram Altersverteilung
		try:
			self.sizes = []
			for i in self.waiting:
				self.sizes.append(i[0])
			self.waitingArray = np.array(self.sizes)
			self.ax[1,1].hist(self.waitingArray, 10, color = "blue")
			self.ax[1,1].set_xlabel("Tage")
			self.ax[1,1].set_ylabel("Anzahl")
			self.ax[1,1].set_title("Wartezeit bis Impfung: %s Tage" %(int(self.waitingArray.mean())))
		except:
			self.ax[1,1].set_xlabel("Tage")
			self.ax[1,1].set_ylabel("Anzahl")
			self.ax[1,1].set_title("Wartezeit bis Impfung:")

		# Bar chart for No-show
		try:
			self.station = []
			self.amount = []
			self.totalAmount = 0
			for i in self.noshow:
				self.station.append(i[1])
				self.amount.append(i[0])
				self.totalAmount+=i[0]

			self.labels = self.station
			self.height = np.arange(len(self.labels)) 
			self.sizes = np.array(self.amount)
			self.bar = self.ax[2,0].bar(self.labels, self.sizes)
			self.ax[2,0].set_title("Nicht erschienen: %s" % (self.totalAmount))
			self.ax[2,1].set_ylabel("Anzahl")
			self.ax[2,0].axis(ymin=0,ymax=np.max(self.sizes)*1.5)
			self.ax[2,0].set_xticklabels(self.labels, rotation=30, ha='right',fontsize=6)
			for bar in self.bar:
				height = bar.get_height()
				label_x_pos = bar.get_x() + bar.get_width() / 2
				self.ax[2,0].text(label_x_pos, height, s=f'{height} ({round(height/(self.totalAmount)*100,1)}%)', ha='center',va='bottom',fontsize=6)
		except:
			self.ax[2,0].set_title("Nicht erschienen:" )
			self.ax[2,1].set_ylabel("Anzahl")

		# Bar chart for Extra Appointments
		try:
			self.station = []
			self.amount = []
			self.totalAmount = 0
			for i in self.extra:
				self.station.append(i[1])
				self.amount.append(i[0])
				self.totalAmount+=i[0]
			self.labels = self.station
			self.height = np.arange(len(self.labels)) 
			self.sizes = np.array(self.amount)
			self.bar = self.ax[2,1].bar(self.labels, self.sizes)
			self.ax[2,1].axis(ymin=0,ymax=np.max(self.sizes)*1.5)
			self.ax[2,1].set_ylabel("Anzahl")
			self.ax[2,1].set_title("Nachrückertermine: %s" % (self.totalAmount))
			self.ax[2,1].set_xticklabels(self.labels, rotation=30, ha='right',fontsize=6)
			for bar in self.bar:
				height = bar.get_height()
				label_x_pos = bar.get_x() + bar.get_width() / 2
				self.ax[2,1].text(label_x_pos, height, s=f'{height} ({round(height/(self.totalAmount)*100,1)}%)', ha='center',va='bottom',fontsize=6)
		except:
			self.ax[2,1].set_ylabel("Anzahl")
			self.ax[2,1].set_title("Nachrückertermine:")
		plt.savefig('tmp/' + str(self.date) + '.png', dpi=(180))
		
	

	def generate(self):

		pdf=MyPDF()
		pdf.alias_nb_pages()
		pdf.add_page()
		pdf.set_auto_page_break(True, 25)
		pdf.add_font('GNU', '', FreeSans, uni=True)
		pdf.add_font('GNU', 'B', FreeSansBold, uni=True)

		pdf.set_font('GNU', 'B', 14)

		pdf.cell(20, 10, 'Impfprotokoll für %s am %s' % (self.vaccine, self.date), ln=1)

		pdf.set_font('GNU', '', 14)

		pdf.cell(20, 10, 'Erstellt: {}'.format(datetime.datetime.now().strftime("%Y-%m-%d um %H:%M:%S"), ln=1))
		pdf.set_font('GNU', 'B' , 20)
		pdf.ln(15)
		pdf.set_font('GNU', 'B', 14)

		current_x =pdf.get_x()
		current_y =pdf.get_y()

		pdf.line(current_x, current_y, current_x+190, current_y)
		pdf.ln(20)
		pdf.image('tmp/' + str(self.date) + '.png', w=210, h=160)
		os.remove('tmp/'+str(self.date) + '.png')
		pdf.set_font('GNU', '', 14)
		self.filename = "../../Reports/Impfzentrum/Tagesreport_Impfen_" + str(self.vaccine).replace(" ","") + "_" + str(self.date) + ".pdf"
		pdf.output(self.filename)
		return self.filename

aux=FPDF('P', 'mm', 'A4')
