from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from prettytable import from_db_cursor
from prettytable import PrettyTable
import sqlite3

conn = sqlite3.connect('marmileve.db')
c = conn.cursor()

class TelaInicial(FloatLayout):

    def on_press_bt(self):
        login = self.ids.login_text.text
        senha = self.ids.senha_text.text
        c.execute('SELECT * FROM login WHERE login = ? and senha = ?', (login, senha))
        query = (c.fetchone())
        if query is not None:
            self.clear_widgets()
            self.add_widget(TelaMenu())

class TelaMenu(FloatLayout):

    def add_pedido(self):
        self.clear_widgets()
        self.add_widget(AddPedido())

    def show_estoque(self):
        self.clear_widgets()
        self.add_widget(ShowEstoque())

    def add_clientes(self):
        self.clear_widgets()
        self.add_widget(AddCliente())

    def telainicial(self):
        self.clear_widgets()
        self.add_widget(TelaInicial())

x = PrettyTable()

class AddPedido(FloatLayout):
    global pedido

    pedido = []
    def telamenu(self):
        self.clear_widgets()
        self.add_widget(TelaMenu())
        x.clear_rows()
        global pedido
        pedido = []
        item = []
        print(str(item) + 'pedido tem que estar limpo')
        print(str(pedido) + 'pedido tem que estar limpo' )
    def addpedido(self):
        global item
        item = []

        if x.field_names == []:
            x.field_names = ['Cliente', 'Prato', 'Tam', 'Qtd']
        item.append(self.ids.cliente.text)
        item.append(self.ids.prato.text)
        item.append((self.ids.tam.text).upper())
        item.append(self.ids.qtd.text)
        print(str(item) + 'item só deve ter um item')
        x.add_row(item)
        pedido.append(item)
        self.ids.resumo.text = str(x)
        print(str(pedido) + 'um ou mais itens')
        return pedido

    def rempedido(self):
        if len(pedido) > 0:
            x.del_row(len(pedido)-1)
            del pedido[len(pedido)-1]
            self.ids.resumo.text = str(x)
    def concluipedido(self):
        global pedido
        if len(pedido) > 0:
            print(pedido)
            for i in pedido:
                c.execute('INSERT INTO pedidos(pedido_cliente, pedido_pratoid, pedido_tam, pedido_qtd, pedido_data) VALUES (?,?,?,?,datetime("now"))', (i[0], i[1], i[2], i[3]))
                conn.commit()
            pedido = []
            x.clear_rows()
            self.ids.resumo.text = 'Pedido adicionado'



class ShowEstoque(FloatLayout):
    def telamenu(self):
        self.clear_widgets()
        self.add_widget(TelaMenu())
    def estoquelist(self):
        c.execute('SELECT * FROM show_estoque')
        t = from_db_cursor(c)
        self.ids.label_estoque.text = str(t)





class AddCliente(FloatLayout):
    def telamenu(self):
        self.clear_widgets()
        self.add_widget(TelaMenu())

class MarmileveApp(App):
    pass

janela = MarmileveApp()
janela.run()
