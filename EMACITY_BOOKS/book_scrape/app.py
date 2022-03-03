import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
import isbn_price

class MyGrid(GridLayout):
	isbn = ObjectProperty(None)

	def btn(self):
		search = self.isbn.text
		price = isbn_price.get_price(search)
		print(price)
		self.isbn.text = ""

class MyApp(App):
	def build(self):
		return MyGrid()

if __name__ == "__main__":
	MyApp().run()
