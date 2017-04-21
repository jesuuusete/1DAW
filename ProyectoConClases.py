import turtle
import time

#region FONDO
wn = turtle.Screen()
wn.title("Welcome to 'Find them all'")
wn.setup(width=1900, height=1000)
turtle.bgpic("fondonuevo.gif")

#endregion

#region GALERIA

wn.register_shape("es.gif")
wn.register_shape("luffyderecha.gif")
wn.register_shape("luffyizquierda.gif")
wn.register_shape("escaleraa.gif")
wn.register_shape("door.gif")
wn.register_shape("suelo.gif")
wn.register_shape("suelopeq.gif")
wn.register_shape("ganar.gif")
wn.register_shape("moneda0.gif")
wn.register_shape("gameover1.gif")
wn.register_shape("well_done.gif")

#endregion

#region LISTAS DE COORDENADAS


lista_suelos_nivel_1 = [(-900, -480.00), (-380.00, -480.00), (140.00, -480.00), (660.00, -480.00), (900.00, -480)]

lista_suelos_nivel_2 = [(-900, -280.00), (-700, -280.00), (-28.00, -280.00), (650.00, -280.00), (820.00, -280.00)]

lista_suelos_nivel_3 = [(-800, -80.00), (-120.00, -80.00), (400.00, -80.00), (1075.00, -80.00)]

lista_suelos_nivel_4 = [(-1020.00, 120.00), (-350.00, 120.00), (400.00, 120.00), (320.00, 120.00), (1070.00, 120.00)]

lista_suelos_nivel_5 = [(-908.00, 320.00), (-235.00, 320.00), (440.00, 320.00), (1100.00, 320.00)]

lista_escaleras = [(-825.00, -385.00), (800.00, -385.00), (520.00, -177.00), (160.00, 23.00), (-880.00, 220.00)]

lista_caida = [(-410.00, -280.00), (267.00, -280.00), (-505.00, -80.00), (690.00, -80.00), (-730.00, 120.00),
               (-60.00, 120.00), (690.00, 120.00), (-615.00, 320.00), (56.00, 320.00), (725.00, 320.00)]

lista_monedas = [(- 350, -440.00), (890, -440), (-100, -240.00), (-700, -240), (875, -40), (-850, -40), (875, 160),
                 (-480, 160), (-200, 360)]

lista_caidasobj = []  # Lista donde se va a guardar los objetos de 'caida'

lista_suelosobj = []  # Lista donde se va a guardar los objetos de 'suelo'

lista_escaobj = []  # lista donde se va a guardar los objetos 'escaleras'

lista_monedasobj = []  # lista donde se va a guardar los objetos 'monedas'

lista_suelos = lista_suelos_nivel_1 + lista_suelos_nivel_2 + lista_suelos_nivel_3 + lista_suelos_nivel_4 + lista_suelos_nivel_5

#endregion


class Grafico:
    def __init__(self, lista, forma, listobj):
        for pos in lista:
            x, y = pos
            self.grafico = turtle.Turtle()
            self.grafico.up()
            self.grafico.speed(0)
            self.grafico.goto(x, y)
            self.grafico.shape(forma)
            listobj.append(self.grafico)


class Suelo(Grafico):
    def __init__(self):
        Grafico.__init__(self, lista_suelos, "suelo.gif", lista_suelosobj)


class Escalera(Grafico):
    def __init__(self):
        Grafico.__init__(self, lista_escaleras, "escaleraa.gif", lista_escaobj)


class Caida(Grafico):
    def __init__(self):
        Grafico.__init__(self, lista_caida, "square", lista_caidasobj)

    def esconder(self):
        """Esconde las tortugas"""
        for obj in lista_caidasobj:
            obj.hideturtle()


