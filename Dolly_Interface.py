import thorpy, pygame
import os
import subprocess
import RPi.GPIO as GPIO          
import time
import sys, termios, tty

in1 = 24
in2 = 23
ena = 25
in3 = 12
in4 = 16
enb = 20
temp1=1


GPIO.setmode(GPIO.BCM)



GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(ena,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
pa=GPIO.PWM(ena,1000)

GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(enb,GPIO.OUT)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
pb=GPIO.PWM(enb,1000)


pa.start(40)
pb.start(40)


#Funcoes Controle Remoto
def pasta_destino_cr(event):
    nome_pasta = event.el.get_value()
    print("Nome da pasta de destino inserido: ", nome_pasta)
def iniciar_cr():
    print("Modo Controle Remoto Ativado")
    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
 
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
 
    button_delay = 0.2
 
    while True:
        char = getch()
 
        if (char == "p"):
            parar_cr()
            GPIO.cleanup()
            exit(0)
 
        if (char == "w"):
            pa.ChangeDutyCycle(75)
            pb.ChangeDutyCycle(75)
            GPIO.output(in1, GPIO.HIGH)
            GPIO.output(in2, GPIO.LOW)
            GPIO.output(in3, GPIO.LOW)
            GPIO.output(in4, GPIO.HIGH)
            time.sleep(button_delay)
        if (char == "x"):
            pa.ChangeDutyCycle(75)
            pb.ChangeDutyCycle(75)
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.HIGH)
            GPIO.output(in3, GPIO.HIGH)
            GPIO.output(in4, GPIO.LOW)
            time.sleep(button_delay)
            
        if (char == "d"):
            pa.ChangeDutyCycle(80)
            pb.ChangeDutyCycle(35)
            GPIO.output(in1, GPIO.HIGH)
            GPIO.output(in2, GPIO.LOW)
            GPIO.output(in3, GPIO.LOW)
            GPIO.output(in4, GPIO.HIGH)
            time.sleep(button_delay)
            
        if (char == "a"):
            pa.ChangeDutyCycle(35)
            pb.ChangeDutyCycle(80)
            GPIO.output(in1, GPIO.HIGH)
            GPIO.output(in2, GPIO.LOW)
            GPIO.output(in3, GPIO.LOW)
            GPIO.output(in4, GPIO.HIGH)
            time.sleep(button_delay)
        if (char == "s"):
            pb.ChangeDutyCycle(65)
            pa.ChangeDutyCycle(65)
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.LOW)
            GPIO.output(in3, GPIO.LOW)
            GPIO.output(in4, GPIO.LOW)
            time.sleep(button_delay)    
def parar_cr():
    print("Modo Controle Remoto Desativado")

#Funcoes Time-Lapse
def pasta_destino_tl(event):
    nome_pasta = event.el.get_value()
    os.mkdir(nome_pasta)
    os.chdir("/home/pi/Desktop/"+nome_pasta)
def valor_freq_tl(event):
    valor_freq = event.el.get_value()
    print("Valor de frequencia inserido: ", valor_freq)
def tempo_grav_tl(event):
    tempo_grav = event.el.get_value()
    print("Tempo de gravacao inserido: ", tempo_grav)
def iniciar_tl():
    c = 0
    ci = 0
    
    print("Modo Time-Lapse Ativado")
    pb.ChangeDutyCycle(70)
    pa.ChangeDutyCycle(70)
    while c != 2:
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
        GPIO.output(in3, GPIO.LOW)
        GPIO.output(in4, GPIO.HIGH)
        time.sleep(1.5)
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)
        GPIO.output(in3, GPIO.LOW)
        GPIO.output(in4, GPIO.LOW)
        os.system("fswebcam -r 1280x720 " + str(c))
        ci = ci + 1
        c = c + 1
        time.sleep(15)
    print("Ciclo finalizado")
    
def parar_tl():
    print("Modo Time-Lapse Desativado")

#Funcoes Gravacao
def pasta_destino_gv(event):
    nome_pasta = event.el.get_value()
    os.mkdir(nome_pasta)
    os.chdir("/home/pi/Desktop/"+nome_pasta)
    
def tempo_grav_gv(event):
    tempo_grav = event.el.get_value()
    print("Tempo de gravacao inserido: ", tempo_grav)
def iniciar_gv():
    print("Modo Gravacao Ativado")
    pb.ChangeDutyCycle(40)
    pa.ChangeDutyCycle(40)
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
    os.system("avconv -t 10 -f video4linux2 -i /dev/video0 video0.avi")
    print("Ciclo finalizado")
    
def parar_gv():
    print("Modo Gravacao Desativado")
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    


def sair():
    GPIO.cleanup()
    exit()

application = thorpy.Application(size=(800, 600), caption='Dollynho')

titulo = thorpy.make_text("Dollynho", 30, (40,40,40))

subtitulo = thorpy.make_text("Escolha um modo de funcionamento:", 20, (40,40,40))

