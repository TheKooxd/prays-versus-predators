import pygame
import uuid
from random import randint
import math

pygame.init()

BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)

size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Hunting')

carryOn = True
 
clock = pygame.time.Clock()

class Food:
	def __init__(self, x, y, size):
		self.x = x
		self.y = y
		self.size = size
	type = "food"

class Entity:
	def __init__(self, id, x, y, type, sight, speed, maxStamina, maxHealth, generation):
		self.id = id
		self.x = x
		self.y = y
		self.type = type
		self.sight = sight
		self.speed = speed
		self.maxStamina = maxStamina
		self.stamina = maxStamina
		self.maxHealth = maxHealth
		self.health = maxHealth
		self.generation = generation
	mating = 0
	size = 5
	age = 0
	food = 50
	dmg = 5
	wonderX = None
	wonderY = None
	def get_closest_pray(self):
		smallestDist = 10000
		selectedPray = ""
		for pray in prays:
			dx, dy = pray.x - self.x, pray.y - self.y
			if (math.hypot(dx, dy) < smallestDist and pray.id is not self.id):
				smallestDist = math.hypot(dx, dy)
				selectedPray = pray
		return selectedPray
	def get_closest_predator(self):
		smallestDist = 10000
		selectedPredator = ""
		for predator in predators:
			dx, dy = self.x - predator.x, self.y - predator.y
			if math.hypot(dx, dy) < smallestDist:
				smallestDist = math.hypot(dx, dy)
				selectedPredator = predator
		return selectedPredator
	def move_towards(self, entity, running):
		dx, dy = entity.x - self.x, entity.y - self.y
		self.move_along_vector(dx, dy, running)
	def wonder(self, x, y):
		if (self.wonderX is None or (self.wonderX - self.x <= self.speed and self.wonderY - self.y <= self.speed )):
			self.wonderX = x
			self.wonderY = y
		dx, dy = self.wonderX - self.x, self.wonderY - self.y
		self.move_along_vector(dx, dy, False)
	def move_away(self, entity):
		dx, dy = self.x - entity.x, self.y - entity.y
		self.move_along_vector(dx, dy, True)
	def move_along_vector(self, dx, dy, run):
		dist = math.hypot(dx, dy)
		speedModifier = 1
		if self.stamina > 0:
			self.stamina -= 2
			speedModifier = 2
		if (dist > 0):
			dx, dy = dx / dist, dy / dist
			if self.on_screen(self.x + int(dx * self.speed), self.y + int(dy * self.speed)):
				self.x += int(dx * self.speed * speedModifier)
				self.y += int(dy * self.speed * speedModifier)
	def collides_with(self, entity):
		if entity.type is not "food":
			if(self.distanse_to(entity) < self.size + entity.size):
				return True
			else:
				return False
		if entity.type is "food":
			if(self.distanse_to(entity)) < self.size + int(entity.size / 3):
				return True
			else:
				return False
	def distanse_to(self, entity):
		dx, dy = self.x - entity.x, self.y - entity.y
		return math.hypot(dx, dy)
	def get_closest_food(self, dx, dy):
		dist = math.hypot(dx, dy)
		if (dist > 0):
			dx, dy = dx / dist, dy / dist
			if self.on_screen(self.x + int(dx * self.speed), self.y + int(dy * self.speed)):
				self.x += int(dx * self.speed)
				self.y += int(dy * self.speed)
	def has_entity_on_sight(self, type):
		if type == "predator":
			smallestDist = 10000
			for predator in predators:
				dx, dy = self.x - predator.x, self.y - predator.y
				if math.hypot(dx, dy) < smallestDist:
					smallestDist = math.hypot(dx, dy)
			if smallestDist < self.sight:
				return True
			else:
				return False
		if type == "pray":
			smallestDist = 10000
			for pray in prays:
				dx, dy = self.x - pray.x, self.y - pray.y
				if math.hypot(dx, dy) < smallestDist:
					smallestDist = math.hypot(dx, dy)
			if smallestDist < self.sight:
				return True
			else:
				return False
	def go_towards_food(self):
		smallestDist = 10000
		selectedFood = None
		for food in foods:
			dx, dy = food.x - self.x, food.y - self.y
			if math.hypot(dx, dy) < smallestDist:
				smallestDist = math.hypot(dx, dy)
				selectedFood = food
		if selectedFood is not None:
			self.move_towards(selectedFood, False)
	def on_screen(self, newx, newy):
		if(newx > 0 and newy > 0 and newx < 700 and newy < 500):
			return True
		else:
			return False
prays = []
predators = []
foods = []
firstTime = True