class Jugador:
    score = 0
    jugando = True

    def __init__(self):
        self.meta = turtle.Turtle()
        self.meta.shape("door.gif")
        self.meta.up()
        self.meta.speed(0)
        self.meta.setpos(880.00, 375.00)
        self.objmain = turtle.Turtle()
        self.objmain.shape("luffyderecha.gif")
        self.objmain.speed(0)
        self.objmain.up()
        self.objmain.goto(-890.00, -430.00)
        self.puntuacion = turtle.Turtle()
        self.score = 0
        self.winner = turtle.Turtle()
        self.winner.hideturtle()

    def mover_derecha(self):
        """Mueve el personaje principal hacia la derecha"""
        if self.jugando:
            if self.objmain.xcor() <= 920:
                self.objmain.setheading(0)
                self.objmain.shape("luffyderecha.gif")
                self.objmain.fd(20)
                while self.toca_caida() == True:
                    self.objmain.setheading(270)
                    self.objmain.fd(200)
                self.desaparecer_moneda()
                self.ganar()

    def mover_izquierda(self):
        """Mueve el personaje principal hacia la izquierda"""
        if self.jugando:
            if self.objmain.xcor() >= -920:
                self.objmain.setheading(180)
                self.objmain.shape("luffyizquierda.gif")
                self.objmain.fd(20)
                while self.toca_caida():
                    self.objmain.setheading(270)
                    self.objmain.fd(200)
                self.desaparecer_moneda()
                self.ganar()

    def salto(self):
        """Permite saltar al personaje principal hacia el lado que esté mirando"""
        if self.jugando:
            direccion = self.objmain.heading()
            speed = self.objmain.speed()
            if self.objmain.heading() == 0:
                self.objmain.speed(5)
                self.objmain.setheading(direccion + 45)
                self.objmain.fd(150)
                self.objmain.setheading(direccion - 45)
                self.objmain.fd(150)
                while self.toca_caida() == True:
                    self.objmain.setheading(270)
                    self.objmain.fd(200)
            elif self.objmain.heading() == 180:
                self.objmain.speed(5)
                self.objmain.setheading(direccion - 45)
                self.objmain.fd(150)
                self.objmain.setheading(direccion + 45)
                self.objmain.fd(150)
                while self.toca_caida() == True:
                    self.objmain.setheading(270)
                    self.objmain.fd(200)
            self.objmain.speed(speed)
            self.objmain.setheading(direccion)

    def subir_escalera(self):
        """Movimiento de subir las escaleras"""
        for i in lista_escaobj:
            if abs(self.objmain.xcor() - i.xcor()) < 20:
                if abs(self.objmain.ycor() - i.ycor()) < 80:
                    dire = self.objmain.heading()
                    self.objmain.setheading(90)
                    self.objmain.fd(200)
                    self.objmain.setheading(dire)

    def bajar_escalera(self):
        """Movimiento de bajar las escaleras"""
        for i in lista_escaobj:
            if abs(self.objmain.xcor() - i.xcor()) < 20:
                if abs(self.objmain.ycor() - i.ycor()) > 120:
                    dire = self.objmain.heading()
                    self.objmain.setheading(270)
                    self.objmain.fd(200)
                    self.objmain.setheading(dire)

    def toca_caida(self):
        """Se cae si se pasa del suelo"""
        for i in lista_caidasobj:
            if abs(self.objmain.xcor() - i.xcor()) < 70:
                if abs(self.objmain.ycor() - i.ycor()) < 55:
                    return True

    def desaparecer_moneda(self):
        """Si el personaje principal pasa por una moneda, la hace desaparecer y lo elimina de la lista"""
        for moneda in lista_monedasobj:
            if abs(self.objmain.xcor() - moneda.xcor()) < 20:
                if abs(self.objmain.ycor() - moneda.ycor()) < 50:
                    moneda.hideturtle()
                    lista_monedasobj.remove(moneda)
                    self.sumar_score()
                    Tiempo.extra += 5

    def sumar_score(self):
        """Suma 1 a la actual score"""
        wn.tracer(False)
        self.score += 1
        self.puntuacion.undo()
        self.puntuacion.color("grey21")
        self.puntuacion.penup()
        self.puntuacion.hideturtle()
        self.puntuacion.setposition(-750, 400)
        self.puntuacion.write("Score: " + str(self.score), move=False, align="center", font=('Pristina', 45, "normal"))
        wn.tracer(1)

    def ganar(self):
        """Si el personaje llega a la meta en tiempo, muestra el mensaje e inmoviliza el personaje"""
        if abs(self.objmain.xcor() - self.meta.xcor()) < 35:
            if abs(self.objmain.ycor() - self.meta.ycor()) < 50:
                if lista_monedasobj == []:
                    self.winner.showturtle()
                    self.winner.speed(5)
                    self.winner.shape("well_done.gif")
                    Tiempo.running = False
                    Jugador.jugando = False
                    wn.exitonclick()


class Coin:
    def __init__(self):
        for coin in lista_monedas:
            x, y = coin
            self.moneda = turtle.Turtle()
            self.moneda.up()
            self.moneda.shape("moneda0.gif")
            self.moneda.speed(0)
            self.moneda.goto(x, y)
            lista_monedasobj.append(self.moneda)


class Tiempo():
    running = True
    extra = 0

    def __init__(self):
        wn.tracer(False)
        self.time_t = turtle.Turtle()
        self.time_t.hideturtle()
        self.time_t.color("gray21")
        self.time_t.up()
        self.time_t.setposition(-400, 400)

        wn.tracer(1)

    def counterdown(self, duracion_inicial):
        """Pone en marcha un contrareloj con un tiempo determinado al iniciar el juego"""
        self.zero = time.time()
        self.time_t.up()
        self.time_t.setposition(-400, 400)
        while self.running:
            self.tiempo = time.time()
            self.resto = round(self.tiempo) - round(self.zero)
            self.total = (duracion_inicial - self.resto + self.extra)
            if int(self.total) >= 0:
                self.time_t.undo()
                self.time_t.write("Time: " + str(self.total), move=False, align="center",
                                  font=('Pristina', 45, "normal"))
            if int(self.total) == 0:
                self.perder = turtle.Turtle()
                self.perder.shape("gameover1.gif")
                self.running = False
                Jugador.jugando = False
                wn.exitonclick()


def iniciar():
    """Inicializa el juego"""
    wn.tracer(False)
    e = Escalera()
    s = Suelo()
    c = Caida()
    c.esconder()
    m = Coin()
    j = Jugador()
    j.desaparecer_moneda()
    wn.onkey(j.subir_escalera, "Up")
    wn.onkeypress(j.mover_derecha, "Right")
    wn.onkeypress(j.mover_izquierda, "Left")
    wn.onkey(j.bajar_escalera, "Down")
    wn.onkey(j.salto, "space")
    wn.tracer(1)
    wn.listen()


iniciar()
t = Tiempo()
t.counterdown(15)
wn.mainloop()
