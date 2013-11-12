# -*- coding:utf-8 -*-
#!/usr/bin/env python -O

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
        start=5120
        max=27120
        data=[]
        
        for seek in range(start, max):
            f.seek(seek)
            data.append(ord(f.read(1)))
        #Хуячим в лоб!!! Тупо, пол бутылки вина - оправданье.
        # Ни когда не смотреть сюда - хуйня
        for i in range(0,2000):#бля!!! тут должен быть класс... сука- там только 2000 z-отчетов
            count=i*11 #быдло код, типа выясняем порядковый номер зетки, бля... только не забыть прибавить 1
            corr=data[count:count+11]#это список. Eжу понятно, строчками ниже вспоминаем битовую математику, нам надо xor-ить и выкинуть стырший разряд
            """Тут настал -пиздец.... Вино кончилось, понесся костыльный быдл код"""
            correct=corr[0]
            for ii in range(9):
                correct=correct^corr[ii+1]

        self.entry.set_text(str(correct))

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

