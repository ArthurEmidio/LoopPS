# -*- coding: utf-8 -*-

# Função responsável por retornar um conjunto de bytes como um inteiro
def getBytesAsInteger(file, quantity):
	data = file.read(quantity)
	result = 0
	for i in range(0, quantity):
		result += ord(data[i]) * 256**i
	
	return result


# Código Principal
file = open("testImage.bmp", "rb")
try:
	
	# Obter o offset de onde começa os dados dos pixels
	file.seek(10)
	offset_bmp_data = getBytesAsInteger(file, 4)
	
	# Obter a largura da imagem
	file.seek(18)
	width = getBytesAsInteger(file, 4)
	bytes_per_line = width*3 # obtendo a quantidade de bytes por linha da imagem (sem contar padding)
	
	# Obter a altura da imagem
	file.seek(22)
	height = getBytesAsInteger(file, 4)
	
	# Calcular o "padding" contido no fim de cada linha do BMP
	if (width % 4) == 0: padding = 0
	else: 				 padding = 4 - (width % 4)
	
	
	# Mostrar os dados obtidos
	print "BMP data offset: " + str(offset_bmp_data)
	print "Tamanho do BMP: " + str(width) + " x " + str(height)
	print "Padding: " + str(padding) + " bytes\n"	
	print "Mensagem:"
	
	
	
	# Começo da análise dos dados dos pixels do BMP
	
	file.seek(offset_bmp_data) # Apontar para o começo dos dados dos pixels do BMP
	
	message = '' # armazena a mensagem decodificada
	char = '' # armazena o caractere que será montado para cada 8 bytes da imagem
	position_in_line = 0 # armazena a posição do byte na atual linha da imagem
	
	# A mensagem continua ser montada até que o caractere montado seja um '\0'
	while char != '\0':
		char_bin = '' # armazena o código binário do próximo caractere decodificado
		
		# Loop para obter os LSBs dos próximos 8 bytes e formar um novo caractere
		for i in range(0,8):
			position_in_line += 1
			
			# Pular os paddings no fim de cada linha (as 3 linhas abaixo são inúteis para a imagem dada, pois padding = 0)
			if position_in_line > bytes_per_line:
				position_in_line = 0
				file.seek(file.tell() + padding)
			
			byte = file.read(1)
			char_bin = str(ord(byte) & 1) + char_bin # Obtém o LSB do byte (através do operador AND) e o concatena no código binário do caractere

		char = chr(int(char_bin, 2)) # converte o binário obtido para um caractere
		message += char # concatena o caractere na mensagem final
	
	print message

finally:
	file.close()