#Botoes invisiveis para espacamento
inv1 = thorpy.make_button("")
inv1.set_size((50,50))
inv1.set_main_color((0,0,0,0))
inv2 = thorpy.make_button("")
inv2.set_size((20,20))
inv2.set_main_color((0,0,0,0))
inv3 = thorpy.make_button("")
inv3.set_size((15,15))
inv3.set_main_color((0,0,0,0))
inv4 = thorpy.make_button("")
inv4.set_size((10,10))
inv4.set_main_color((0,0,0,0))
inv5 = thorpy.make_button("")
inv5.set_size((10,10))
inv5.set_main_color((0,0,0,0))
inv6 = thorpy.make_button("")
inv6.set_size((5,5))
inv6.set_main_color((0,0,0,0))
inv7 = thorpy.make_button("")
inv7.set_size((10,10))
inv7.set_main_color((0,0,0,0))
inv8 = thorpy.make_button("")
inv8.set_size((10,10))
inv8.set_main_color((0,0,0,0))
inv9 = thorpy.make_button("")
inv9.set_size((10,10))
inv9.set_main_color((0,0,0,0))
inv10 = thorpy.make_button("")
inv10.set_size((10,10))
inv10.set_main_color((0,0,0,0))
inv11 = thorpy.make_button("")
inv11.set_size((5,5))
inv11.set_main_color((0,0,0,0))
inv12 = thorpy.make_button("")
inv12.set_size((10,10))
inv12.set_main_color((0,0,0,0))
inv13 = thorpy.make_button("")
inv13.set_size((10,10))
inv13.set_main_color((0,0,0,0))
inv14 = thorpy.make_button("")
inv14.set_size((5,5))
inv14.set_main_color((0,0,0,0))
inv15 = thorpy.make_button("")
inv15.set_size((10,10))
inv15.set_main_color((0,0,0,0))
inv16 = thorpy.make_button("")
inv16.set_size((10,10))
inv16.set_main_color((0,0,0,0))
inv17 = thorpy.make_button("")
inv17.set_size((10,10))
inv17.set_main_color((0,0,0,0))
inv18 = thorpy.make_button("")
inv18.set_size((10,10))
inv18.set_main_color((0,0,0,0))

#Elementos do modo controle remoto
titulo_cr = thorpy.make_text("Modo Controle Remoto", 24, (40,40,40))
texto_cr = thorpy.make_text("'Iniciar' - Ativar o modo de controle remoto\n'Parar' - Desativar o modo de controle remoto\n'W' - Mover para frente\n'S' - Mover para tras\n'A' - Curva para a esquerda\n'D' - Curva para a direita\n'P' - Parar", 16, (40,40,40))
botao_iniciar_cr = thorpy.make_button("Iniciar", func=iniciar_cr)
botao_iniciar_cr.set_font('Helvetica')
botao_iniciar_cr.set_font_size(18)
botao_iniciar_cr.set_size((100,50))
botao_iniciar_cr.set_main_color((100,255,100))
botao_parar_cr = thorpy.make_button("Parar", func=parar_cr)
botao_parar_cr.set_font('Helvetica')
botao_parar_cr.set_font_size(18)
botao_parar_cr.set_size((100,50))
botao_parar_cr.set_main_color((255,100,100))
pasta_cr = thorpy.Inserter(name="Nome da pasta de destino:")


#Reacoes Controle Remoto
reacao_pasta_cr = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT,
                          reac_func=pasta_destino_cr,
                          event_args={"id":thorpy.constants.EVENT_INSERT,"el":pasta_cr})

#Launcher do modo controle remoto
caixa_cr = thorpy.make_ok_box([titulo_cr, inv4, texto_cr, inv5, botao_iniciar_cr, inv6, botao_parar_cr,
                               inv7, pasta_cr, inv8])
caixa_cr.set_main_color((200,220,230))
caixa_cr.fit_children(margins=(20,20))
caixa_cr.add_reaction(reacao_pasta_cr)
botao_cr = thorpy.make_button("Controle Remoto")
botao_cr.set_font_size(17)
botao_cr.set_font_color((40,40,40))
botao_cr.set_size((200,50))
botao_cr.set_main_color((230,230,215))
thorpy.set_launcher(botao_cr, caixa_cr)

#Elementos do modo time-lapse
titulo_tl = thorpy.make_text("Modo Time-Lapse", 24, (40,40,40))
texto_tl = thorpy.make_text("'Iniciar' - Ativar o modo de time-lapse\n'Parar' - Desativar o modo de time-lapse", 16, (40,40,40))
botao_iniciar_tl = thorpy.make_button("Iniciar", func=iniciar_tl)
botao_iniciar_tl.set_font('Helvetica')
botao_iniciar_tl.set_font_size(18)
botao_iniciar_tl.set_size((100,50))
botao_iniciar_tl.set_main_color((100,255,100))
botao_parar_tl = thorpy.make_button("Parar", func=parar_tl)
botao_parar_tl.set_font('Helvetica')
botao_parar_tl.set_font_size(18)
botao_parar_tl.set_size((100,50))
botao_parar_tl.set_main_color((255,100,100))
pasta_tl = thorpy.Inserter(name="Nome da pasta de destino:")
freq_tl = thorpy.Inserter(name="Frequencia (fotos/segundo):")
tempo_tl = thorpy.Inserter(name="Tempo de captura (segundos):")

