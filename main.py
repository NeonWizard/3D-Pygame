import wireframe
import pygame, sys
import copy
import random
from pygame.locals import *

aqua = pygame.Color(75,100,255)

key_to_function = {
	pygame.K_LEFT:   (lambda x: x.translateAll('x', -10)),
	pygame.K_RIGHT:  (lambda x: x.translateAll('x',  10)),
	pygame.K_DOWN:   (lambda x: x.translateAll('y',  10)),
	pygame.K_UP:     (lambda x: x.translateAll('y', -10)),
	pygame.K_EQUALS: (lambda x: x.scaleAll(1.25, (pv.width/2, pv.height/2))),
	pygame.K_MINUS:  (lambda x: x.scaleAll(0.8, (pv.width/2, pv.height/2))),
	pygame.K_q:      (lambda x: x.rotateAll('X',  0.1)),
	pygame.K_w:      (lambda x: x.rotateAll('X', -0.1)),
	pygame.K_a:      (lambda x: x.rotateAll('Y',  0.1)),
	pygame.K_s:      (lambda x: x.rotateAll('Y', -0.1)),
	pygame.K_z:      (lambda x: x.rotateAll('Z',  0.1)),
	pygame.K_x:      (lambda x: x.rotateAll('Z', -0.1)),
	pygame.K_r:      (lambda x: x.clearAll())}

def placeCube(loc,viewer):
	cube = wireframe.Wireframe()
	cube.addNodes([(x,y,z) for x in (loc[0]-100,loc[0]+100) for y in (loc[1]-100,loc[1]+100) for z in (loc[0]-100,loc[0]+100)])
	cube.addEdges([(n,n+4) for n in range(0,4)]+[(n,n+1) for n in range(0,8,2)]+[(n,n+2) for n in (0,1,4,5)])
	viewer.addWireframe(str(len(viewer.wireframes)),cube)

def drawRect(rect,viewer):
	rectangle = wireframe.Wireframe()
	rectangle.addNodes([(x,y,z) for x in (rect[0],rect[0]+rect[2]) for y in (rect[1],rect[1]+rect[3]) for z in (rect[0],rect[0]+rect[2])])
	rectangle.addEdges([(n,n+4) for n in range(0,4)]+[(n,n+1) for n in range(0,8,2)]+[(n,n+2) for n in (0,1,4,5)])
	viewer.addWireframe(str(len(viewer.wireframes)),rectangle)

