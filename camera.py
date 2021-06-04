class Camera:
    width = 100 * 16
    height = 100 * 9
    pan_speed = 10
    boundary = 100

    def __init__(self, board, x, y, level_size):
        self.board = board
        self.x = x
        self.y = y
        self.level_size = level_size

        self.left = False  # if the user is moving the camera
        self.right = False
        self.up = False
        self.down = False

    def draw(self, window):
        self.board.draw(window)
        size = self.board.partition_size
        for arr in self.board.partitions:
            for block in arr:
                if block.x + size > self.x and \
                        block.y + size > self.y and \
                        block.x < self.x + self.width and \
                        block.y < self.y + self.height:
                    block.draw(window, self.x, self.y)

    def move(self):
        if self.up:
            self.y -= self.pan_speed
            self.y = max(self.y, self.boundary)
        if self.down:
            self.y += self.pan_speed
            self.y = min(self.y, self.level_size[1] - self.height + self.boundary)
        if self.left:
            self.x -= self.pan_speed
            self.x = max(self.x, self.boundary)
        if self.right:
            self.x += self.pan_speed
            self.x = min(self.x, self.level_size[0] - self.width - self.boundary)

    def center(self, pos):
        self.x = pos[0] - self.width / 2
        self.y = pos[1] - self.height / 2
