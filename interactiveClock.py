""" 
Reloj Interactivo 3D con digitalización y modo manual usando una Lista Circular Doble.
permite mover manecillas del reloj para ajustar la hora
arrastrar una manecilla se detiene la actualización automática y, al soltar, se establece el
“tiempo manual” para que el reloj avance desde ese nuevo punto

La tecla "R" reinicia el reloj a la hora del sistema
"""

import pygame
import math
import time
import sys
from clockLists import CircularDoublyLinkedList

# Ventana de pygame
pygame.init()
width = 600
height = 800                # La ventana tiene 600x800; la parte inferiorestara la hora digital
center = (width // 2, 300)  # centro del reloj
radius = 250                # radio del reloj

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Reloj Interactivo 3D - Estructuras de Datos")
clock = pygame.time.Clock()

# globales
clockHandsAngles = {'hour': 90, 'minute': 90, 'second': 90}  # Ángulos en grados para cada manecilla
activeHand = None      # Indica cuál manecilla se está moviendo ("hour", "minute" o "second")
manualMode = False     # Indica si se está en modo manual (usuario controla la hora)
manualSeconds = None   # Tiempo manual en segundos, calculado a partir de los ángulos
lastUpdateTime = pygame.time.get_ticks() / 1000.0

# lista circular de los numeros
clockNumbers = CircularDoublyLinkedList()
for num in [12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
    clockNumbers.insert(num)

def polarToCartesian(center, angleDeg, length):
    """
    Convierte coordenadas polares (ángulo en grados y longitud) a coordenadas cartesianas (x, y)
    se le resta 90° al ángulo para que 0° (de la función trigonométrica) apunte hacia arriba
    """
    angleRad = math.radians(angleDeg - 90)
    x = center[0] + length * math.cos(angleRad)
    y = center[1] + length * math.sin(angleRad)
    return (x, y)

def pointLineDistance(pt, lineStart, lineEnd):
    """
    Calcula la distancia mínima entre un punto (pt) y el segmento definido por lineStart y lineEnd
    para determinar si el clic del usuario fue lo cercano a una manecilla
    """
    (px, py) = pt
    (x1, y1) = lineStart
    (x2, y2) = lineEnd
    dx = x2 - x1
    dy = y2 - y1
    if dx == 0 and dy == 0:
        return math.hypot(px - x1, py - y1)
    t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)
    if t < 0:
        return math.hypot(px - x1, py - y1)
    elif t > 1:
        return math.hypot(px - x2, py - y2)
    projX = x1 + t * dx
    projY = y1 + t * dy
    return math.hypot(px - projX, py - projY)

def drawClockFace(surface):
    """
    Dibuja la cara del reloj:
    
    Un círculo base con borde
    ticks (marcas) para minuto de 5 en 5
    y los numeros del reloj btenidos mediante la lista circular
    """
    pygame.draw.circle(surface, (30, 30, 30), center, radius)
    pygame.draw.circle(surface, (240, 200, 0), center, radius, 4)
    # dibujar marcas
    for i in range(60):
        angle = math.radians(i * 6 - 90)
        xStart = center[0] + (radius - 20) * math.cos(angle)
        yStart = center[1] + (radius - 20) * math.sin(angle)
        xEnd = center[0] + radius * math.cos(angle)
        yEnd = center[1] + radius * math.sin(angle)
        if i % 5 == 0:
            tickWidth = 4
            color = (240, 200, 0)
        else:
            tickWidth = 2
            color = (100, 100, 100)
        pygame.draw.line(surface, color, (xStart, yStart), (xEnd, yEnd), tickWidth)
    # dibujar numeros del reloj usando la lista circular
    font = pygame.font.SysFont("Times New Roman", 32, bold=True)
    numbers = clockNumbers.traverse()
    for i, num in enumerate(numbers):
        angle = math.radians(i * 30 - 90)
        xPos = center[0] + (radius - 40) * math.cos(angle)
        yPos = center[1] + (radius - 40) * math.sin(angle)
        text = font.render(str(num), True, (240, 200, 0))
        surface.blit(text, text.get_rect(center=(xPos, yPos)))

def drawHands(surface):
    """
    Dibuja las manecillas del reloj usando los angulos guardados en clockHandsAngles
    retorna las posiciones finales de cada manecilla para la deteccioon de eventos
    """
    # mmanecilla de la hora 50% del radio, grosor 8
    hourEnd = polarToCartesian(center, clockHandsAngles['hour'], radius * 0.5)
    pygame.draw.line(surface, (255, 255, 255), center, hourEnd, 8)
    # manecilla del minuto 75% del radio, grosor 6
    minuteEnd = polarToCartesian(center, clockHandsAngles['minute'], radius * 0.75)
    pygame.draw.line(surface, (100, 200, 255), center, minuteEnd, 6)
    # manecilla del segundo 90% del radio, grosor 2
    secondEnd = polarToCartesian(center, clockHandsAngles['second'], radius * 0.9)
    pygame.draw.line(surface, (255, 50, 50), center, secondEnd, 2)
    # dibuja un pequeño circulo en el centro
    pygame.draw.circle(surface, (240, 200, 0), center, 10)
    return hourEnd, minuteEnd, secondEnd

def digitalTimeFromAngles(clockHandsAngles):
    """
    Convierte los angulos de clockHandsAngles en una hora digital (HH:MM:SS) en formato 12 horas
    cada 30° equivale a 1 hora y cada 6° a 1 minuto o 1 segundo
    """
    hour = int(math.floor(clockHandsAngles["hour"] / 30)) % 12
    if hour == 0:
        hour = 12
    minute = int(math.floor(clockHandsAngles["minute"] / 6)) % 60
    second = int(math.floor(clockHandsAngles["second"] / 6)) % 60
    return hour, minute, second

def drawDigitalTime(surface):
    # dibuja la hora digital (HH:MM:SS) en la parte inferior de la ventana
    
    h, m, s = digitalTimeFromAngles(clockHandsAngles)
    timeStr = f"{h:02}:{m:02}:{s:02}"
    font = pygame.font.SysFont("Arial", 40, bold=True)
    text = font.render(timeStr, True, (255, 255, 255))
    surface.blit(text, text.get_rect(center=(center[0], height - 80)))

def updateFromSystem():
    """
    Actualiza clockHandsAngles según la hora actual del sistema
    s se gace la conversión: 
    cad asegundo 6°, cada minuto 6° y cada hora 30° 
    """
    t = time.localtime()
    sec = t.tm_sec
    minute = t.tm_min
    hour = t.tm_hour % 12
    global clockHandsAngles
    clockHandsAngles['second'] = sec * 6
    clockHandsAngles['minute'] = minute * 6 + sec * 0.1
    clockHandsAngles['hour'] = hour * 30 + minute * 0.5

def computeManualSecondsFromAngles():
    """
    Convierte la hora digital (derivada de clockHandsAngles) en total de segundos
    se interpreta la hora 12 como 0 para facilitar el cálculo.
    """
    h, m, s = digitalTimeFromAngles(clockHandsAngles)
    hourForCalc = 0 if h == 12 else h
    return hourForCalc * 3600 + m * 60 + s

def updateManualMode(delta):
    """
    En modo manual, actualiza el tiempo manual
    si manualSeconds es None, se inicializa calculándolo a partir de clockHandsAngles
    se suma delta (segundos transcurridos) y se recalculan los ángulos.
    se usan 43200 segundos para representar 12 horas.
    """
    global manualSeconds, clockHandsAngles
    if manualSeconds is None:
        manualSeconds = computeManualSecondsFromAngles()
    manualSeconds += delta
    clockHandsAngles['hour'] = (manualSeconds % 43200) / 43200 * 360
    clockHandsAngles['minute'] = ((manualSeconds % 3600) / 3600) * 360
    clockHandsAngles['second'] = ((manualSeconds % 60) / 60) * 360

#bucle
lastUpdateTime = pygame.time.get_ticks() / 1000.0
running = True

while running:
    currentTime = pygame.time.get_ticks() / 1000.0
    deltaTime = currentTime - lastUpdateTime
    lastUpdateTime = currentTime

    screen.fill((0, 0, 0))
    drawClockFace(screen)
    
    """ 
    Actualizar el tiempo:
    
    Si manualMode está activado Y no hay ninguna manecilla en movimiento (activeHand es None),
    se actualiza en modo manual; de lo contrario, si no se está en modo manual, se usa la hora del sistema.
    
    """
    if manualMode and activeHand is None:
        updateManualMode(deltaTime)
    elif not manualMode:
        updateFromSystem()
    
    # Dibujar manecillas y la hora digital
    hourEnd, minuteEnd, secondEnd = drawHands(screen)
    drawDigitalTime(screen)
    
    # Procesar eventos de Pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # Reinicia el reloj al tiempo del sistema
                manualMode = False
                manualSeconds = None
                updateFromSystem()
                activeHand = None

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            # Detectar si el clic se hizo cerca de alguna manecilla (umbral 10 píxeles)
            if pointLineDistance(mousePos, center, hourEnd) < 10:
                activeHand = 'hour'
                manualMode = True
            elif pointLineDistance(mousePos, center, minuteEnd) < 10:
                activeHand = 'minute'
                manualMode = True
            elif pointLineDistance(mousePos, center, secondEnd) < 10:
                activeHand = 'second'
                manualMode = True

        elif event.type == pygame.MOUSEBUTTONUP:
            # Al soltarse recalcula manualSeconds a partir de los angulos actuales
            if activeHand is not None:
                manualSeconds = computeManualSecondsFromAngles()
            activeHand = None

        elif event.type == pygame.MOUSEMOTION:
            if activeHand is not None:
                mx, my = pygame.mouse.get_pos()
                angle = math.degrees(math.atan2(my - center[1], mx - center[0])) + 90
                if angle < 0:
                    angle += 360
                clockHandsAngles[activeHand] = angle

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
