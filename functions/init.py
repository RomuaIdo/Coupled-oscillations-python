#Inputs iniciais do usuário

def input_number_of_masses():
    while True:
        try:
            number_of_masses = int(input('Digite o número de massas no sistema (mínimo 1): '))
            if number_of_masses < 1:
                print("O número de massas deve ser pelo menos 1.")
                continue
            return number_of_masses
        except ValueError:
            print("Por favor, insira um número inteiro válido.")

def input_mass_values(number_of_masses):
    mass_values = []
    for i in range(number_of_masses):
        while True:
            try:
                mass = float(input(f'Digite o valor da massa {i+1} (kg): '))
                if mass <= 0:
                    print("A massa deve ser positiva.")
                    continue
                mass_values.append(mass)
                break
            except ValueError:
                print("Por favor, insira um valor numérico válido.")
    return mass_values

def input_spring_constants(number_of_masses):
    spring_constants = []
    for i in range(number_of_masses + 1):
        if i == 0:
            prompt = f'Digite o valor da constante da mola da parede esquerda (N/m): '
        elif i == number_of_masses:
            prompt = f'Digite o valor da constante da mola da parede direita (N/m): '
        else:
            prompt = f'Digite o valor da constante da mola {i} (N/m): '
        while True:
            try:
                constant = float(input(prompt))
                if constant <= 0:
                    print("A constante da mola deve ser positiva.")
                    continue
                spring_constants.append(constant)
                break
            except ValueError:
                print("Por favor, insira um valor numérico válido.")
    return spring_constants

def input_initial_conditions(number_of_masses):
    initial_positions = []
    initial_velocities = []

    for i in range(number_of_masses):
        while True:
            try:
                position = float(input(f'Digite a posição inicial da massa {i+1} (m): '))
                initial_positions.append(position)
                break
            except ValueError:
                print("Por favor, insira um valor numérico válido para a posição.")
        
        while True:
            try:
                velocity = float(input(f'Digite a velocidade inicial da massa {i+1} (m/s): '))
                initial_velocities.append(velocity)
                break
            except ValueError:
                print("Por favor, insira um valor numérico válido para a velocidade.")

    return initial_positions, initial_velocities


