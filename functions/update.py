from scipy.linalg import eigh
import numpy as np
import pygame
from functions.render import render_dynamics

def compute_normal_modes(mass_values, spring_constants):
    n = len(mass_values)
    K = np.zeros((n, n))
    M = np.diag(mass_values)

    # Construção correta da matriz de rigidez K incluindo as molas das paredes
    # spring_constants[0] é a mola da parede esquerda
    # spring_constants[1] a spring_constants[n-1] são as molas entre as massas
    # spring_constants[n] é a mola da parede direita

    for i in range(n):
        if i == 0:
            K[i, i] = spring_constants[0] + spring_constants[1]
            if n > 1:
                K[i, i+1] = -spring_constants[1]
        elif i == n - 1:
            K[i, i] = spring_constants[i] + spring_constants[i+1]
            K[i, i-1] = -spring_constants[i]
        else:
            K[i, i] = spring_constants[i] + spring_constants[i+1]
            K[i, i-1] = -spring_constants[i]
            K[i, i+1] = -spring_constants[i+1]

    # Resolve o problema de autovalores generalizado K x = omega^2 M x
    try:
        eigenvalues, eigenvectors = eigh(K, M)
    except Exception as e:
        print(f"Erro ao resolver o problema de autovalores: {e}")
        pygame.quit()
        quit()

    # Filtra apenas os modos com autovalores positivos
    positive_indices = eigenvalues > 0
    eigenvalues = eigenvalues[positive_indices]
    eigenvectors = eigenvectors[:, positive_indices]

    if len(eigenvalues) == 0:
        print("Nenhum modo normal com autovalor positivo foi encontrado.")
        pygame.quit()
        quit()

    return eigenvalues, eigenvectors

def calculate_frequencies(eigenvalues):
    frequencies = np.sqrt(eigenvalues)
    return frequencies

def calculate_amplitudes_and_phases(initial_positions, initial_velocities, eigenvectors, frequencies, mass_values):
    # Projeta as condições iniciais nos modos normais para obter amplitudes e fases
    A = np.zeros(len(frequencies))
    phi = np.zeros(len(frequencies))

    x0 = np.array(initial_positions)
    v0 = np.array(initial_velocities)
    M = np.array(mass_values)

    for j in range(len(frequencies)):
        mode = eigenvectors[:, j]

        # Produto escalar ponderado pela matriz de massa
        A_j = np.dot(x0 * M, mode)  # x0^T * M * modo
        B_j = np.dot(v0 * M, mode) / frequencies[j]  # v0^T * M * modo / omega_j

        amplitude = np.sqrt(A_j**2 + B_j**2)
        phase = np.arctan2(-B_j, A_j)

        A[j] = amplitude
        phi[j] = phase

    return A, phi

def update_simulation_states(eigenvalues, eigenvectors, amplitudes, phases, t):
    # Calcula as posições das massas no tempo t usando a decomposição modal
    positions = np.zeros(len(eigenvectors))
    velocities = np.zeros(len(eigenvectors))
    accelerations = np.zeros(len(eigenvectors))
    for j in range(len(eigenvalues)):
        omega = np.sqrt(eigenvalues[j])
        mode = eigenvectors[:, j]
        positions += amplitudes[j] * np.cos(omega * t + phases[j]) * mode
        velocities += -amplitudes[j] * omega * np.sin(omega * t + phases[j]) * mode
        accelerations += -amplitudes[j] * (omega ** 2) * np.cos(omega * t + phases[j]) * mode
    return positions, velocities, accelerations

def prepare_mode_info_strings(frequencies, amplitudes, phases):
    """
    Prepara uma lista de listas com as informações dos modos para exibição na tela.
    Cada sublista contém as linhas de informações para um modo, formatadas para exibição vertical.
    """
    mode_info_list = []
    for i in range(len(frequencies)):
        mode_info = [
            f"Modo {i+1}:",
            f"  Frequencia: {frequencies[i]:.2f} rad/s",
            f"  Amplitude: {amplitudes[i]:.2f} m",
            f"  Fase: {np.degrees(phases[i]):.2f} graus"
        ]
        mode_info_list.append(mode_info)
    return mode_info_list




def handle_events(paused):
    """
    Lida com os eventos do Pygame.
    Retorna o estado atualizado de 'paused'.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused  # Alterna o estado de pausa
    return paused

def run_main_loop(screen, clock, title_font, mode_font, paused_font, default_font, eigenvalues, eigenvectors, amplitudes, phases, masses, colors, mode_info_list, origin, base_spacing, screen_width, screen_height, max_history=200):
    t = 0  # Tempo inicial
    running = True
    paused = False  # Estado inicial de pausa

    # Inicializar históricos
    positions_history = [[] for _ in range(len(masses))]
    velocities_history = [[] for _ in range(len(masses))]
    accelerations_history = [[] for _ in range(len(masses))]

    while running:
        delta_time = clock.tick(60) / 1000.0  # Tempo em segundos desde o último frame

        # Lidar com os eventos e atualizar o estado de pausa
        paused = handle_events(paused)

        if not paused:
            t += delta_time
            positions, velocities, accelerations = update_simulation_states(eigenvalues, eigenvectors, amplitudes, phases, t)
            # Atualizar históricos
            for i in range(len(masses)):
                positions_history[i].append(positions[i])
                velocities_history[i].append(velocities[i])
                accelerations_history[i].append(accelerations[i])
                # Manter o tamanho máximo do histórico
                if len(positions_history[i]) > max_history:
                    positions_history[i].pop(0)
                if len(velocities_history[i]) > max_history:
                    velocities_history[i].pop(0)
                if len(accelerations_history[i]) > max_history:
                    accelerations_history[i].pop(0)
        else:
            # Quando pausado, não atualiza os estados, apenas continua desenhando
            pass

        render_dynamics(screen, positions, velocities, accelerations, masses, colors, title_font, mode_info_list, mode_font, paused, paused_font, default_font, screen_width, screen_height, 
                        scale=50, origin=origin, base_spacing=base_spacing, 
                        positions_history=positions_history, velocities_history=velocities_history, 
                        accelerations_history=accelerations_history, max_history=max_history)

