import cv2
import numpy
import sys
import os
import xml.etree.ElementTree as ET
from tqdm import tqdm

def cargar_data():
	file = open(folder_result+"Image_database.csv", "w")
	dirFiles = os.popen("ls "+folder_info).read()
	header = "Filename;User_id;Image_number;Iris;Age;Gender;Device_type;Device_name;Camera_type;Camera_Resolution;DPI;Location;Illumination;Author\n"
	file.write(header)
	total_files = int(os.popen("ls "+folder_info+" | wc -l").read())-1
	for filename in tqdm(dirFiles.split(), total = total_files):

		#Generar path
		info_path = os.path.join(folder_info, filename)

		#Lectura xml
		tree = ET.parse(info_path)
		root = tree.getroot()
		user = root.find('user')
		id_user = str(user.get('id'))
		device = root.find('device')
		iris = root.find('iris').text
		image_number = str(root.find('image_number').text)
		gender = user.find('gender').text
		name = root.find('filename').text
		age = str(user.find('age').text)
		device_name = device.find('name').text
		camera = device.find('camera')
		device_type = device.find('type').text
		camera_type = camera.get('type')
		resolution = camera.find('resolution').text
		dpi = camera.find('dpi').text
		conditions = root.find('conditions')
		location = conditions.find('location').text
		illumination = conditions.find('illumination').text
		author = root.find('author').text

		line = name+";"+id_user+";"+image_number+";"+iris+";"+age+";"+gender+";"+device_type+";"+device_name+";"+camera_type+";"+resolution+";"+dpi+";"+location+";"+illumination+";"+author+"\n"

		file.write(line)
		

folder_info = sys.argv[1]
folder_result = "result/"

try:
    os.stat(folder_result)
except:
    os.mkdir(folder_result) 

print "Cargando datos... Espere por favor!"
cargar_data()
print "Carga satisfactoria\n"
print "\nArchivos generados exitosamente\n"
