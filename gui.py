# -*- coding:utf-8 -*-
#!/usr/bin/env python -O

import pygtk
try:
      	import pygtk
        pygtk.require('2.0')
except:
        sys.exit(1)
try:
        import gtk
        import gtk.glade
except:
        sys.exit(1)


class Guifp:
    def close_app(self, widget):
        gtk.main_quit()
    def select_file(self, widget):
        self.entry.set_text('')
        f=open(self.filechoiserbutton.get_filename(), 'rb')
        seek=5120
        data=[]
        for i in range(11):
            f.seek(seek)
            seek=seek+1
            data.append(ord(f.read(1)))
        for i in data:
            get=self.entry.get_text()+str(hex(i))[2:]
            self.entry.set_text(get)
        f.close()


    def __init__(self):
        self.builder=gtk.Builder()
        self.builder.add_from_file('gui.glade')
        self.window=self.builder.get_object('window')
        self.window.set_size_request(400,400)
        self.entry=self.builder.get_object('entry')

        self.listote=self.builder.get_object('listore')
        self.treeview=self.builder.get_object('treeview')
        self.filechoiserbutton=self.builder.get_object("filechooserbutton")
        self.filechoiserbutton.connect("file-set", self.select_file)

        if(self.window):
            self.window.connect('destroy', self.close_app)
        self.window.show_all()

    def main(self):
        gtk.main()

if __name__=='__main__':
    app=Guifp()
    app.main()

