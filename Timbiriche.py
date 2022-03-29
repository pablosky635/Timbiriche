# Feb 2020
# Simulación del juego de timbiriche

import numpy as np
import random
import time 

x = 0
us= 0
pc= 0
m = np.array([[1,2,3,4,x],
			  [5,6,7,8,9],
			  [10,11,12,13,x],
			  [14,15,16,17,18],
			  [19,20,21,22,x],
			  [23,24,25,26,27],
			  [28,29,30,31,x],
			  [32,33,34,35,36],
			  [37,38,39,40,x]])

exclude = [0] #excluimos el 0

def getBoxes():
	#Números con los que se forma una caja
	return(np.array([[m[0,0], m[1,0], m[1,1], m[2,0]],		
					 [m[0,1], m[1,1], m[1,2], m[2,1]],
					 [m[0,2], m[1,2], m[1,3], m[2,2]],
					 [m[0,3], m[1,3], m[1,4], m[2,3]],
					 [m[2,0], m[3,0], m[3,1], m[4,0]],
					 [m[2,1], m[3,1], m[3,2], m[4,1]],
					 [m[2,2], m[3,2], m[3,3], m[4,2]],
					 [m[2,3], m[3,3], m[3,4], m[4,3]],
					 [m[4,0], m[5,0], m[5,1], m[6,0]],
					 [m[4,1], m[5,1], m[5,2], m[6,1]],
					 [m[4,2], m[5,2], m[5,3], m[6,2]],
					 [m[4,3], m[5,3], m[5,4], m[6,3]],
					 [m[6,0], m[7,0], m[7,1], m[8,0]],
					 [m[6,1], m[7,1], m[7,2], m[8,1]],
					 [m[6,2], m[7,2], m[7,3], m[8,2]],
					 [m[6,3], m[7,3], m[7,4], m[8,3]]]))

#Pintar tablero
def draw(m):
	i=0
	print('*---'+str(m[i][0])+'---*---'+str(m[i][1])+'---*---'+str(m[i][2])+'---*---'+str(m[i][3])+'---*')
	print('¦       ¦       ¦       ¦       ¦ \n'+str(m[i+1][0])+'       '+str(m[i+1][1])+'       '+str(m[i+1][2])+'       '+str(m[i+1][3])+'       '+str(m[i+1][4])+'\n¦       ¦       ¦       ¦       ¦')
	for i in range(2,8,2):
		print('*---'+str((cond(m[i][0])))+'--*---'+str((cond(m[i][1])))+'--*---'+str((cond(m[i][2])))+'--*---'+str((cond(m[i][3])))+'--*')
		print('¦       ¦       ¦       ¦       ¦ \n'+str((cond(m[i+1][0])))+'      '+str((cond(m[i+1][1])))+'      '+str((cond(m[i+1][2])))+'      '+str((cond(m[i+1][3])))+'      '+str((cond(m[i+1][4])))+'\n¦       ¦       ¦       ¦       ¦')

	print('*---'+str((cond(m[8][0])))+'---*--'+str((cond(m[8][1])))+'---*--'+str((cond(m[8][2])))+'---*--'+str((cond(m[8][3])))+'--*')
	
def cond(num):
	if num == 0:
		return "00"
	else:
		return num

def recorrer(m):
	xtra = []
	for x in np.nditer(m):
		xtra.append(x)
	return xtra

def computer(m):
	global pc
	xtra = recorrer(m)
	boxes = getBoxes()

	for row in boxes:
		new = [x for x in row if not x==0]

		if len(new) != 0:
			if len(new) == 1: 	    #Cerrar una box
				if checkDobles(new) == True:		#Se cierran dos cajas con ese número
					pc +=2
				else:
					pc +=1
				selectNum(new)
				print("COMPUTER: "+str(new))
				computer(m)
				return
			elif len(new) == 2: 	#No ceder box
				exclude.extend(new)
	nums = [x for x in xtra if not x in exclude]	#Nums disponibles 

	if len(nums) == 0:	#Ya no hay números disponibles para no ceder cajas.
		sinoption = [x for x in np.nditer(m) if not x ==0]
		if len(sinoption) !=0:
			num = random.choice(sinoption)	  
			print("Computer SOP"+str(num))
			selectNum(num)

			#selectNum(sinoption[0])
			#print("COMPUTER1: "+str(sinoption[0]))
		else:
			return
	else:
		num = random.choice(nums)
		print("COMPUTER2:"+str(num))
		selectNum(num)

		#selectNum(nums[0])	#Si hay disponibles elegir el primero
		#print("COMPUTER2: "+str(nums[0]))




def user():
	draw(m)
	global us
	#ojo arreglar
	boxes = getBoxes()
	if boxes.any() == False:
		#print("Termina el juego")
		return
	opc = int(input("Elige un número "))

	for j in boxes:
		if opc in j:
			x = np.where(boxes == opc)
			boxes[x] = 0	#Asigna 0 donde aparece opc
			p = boxes[x[0]]		#array donde se encuentran opc	
			selectNum(opc)

			if len(p) > 1:	
				if p[0].any() == False and p[1].any() == False:	#Dos cajas cerradas
					#print("Caja doble!!")
					us +=2
					user()
				elif p[0].any() == False:
					#print("Caja 0!")
					us +=1
					user()
				elif p[1].any() == False:
					#print("Caja 1!")
					us +=1
					user()
				#else:
					#print("NO HUBO CAJAS")
			else:
				print("Caja sola")
				if p[0].any() == False:
					us +=1
					user()
				#else:
					#print("caja sola no cerrada")

def checkDobles(num):		#Obtiene los arreglos en donde se encuentra el número (si está en al menos 2 arrays).
	boxes = getBoxes()
	y = np.where(boxes == num)
	if len(y[0]) > 1:	#si está en dos
		return checkZeros(boxes[y[0]],num)
	else:
		return 0

def checkZeros(dobles,num):
	for x in np.nditer(dobles,op_flags=['readwrite']):
		if x[...] == num:
			x[...] = 0
			break
	if dobles.any() == False:  # hay puros 0
		return 1
	else:
		return 0


def selectNum(num):
	for x in np.nditer(m,op_flags=["readwrite"]):
		if x[...] == num:
			x[...] = 0
			break
def game():
	#draw(m)
	while(m.any() != False):
		turno = "User"
		print("Turno: "+str(turno))
		user()
		if m.any() != False:
			draw(m)
			turno = "PC"
			print("Turno: "+str(turno))
			time.sleep(0.5)
			computer(m)
		#print("M"+str(m))
	draw(m)
	print("PC : "+str(pc))
	print("User: "+str(us))


game()
