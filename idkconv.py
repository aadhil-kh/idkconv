#!/usr/bin/python3
from gi.repository import Gtk
import os,sys
class Gui:
	
	#constructor
	def __init__(self):
		self.file_selected=False
		
		#build the UI
		self.builder=Gtk.Builder()
		self.builder.add_from_file('interface.ui')
		self.builder.connect_signals(self)
		self.window=self.builder.get_object('window')
		self.about=self.builder.get_object('aboutdialog')
		self.combo=self.builder.get_object('combo')
		self.out_text=self.builder.get_object('destination')
		self.file_chooser=self.builder.get_object('file_choose')
		cellrenderertext = Gtk.CellRendererText()
		self.combo.pack_start(cellrenderertext, True)
		self.combo.add_attribute(cellrenderertext, "text", 0)
		self.window.show_all()
		self.window.set_resizable(False)
	#Exit on close
	def on_window_destroy(self,window):
		Gtk.main_quit()
		
	#Fires when file is selected
	def on_file_set(self,mfile):
		self.name=mfile.get_filename()
		if self.name[-3:]=="ogg" or self.name[-3:]=="mp3" or self.name[-3:]=="wav":
			liststore=Gtk.ListStore(str)
			for item in ["mp3", "wav", "ogg"]:
				liststore.append([item])
			self.combo.set_model(liststore)
			self.set_source()
		elif self.name[-3:]=="mp4" or self.name[-3:]=="avi" or self.name[-3:]=="flv":
			liststore=Gtk.ListStore(str)
			for item in ["mp4","avi","vob","mkv","mp3","wav","ogg","webm"]:
				liststore.append([item])
			self.combo.set_model(liststore)
			self.set_source()
		elif self.name[-3:]=="mkv" or self.name[-3:]=="webm" or self.name[-3:]=="vob":
			liststore=Gtk.ListStore(str)
			for item in ["mp4","avi","vob","mkv","mp3","wav","ogg","webm"]:
				liststore.append([item])
			self.combo.set_model(liststore)
			self.set_source()
		else:
			#clear text in source,destination and liststore
			self.combo.set_model(None)
			self.builder.get_object('source').set_text("")
			self.builder.get_object('destination').set_text("")
			self.file_chooser.unselect_all()
			self.file_selected=False
			msg=Gtk.MessageDialog()
			msg.set_property("message_type",Gtk.MessageType.ERROR)
			msg.set_property("text","Format you specified is not supported")
			msg.run()
			msg.destroy()
	
	#set the source filename
	def set_source(self):
		self.builder.get_object('source').set_text(self.name)
		self.builder.get_object('destination').set_text(self.name[:-4])
		self.file_selected=True
		self.combo.set_active(0)
		
	#to retrieve the extension selected
	def get_active_text(self):
		model = self.combo.get_model()
		active = self.combo.get_active()
		if active < 0:
			return False
		return model[active][0]
	
	#Fires on convert button clicked
	def on_convert_clicked(self,button):
		
		#Check if file and format to convert is selected 
		if self.file_selected and self.get_active_text():
			output_path=os.path.dirname(self.name)
			output_filename=os.path.basename(self.name)
			output_filename=output_path+"/"+output_filename.split(".")[0]+"."+self.get_active_text()
			
			#conversion happens here
			os.system("avconv -i \""+self.name+"\" \""+output_filename+"\"")
			print(self.name)
		else:
			msg=Gtk.MessageDialog()
			msg.set_property("message_type",Gtk.MessageType.WARNING)
			msg.set_property("text","Format you specified is not supported")
			msg.run()
			msg.destroy()
	
	#About dialog 		
	def on_about_clicked(self,about):
		self.about.run()
		
	def on_aboutdialog_delete_event(self,about,a):
		self.about.hide()
def main():
	app=Gui()
	Gtk.main()
sys.exit(main())
