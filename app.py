from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient
from datetime import datetime


cluster = MongoClient("mongodb+srv://dumar:xexeca@cluster0.akts7tc.mongodb.net/?retryWrites=true&w=majority")
db = cluster["dumar"]
users = db["users"]
orders = db["orders"]

app = Flask(__name__)


@app.route("/", methods=["get", "post"])
def reply():
    text = request.form.get("Body")
    number = request.form.get("From")
    number = number.replace("whatsapp:", "")
    response = MessagingResponse()
    user = users.find_one({"number": number})
    if bool(user) == False:
        response.message("Olá, obrigado por entrar em contato com a *Dumar Eventos*.\nDigite o campeonato que deseja mais informações:" "\n\n*Digite*\n\n 1️⃣ Circuito Mundial Santa Catarina Beach Tennis Winter \n 2️⃣ Balneário Camboriú Ultimate Games")
        users.insert_one({"number": number, "status": "main", "messages": []})
    elif user["status"] == "main":
        try:
            option = int(text)
        except:
            response.message("Por favor, digite um número válido")
            return str(response)

        if option == 1:
            response.message("Você está no menu *Circuito Mundial Santa Catarina Beach*\n\nDigite a opção desejada:️ \n1️⃣Informações:\n2️⃣Inscrições\n0️⃣Para voltar ao Menu")
            users.update_one({"number": number}, {"$set": {"status": "bt"}})
        elif option == 2:
            response.message("Você está no menu *Balneário Camboriú Ultimate Games*\n\nDigite a opção desejada:️ \n1️⃣Informações:\n2️⃣Inscrições\n0️⃣Para voltar ao Menu")
            users.update_one({"number": number}, {"$set": {"status": "cross"}})
        else:
            response.message("Por favor, digite um número válido")
            return str(response)
    elif   user["status"] == "bt":
        try:
            option  = int(text)
        except:
            response.message("Por favor, digite um número válido")
            return str(response)
        if option == 0:
            users.update_one({"number": number}, {"$set": {"status": "main"}})
            response.message("\nDigite o campeonato que deseja mais informações:" "\n\n*Digite*\n\n 1️⃣ Circuito Mundial Santa Catarina Beach Tennis Winter \n 2️⃣ Balneário Camboriú Ultimate Games")
        elif option == 1:
            response.message("O Circuito Mundial Santa Catarina Beach Tennis, acontecerá nos dias 12 a 16 de julho de 2023, na Barra Sul em Balneário Camboriú.\n\nDigite 0️⃣ para retornar ao menu inicial")
        elif option == 2:
            response.message("Inscrições são feitas pelo site *http://www.torneioja.com.br/torneio/385* \n\nDigite 0️⃣ para retornar ao menu inicial")
    elif user["status"] == "cross":
        try:
            option = int(text)
        except:
            response.message("Por favor, digite um número válido")
            return str(response)
        if option == 0:
            users.update_one({"number": number}, {"$set": {"status": "main"}})
            response.message("\nDigite o campeonato que deseja mais informações:" "\n\n*Digite*\n\n 1️⃣ Circuito Mundial Santa Catarina Beach Tennis Winter \n 2️⃣ Balneário Camboriú Ultimate Games")

    users.update_one({"number": number}, {"$push": {"messages": {"text": text, "date": datetime.now()}}})
    return str(response)

if __name__ == "__main__":
    app.run(0)
