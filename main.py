import random  # Importação para gerar cores aleatórias
from functions.init import *
from functions.graphs import *
from functions.update import *
from functions.render import *



def main():
    # Configurações da tela
    screen_width = 1200
    screen_height = 800

    number_of_masses = input_number_of_masses()
    mass_values = input_mass_values(number_of_masses)
    spring_constants = input_spring_constants(number_of_masses)
    initial_positions, initial_velocities = input_initial_conditions(number_of_masses)

    eigenvalues, eigenvectors = compute_normal_modes(mass_values, spring_constants)
    frequencies = calculate_frequencies(eigenvalues)
    amplitudes, phases = calculate_amplitudes_and_phases(
        initial_positions, initial_velocities, eigenvectors, frequencies, mass_values
    )

    display_mode_information(frequencies, amplitudes, phases)

    # Preparar as strings de informação dos modos para exibição na tela
    mode_info_list = prepare_mode_info_strings(frequencies, amplitudes, phases)

    # Gerar cores aleatórias para cada massa
    colors = []
    for _ in range(number_of_masses):
        color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))  # Evitar cores muito escuras
        colors.append(color)

    # Ajustar o espaçamento e origem para centralizar o sistema
    base_spacing = 150  # Espaçamento base entre massas
    total_width = (number_of_masses - 1) * base_spacing
    origin_x = (screen_width - total_width) // 2  # Centralizar horizontalmente
    origin_y = screen_height // 2  # Centralizar verticalmente
    origin = (origin_x, origin_y)
    screen, clock, title_font, mode_font, paused_font, default_font = setup_simulation_parameters(screen_width, screen_height)

    run_main_loop(screen, clock, title_font, mode_font, paused_font, default_font, eigenvalues, eigenvectors, amplitudes, phases, mass_values, colors, mode_info_list, origin, base_spacing, screen_width, screen_height)

if __name__ == '__main__':
    main()