class ProjectionViewer:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.mousex, self.mousey = 0, 0
		self.screen = pygame.display.set_mode((width, height))
		pygame.display.set_caption('Wireframe')
		self.background = (15,15,20)

		self.wireframes = {}
		self.displayNodes = True
		self.displayEdges = True
		self.nodeColour = (255,255,255)
		self.edgeColour = (200,200,200)
		self.nodeRadius = 4
		self.drawStart = None

	def addWireframe(self, name, wireframe):
		self.wireframes[name] = wireframe

	def run(self):
		running = True
		while running:
			#self.rotateAll("X", .001)
			#self.rotateAll("Y", .0001)
			#self.rotateAll("Z", .001)
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
					running = False
				elif event.type == KEYDOWN:
					if event.key in key_to_function:
						key_to_function[event.key](self)

					elif event.key == K_t:
						placeCube((self.mousex,self.mousey),pv)

				elif event.type == MOUSEBUTTONDOWN:
					self.mousex, self.mousey = event.pos
					if event.button == 1:
						self.drawStart = event.pos

					elif event.button == 4:
						self.scaleAll(1.2, (self.mousex, self.mousey))

					elif event.button == 5:
						self.scaleAll(.8, (self.mousex, self.mousey))

				elif event.type == MOUSEBUTTONUP:
					self.mousex, self.mousey = event.pos
					if event.button == 1:
						left = min(self.drawStart[0],event.pos[0])
						top = min(self.drawStart[1],event.pos[1])
						right = max(self.drawStart[0],event.pos[0])
						bottom = max(self.drawStart[1],event.pos[1])
						drawRect(pygame.Rect(left,top,right-left,bottom-top),pv)
						self.drawStart = None



				elif event.type == MOUSEMOTION:
					if pygame.mouse.get_pressed()[1]:
						self.translateAll("x", event.pos[0]-self.mousex)
						self.translateAll("y", event.pos[1]-self.mousey)

					elif pygame.mouse.get_pressed()[2]:
						self.rotateAll("Y", (event.pos[0]-self.mousex)/100.0)
						self.rotateAll("X", (event.pos[1]-self.mousey)/100.0)
                                               
					self.mousex, self.mousey = event.pos
					
			self.display()  
			pygame.display.update()
		
	def display(self):
		self.screen.fill(self.background)
		if self.drawStart:
			#print str(self.drawStart[0])+","+str(self.drawStart[1])+" : "+str(self.mousex)+","+str(self.mousey)
			pygame.draw.rect(self.screen,aqua,[self.drawStart[0],self.drawStart[1],self.mousex-self.drawStart[0],self.mousey-self.drawStart[1]])

		for wireframe in self.wireframes.values():
			if self.displayEdges:
				for edge in wireframe.edges:
					pygame.draw.aaline(self.screen, self.edgeColour, (edge.start.x, edge.start.y), (edge.stop.x, edge.stop.y), 1)

			if self.displayNodes:
				for node in wireframe.nodes:
					pygame.draw.circle(self.screen, self.nodeColour, (int(node.x), int(node.y)), self.nodeRadius, 0)

	def translateAll(self, axis, d):
		for wireframe in self.wireframes.itervalues():
			wireframe.translate(axis, d)

	def scaleAll(self, scale, center):
		center_x = center[0]
		center_y = center[1]

		for wireframe in self.wireframes.itervalues():
			wireframe.scale((center_x, center_y), scale)

	def rotateAll(self, axis, theta):
		rotateFunction = "rotate" + axis

		for wireframe in self.wireframes.itervalues():
			center = wireframe.findCenter()
			getattr(wireframe, rotateFunction)(center, theta)

	def clearAll(self):
		self.wireframes = {}


pv = ProjectionViewer(800, 600)

"""for i in range(0,5):
	placeCube((300+200*i,300),pv)"""

tesseract = wireframe.Wireframe()
tesseract.addNodes([(x,y,z) for x in (150,350) for y in (100,300) for z in (150,350)]+[(x,y,z) for x in (200,300) for y in (150,250) for z in (200,300)])
#Basic edges for the two cubes
tesseract.addEdges([(n,n+4) for n in range(0,4)]+[(n,n+1) for n in range(0,8,2)]+[(n,n+2) for n in (0,1,4,5)]+[(n+8,n+12) for n in range(0,4)]+[(n+8,n+9) for n in range(0,8,2)]+[(n+8,n+10) for n in (0,1,4,5)])
#Edges for connecting the cubes
tesseract.addEdges([n,n+8]for n in range(0,8))

rectangle = wireframe.Wireframe()
rectangle.addNodes([(x,y,z) for x in (150,450) for y in (350,550) for z in (150,350)])
rectangle.addEdges([(n,n+4) for n in range(0,4)]+[(n,n+1) for n in range(0,8,2)]+[(n,n+2) for n in (0,1,4,5)])

prism = wireframe.Wireframe()
prism.addNodes([(100,100,100),(200,100,100),(200,100,200),(125,200,125)])
prism.addEdges([(0,1),(0,2),(1,2)] + [(x,3) for x in range(0,3)])

pv.addWireframe("prism", prism)
#pv.addWireframe("tesseract", tesseract)
#pv.addWireframe("cube2", cube2)
#pv.addWireframe("rectangle", rectangle)

pv.run()