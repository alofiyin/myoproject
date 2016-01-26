#_*_coding:utf-8_*_
#$Id: SrvEventlet.py 3316 2015-08-02 10:27:53Z fyin $
# Copyright (c) 2015 fiyin <alofiyin@gmail.com>
#二维码识别模块 需要 zbar程序支持

import os,pdb
from PIL import Image
import subprocess


class Zbar():
	def __init__(self,im,scratch_image_name='temp.bmp',exe_name='zbarimg'):
		self.exe_name = exe_name 
		self.scratch_image_name = scratch_image_name 
		self.cleanup_scratch_flag = True  # Temporary files cleaned up after OCR operation
		self.im = im
	def call(self):
		#args = [self.exe_name, self.scratch_image_name,stdout=sp.PIPE,shell=True]
		#pdb.set_trace()
		#proc = subprocess.Popen(args,shell=True)
		proc = subprocess.Popen("%s %s" %(self.exe_name,self.scratch_image_name), stdout=subprocess.PIPE, shell=True)
		retcode = proc.wait()
		result = proc.stdout.read().decode().strip()
		if retcode!=0:
			return False
		return result

	def image_to_string(self,im=None):
		if im :
			self.im = im
		try:
			self.image_to_scratch()
			text = self.call()
		finally:
			if self.cleanup_scratch_flag:
				self.perform_cleanup()
		return text


		
	def image_to_scratch(self):
		"""Saves image in memory to scratch file.  .bmp format will be read correctly by Tesseract"""
		self.im.save(self.scratch_image_name, dpi=(200,200))

	def perform_cleanup(self):
		try:
			os.remove(self.scratch_image_name)
		except OSError:
			pass
