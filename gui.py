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
        self.listore.clear()
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
            for ii in range(1,9):
                correct=correct+corr[ii]

            correct=correct&0x00FF
            correct+=0xaa
            c=correct&0x00ff
            if c!=corr[10]:
                z=str(i+1)
                date="%s/%s/%s"%(hex(corr[0])[2:],hex(corr[1])[2:],hex(corr[2])[2:])
                summ="%s%s%s%s%s%s.%s"%(hex(corr[9])[2:],hex(corr[8])[2:],hex(corr[7])[2:],hex(corr[6])[2:],hex(corr[5])[2:],hex(corr[4])[2:],hex(corr[3])[2:])
                summ=float(summ)
                iter=self.listore.append([z, date,str(summ),str(hex(c)[2:])])
            self.treeview.show_all()

        f.close()


    def __init__(self):
        self.builder=gtk.Builder()
        self.builder.add_from_file('gui.glade')
        self.window=self.builder.get_object('window')
        self.window.set_size_request(400,400)
        self.entry=self.builder.get_object('entry')

        self.listore=self.builder.get_object('liststore')
        self.modelfilter=self.listore.filter_new()
        self.treeview=self.builder.get_object('treeview')
        self.filechoiserbutton=self.builder.get_object("filechooserbutton")
        self.filechoiserbutton.connect("file-set", self.select_file)

        trc=[]
        for i in range(4):
            trc.append(gtk.CellRendererText())
        column=gtk.TreeViewColumn("Номер Z", trc[0], text=0)
        self.treeview.append_column(column)

        column=gtk.TreeViewColumn("Дата ", trc[1], text=1)
        self.treeview.append_column(column)

        column=gtk.TreeViewColumn("Сумма", trc[2], text=2)
        self.treeview.append_column(column)

        column=gtk.TreeViewColumn("Контрольная сумма", trc[3], text=3)
        self.treeview.append_column(column)
        if(self.window):
            self.window.connect('destroy', self.close_app)
        self.window.show_all()

    def main(self):
        gtk.main()

if __name__=='__main__':
    app=Guifp()
    app.main()

