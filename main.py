from asyncore import write
from unittest import result
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.textinput import TextInput
from fractions import *
import numpy as np
from kivy.graphics import *

class Land(BoxLayout):
    count_outer=0
    count_inner=0
    os=list()
    oid=StringProperty("0")
    child_count=dict()
    txid=StringProperty()
    den=list()
    iid=dict()
    result=dict()
    result_formatted=dict()
    result_label=dict()
    calc_enabled=BooleanProperty(False)
    text_box=dict()

    def on_press_inner(self,id,oid,rb):
        self.count_inner+=1
        self.child_count[oid]+=1
        ti=TextInput(multiline=False, halign="center",input_filter="int",hint_text="Enter share",write_tab=False)
        ti.bind(text= lambda x,y: self.input_share(ti,ti.txid))
        ti.bind(focus=self.on_focus)
        ti.txid=str(oid)+'_'+str(self.child_count[oid])
        ti.on_text_validate= lambda: self.input_share(ti,ti.txid)        
        id.add_widget(ti)

        self.text_box[ti.txid]=ti

        res=Label(text="-",color=[0.04, 0.2, 0.04, 1])
        res.txid=str(oid)+'_'+str(self.child_count[oid])
        self.result_label[res.txid]= res

        rb.add_widget(res)


        #print(ti.txid)
        print(self.child_count)
        print(self.result_label)
        print(self.count_inner)
        if len(self.iid)==self.count_inner:
            self.calc_enabled=True
        else:
            self.calc_enabled=False


    def on_focus(self, txid,v):
        print(txid.txid)
        if v:
            print('User Focused')
        else:
            print('User defocused')

    def on_press_outer(self):
        self.count_outer+=1
        self.count_inner+=1
        outer_box = BoxLayout(size_hint=(None, None), size=(dp(80),dp(40)))
        outer_box.add_widget(Label(text=str(self.count_outer),color=[0.04, 0.2, 0.04, 1])) 
        b_outer = Button(text="+")          
        outer_box.add_widget(b_outer)
        
        self.ids.outer_stack.add_widget(outer_box)
        inner_box = BoxLayout()
        # with inner_box.canvas:
        #     # Add a red color
        #     Color(1., 0, 0)

        #     # Add a rectangle
        #     Rectangle(pos=self.ids.inner_stack.pos, size=self.ids.inner_stack.size)
        #     inner_box.canvas.ask_update()
        
        ti=TextInput(multiline=False,halign="center",input_filter="int",hint_text="Enter share",write_tab=False)
        ti.txid=str(self.count_outer)+"_1"
        ti.bind(focus=self.on_focus)
        self.text_box[ti.txid]=ti
        self.os.append([None])
        ti.bind(text= lambda x,y: self.input_share(ti,ti.txid))
        ti.on_text_validate= lambda: self.input_share(ti,ti.txid)
        inner_box.add_widget(ti)
        self.ids.inner_stack.add_widget(inner_box)
        
        inner_box.oid=str(self.count_outer)
        print(inner_box.oid)
        if inner_box.oid not in self.child_count:
            self.child_count[inner_box.oid]=1
        else:
            self.child_count[inner_box.oid]+=1
        

        result_box = BoxLayout()
        res=Label(text="-",color=[0.04, 0.2, 0.04, 1])
        res.txid=str(self.count_outer)+"_1"
        self.result_label[res.txid]= res
        result_box.add_widget(res)
        self.ids.result_stack.add_widget(result_box)

        b_outer.on_press = lambda: self.on_press_inner(inner_box,inner_box.oid,result_box)

        print(self.os)
        if len(self.iid)==self.count_inner:
            self.calc_enabled=True
        else:
            self.calc_enabled=False



    def input_share(self,widget,stre):
        print(widget.text)
        print(stre)
        if widget.text != '':
            self.iid[stre]=int(widget.text)
        print(self.iid)
        if len(self.iid)==self.count_inner:
            self.calc_enabled=True
        else:
            self.calc_enabled=False

    def calculate(self):
        dens=dict()
        for key in self.iid:
            keyf=key.split('_')
            dens[keyf[0]]=dens.get(keyf[0],0) + self.iid[key]
        print(dens)
        for key in self.iid:
            self.result[key]=Fraction(1,self.count_outer)*Fraction(self.iid[key],dens[key.split('_')[0]])
        c_list=list(self.result.values())
        for i in range(len(c_list)):
            c_list[i]=c_list[i].denominator
        k_list=list(self.result.keys())
        d_list=list(self.result.values())
        for i in range(len(c_list)):
            d_list[i]=d_list[i].denominator
        d_dic = {k_list[i]: d_list[i] for i in range(len(k_list))}
        print(c_list)
        lc=np.lcm.reduce(c_list)
        print(lc)
        print(self.result)
        for key in self.result:
            keyf=key.split('_')
            self.result_formatted[key]=int(self.result[key].numerator*lc/d_dic[key])
        gc=lc
        gcd=np.gcd.reduce(list(self.result_formatted.values()))
        gc=np.gcd(gcd,gc)
        print(gc)
        lc=int(lc/gc)
        for key in self.result_formatted:
            self.result_formatted[key]=int(self.result_formatted[key]/gc)
        print(self.result)
        print(lc)
        print(self.result_formatted)
        for key in self.result_label:
            self.result_label[key].text=str(self.result_formatted[key])
        self.ids.lccm.text=str(lc)
    
    def clear_inp(self):
        self.iid.clear()
        self.result.clear()
        self.result_formatted.clear()
        self.calc_enabled=False
        for i in self.text_box:
            self.text_box[i].text=''
        for i in self.result_label:
            self.result_label[i].text='-'
        self.ids.lccm.text='-'
        pass
    def reset_all(self):
        self.ids.outer_stack.clear_widgets()
        self.ids.inner_stack.clear_widgets()
        self.ids.result_stack.clear_widgets()
        self.iid.clear()
        self.result.clear()
        self.result_formatted.clear()
        self.calc_enabled=False
        self.count_outer=0
        self.count_inner=0
        self.ids.lccm.text='-'
        self.result_label.clear()
        self.text_box.clear()
        self.den.clear()
        self.child_count.clear()
        self.os.clear()


class Land(App):
    pass
Land().run()

