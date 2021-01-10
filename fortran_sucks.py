from random import randint

is_string = False
string_symbol = ""

fortran_file, extension = input("File path to stupidify: ").split(".")


def randomCase(char):
	global is_string
	if is_string:
		return char
	if randint(0, 1) == 0:
		return char.lower()
	else:
		return char.upper()


with open(fortran_file + "." + extension, "r") as file:
	with open(fortran_file + "-stupidified." + extension, "w") as new_file:
		
		for line in file:

			for char in line:
				if char == '"':
					is_string = not is_string
				new_file.write(randomCase(char))