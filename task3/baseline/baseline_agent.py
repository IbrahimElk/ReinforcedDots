import random

# FIXME:
# NEEDS TO CONERTED TO OUR REPRESENTATION. 
# THEN MAKE_MOVE FUNCTION CAN BE USED TO CHOOSE THE NEXT ACTION TO EXPLORE IN THE MINIMAX. 
# THAT FUNCTION DESCRIBES WHAT YOU SHOULD DO IN ORDER. 
# AND I THINK IT ADDRESSES WHAT JKB WAS TRYING TO SAY. 
# SEE ORIGINAL JAVASCRIPT IMPLEMENTATION. 

# TODO: TRY TO UNDERSTAND WHAT MAKE_MOVE FUNCTION DOES. 

# THIS WAS CONVERTED USING CHATGPT, IS NOT GUARANTEED TO BE CORRECT. 
class DotsAndBoxesSolver:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.player = 1
        self.score = [0, 0]
        self.h_ = [[0] * cols for _ in range(rows + 1)]
        self.v_ = [[0] * (cols + 1) for _ in range(rows)]
        self.box = [[0] * cols for _ in range(rows)]

    def restart(self):
        self.score = [0, 0]
        self.h_ = [[0] * self.cols for _ in range(self.rows + 1)]
        self.v_ = [[0] * (self.cols + 1) for _ in range(self.rows)]
        self.box = [[0] * self.cols for _ in range(self.rows)]
        if self.player != 1:
            self.make_move()

    def hmove(self, i, j):
        if self.h_[i][j] < 1:
            self.sethedge(i, j)
            if sum(self.score) == self.rows * self.cols:
                print(f"Game over.\nScore: Red = {self.score[0]}, Blue = {self.score[1]}")
            elif self.player == 0:
                self.make_move()

    def vmove(self, i, j):
        if self.v_[i][j] < 1:
            self.setvedge(i, j)
            if sum(self.score) == self.rows * self.cols:
                print(f"Game over.\nScore: Red = {self.score[0]}, Blue = {self.score[1]}")
            elif self.player == 0:
                self.make_move()

    def sethedge(self, x, y):
        self.h_[x][y] = 1
        if x > 0:
            self.box[x - 1][y] += 1
        if x < self.rows:
            self.box[x][y] += 1
        self.checkh(x, y)
        self.player = 1 - self.player

    def setvedge(self, x, y):
        self.v_[x][y] = 1
        if y > 0:
            self.box[x][y - 1] += 1
        if y < self.cols:
            self.box[x][y] += 1
        self.checkv(x, y)
        self.player = 1 - self.player

    def takeedge(self, zz, x, y):
        if zz > 1:
            self.setvedge(x, y)
        else:
            self.sethedge(x, y)

    def make_move(self):
        self.take_safe_3s()
        if self.sides3():
            if self.sides01():
                self.take_all_3s()
                self.takeedge(self.zz, self.x, self.y)
            else:
                self.sac(self.u, self.v)
            if sum(self.score) == self.rows * self.cols:
                print(f"Game over.\nScore: Red = {self.score[0]}, Blue = {self.score[1]}")
        elif self.sides01():
            self.takeedge(self.zz, self.x, self.y)
        elif self.singleton():
            self.takeedge(self.zz, self.x, self.y)
        elif self.doubleton():
            self.takeedge(self.zz, self.x, self.y)
        else:
            self.make_any_move()

    def take_safe_3s(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.box[i][j] == 3:
                    if self.v_[i][j] < 1:
                        if j == 0 or self.box[i][j - 1] != 2:
                            self.setvedge(i, j)
                    elif self.h_[i][j] < 1:
                        if i == 0 or self.box[i - 1][j] != 2:
                            self.sethedge(i, j)
                    elif self.v_[i][j + 1] < 1:
                        if j == self.cols - 1 or self.box[i][j + 1] != 2:
                            self.setvedge(i, j + 1)
                    else:
                        if i == self.rows - 1 or self.box[i + 1][j] != 2:
                            self.sethedge(i + 1, j)

    def sides3(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.box[i][j] == 3:
                    self.u = i
                    self.v = j
                    return True
        return False

    def take_all_3s(self):
        while self.sides3():
            self.take_box(self.u, self.v)

    def sides01(self):
        self.zz = 1 if random.random() < 0.5 else 2
        i = random.randint(0, self.rows - 1)
        j = random.randint(0, self.cols - 1)
        if self.zz == 1:
            if self.rand_hedge(i, j):
                return True
            else:
                self.zz = 2
                if self.rand_vedge(i, j):
                    return True
        else:
            if self.rand_vedge(i, j):
                return True
            else:
                self.zz = 1
                if self.rand_hedge(i, j):
                    return True
        return False

    def safehedge(self, i, j):
        if self.h_[i][j] < 1:
            if i == 0:
                if self.box[i][j] < 2:
                    return True
            elif i == self.rows:
                if self.box[i - 1][j] < 2:
                    return True
            elif self.box[i][j] < 2 and self.box[i - 1][j] < 2:
                return True
        return False

    def safevedge(self, i, j):
        if self.v_[i][j] < 1:
            if j == 0:
                if self.box[i][j] < 2:
                    return True
            elif j == self.cols:
                if self.box[i][j - 1] < 2:
                    return True
            elif self.box[i][j] < 2 and self.box[i][j - 1] < 2:
                return True
        return False

    def rand_hedge(self, i, j):
        x = i
        y = j
        while x != i or y != j:
            if self.safehedge(x, y):
                return True
            else:
                y += 1
                if y == self.cols:
                    y = 0
                    x += 1
                    if x == self.rows:
                        x = 0
        return False

    def rand_vedge(self, i, j):
        x = i
        y = j
        while x != i or y != j:
            if self.safevedge(x, y):
                return True
            else:
                y += 1
                if y > self.cols:
                    y = 0
                    x += 1
                    if x == self.rows:
                        x = 0
        return False

    def singleton(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.box[i][j] == 2:
                    numb = 0
                    if self.h_[i][j] < 1:
                        if i < 1 or self.box[i - 1][j] < 2:
                            numb += 1
                    self.zz = 2
                    if self.v_[i][j] < 1:
                        if j < 1 or self.box[i][j - 1] < 2:
                            numb += 1
                            if numb > 1:
                                self.x = i
                                self.y = j
                                return True
                    if self.v_[i][j + 1] < 1:
                        if j + 1 == self.cols or self.box[i][j + 1] < 2:
                            numb += 1
                            if numb > 1:
                                self.x = i
                                self.y = j + 1
                                return True
                    self.zz = 1
                    if self.h_[i + 1][j] < 1:
                        if i + 1 == self.rows or self.box[i + 1][j] < 2:
                            numb += 1
                            if numb > 1:
                                self.x = i + 1
                                self.y = j
                                return True
        return False

    def doubleton(self):
        self.zz = 2
        for i in range(self.rows):
            for j in range(self.cols - 1):
                if self.box[i][j] == 2 and self.box[i][j + 1] == 2 and self.v_[i][j + 1] < 1:
                    if self.ldub(i, j) and self.rdub(i, j + 1):
                        self.x = i
                        self.y = j + 1
                        return True
        self.zz = 1
        for j in range(self.cols):
            for i in range(self.rows - 1):
                if self.box[i][j] == 2 and self.box[i + 1][j] == 2 and self.h_[i + 1][j] < 1:
                    if self.udub(i, j) and self.ddub(i + 1, j):
                        self.x = i + 1
                        self.y = j
                        return True
        return False

    def ldub(self, i, j):
        if self.v_[i][j] < 1:
            if j < 1 or self.box[i][j - 1] < 2:
                return True
        elif self.h_[i][j] < 1:
            if i < 1 or self.box[i - 1][j] < 2:
                return True
        elif i == self.rows - 1 or self.box[i + 1][j] < 2:
            return True
        return False

    def rdub(self, i, j):
        if self.v_[i][j + 1] < 1:
            if j + 1 == self.cols or self.box[i][j + 1] < 2:
                return True
        elif self.h_[i][j] < 1:
            if i < 1 or self.box[i - 1][j] < 2:
                return True
        elif i + 1 == self.rows or self.box[i + 1][j] < 2:
            return True
        return False

    def udub(self, i, j):
        if self.h_[i][j] < 1:
            if i < 1 or self.box[i - 1][j] < 2:
                return True
        elif self.v_[i][j] < 1:
            if j < 1 or self.box[i][j - 1] < 2:
                return True
        elif j == self.cols - 1 or self.box[i][j + 1] < 2:
            return True
        return False

    def ddub(self, i, j):
        if self.h_[i + 1][j] < 1:
            if i == self.rows - 1 or self.box[i + 1][j] < 2:
                return True
        elif self.v_[i][j] < 1:
            if j < 1 or self.box[i][j - 1] < 2:
                return True
        elif j == self.cols - 1 or self.box[i][j + 1] < 2:
            return True
        return False

    def make_any_move(self):
        i = random.randint(0, self.rows - 1)
        j = random.randint(0, self.cols - 1)
        if random.random() < 0.5:
            self.takeedge(1, i, j)
        else:
            self.takeedge(2, i, j)

    def checkh(self, i, j):
        if i > 0 and j > 0:
            if self.box[i - 1][j] == 4:
                self.take_box(i - 1, j)
        if i < self.rows and j > 0:
            if self.box[i][j] == 4:
                self.take_box(i, j)

    def checkv(self, i, j):
        if i > 0 and j > 0:
            if self.box[i][j - 1] == 4:
                self.take_box(i, j - 1)
        if i > 0 and j < self.cols:
            if self.box[i][j] == 4:
                self.take_box(i, j)

    def take_box(self, i, j):
        self.box[i][j] = -self.player + 1
        self.score[self.player] += 1
        print(f"Player {self.player} takes box ({i}, {j})")


# Example usage:
game = DotsAndBoxesSolver(2, 2)
game.restart()



    