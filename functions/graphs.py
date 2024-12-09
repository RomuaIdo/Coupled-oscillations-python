import pygame


def draw_graph(screen, data_history, color, graph_rect, label, max_history, max_value):
    """
    Desenha um gráfico simples em uma área designada.

    :param screen: Surface do Pygame para desenhar.
    :param data_history: Lista contendo os dados históricos para a massa.
    :param color: Cor da linha do gráfico.
    :param graph_rect: pygame.Rect definindo a área do gráfico.
    :param label: String com o nome do gráfico (e.g., "Posição").
    :param max_history: Número máximo de pontos no histórico.
    :param max_value: Valor máximo esperado para escala Y.
    """
    # Define margens internas para evitar que as linhas toquem as bordas
    padding_x = 5
    padding_y = 20

    # Desenha fundo do gráfico
    pygame.draw.rect(screen, (30, 30, 30), graph_rect)
    
    # Desenha borda do gráfico
    pygame.draw.rect(screen, (200, 200, 200), graph_rect, 2)
    
    # Desenha o label do gráfico
    label_font = pygame.font.SysFont(None, 14)
    label_surface = label_font.render(label, True, (255, 255, 255))
    label_rect = label_surface.get_rect(midtop=(graph_rect.centerx, graph_rect.top + 5))
    screen.blit(label_surface, label_rect)
    
    # Desenha as linhas de grade horizontais
    num_grids = 4
    for i in range(1, num_grids + 1):
        y = graph_rect.top + i * graph_rect.height / (num_grids + 1)
        pygame.draw.line(screen, (50, 50, 50), (graph_rect.left, y), (graph_rect.right, y), 1)
    
    # Desenha as linhas de grade verticais
    num_grids_v = 4
    for i in range(1, num_grids_v + 1):
        x = graph_rect.left + i * graph_rect.width / (num_grids_v + 1)
        pygame.draw.line(screen, (50, 50, 50), (x, graph_rect.top), (x, graph_rect.bottom), 1)
    
    # Plota os dados
    if len(data_history) < 2:
        return  # Necessita de pelo menos dois pontos para desenhar uma linha

    # Normaliza os dados para o gráfico, garantindo que fiquem dentro dos limites
    normalized_data = [min(max(d, -max_value), max_value) for d in data_history[-max_history:]]  # Limitar os valores

    # Define a linha central do gráfico (valor zero)
    y_center = graph_rect.top + (graph_rect.height - 2 * padding_y) / 2 + padding_y

    # Inverte o eixo Y para que valores positivos fiquem para cima e negativos para baixo
    points = []
    for idx, value in enumerate(normalized_data):
        # Calcula a posição X
        x = graph_rect.left + padding_x + (idx / max_history) * (graph_rect.width - 2 * padding_x)
        
        # Calcula a posição Y
        y = y_center - (value / max_value) * (graph_rect.height - 2 * padding_y) / 2
        
        # Assegura que y está dentro do gráfico
        y = max(graph_rect.top + padding_y, min(y, graph_rect.bottom - padding_y))
        
        points.append((x, y))
    
    # Desenha as linhas do gráfico
    pygame.draw.lines(screen, color, False, points, 2)

def draw_graphs(screen, positions_history, velocities_history, accelerations_history, colors, screen_width, screen_height, max_history=200, padding=10):
    """
    Desenha os três gráficos (Posição, Velocidade, Aceleração) para cada massa na parte superior da tela.
    Cada massa possui seus próprios três gráficos organizados verticalmente.
    """
    num_masses = len(positions_history)
    graph_height = 60
    graph_width = 180
    graph_spacing = 30  # Espaçamento horizontal entre os conjuntos de gráficos
    vertical_spacing = 5  # Espaçamento vertical entre gráficos de uma mesma massa

    total_width = num_masses * graph_width + (num_masses - 1) * graph_spacing
    start_x = (screen_width - total_width) // 2
    start_y = 80  # Posição Y inicial para os gráficos

    for mass_idx in range(num_masses):
        mass_color = colors[mass_idx]

        # Define as áreas dos gráficos para esta massa
        pos_rect = pygame.Rect(start_x + mass_idx * (graph_width + graph_spacing),
                               start_y,
                               graph_width,
                               graph_height)
        vel_rect = pygame.Rect(start_x + mass_idx * (graph_width + graph_spacing),
                               start_y + graph_height + vertical_spacing,
                               graph_width,
                               graph_height)
        acc_rect = pygame.Rect(start_x + mass_idx * (graph_width + graph_spacing),
                               start_y + 2 * (graph_height + vertical_spacing),
                               graph_width,
                               graph_height)

        # Define o valor máximo para a escala Y de cada gráfico
        # Posição: base no amplitude das posições
        all_positions = [abs(pos) for pos in positions_history[mass_idx]]
        max_position = max(all_positions) if all_positions else 1.0
        max_position = max_position * 1.1  # Pequeno buffer para evitar tocar as bordas

        # Velocidade: base na amplitude das velocidades
        all_velocities = [abs(vel) for vel in velocities_history[mass_idx]]
        max_velocity = max(all_velocities) if all_velocities else 1.0
        max_velocity = max_velocity * 1.1  # Pequeno buffer

        # Aceleração: base na amplitude das acelerações
        all_accelerations = [abs(acc) for acc in accelerations_history[mass_idx]]
        max_acceleration = max(all_accelerations) if all_accelerations else 1.0
        max_acceleration = max_acceleration * 1.1  # Pequeno buffer

        # Desenha os gráficos com ajustes na escala e posicionamento
        draw_graph(screen, positions_history[mass_idx], mass_color, pos_rect, f"Posição {mass_idx+1}", max_history, max_position)
        draw_graph(screen, velocities_history[mass_idx], mass_color, vel_rect, f"Velocidade {mass_idx+1}", max_history, max_velocity)
        draw_graph(screen, accelerations_history[mass_idx], mass_color, acc_rect, f"Aceleração {mass_idx+1}", max_history, max_acceleration)

