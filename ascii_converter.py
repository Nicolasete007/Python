import cv2

image = cv2.imread("C:\\Users\\Nico\\Desktop\\imagen2.png")

def get_string(image):
	
	#charachters = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1[]?-_+~<>i!lI;:,\"^`'. "
	charachters = "$@B%8&WM#*owmO0QCJUYXzcvunxr-+~<>:\"^'. "
	rows, cols = image.shape[0:2]

	final_string = ""

	for r in range(rows):
		for c in range(cols):
			pixel = gray[r,c]
			char = charachters[int(pixel/255*len(charachters))-1]
			final_string = final_string + char
		final_string = final_string + "\n"

	return final_string

width = 150
height = int(image.shape[0]/image.shape[1]*width/2.5)
dim = (width, height)

resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
contrast = cv2.equalizeHist(gray)

print(get_string(gray))

while True:
	break
	cv2.imshow("Imagen", gray)
	cv2.imshow("Contraste", contrast)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break