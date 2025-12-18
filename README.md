# paraleloA-uide
Nombre del Juego:
"Serpiente Peligrosa" - Un juego clásico reinventado con elementos de riesgo y recompensa.

Descripción del Proyecto:
"Serpiente Peligrosa" es una evolución moderna del clásico juego de la serpiente, desarrollado en Python con la librería Tkinter. Este proyecto combina la nostalgia del juego tradicional con nuevas mecánicas estratégicas donde el jugador debe equilibrar el crecimiento y la supervivencia.

Objetivos Principales:
1. Recrear un clásico con mejoras visuales y mecánicas modernas
2. Demostrar habilidades de programación en Python usando POO y Tkinter
3. Implementar un sistema de juego balanceado con riesgo/recompensa

Funcionalidades del Programa:
1. Sistema de Juego Básico
 - Control de serpiente con teclas de flecha (↑ ↓ ← →)
 - Movimiento continuo y automático
 - Sistema de puntuación dinámico
 - Detección de colisiones con bordes y cuerpo propio

2. Mecánicas Únicas
 - Sistema de crecimiento dual: Manzanas (+1 segmento) vs Calaveras (-2 segmentos)
 - Efectos visuales inmediatos al consumir ítems
 - Longitud mínima garantizada (3 segmentos)
 - Generación inteligente de ítems (sin superposiciones)

3. Interfaz de Usuario
 - Pantalla de inicio con instrucciones claras
 - Indicadores en tiempo real de puntuación y longitud
 - Efectos gráficos para acciones del jugador

Estados del Juego:
text
INICIO → JUGANDO → (GAME OVER/REINICIO)
 - Pantalla de Game Over con estadísticas finales

Sistema de Ítems
Ítem	Efecto	Puntuación	Representación

🍎 Manzana	+1 segmento	+10 puntos	Círculo rojo

💀 Calavera	-2 segmentos	-5 puntos	Polígono blanco


4. Estados del Juego
text
INICIO → JUGANDO → (GAME OVER/REINICIO)
