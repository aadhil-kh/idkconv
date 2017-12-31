#!/usr/bin/python3
from gi.repository import Gtk
import os,sys
class Gui:
	def __init__(self):
		self.boo=False
		self.builder=Gtk.Builder()
		self.builder.add_from_file('interface.ui')
		self.builder.connect_signals(self)
		self.window=self.builder.get_object('window')
		self.about=self.builder.get_object('aboutdialog')
		self.combo=self.builder.get_object('combo')
		cellrenderertext = Gtk.CellRendererText()
		self.combo.pack_start(cellrenderertext, True)
		self.combo.add_attribute(cellrenderertext, "text", 0)
		self.window.show_all()
	def on_window_destroy(self,window):
		Gtk.main_quit()
	def on_file_set(self,mfile):
		self.name=mfile.get_filename()
		source=self.builder.get_object('source')
		buf=Gtk.EntryBuffer()
		buf.set_text(self.name,-1)
		source.set_buffer(buf)
		self.boo=True
		if self.name[-3:]=="ogg" or self.name[-3:]=="mp3" or self.name[-3:]=="wav":
			liststore=Gtk.ListStore(str)
			for item in ["mp3", "wav", "ogg"]:
				liststore.append([item])
			self.combo.set_model(liststore)
		elif self.name[-3:]=="mp4" or self.name[-3:]=="avi" or self.name[-3:]=="flv":
			liststore=Gtk.ListStore(str)
			for item in ["mp4","avi","vob","mkv","mp3","wav","ogg","webm"]:
				liststore.append([item])
			self.combo.set_model(liststore)
		elif self.name[-3:]=="mkv" or self.name[-3:]=="webm" or self.name[-3:]=="vob":
			liststore=Gtk.ListStore(str)
			for item in ["mp4","avi","vob","mkv","mp3","wav","ogg","webm"]:
				liststore.append([item])
			self.combo.set_model(liststore)
		else:
			msg=Gtk.MessageDialog()
			msg.set_property("message_type",Gtk.MessageType.WARNING)
			msg.set_property("text","Format you specified is not supported")
			msg.run()
			msg.destroy()
			self.boo=False
	def get_active_text(self):
		model = self.combo.get_model()
		active = self.combo.get_active()
		if active < 0:
			return None
		return model[active][0]
	def on_convert_clicked(self,button):
		if self.boo:
			output_path=os.path.dirname(self.name)
			output_filename=os.path.basename(self.name)
			output_filename=output_path+"/"+output_filename.split(".")[0]+"."+self.get_active_text()
			os.system("avconv -i \""+self.name+"\" \""+output_filename+"\"")
			print(self.name)
		else:
			msg=Gtk.MessageDialog()
			msg.set_property("message_type",Gtk.MessageType.WARNING)
			msg.set_property("text","Format you specified is not supported")
			msg.run()
			msg.destroy()
	def on_about_clicked(self,about):
		self.about.run()
	def on_aboutdialog_delete_event(self,about,a):
		self.about.hide()
def main():
	app=Gui()
	Gtk.main()
sys.exit(main())
