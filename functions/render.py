import os
import pygame
import numpy as np
from functions.graphs import draw_graphs

def initialize_pygame(screen_width, screen_height):
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Spring Simulation')
    return screen

def setup_simulation_parameters(screen_width=1200, screen_height=800):
    screen = initialize_pygame(screen_width, screen_height)
    clock = pygame.time.Clock()
    
    # Carrega a fonte do stardew valley
    try:
        # Define caminhos absolutos para garantir que a fonte seja encontrada
        current_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(current_dir, "../assets/", "stardew.ttf")
        
        # Carrega a fonte com tamanhos diferentes
        title_font = pygame.font.Font(font_path, 36)   # Fonte para o título
        mode_font = pygame.font.Font(font_path, 20)    # Fonte para as informações dos modos
        paused_font = pygame.font.Font(font_path, 48)  # Fonte para a mensagem de pausa
    except FileNotFoundError:
        print("Erro: O arquivo de fonte 'stardew.ttf' não foi encontrado no diretório.")
        pygame.quit()
        quit()
    
    # Inicializa a fonte para numeração das massas (fonte padrão)
    default_font = pygame.font.SysFont(None, 24)
    
    return screen, clock, title_font, mode_font, paused_font, default_font



def draw_masses(screen, positions, masses, colors, default_font, font_scale=50, origin=(600, 400), base_spacing=150, draw_numbers=True):
    max_mass = max(masses)
    if max_mass == 0:
        max_mass = 1  # Evita divisão por zero

    base_size = 40  # Tamanho base para o quadrado da massa

    # Definir limites para o tamanho das massas
    min_size = 20
    max_size = 60

    masses_y = []

    for i, pos in enumerate(positions):
        mass = masses[i]
        color = colors[i]  # Obter a cor da lista de cores

        # Escala baseada na massa relativa ao máximo para suavizar variações
        size = min_size + (mass / max_mass) * (max_size - min_size)
        size = int(size)

        # Computar a posição atual da massa
        x_base = origin[0] + i * base_spacing
        x = x_base + int(pos * font_scale)
        y = origin[1] - size // 2  # Fixar y para que o centro esteja em origin[1]

        # Define o retângulo da massa
        rect = pygame.Rect(x - size // 2, y, size, size)

        # Desenhar a massa com a cor específica
        pygame.draw.rect(screen, color, rect)

        # Armazenar o y_center (fixo em origin[1])
        y_center = origin[1]
        masses_y.append(y_center)

        # Desenha a numeração da massa
        if draw_numbers:
            number_text = default_font.render(str(i+1), True, (255, 165, 0))  # Número em laranja
            text_rect = number_text.get_rect(center=(x, y - 10))  # Posicionado acima da massa
            screen.blit(number_text, text_rect)

    return masses_y

def draw_springs(screen, positions, masses, masses_y, scale=50, origin=(600, 400), base_spacing=150):
    spring_color = (128, 128, 128)  # Cinza

    n = len(positions)
    # Desenha a mola da parede esquerda conectando à primeira massa
    x1_base = origin[0] - base_spacing  # Posição da parede esquerda
    x2_base = origin[0]  # Posição da primeira massa

    x1 = x1_base
    y1 = masses_y[0]
    x2 = origin[0] + int(positions[0] * scale)
    y2 = masses_y[0]

    pygame.draw.line(screen, spring_color, (x1, y1), (x2, y2), 4)  # Mola da parede esquerda

    # Desenha as molas entre as massas
    for i in range(n - 1):
        # As molas conectam a massa i com a massa i+1, independentemente de suas posições relativas
        x1_base = origin[0] + i * base_spacing
        x2_base = origin[0] + (i + 1) * base_spacing

        x1 = x1_base + int(positions[i] * scale)
        y1 = masses_y[i]
        x2 = x2_base + int(positions[i + 1] * scale)
        y2 = masses_y[i + 1]

        pygame.draw.line(screen, spring_color, (x1, y1), (x2, y2), 4)  # Mola entre massas

    # Desenha a mola da parede direita conectando à última massa
    x1_base = origin[0] + (n - 1) * base_spacing  # Posição da última massa
    x2_base = origin[0] + n * base_spacing      # Posição da parede direita

    x1 = x1_base + int(positions[-1] * scale)
    y1 = masses_y[-1]
    x2 = x2_base
    y2 = masses_y[-1]

    pygame.draw.line(screen, spring_color, (x1, y1), (x2, y2), 4)  # Mola da parede direita

def draw_title(screen, title_font, screen_width, screen_height, title_text="Spring Simulation", padding=20):
    """
    Renderiza um título centralizado na parte superior da tela.
    Adiciona espaçamento entre o título e os gráficos.
    """
    # Renderiza o texto do título
    title_surface = title_font.render(title_text, True, (255, 255, 255))  # Texto em branco
    title_rect = title_surface.get_rect(center=(screen_width // 2, padding + title_surface.get_height() // 2))
    
    # Desenha o título na tela
    screen.blit(title_surface, title_rect)

def render_mode_information(screen, mode_info_list, mode_font, screen_width, screen_height, padding=10):
    """
    Renderiza as informações dos modos na parte inferior central da tela.
    Cada modo é exibido em formato vertical, e múltiplos modos são colocados lado a lado.
    Ajusta o tamanho da fonte e a posição com base na quantidade de modos.
    """
    number_of_modes = len(mode_info_list)
    
    # Calcula a largura total necessária para renderizar todos os modos lado a lado
    # Considerando um pequeno espaçamento entre os modos
    mode_width = 250  # Largura reservada para cada modo
    spacing_between_modes = 20  # Espaçamento entre os modos
    
    total_width = number_of_modes * mode_width + (number_of_modes - 1) * spacing_between_modes
    
    # Inicia a posição x para centralizar os modos
    start_x = (screen_width - total_width) // 2
    # Inicia a posição y próximo ao fundo da tela
    start_y = screen_height - 200  # Ajuste conforme necessário
    
    for i, mode_info in enumerate(mode_info_list):
        # Cada mode_info é uma lista de linhas
        lines = mode_info
        # Calcula a posição x para este modo
        mode_x = start_x + i * (mode_width + spacing_between_modes)
        
        # Calcula a posição y inicial para este modo
        mode_y = start_y
        
        for line in lines:
            text_surface = mode_font.render(line, True, (255, 255, 255))  # Texto em branco
            text_rect = text_surface.get_rect(center=(mode_x + mode_width // 2, mode_y))
            screen.blit(text_surface, text_rect)
            mode_y += mode_font.get_linesize() + 2  # Avançar para a próxima linha

def draw_paused(screen, paused_font, screen_width, screen_height):
    """
    Desenha uma mensagem de pausa centralizada na tela.
    """
    paused_text = paused_font.render("Paused", True, (255, 0, 0))  # Texto em vermelho
    paused_rect = paused_text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(paused_text, paused_rect)

def render_dynamics(screen, positions, velocities, accelerations, masses, colors, title_font, mode_info_list, mode_font, paused, paused_font, default_font, screen_width, screen_height, 
                    scale=50, origin=(600, 400), base_spacing=150, 
                    positions_history=None, velocities_history=None, accelerations_history=None, max_history=200):
    # Preenche o fundo
    screen.fill((0, 0, 0))
    
    # Desenha o título
    draw_title(screen, title_font, screen_width, screen_height)
    
    # Desenha os gráficos na parte superior
    draw_graphs(screen, positions_history, velocities_history, accelerations_history, colors, screen_width, screen_height, max_history)
    
    # Como todas as masses_y são origin_y, podemos criar essa lista diretamente
    masses_y = [origin[1]] * len(masses)
    
    # Desenha as paredes
    wall_color = (173, 255, 47)  # Amarelo
    wall_width = 20
    wall_height = 100

    # Posição da parede esquerda
    left_wall_rect = pygame.Rect(origin[0] - base_spacing - wall_width, origin[1] - wall_height // 2, wall_width, wall_height)
    pygame.draw.rect(screen, wall_color, left_wall_rect)

    # Posição da parede direita
    right_wall_rect = pygame.Rect(origin[0] + (len(masses)-1)*base_spacing + base_spacing, origin[1] - wall_height // 2, wall_width, wall_height)
    pygame.draw.rect(screen, wall_color, right_wall_rect)

    # Desenha as molas primeiro (incluindo as molas das paredes)
    draw_springs(screen, positions, masses, masses_y, scale, origin, base_spacing)
    
    # Desenha as massas depois das molas
    draw_masses(screen, positions, masses, colors, default_font, scale, origin, base_spacing, draw_numbers=True)
    
    # Desenha as informações dos modos na parte inferior
    render_mode_information(screen, mode_info_list, mode_font, screen_width, screen_height)
    
    # Se estive pausado, desenhar a mensagem de pausa
    if paused:
        draw_paused(screen, paused_font, screen_width, screen_height)
    
    # Atualiza a tela
    pygame.display.flip()



def display_mode_information(frequencies, amplitudes, phases):
    print("\nInformações dos Modos Normais:")
    for i in range(len(frequencies)):
        print(f'\nModo {i+1}:')
        print(f'  Frequência: {frequencies[i]:.2f} rad/s')
        print(f'  Amplitude: {amplitudes[i]:.2f} m')
        print(f'  Fase: {np.degrees(phases[i]):.2f} graus')


