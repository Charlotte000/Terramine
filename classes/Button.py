
import pygame
pygame.font.init()

class Button:
	def __init__(self, pos, text, fontSize, isActive=True):
		self.pos = pos
		self.text = text
		self.font = pygame.font.Font(r"data\font.ttf", fontSize)

		if isinstance(text, list):
			self.size = [
				max(self.font.size(i)[0] for i in self.text), 
				sum(self.font.size(i)[1] + 5 for i in self.text)
			]
		else:
			self.size = list(self.font.size(self.text))
		self.size[0] += 20
		self.size[1] += 20

		self.hover = False
		self.isActive = isActive

	def render(self, mousePos):
		if self.isActive:
			isCollide = pygame.Rect((self.pos[0] - self.size[0] / 2, 
				self.pos[1] - self.size[1] / 2, *self.size)).collidepoint(mousePos)

			if not self.hover and isCollide:
				self.size[0] += 15
				self.size[1] += 15
			elif self.hover and not isCollide:
				self.size[0] -= 15
				self.size[1] -= 15
			self.hover = isCollide

	def draw(self, window):
		pygame.draw.rect(
			window, 
			(137, 135, 135) if self.hover else (107, 105, 105), 
			(self.pos[0] - self.size[0] / 2, self.pos[1] - self.size[1] / 2, *self.size))
		pygame.draw.rect(
			window, 
			(215, 215, 215), 
			(self.pos[0] - self.size[0] / 2, self.pos[1] - self.size[1] / 2, *self.size), 
			1)

		if isinstance(self.text, list):
			for off, i in enumerate(self.text):
				size = list(self.font.size(i))
				window.blit(
					self.font.render(i, False, (255, 255, 255)), 
					(
						self.pos[0] - size[0] / 2, 
						self.pos[1] - self.size[1] / 2 + 10 + (size[1] + 5) * off
					))
		else:
			size = list(self.font.size(self.text))
			window.blit(
				self.font.render(self.text, False, (255, 255, 255)), 
				(self.pos[0] - size[0] / 2, self.pos[1] - size[1] / 2))
