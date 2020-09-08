import pygame as pg
pg.init()
pg.font.init()

WHITE   = (255, 255, 255)
BLACK   = (  0,   0,   0)
RED     = (255,   0,   0)
GREEN   = (  0, 255,   0)
BLUE    = (  0,   0, 255)
YELLOW  = (255, 255,   0)
MAGENTA = (255,   0, 255)
CYAN    = (  0, 255, 255)

TILE_SIZE = 50
ROWS = 10
COLUMNS = 20
OFFSET = 1

font_size = int(TILE_SIZE/3)
font = pg.font.SysFont('roboto', font_size, False, False)
font_size_big = int(TILE_SIZE/2)
fontBig = pg.font.SysFont('roboto', font_size_big, False, False)

START = (0, 0)
END = (9, 19)

d_cost = 14 # diagonal cost
n_cost = 10	# normal cost

MIN_TILE = None

FINAL_PATH = []


def heuristic(start, goal):

	dx = abs(start[0] - goal[0])
	dy = abs(start[1] - goal[1])
	return n_cost * (dx + dy) + (d_cost - 2 * n_cost) * min(dx, dy)


def CalculateAllCost(current_tile):

	row = current_tile.row
	column = current_tile.column

	# Para encontrar de donde viene la casilla (solo una anterior) busca las 8 de alrededor,
	# compara las G, y se queda con la menor
	smallest_G_tile = find_least_G(current_tile)
	current_tile.comes_from = smallest_G_tile

	current_tile.G = heuristic((smallest_G_tile.row, smallest_G_tile.column), (row, column)) + smallest_G_tile.G
	current_tile.H = heuristic((row, column), END)
	current_tile.F = current_tile.G + current_tile.H


def find_least_G(tile):
	
	nearby_tiles = find_nearby_tiles(tile)

	smallest_G_tile = None
	for t in nearby_tiles:
		
		if smallest_G_tile == None:

			if t.closed:
				smallest_G_tile = t
			else:
				next
		else:

			if t.closed and smallest_G_tile.G > t.G:
				smallest_G_tile = t

	return smallest_G_tile


def find_nearby_tiles(tile):

	tiles_list = []
	row = tile.row
	col = tile.column
	minRow = row-1 if row > 0 else 0 
	maxRow = row+1 if row < len(BOARD)-1 else len(BOARD)-1
	minCol = col-1 if col > 0 else 0
	maxCol = col+1 if col < len(BOARD[0])-1 else len(BOARD[0])-1
	
	for r in range(minRow, maxRow+1, 1):
		for c in range(minCol, maxCol+1, 1):
			if r != row or c != col and not BOARD[r][c].wall:
				tiles_list.append(BOARD[r][c])

	return tiles_list


def openTiles(current_tile):

	nearby_tiles = find_nearby_tiles(current_tile)
	for tile in nearby_tiles:
		if not tile.closed and not tile.wall:
			tile.open = True


def closeTiles(tile):

	global MIN_TILE

	if tile.open:
		if MIN_TILE == None:
			MIN_TILE = tile
		else:
			if MIN_TILE.F > tile.F:
				MIN_TILE = tile
			elif MIN_TILE.F == tile.F:
				if MIN_TILE.H > tile.H:
					MIN_TILE = tile


def make_final_path(tile):

	FINAL_PATH.append(tile)
	tile.path = True

	if tile.comes_from == None:
		return
	else:
		return make_final_path(tile.comes_from)


def draw_final_path(path):

	for i in range(len(path)-1):
		tile = path[i].rect.centerx, path[i].rect.centery
		tile2 = path[i+1].rect.centerx, path[i+1].rect.centery

		pg.draw.line(SCREEN, YELLOW, tile, tile2, int(TILE_SIZE/10))


class Tile:

	def __init__(self, row, column, offset):

		self.row = row
		self.column = column

		s = TILE_SIZE
		o = OFFSET
		x = column*s + o*(column + 1)
		y = row*s + o*(row + 1)

		self.rect = pg.Rect((x, y), (s, s))

		self.wall = False
		self.start = False if (row, column) != START else True
		self.end = False if (row, column) != END else True
		self.path = False
		self.open = False
		self.closed = False if not self.start else True

		self.color = WHITE

		self.G = 0
		self.H = 0
		self.F = 0

		self.comes_from = None

	def draw(self):

		if self.wall:
			self.color = BLACK
		elif self.start:
			self.color = CYAN
		elif self.end:
			self.color = MAGENTA
		elif self.open:
			self.color = GREEN
		elif self.closed:
			self.color = RED
		else:
			self.color = WHITE

		#if self.path and not (self.start or self.end):
		#	self.color = YELLOW

		pg.draw.rect(SCREEN, self.color, self.rect)

		
		if self.color != WHITE:
			
			self.textF = fontBig.render(str(self.F), True, BLACK)
			self.textG = font.render(str(self.G), True, BLACK)
			self.textH = font.render(str(self.H), True, BLACK)
			
			self.textFrect = self.textF.get_rect(center = (self.rect.x + TILE_SIZE/2, TILE_SIZE*.75 + self.rect.y))
			self.textGrect = self.textG.get_rect(center = (self.rect.x + TILE_SIZE/4, self.rect.y + TILE_SIZE/3.5))
			self.textHrect = self.textH.get_rect(center = (self.rect.right - TILE_SIZE/4, self.rect.y + TILE_SIZE/3.5))
			
			SCREEN.blit(self.textF, self.textFrect)
			SCREEN.blit(self.textG, self.textGrect)
			SCREEN.blit(self.textH, self.textHrect)
		

	def update(self, pos, pressed):

		global MIN_TILE

		if self.rect.collidepoint(pos) and not self.start and not self.end:

			if pressed[0]:
				self.wall = True
			if pressed[2]:
				self.wall = False

			"""
			if pressed[2]:
				self.open = False
				self.closed = True
			"""

		if start:
			if self.closed:
				self.open = False
				openTiles(self)
			if (self.open or self.closed) and not (self.start or self.wall):
				CalculateAllCost(self)

		self.draw()


SCREEN = pg.display.set_mode((COLUMNS*(TILE_SIZE + OFFSET) + OFFSET, ROWS*(TILE_SIZE + OFFSET) + OFFSET))


#--- C R E A T E   B O A R D ---#

def Board():

	board = []
	for row in range(ROWS):
		column_list = []

		for column in range(COLUMNS):
			column_list.append(Tile(row, column, OFFSET))
		
		board.append(column_list)
	return board

BOARD = Board()

#--- C R E A T E   B O A R D ---#


#--- M A I N   L O O P ---#

done = False
start = False
while not done:
	for event in pg.event.get():
		if event.type == pg.QUIT:
			done = True
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_SPACE:
				start = True

	SCREEN.fill(BLACK)

	for row in BOARD:
		for tile in row:
			tile.update(pg.mouse.get_pos(), pg.mouse.get_pressed())
			if start:
				closeTiles(tile)

	if MIN_TILE != None:
		MIN_TILE.open = False
		MIN_TILE.closed = True
		if MIN_TILE.end == True:
			start = False
			make_final_path(MIN_TILE)

		MIN_TILE = None

	if FINAL_PATH != []:
		draw_final_path(FINAL_PATH)

	pg.display.flip()

#--- M A I N   L O O P ---#

pg.quit()