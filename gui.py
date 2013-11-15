# -*- coding:utf-8 -*-
#!/usr/bin/env python -O
import re
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
    def key_treeview(self,widget, event):
        key=gtk.gdk.keyval_name(event.keyval)
        if key=="Return":
            self.test.set_text("OK")
            treeselection=self.treeview.get_selection()
            mode=treeselection.get_mode()
            (model, iter)=treeselection.get_selected()
            self.test.set_text('Редактируем смену №: %s'%model[iter][0])
            self.redow.show()
            self.window.set_sensitive(0)
            iter=self.listredo.append([model[iter][1], model[iter][2], True])

    def close_child(self, widget, data=None):
        self.redow.hide()
        self.window.set_sensitive(1)
        return True
    def row_change(self, cell, path, text,data):
        liststore, column =data
        liststore[path][column]=text
        return
    def save(self, widget):
        treeselection=self.treechild.get_selection()
        (model, iter)=treeselection.get_selected()
        date=model[iter][0]
        summ=model[iter][1]
        treeselection=self.treeview.get_selection()
        (model, iter)=treeselection.get_selected()
        model[iter][1]=date
        model[iter][2]=summ
        sp=date.split('/')
        data=[]
        for i in sp:
            data.append(int(i,16))
        sp=summ.split('.')
        data.append(int(sp[1], 16))
        if len(sp[0])%2==1:
            sp='0'+sp[0]
        else:
            sp=sp[0]
        sp=re.findall('(\d{2})', sp)
        sp.reverse()
        for i in range(len(sp)):
            sp[i]=int(sp[i],16)
        data=data+sp
        for i in range(10-len(data)):
            data.append(0)

        corr=0
        st=''
        for i in data:
            corr+=i
            st+=st+' '+str(i)
        c=corr&0x00FF
        c+=0xaa
        self.test.set_text("дата: %s"%(st))


        self.redow.hide()
        self.window.set_sensitive(1)
        return True

    def __init__(self):
        self.builder=gtk.Builder()
        self.builder.add_from_file('gui.glade')
        self.window=self.builder.get_object('window')
        self.window.set_size_request(400,400)
        self.redow=self.builder.get_object('redow')
        self.entry=self.builder.get_object('entry')


        self.cancel=self.builder.get_object('cancel')
        self.cancel.connect('clicked', self.close_child)
        self.btsave=self.builder.get_object('save')
        self.btsave.connect('clicked', self.save)

        self.test=self.builder.get_object('test')

        self.listore=self.builder.get_object('liststore')
        self.listredo=self.builder.get_object('listredo')
        self.modelfilter=self.listore.filter_new()
        self.treeview=self.builder.get_object('treeview')
        self.treechild=self.builder.get_object('treechild')
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

        self.treeview.connect('key_release_event', self.key_treeview)
        self.redow.connect('destroy', self.close_child)
        self.redow.connect('delete_event', self.close_child)

        reotcr=[]
        for i in range(2):
            reotcr.append(gtk.CellRendererText())

        model=self.treechild.get_model()
        reotcr[0].connect('edited', self.row_change, (model,0))
        column=gtk.TreeViewColumn("Дата", reotcr[0], text=0, editable=2)
        self.treechild.append_column(column)

        column=gtk.TreeViewColumn("Сумма", reotcr[1], text=1, editable=2)
        self.treechild.append_column(column)


        if(self.window):
            self.window.connect('destroy', self.close_app)
        self.window.show()

    def main(self):
        gtk.main()

if __name__=='__main__':
    app=Guifp()
    app.main()

