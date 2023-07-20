from tkinter import Frame, Label, CENTER
from operator import itemgetter
import random
import logic
import time
import copy
import constants as c

def gen():
    return random.randint(0, c.GRID_LEN - 1)

class GameGrid(Frame):
    def __init__(self):
        Frame.__init__(self)

        self.grid()
        self.master.title('2048')
        self.master.bind("<Key>", self.key_down)

        self.commands = {
            c.KEY_UP: logic.up,
            c.KEY_DOWN: logic.down,
            c.KEY_LEFT: logic.left,
            c.KEY_RIGHT: logic.right,
            c.KEY_UP_ALT1: logic.up,
            c.KEY_DOWN_ALT1: logic.down,
            c.KEY_LEFT_ALT1: logic.left,
            c.KEY_RIGHT_ALT1: logic.right,
            c.KEY_UP_ALT2: logic.up,
            c.KEY_DOWN_ALT2: logic.down,
            c.KEY_LEFT_ALT2: logic.left,
            c.KEY_RIGHT_ALT2: logic.right,
        }

        self.grid_cells = []
        self.init_grid()
        self.matrix = logic.new_game(c.GRID_LEN)
        self.history_matrixs = []
        self.update_grid_cells()

        # RUN AGENT HERE
        # self.greedyAction()
        # self.greedyActionMonotonicity()
        # self.greedyActionMonoSmooth()
        # self.greedyActionEmpty()
        # self.greedyActionCornerPriority()
        # self.minimax_cutoff(('left', list(self.matrix)), 2, "max")
        # self.minimaxAgent()
        self.expectimaxAgent()

        self.mainloop()

    def init_grid(self):
        background = Frame(self, bg=c.BACKGROUND_COLOR_GAME,width=c.SIZE, height=c.SIZE)
        background.grid()

        for i in range(c.GRID_LEN):
            grid_row = []
            for j in range(c.GRID_LEN):
                cell = Frame(
                    background,
                    bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                    width=c.SIZE / c.GRID_LEN,
                    height=c.SIZE / c.GRID_LEN
                )
                cell.grid(
                    row=i,
                    column=j,
                    padx=c.GRID_PADDING,
                    pady=c.GRID_PADDING
                )
                t = Label(
                    master=cell,
                    text="",
                    bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                    justify=CENTER,
                    font=c.FONT,
                    width=5,
                    height=2)
                t.grid()
                grid_row.append(t)
            self.grid_cells.append(grid_row)

    def update_grid_cells(self):
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="",bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(
                        text=str(new_number),
                        bg=c.BACKGROUND_COLOR_DICT[new_number],
                        fg=c.CELL_COLOR_DICT[new_number]
                    )
        self.update_idletasks()

    def key_down(self, event):
        key = event.keysym
        print(event)
        if key == c.KEY_QUIT: exit()
        if key == c.KEY_BACK and len(self.history_matrixs) > 1:
            self.matrix = self.history_matrixs.pop()
            self.update_grid_cells()
            print('back on step total step:', len(self.history_matrixs))
        elif key in self.commands: # up, down, left, right key_down actions
            self.matrix, done = self.commands[key](self.matrix) # given a key_down command, return the result of the action and game_state
            if done:
                self.matrix = logic.add_two(self.matrix)
                # record last move
                self.history_matrixs.append(self.matrix)
                # print(self.matrix) # view updated matrix
                self.update_grid_cells()
                if logic.game_state(self.matrix) == 'lose':
                    # self.grid_cells[1][1].configure(text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    # self.grid_cells[1][2].configure(text="Lose!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    print("lose")
        # print(self.history_matrixs)

    '''
    Greedy Agent (default)
    '''
    def greedyAction(self):
        done = False
        # printing the current board
        for i in range(len(self.matrix[0])):
            print(self.matrix[i])

        actions = {
            'left': list(logic.actionLeft(self.matrix)),
            'right': list(logic.actionRight(self.matrix)),
            'down': list(logic.actionDown(self.matrix)),
            'up': list(logic.actionUp(self.matrix))
        }

        print("left val: "+str(actions['left'][0]))
        print("right val: "+str(actions['right'][0]))
        print("down val: "+str(actions['down'][0]))
        print("up val: "+str(actions['up'][0]))
        # return max_val's key
        max_val_action = max(actions, key=actions.get)  # CHECK BACK ON THIS
        # return max_val
        max_val = max(actions['left'][0], actions['right'][0], actions['down'][0], actions['up'][0]) 
        # when largest value of all actions are 0 (no merges)
        if max_val == 0: 
            # stores the valid actions
            valid_actions = []
            for key in actions:
                # Invalid move (same matrix as original matrix)
                if actions[key][1] == self.matrix:
                    # set action's value to -1
                    actions[key][0] = -1
                    print(key+" is an INVALID MOVE")
                    print(actions[key][0])
                else:
                    valid_actions.append(key)

            max_val_action = random.choice(valid_actions)
            

        if max_val_action == 'left':
            self.matrix, done = logic.left(self.matrix)
        elif max_val_action == 'right':
            self.matrix, done = logic.right(self.matrix)
        elif max_val_action == 'down':
            self.matrix, done = logic.down(self.matrix)
        elif max_val_action == 'up':
            self.matrix, done = logic.up(self.matrix)
        else: 
            done = True
        
        # confirming changes
        if done:
            self.matrix = logic.add_two(self.matrix)
            self.history_matrixs.append(self.matrix)
            self.update_grid_cells()

            # game ending state
            if logic.game_state(self.matrix) == 'lose':
                print("lose")
                # print final state of board
                for i in range(len(self.matrix[0])):
                    print(self.matrix[i])
                
            else:
                # recursive call
                return self.greedyAction() 


    '''
    Greedy Agent with Monotonicity Heuristic
    '''
    def greedyActionMonotonicity(self):
        done = False
        for i in range(len(self.matrix[0])):
            print(self.matrix[i])

        actions = {
            'left': list(logic.actionLeft(self.matrix)),
            'right': list(logic.actionRight(self.matrix)),
            'down': list(logic.actionDown(self.matrix)),
            'up': list(logic.actionUp(self.matrix))
        }

        print("left val: "+str(actions['left'][0]))
        print("right val: "+str(actions['right'][0]))
        print("down val: "+str(actions['down'][0]))
        print("up val: "+str(actions['up'][0]))
        # return max_val's key
        max_val_action = max(actions, key=actions.get)  # CHECK BACK ON THIS
        # return max_val
        max_val = max(actions['left'][0], actions['right'][0], actions['down'][0], actions['up'][0]) 
        # when largest value of all actions are 0 (no merges)
        if max_val == 0: 
            # stores the valid actions
            valid_actions = []
            for key in actions:
                # Invalid move (same matrix as original matrix)
                if actions[key][1] == self.matrix:
                    # set action's value to -1
                    actions[key][0] = -1
                    print(key+" is an INVALID MOVE")
                    print(actions[key][0])
                else:
                    valid_actions.append(key)

            valid_action_scores = [] # list of tuples : ("left", 10)
            for i in valid_actions:
                valid_action_scores.append((i, self.monotonicity(actions[i][1])))
            max_val_action = max(valid_action_scores, key=itemgetter(1))[0]
    
        else:
            merged = [] # list to store moves that result in a merge
            for key in actions:
                if actions[key][0] != 0:
                    merged.append((key, self.monotonicity(actions[key][1]))) # score = monotonicity(actions[key][1])
            max_val_action = max(merged, key=itemgetter(1))[0]
            print("max_val_action_notZero: ",max_val_action)
            

        if max_val_action == 'left':
            self.matrix, done = logic.left(self.matrix)
        elif max_val_action == 'right':
            self.matrix, done = logic.right(self.matrix)
        elif max_val_action == 'down':
            self.matrix, done = logic.down(self.matrix)
        elif max_val_action == 'up':
            self.matrix, done = logic.up(self.matrix)
        else: 
            done = True
        
        # confirming changes
        if done:
            self.matrix = logic.add_two(self.matrix)
            self.history_matrixs.append(self.matrix)
            self.update_grid_cells()

            # game ending state
            if logic.game_state(self.matrix) == 'lose':
                print("lose")
                # print final state of board
                for i in range(len(self.matrix[0])):
                    print(self.matrix[i])
            else:
                # recursive call
                return self.greedyActionMonotonicity()

    '''
    Greedy Agent with Monotonicity & Smoothness Heuristic
    '''
    def greedyActionMonoSmooth(self):
        done = False
        for i in range(len(self.matrix[0])):
            print(self.matrix[i])

        actions = {
            'left': list(logic.actionLeft(self.matrix)),
            'right': list(logic.actionRight(self.matrix)),
            'down': list(logic.actionDown(self.matrix)),
            'up': list(logic.actionUp(self.matrix))
        }

        print("left val: "+str(actions['left'][0]))
        print("right val: "+str(actions['right'][0]))
        print("down val: "+str(actions['down'][0]))
        print("up val: "+str(actions['up'][0]))
        # return max_val's key
        max_val_action = max(actions, key=actions.get)  # CHECK BACK ON THIS
        # return max_val
        max_val = max(actions['left'][0], actions['right'][0], actions['down'][0], actions['up'][0]) 
        # when largest value of all actions are 0 (no merges)
        if max_val == 0: 
            # stores the valid actions
            valid_actions = []
            for key in actions:
                # Invalid move (same matrix as original matrix)
                if actions[key][1] == self.matrix:
                    # set action's value to -1
                    actions[key][0] = -1
                    print(key+" is an INVALID MOVE")
                    print(actions[key][0])
                else:
                    valid_actions.append(key)

            valid_action_scores = [] # list of tuples : ("left", 10)
            for i in valid_actions:
                valid_action_scores.append((i, self.monotonicity(actions[i][1])-self.smoothness(actions[i][1])))
            max_val_action = max(valid_action_scores, key=itemgetter(1))[0]
    
        else:
            merged = [] # list to store moves that result in a merge
            for key in actions:
                if actions[key][0] != 0:
                    merged.append((key, self.monotonicity(actions[key][1])-self.smoothness(actions[key][1]))) 
            max_val_action = max(merged, key=itemgetter(1))[0]
            print("max_val_action_notZero: ",max_val_action)
            

        if max_val_action == 'left':
            self.matrix, done = logic.left(self.matrix)
        elif max_val_action == 'right':
            self.matrix, done = logic.right(self.matrix)
        elif max_val_action == 'down':
            self.matrix, done = logic.down(self.matrix)
        elif max_val_action == 'up':
            self.matrix, done = logic.up(self.matrix)
        else: 
            done = True
        
        # confirming changes
        if done:
            self.matrix = logic.add_two(self.matrix)
            self.history_matrixs.append(self.matrix)
            self.update_grid_cells()

            # game ending state
            if logic.game_state(self.matrix) == 'lose':
                print("lose")
                # print final state of board
                for i in range(len(self.matrix[0])):
                    print(self.matrix[i])
            else:
                # recursive call
                return self.greedyActionMonoSmooth()

    '''
    Greedy Agent with Corner Priority + Smoothness Heuristic
    '''
    def greedyActionCornerPriority(self):
        done = False
        for i in range(len(self.matrix[0])):
            print(self.matrix[i])

        actions = {
            'left': list(logic.actionLeft(self.matrix)),
            'right': list(logic.actionRight(self.matrix)),
            'down': list(logic.actionDown(self.matrix)),
            'up': list(logic.actionUp(self.matrix))
        }

        print("left val: "+str(actions['left'][0]))
        print("right val: "+str(actions['right'][0]))
        print("down val: "+str(actions['down'][0]))
        print("up val: "+str(actions['up'][0]))
        # return max_val's key
        max_val_action = max(actions, key=actions.get)  # CHECK BACK ON THIS
        # return max_val
        max_val = max(actions['left'][0], actions['right'][0], actions['down'][0], actions['up'][0]) 
        # when largest value of all actions are 0 (no merges)
        if max_val == 0: 
            # stores the valid actions
            valid_actions = []
            for key in actions:
                # Invalid move (same matrix as original matrix)
                if actions[key][1] == self.matrix:
                    # set action's value to -1
                    actions[key][0] = -1
                    print(key+" is an INVALID MOVE")
                    print(actions[key][0])
                else:
                    valid_actions.append(key)

            valid_action_scores = [] # list of tuples : ("left", 10)
            for i in valid_actions:
                valid_action_scores.append((i, self.cornerPriority(actions[i][1])+self.smoothness(actions[i][1])))
            max_val_action = min(valid_action_scores, key=itemgetter(1))[0]
    
        else:
            merged = [] # list to store moves that result in a merge
            for key in actions:
                if actions[key][0] != 0:
                    merged.append((key, self.cornerPriority(actions[key][1])+self.smoothness(actions[key][1]))) # score = monotonicity(actions[key][1])
            max_val_action = min(merged, key=itemgetter(1))[0]
            print("max_val_action_notZero: ",max_val_action)
            

        if max_val_action == 'left':
            self.matrix, done = logic.left(self.matrix)
        elif max_val_action == 'right':
            self.matrix, done = logic.right(self.matrix)
        elif max_val_action == 'down':
            self.matrix, done = logic.down(self.matrix)
        elif max_val_action == 'up':
            self.matrix, done = logic.up(self.matrix)
        else: 
            done = True
        
        # confirming changes
        if done:
            self.matrix = logic.add_two(self.matrix)
            self.history_matrixs.append(self.matrix)
            self.update_grid_cells()

            # game ending state
            if logic.game_state(self.matrix) == 'lose':
                print("lose")
                # print final state of board
                for i in range(len(self.matrix[0])):
                    print(self.matrix[i])
            else:
                # recursive call
                return self.greedyActionCornerPriority()

    def minimaxAgent(self):
        # for i in range(len(self.matrix[0])):
        #     print(self.matrix[i])
        # print("\n")
        done = False
        actions = {
            'left': list(logic.actionLeft(self.matrix)),
            'right': list(logic.actionRight(self.matrix)),
            'down': list(logic.actionDown(self.matrix)),
            'up': list(logic.actionUp(self.matrix))
        }

        # filter out invalid actions. Valid actions appended into list
        valid_actions = []
        for action_name in actions:
            # valid action
            if actions[action_name][1] != self.matrix:
                # action = {'action_name': <action_name>, 'merge_val': 0, 'matrix': <matrix>, 'eval': 0}
                valid_actions.append({'action_name' : action_name, 'merge_val' : actions[action_name][0],'matrix' : actions[action_name][1], 'eval' : 0})
        max_action = {'action_name' : valid_actions[0]['action_name'], 'matrix' : valid_actions[0]['matrix'], 'eval' : float('inf')}

        for action in valid_actions:
            randomStates = [] 
            for row in range(c.GRID_LEN):
                for col in range(c.GRID_LEN):
                    action_matrix = action['matrix']
                    # access matrix for current observed action
                    if action_matrix[row][col] == 0:
                        action_matrix[row][col] = 2
                        randomStates.append({'matrix' : copy.deepcopy(action_matrix), 'eval': 0})
                        action_matrix[row][col] = 4
                        randomStates.append({'matrix' : copy.deepcopy(action_matrix), 'eval': 0})
                        action_matrix[row][col] = 0
            for state in randomStates:
                # CHOOSE EVALUATION HERE
                state['eval'] = self.cornerPriority(state['matrix'])-self.smoothness(state['matrix'])
            action['eval'] = (min(randomStates, key=lambda x:x['eval']))['eval']
        max_action = max(valid_actions, key=lambda x:x['eval'])

        if max_action['action_name'] == 'left':
            self.matrix, done = logic.left(self.matrix)
        elif max_action['action_name'] == 'right':
            self.matrix, done = logic.right(self.matrix)
        elif max_action['action_name'] == 'down':
            self.matrix, done = logic.down(self.matrix)
        elif max_action['action_name'] == 'up':
            self.matrix, done = logic.up(self.matrix)
        else: 
            done = True
        
        # confirming changes
        if done:
            self.matrix = logic.add_two(self.matrix)
            self.history_matrixs.append(self.matrix)
            self.update_grid_cells()

            # game ending state
            if logic.game_state(self.matrix) == 'lose':
                print("lose")
                # print final state of board
                for i in range(len(self.matrix[0])):
                    print(self.matrix[i])
            else:
                self.minimaxAgent()

    def expectimaxAgent(self):
        done = False
        actions = {
            'left': list(logic.actionLeft(self.matrix)),
            'right': list(logic.actionRight(self.matrix)),
            'down': list(logic.actionDown(self.matrix)),
            'up': list(logic.actionUp(self.matrix))
        }

        # filter out invalid actions. Valid actions appended into list
        valid_actions = []
        for action_name in actions:
            # valid action
            if actions[action_name][1] != self.matrix:
                # action = {'action_name': <action_name>, 'merge_val': 0, 'matrix': <matrix>, 'eval': 0}
                valid_actions.append({'action_name' : action_name, 'merge_val' : actions[action_name][0],'matrix' : actions[action_name][1], 'eval' : 0})
        

        for action in valid_actions:
            action_val = 0
            randomStates = [] 
            for row in range(c.GRID_LEN):
                for col in range(c.GRID_LEN):
                    action_matrix = action['matrix']
                    # access matrix for current observed action
                    if action_matrix[row][col] == 0:
                        action_matrix[row][col] = 2
                        randomStates.append({'matrix' : copy.deepcopy(action_matrix), 'eval': 0, 'prob': 0.9})
                        action_matrix[row][col] = 4
                        randomStates.append({'matrix' : copy.deepcopy(action_matrix), 'eval': 0, 'prob': 0.1})
                        action_matrix[row][col] = 0
            for state in randomStates:
                # CHOOSE EVALUATION HERE
                # state['eval'] = self.cornerPriority(state['matrix']) - self.smoothness(state['matrix']) # smoothness
                # state['eval'] = self.cornerPriority(state['matrix']) # cornerPriority
                # state['eval'] = self.monotonicity(state['matrix']) # monotonicity
                state['eval'] = self.emptyTile(state['matrix']) # emptyTile
                action_val += state['prob']*state['eval']
            action['eval'] = action_val
        max_action = max(valid_actions, key=lambda x:x['eval'])

        if max_action['action_name'] == 'left':
            self.matrix, done = logic.left(self.matrix)
        elif max_action['action_name'] == 'right':
            self.matrix, done = logic.right(self.matrix)
        elif max_action['action_name'] == 'down':
            self.matrix, done = logic.down(self.matrix)
        elif max_action['action_name'] == 'up':
            self.matrix, done = logic.up(self.matrix)
        else: 
            done = True
        
        # confirming changes
        if done:
            self.matrix = logic.add_two(self.matrix)
            self.history_matrixs.append(self.matrix)
            self.update_grid_cells()

            # game ending state
            if logic.game_state(self.matrix) == 'lose':
                print("lose")
                # print final state of board
                for i in range(len(self.matrix[0])):
                    print(self.matrix[i])
            else:
                self.minimaxAgent()

    # args: matrix, returns score
    def monotonicity(self, mat):
        best_score = -1
        turn = 1
        # covers the four corners of the board
        while turn < 5:
            current = 0
            for i in range(c.GRID_LEN):
                for j in range(c.GRID_LEN-1):
                    if mat[i][j] >= mat[i][j+1]:
                        current += 1
            for j in range(c.GRID_LEN):
                for i in range(c.GRID_LEN-1):
                    if mat[i][j] >= mat[i+1][j]:
                        current += 1
            if current > best_score:
                best_score = current
            mat = self.rot_90_deg_cw(mat)
            turn += 1

        return best_score

    def smoothness(self, mat):
        smoothness_score = 0
        # calculate row smoothness score
        for row in mat:
            for q in range(c.GRID_LEN-1):
                smoothness_score += abs(row[q] - row[q+1])
        # calculate column smoothness score
        for j in range(c.GRID_LEN):
            for k in range(c.GRID_LEN-1):
                smoothness_score += abs(mat[k][j] - mat[k+1][j])
        return smoothness_score

    def emptyTile(self, mat):
        empty_count = 0
        empty_multiplier = 100
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN-1):
                if mat[i][j] == 0:
                    empty_count += 1
        # print("empty_count: ",empty_count)
        return empty_multiplier*empty_count

    def cornerPriority(self, mat):
        # print("corner priority matrix")
        # print(mat)
        max_tile = max(max(tile) for tile in mat)
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN):
                if max_tile == mat[i][j]:
                    #check Manhattan distance from all corners 
                    top_left_dist = abs(i - 0) + abs(j - 0)
                    top_right_dist = abs(i - 0) + abs(j - 3)
                    bottom_left_dist = abs(i - 3) + abs(j - 0)
                    bottom_right_dist = abs(i - 3) + abs(j - 3)
        best_score = min(top_left_dist, top_right_dist, bottom_left_dist, bottom_right_dist)
        return best_score

    def rot_90_deg_cw(self, mat):
        rot_matrix = []
        for i in range(len(mat[0])):
            temp_list = list(map(lambda x: x[i], mat))
            temp_list.reverse()
            rot_matrix.append(temp_list)
        return rot_matrix
        
    def generate_next(self):
        index = (gen(), gen())
        while self.matrix[index[0]][index[1]] != 0:
            index = (gen(), gen())
        self.matrix[index[0]][index[1]] = 2


game_grid = GameGrid()