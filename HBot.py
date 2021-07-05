from pyrogram import Client, filters
from bs4 import BeautifulSoup
from urllib.request import urlopen
from mega import Mega
from pyromod.helpers import array_chunk, ikb
import glob
import os

app = Client("my_bot")


#FUNCTIONS######################################################################
async def download(link, local, filename):
	meganz = Mega()
	mega = meganz.login()
	await mega.download_url(link, local, filename + ".mp4")

async def upload(filename):
	await client.send_video(message.chat.id, filename, caption = filename)

def delete():
	delList = glob.glob("/downloads")
	for i in delList:
		os.remove(i)

################################################################################

@app.on_message(filters.regex(r"^/start"))
async def bot_start(client, message):
	user = message.from_user.id
	await client.send_message(user, "Olá! Eu sou um bot feito para você baixar seu glorioso de uma fansub aí que não vou citar pra não dar problema (começa com \"F\" e termina com \"ênix Fansub\").\n\n <b>Como usar:</b>\n/anime <code>&#60link do glorioso&#62</code>")

links = ()
user = 0
@app.on_message(filters.regex(r"^/add (?P<link>.+)$"))
async def get_links(client, message):
	user = message.from_user.id
	anime = message.matches[0]['link']
	fh = "fenixhentai.org"

	if fh in anime:
		html = urlopen(anime)
		soup = BeautifulSoup(html.read(), 'html.parser')
		links = [a["href"] for a in soup.findAll("a", {"title": "mega"})]

		buttons = []

		for i in range(1,len(links)+1):
			buttons.append((f"Episódio {i}", f"episode {i}"))

		keyboard = array_chunk(buttons, 3)
		keyboard.append([("Baixar tudo", "download all")])
		await message.reply_text("Selecione o episódio que você quer baixar:",  reply_markup=ikb(keyboard))

	else:
		await client.send_message(user, "Link inválido!\nEu só consigo baixar desenhos educativos do <a href=\"https://fenixhentai.org\">Fênix Hentai</a>")



@app.on_callback_query(filters.regex(r"^episode (?P<number>\d+)"))
async def keyboard_dl(client, callback):
	number = callback.matches[0]['number']
	link = links[number-1]
	await client.send_message(user, "Aguarde, seu episódio será enviado em breve...")
	download(link, "/downloads", str(number))
	upload(str(number))
	await client.send_message(user, "Sucesso!")
	delete()

@app.on_callback_query(filters.regex(r"^download all"))
async def downloadAll(client, callback):
	i=0
	await client.send_message(user, "Aguarde, seus episódios serão enviados em breve...")
	for link in links:
		i =+ 1
		download(link, "/downloads", str(i))
		upload(str(i))
	await client.send_message(user, "Sucesso!")
	delete()


app.run()