def multiply(entity1, entity2):
	temp = Entity(str(uuid.uuid4()), entity1.x, entity1.y, entity1.type, int((entity1.sight / entity2.sight) * (randint(90, 400) / 100 )), int((entity1.speed / entity2.speed) * (randint(90, 400) / 100 )), int((entity1.maxStamina / entity2.maxStamina) * (randint(90, 400) / 100 )), int((entity1.maxHealth / entity2.maxHealth) * (randint(90, 400) / 100 )), entity1.generation + 1)
	if entity1.type is "predator":
		predators.append(temp)
	else:
		prays.append(temp)

# -------- Main Program Loop -----------
while carryOn:
	predators = [x for x in predators if x.health > 0]
	prays = [x for x in prays if x.health > 0]
	foods = [x for x in foods if x.size > 0]

	# --- stat printing
	lastGenPred = None
	firstGenPred = None
	lastGenPray = None
	firstGenPray = None
	for predator in predators:
		if(predator.generation < lastGenPred or lastGenPred is None):
			lastGenPred = predator.generation
		if(predator.generation > firstGenPred or firstGenPred is None):
			firstGenPred = predator.generation
	for pray in prays:
		if(pray.generation < lastGenPray or lastGenPray is None):
			lastGenPray = pray.generation
		if(pray.generation > firstGenPray or firstGenPray is None):
			firstGenPray = pray.generation

	print ('predators: ', lastGenPred, ' <-> ', firstGenPred)
	print ('prays ', lastGenPray, ' <-> ', firstGenPray)

	if firstTime:
		for x in range(3):
			predators.append(Entity(str(uuid.uuid4()), randint(1, 200), randint(1, 150), "predator", 25, 2, 100, 100, 1))
		for x in range(10):
			prays.append(Entity(str(uuid.uuid4()), randint(500, 700), randint(250, 500), "pray", 25, 2, 100, 100, 1))
		for x in range(5):
			foods.append(Food(randint(500, 700), randint(250, 500), randint(100, 1000)))
		firstTime = False
	for event in pygame.event.get(): 
		if event.type == pygame.QUIT: 
			carryOn = False 

	for predator in predators:
		if (predator.has_entity_on_sight("pray") and predator.food < 90 and predator.health > 20):
			predator.move_towards(predator.get_closest_pray(), True)
		else:
			predator.wonder(randint(0, 700), randint(0, 500))
		if predator.food < 10:
			predator.health -= 5
		if (randint(0, 50) == 1 and predator.food is not 0):
			predator.food -= 1
		predator.stamina += 1
		predator.mating += 1 + (predator.food / 10 / 2) + (predator.health / 10 / 2)
		predator.age += 1
		if predator.age > 1500:
			predator.health = 0

	for pray in prays:
		for predator in predators:
			if pray.collides_with(predator):
				pray.health -= predator.dmg
				predator.food += 10 * pray.generation
		for prayList in prays:
			if ((pray.collides_with(prayList) and prayList.id is not pray.id) and pray.mating > 5000 and prayList.mating > 5000):
				multiply(pray, prayList)
				pray.mating = 0
				prayList.mating = 0
		for food in foods:
			if pray.collides_with(food):
				pray.food += 1
				food.size -= 1
		if pray.has_entity_on_sight("predator"):
			pray.move_away(pray.get_closest_predator())
		elif (pray.food > 50 and pray.mating > 5000):
			pray.move_towards(pray.get_closest_pray(), True)
		elif pray.food < 80:
			pray.go_towards_food()
		else:
			pray.wonder(randint(0, 700), randint(0, 500))
		if (randint(0, 100) > 97 and pray.food is not 0):
			pray.food -= 1
		if pray.food < 10:
			pray.health -= 1
		if pray.age > 1500:
			pray.health = 0
		pray.mating += (pray.food / 10 / 2) + (pray.health / 10 / 2)
		pray.stamina += 1
		pray.age += 1

	if (randint(0,50) == 5 and len(foods) < 10):
		foods.append(Food(randint(500, 700), randint(250, 500), randint(100, 1000)))

	screen.fill(BLACK)
	for food in foods:
		pygame.draw.rect(screen, WHITE, (food.x, food.y, int(food.size / 100), int(food.size / 100)), 0)
	for predator in predators:
		pygame.draw.circle(screen, RED, (predator.x, predator.y), predator.size, predator.size)
	for pray in prays:
		pygame.draw.circle(screen, GREEN, (pray.x, pray.y), pray.size, pray.size)
 
	pygame.display.flip()
     
	clock.tick(60)
 
pygame.quit()