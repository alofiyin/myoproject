#_*_coding:utf-8_*_
#$Id: SrvEventlet.py 3316 2015-08-02 10:27:53Z fyin $
# Copyright (c) 2015 fiyin <alofiyin@gmail.com>
#图片文字识别模块 需要 Tesseract程序支持
# mod fiyin 
from PIL import Image
import os
import subprocess

class pytesser():
	def __init__(self,im,lang='eng',scratch_image_name='/tmp/temp.bmp',scratch_text_name_root='/tmp/temp',tesseract_exe_name='tesseract'):
		self.tesseract_exe_name = tesseract_exe_name # Name of executable to be called at command line
		self.scratch_image_name = scratch_image_name # This file must be .bmp or other Tesseract-compatible format
		self.scratch_text_name_root = scratch_text_name_root # Leave out the .txt extension
		self.lang = lang
		self.cleanup_scratch_flag = True  # Temporary files cleaned up after OCR operation
		self.im = im
	def call_tesseract(self):
		"""Calls external tesseract.exe on input file (restrictions on types),
		outputting output_filename+'txt'"""
		args = [self.tesseract_exe_name, self.scratch_image_name, self.scratch_text_name_root,'-l',self.lang]
		proc = subprocess.Popen(" ".join(args),shell=True)
		retcode = proc.wait()
		if retcode!=0:
			#check_for_errors()
			return False
		return True	

	def image_to_string(self,im=None):
		"""Converts im to file, applies tesseract, and fetches resulting text.
		If cleanup=True, delete scratch files after operation."""
		if im :
			self.im = im
		try:
			self.image_to_scratch()
			self.call_tesseract()
			text = self.retrieve_text()
		finally:
			if self.cleanup_scratch_flag:
				self.perform_cleanup()
		return text


		
	def image_to_scratch(self):
		"""Saves image in memory to scratch file.  .bmp format will be read correctly by Tesseract"""
		self.im.save(self.scratch_image_name, dpi=(200,200))
	def	retrieve_text(self):
		inf = open(self.scratch_text_name_root + '.txt')
		text = inf.read()
		inf.close()
		return text		

	def perform_cleanup(self):
		"""Clean up temporary files from disk"""
		for name in (self.scratch_image_name, self.scratch_text_name_root + '.txt', "tesseract.log"):
			try:
				os.remove(name)
			except OSError:
				pass


class Tesser_General_Exception(Exception):
	pass

class Tesser_Invalid_Filetype(Tesser_General_Exception):
	pass

def check_for_errors(logfile = "tesseract.log"):
	inf = file(logfile)
	text = inf.read()
	inf.close()
	# All error conditions result in "Error" somewhere in logfile
	if text.find("Error") != -1:
		raise Tesser_General_Exception(text)
				
if __name__=='__main__':
	im = Image.open('/home/opt/tesseract-ocr/phototest.tif')
	pt = pytesser(im,tesseract_exe_name='/usr/local/bin/tesseract')
	text = pt.image_to_string()
	print (text)
	exit()
	try:
		text = pt.image_file_to_string('fnord.tif', graceful_errors=False)
	except Tesser_General_Exception as value:
		print ("fnord.tif is incompatible filetype.  Try graceful_errors=True")
		print (value)
	text = pt.image_file_to_string('fnord.tif', graceful_errors=True)
	print ("fnord.tif contents:", text)
	text = tp.image_file_to_string('fonts_test.png', graceful_errors=True)
	print (text)