#Reacoes Time-Lapse
reacao_pasta_tl = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT,
                          reac_func=pasta_destino_tl,
                          event_args={"id":thorpy.constants.EVENT_INSERT,"el":pasta_tl})
reacao_freq_tl = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT,
                        reac_func=valor_freq_tl,
                        event_args={"id":thorpy.constants.EVENT_INSERT,"el":freq_tl})
reacao_tempo_tl = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT,
                        reac_func=tempo_grav_tl,
                        event_args={"id":thorpy.constants.EVENT_INSERT,"el":tempo_tl})

#Launcher do modo time-lapse
caixa_tl = thorpy.make_ok_box([titulo_tl, inv9, texto_tl, inv10, freq_tl, tempo_tl, inv13,
                               botao_iniciar_tl, botao_parar_tl, inv11, pasta_tl, inv12])
caixa_tl.set_main_color((200,220,230))
caixa_tl.fit_children(margins=(20,20))
caixa_tl.add_reaction(reacao_pasta_tl)
caixa_tl.add_reaction(reacao_freq_tl)
caixa_tl.add_reaction(reacao_tempo_tl)
botao_tl = thorpy.make_button("Time-Lapse")
botao_tl.set_font_size(17)
botao_tl.set_font_color((40,40,40))
botao_tl.set_size((200,50))
botao_tl.set_main_color((230,230,215))
thorpy.set_launcher(botao_tl, caixa_tl)

#Elementos do modo gravacao
titulo_gv = thorpy.make_text("Modo Gravacao", 24, (40,40,40))
texto_gv = thorpy.make_text("'Iniciar' - Ativar o modo de gravacao\n'Parar' - Desativar o modo de gravacao", 16, (40,40,40))
botao_iniciar_gv = thorpy.make_button("Iniciar", func=iniciar_gv)
botao_iniciar_gv.set_font('Helvetica')
botao_iniciar_gv.set_font_size(18)
botao_iniciar_gv.set_size((100,50))
botao_iniciar_gv.set_main_color((100,255,100))
botao_parar_gv = thorpy.make_button("Parar", func=parar_gv)
botao_parar_gv.set_font('Helvetica')
botao_parar_gv.set_font_size(18)
botao_parar_gv.set_size((100,50))
botao_parar_gv.set_main_color((255,100,100))
pasta_gv = thorpy.Inserter(name="Nome da pasta de destino:")
tempo_gv = thorpy.Inserter(name="Tempo de captura (segundos):")

#Reacoes Gravacao
reacao_pasta_gv = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT,
                          reac_func=pasta_destino_gv,
                          event_args={"id":thorpy.constants.EVENT_INSERT,"el":pasta_gv})
reacao_tempo_gv = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT,
                        reac_func=tempo_grav_gv,
                        event_args={"id":thorpy.constants.EVENT_INSERT,"el":tempo_gv})

#Launcher do modo gravacao
caixa_gv = thorpy.make_ok_box([titulo_gv, inv14, texto_gv, inv15, tempo_gv, inv16,
                               botao_iniciar_gv, botao_parar_gv, inv17, pasta_gv, inv18])
caixa_gv.set_main_color((200,220,230))
caixa_gv.fit_children(margins=(20,20))
caixa_gv.add_reaction(reacao_pasta_gv)
caixa_gv.add_reaction(reacao_tempo_gv)
botao_gv = thorpy.make_button("Gravacao")
botao_gv.set_font_size(17)
botao_gv.set_font_color((40,40,40))
botao_gv.set_size((200,50))
botao_gv.set_main_color((230,230,215))
thorpy.set_launcher(botao_gv, caixa_gv)

#Botao sair
botao_sair = thorpy.make_button("Sair", func=sair)
botao_sair.set_font('Helvetica')
botao_sair.set_font_size(14)
botao_sair.set_size((56,28))
botao_sair.set_main_color((230,230,215))

#Caixa do menu principal
elementos = [subtitulo, inv2, botao_cr, botao_tl, botao_gv, inv3, botao_sair]
caixa_central = thorpy.Box(elements=elementos)
caixa_central.fit_children(margins=(30,30))
caixa_central.center()
caixa_central.set_main_color((220,220,220,180))

background = thorpy.Background(color=(100, 150, 180), elements=[titulo, inv1, caixa_central])

thorpy.store(background)

menu = thorpy.Menu(background)
menu.play()

application.quit()
