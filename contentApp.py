#!/usr/bin/python3

import webapp
import urllib.parse

contents = {}
content_inverso = {}

formulario = """
 <form action="" method="POST">
  URL:<br>
  <input type="text" name="URL" value="http://"><br>
  <input type="submit" value="Enviar">
</form>
"""


def loop():
    htmlAnswer = ""
    for element in content_inverso:
        htmlAnswer += "<html><a href=" + str(element) + ">" + str(element) + "</a> -----> <a href=" + content_inverso[element] + ">" +  str(content_inverso[element]) + "</a></body></html><br>"    
    return htmlAnswer


def fichero_read():
    infile = open('texto.txt', 'r')
    for key in infile:
        cont = len(contents)
        contents[key] = cont
        content_inverso[cont] = key
    infile.close()


def fichero_write(var):
    infile = open('texto.txt', 'a') 
    infile.write(var + '\n')
    infile.close()


class contentApp(webapp.webApp):

    def parse(self, request):
        return (request.split()[0], request.split()[1], request)

    def process(self, parsedRequest):
        metodo, recurso, peticion = parsedRequest

        if metodo == "GET":
            if recurso == '/':
                if len(content_inverso) != 0:
                    htmlAnswer =  loop()
                    print("dic" + str(content_inverso))
                    return("200 OK", "<html>" + formulario + htmlAnswer + "</html>")
                else:
                    return("200 OK", "<html>" + formulario + "</html>")
            else:
                try:
                    if int(recurso.split('/')[1]) in content_inverso:
                        return("302 Found\r\nLocation: " + 
                            content_inverso[int(recurso.split('/')[1])], "")
                    else:
                        return("404 Not found", "<html>Not found, ERROR!</html>")
                except ValueError:
                    return("404 Not found", "<html>Not found, ERROR!</html>")

        if metodo == "POST":
            cuerpo = peticion.split('\r\n\r\n', 1)[1]
            if recurso == '/':
                key = urllib.parse.unquote_plus(cuerpo.split('=')[1])
                cont = len(contents)
                if key in contents:
                    return ("200 OK", "<html><a href=" + str(contents[key]) + ">" +
                            str(contents[key]) + "</a> -----> <a href=" +  key + ">" +
                            key + "</a>" + "</body></html>")
                else:
                    contents[key] = cont
                    content_inverso[cont] = urllib.parse.unquote_plus(cuerpo.split('=')[1])
                    fichero_write(key)
                    return ("200 OK", "<html><a href=" + str(contents[key]) + ">" + str(contents[key]) +
                            "</a> -----> <a href=" +  content_inverso[cont] + ">" +  content_inverso[cont] +
                            "</a>" + "</body></html>")
            else:
                return ("404 Not found", "<html>Not found!</html>")

if __name__ == "__main__":
    fichero_read()
    testWebApp = contentApp("localhost", 1234)
