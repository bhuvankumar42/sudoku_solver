import pygame

pygame.font.init()

BLACK = (0, 0, 0)
GREEN = (0, 170, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
FPS = 30

def find_empty(bo):
	for i, row in enumerate(bo):
		for j, val in enumerate(row):
			if val == 0:
				return (i, j) #(row, column)
	return None

def valid(bo, num, pos):
	#row
	for i in range(len(bo[0])):
		if bo[pos[0]][i] == num and pos[1] != i:
			return False

	#column
	for i in range(len(bo)):
		if bo[i][pos[1]] == num and pos[0] != i:
			return False

	#box
	box_row = pos[0]//3
	box_col = pos[1]//3
	
	for i in range(box_row * 3, box_row * 3 + 3):
		for j in range(box_col * 3, box_col * 3 + 3):
			if bo[i][j] == num and pos != (i, j):
				return False

	return True


class Grid():
	board = [
		[5, 3, 0, 0, 7, 0, 0, 0, 0],
		[6, 0, 0, 1, 9, 5, 0, 0, 0],
		[0, 9, 8, 0, 0, 0, 0, 6, 0],
		[8, 0, 0, 0, 6, 0, 0, 0, 3],
		[4, 0, 0, 8, 0, 3, 0, 0, 1],
		[7, 0, 0, 0, 2, 0, 0, 0, 6],
		[0, 6, 0, 0, 0, 0, 2, 8, 0],
		[0, 0, 0, 4, 1, 9, 0, 0, 5],
		[0, 0, 0, 0, 8, 0, 0, 7, 9]
	]

	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.cells = [[Cell(self.board[i][j], i, j) for j in range(9)] for i in range(9)]
		self.selected = None

	def draw(self, win):
		row = 9
		cell_side = self.width/row
		#rows
		for i in range(0, row+1):
			if i % 3 == 0:
				pygame.draw.line(win, BLACK, (0, i*cell_side), (self.height, i*cell_side), 3)
			else:
				pygame.draw.line(win, BLACK, (0, i*cell_side), (self.height, i*cell_side), 1)

		#columns
		for i in range(0, row+1):
			if i % 3 == 0:
				pygame.draw.line(win, BLACK, (i*cell_side, 0), (i*cell_side, self.width), 3)
			else:
				pygame.draw.line(win, BLACK, (i*cell_side, 0), (i*cell_side, self.width), 1)

		#numbers inside cells
		for i in range(9):
			for j in range(9):
				self.cells[i][j].draw(win)

	def valid_solution(self):
		#to check if a solution exists for given board
		for i in range(9):
			for j in range(9):
				if not valid(self.board, self.board[i][j], (i, j)):
					return False
		return True

	def select(self, row, col):
		for i in range(9):
			for j in range(9):
				self.cells[i][j].selected = False

		self.cells[row][col].selected = True
		self.selected = (row, col)

	def click(self, pos):
		#to select a cell with a mouse click
		if pos[0] < self.width and pos[1] < self.height:
			gap = self.width / 9
			col = pos[0] // gap
			row = pos[1] // gap
			return (int(row), int(col))
		else:
			return None

	def set_value(self, row, col, val):
		self.cells[row][col].value = val
		self.cells[row][col].colour = BLACK
		self.board[row][col] = val

	def clear_solution(self):
		#clearing the solution
		for row in range(9):
			for col in range(9):
				if self.cells[row][col].colour == GREEN:
					self.set_value(row, col, 0)

	def clear_board(self):
		#to clear the full board
		for row in range(9):
			for col in range(9):
				self.set_value(row, col, 0)

def redraw_window(win, grid):
	win.fill(WHITE)
	fnt = pygame.font.SysFont("comicsans", 20)
	text_1 = fnt.render("Press C to clear grid   |   Press X to clear solution", 1, BLACK)
	text_2 = fnt.render("Press DEL to clear selected cell", 1, BLACK)
	text_3 = fnt.render("Press SPACE for solution", 1, BLACK)
	win.blit(text_1, (5, 540))
	win.blit(text_2, (5, 565))
	win.blit(text_3, (5, 590))
	grid.draw(win)

def solve(grid):
	empty = find_empty(grid.board)
	if not empty:
		return True
	else:
		row, col = empty

	for i in range(1, 10):
		if valid(grid.board, i, (row, col)):
			grid.set_value(row, col, i)
			grid.cells[row][col].colour = GREEN
			
			if solve(grid):
				return True

			grid.board[row][col] = 0
	return False

class Cell:
	side = 540
	def __init__(self, value, row, col, colour=BLACK):
		self.value = value
		self.row = row
		self.col = col
		self.colour = colour
		self.selected = False

	def draw(self, win):
		fnt = pygame.font.SysFont("comicsans", 40)
		cell_size = self.side/9
		x = cell_size* self.col
		y = cell_size* self.row

		if self.value != 0:
			text = fnt.render(str(self.value), 1, self.colour)
			win.blit(text, (x + (cell_size/2 - text.get_width()/2), y + (cell_size/2 - text.get_height()/2)))

		if self.selected:
			if self.selected:
				pygame.draw.rect(win, (255, 0, 0), (x, y, cell_size, cell_size), 2)

def main():
	
	width, height = 540, 625
	win = pygame.display.set_mode((width, height))
	pygame.display.set_caption("Sudoku Solver")
	grid = Grid(540, 540)
	clock = pygame.time.Clock()
	clock.tick(FPS)
	run = True
	fnt = pygame.font.SysFont("comicsans", 60)
	no_solution = False
	i = 0

	while run:
		key = None
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					grid.clear_solution()
					solve(grid)
					no_solution = False
					if not grid.valid_solution():
						grid.clear_solution()
						no_solution = True

				if event.key == pygame.K_LEFT:
					if grid.selected != None and grid.selected[1] > 0:
						grid.select(grid.selected[0], grid.selected[1] - 1)

				if event.key == pygame.K_RIGHT:
					if grid.selected != None and grid.selected[1] < 8:
						grid.select(grid.selected[0], grid.selected[1] + 1)

				if event.key == pygame.K_UP:
					if grid.selected != None and grid.selected[0] > 0:
						grid.select(grid.selected[0] - 1 , grid.selected[1])

				if event.key == pygame.K_DOWN:
					if grid.selected != None and grid.selected[0] < 8:
						grid.select(grid.selected[0] + 1, grid.selected[1])

				if event.key == pygame.K_c:
					grid.clear_board()

				if event.key == pygame.K_x:
					grid.clear_solution()

				if event.key == pygame.K_DELETE:
					if grid.selected:
						grid.set_value(grid.selected[0], grid.selected[1], 0)

				if event.key == pygame.K_1 or event.key == pygame.K_KP1:
					key = 1

				if event.key == pygame.K_2 or event.key == pygame.K_KP2:
					key = 2

				if event.key == pygame.K_3 or event.key == pygame.K_KP3:
					key = 3

				if event.key == pygame.K_4 or event.key == pygame.K_KP4:
					key = 4

				if event.key == pygame.K_5 or event.key == pygame.K_KP5:
					key = 5

				if event.key == pygame.K_6 or event.key == pygame.K_KP6:
					key = 6

				if event.key == pygame.K_7 or event.key == pygame.K_KP7:
					key = 7

				if event.key == pygame.K_8 or event.key == pygame.K_KP8:
					key = 8

				if event.key == pygame.K_9 or event.key == pygame.K_KP9:
					key = 9

			if event.type == pygame.MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()
				clicked = grid.click(pos)
				if clicked:
					grid.select(clicked[0], clicked[1])

		if key and grid.selected:
			grid.set_value(grid.selected[0], grid.selected[1], key)
		
		redraw_window(win, grid) 
		
		if no_solution and i < 45:
			text = fnt.render("No Solution!", 1, RED)
			pygame.draw.rect(win, WHITE, (270 - text.get_width()/2 , 270 - text.get_height()/2, text.get_width(), text.get_height()))
			win.blit(text, (270 - text.get_width()/2 , 270 - text.get_height()/2))
			i += 1

		if i == 45 or not no_solution:
			i = 0
			no_solution = False    		

		pygame.display.update()

	pygame.quit()

if __name__ == '__main__':
	main()

