import cv2
import numpy
import sys
import os
import xml.etree.ElementTree as ET
from tqdm import tqdm

def cargar_data():
	dirFiles = os.popen("ls "+folder_data).read()
	total_files = int(os.popen("ls "+folder_data+" | wc -l").read())-1
	#print total_files
	first = True
	id_device = 0
	for filename in tqdm(dirFiles.split(), total = total_files):

		#Generar path
		img_path = os.path.join(folder_data, filename)
		infoname = os.path.splitext(filename)[0]+".xml"
		info_path = os.path.join(folder_info, infoname)

		#Lectura de imagen
		img = cv2.imread(img_path)

		if img is None:
			print ('Cannot open file:', img_path)
			continue

		#Obtener imagen en escala de grises
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		#Lectura xml
		tree = ET.parse(info_path)
		root = tree.getroot()
		user = root.find('user')
		id_user = user.get('id')
		device = root.find('device')
		iris = root.find('iris').text
		gender = user.find('gender').text
		age = user.find('age').text
		device_name = device.find('name').text
		camera = device.find('camera')
		camera_type = camera.get('type')

		if device_name not in devices:
			devices[device_name] = id_device
			id_device = id_device+1

		id_gender = 0
		if(gender == "F"): id_gender = 1 #M:0 F:1 
		id_iris = 0
		if(iris == "right"): id_iris = 1 #Left:0 Right:1
		id_type = 0
		if(camera_type == "rear"): id_type = 1 #Front:0 Rear:1 

		#Redimensiona imagen para su almacenamiento
		gray_resize = cv2.resize(gray, (160, 120))

		#Vectorizar imagen redimensionada
		image = numpy.asarray(gray_resize).reshape(-1)

		#Agregar genero, edad e informacion de dispositivo
		image = numpy.append(image,int(id_user))
		image = numpy.append(image,id_type)
		image = numpy.append(image,id_iris)
		image = numpy.append(image,id_gender)
		image = numpy.append(image,int(age))
		image = numpy.append(image,int(devices[device_name]))

		if first:
			matrix = numpy.asmatrix(image)
			first = False
		else:
			matrix_aux = numpy.asmatrix(image)
			matrix = numpy.concatenate((matrix,matrix_aux), axis=0)
	return matrix

def device_dict():
	file = open("devices.dat", "r")
	devices = dict()
	for device in file:
		device_info = device.split(":")
		devices[device_info[0]] = int(device_info[1])
	return devices

def device_update():
	file = open("devices.dat", "w")
	for device in devices:
		line = device+":"+str(devices[device])+"\n"
		file.write(line)

def get_iris_vector():
	print "\nVector columna Iris\n"
	col = int(matrix[0].size-4)
	print matrix[:,col]
	print "\n"
	print "Left: 0 - Right: 1"
	numpy.savetxt(folder_result+'iris_column.dat', matrix[:,col], delimiter=';',fmt='%d')

def get_gender_vector():
	print "\nVector columna Genero\n"
	col = int(matrix[0].size-3)
	print matrix[:,col]
	print "\n"
	print "M: 0 - F: 1"
	numpy.savetxt(folder_result+'gender_column.dat', matrix[:,col], delimiter=';',fmt='%d')

def get_age_vector():
	print "\nVector columna Edad\n"
	col = int(matrix[0].size-2)
	print matrix[:,col]
	numpy.savetxt(folder_result+'age_column.dat', matrix[:,col], delimiter=';',fmt='%d')

def get_device_vector():
	print "\nVector columna Device\n"
	col = int(matrix[0].size-1)
	print matrix[:,col]
	print "\n"
	print devices
	numpy.savetxt(folder_result+'device_column.dat', matrix[:,col], delimiter=';',fmt='%d')

def write():
	numpy.savetxt(folder_result+'database.csv', matrix, delimiter=';',fmt='%d')
	print "Archivo database creado"


folder_data = sys.argv[1]
folder_info = sys.argv[2]
folder_result = "result/"

try:
    os.stat(folder_result)
except:
    os.mkdir(folder_result)

devices = device_dict()
print "Cargando datos... Espere por favor!"
matrix = cargar_data()
print "Carga satisfactoria\n"

write()
#get_iris_vector()
get_gender_vector()
get_age_vector()
get_device_vector()
device_update()
print "\nArchivos generados exitosamente\n"
