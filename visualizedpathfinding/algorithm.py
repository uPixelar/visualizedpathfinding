from collections import deque

DR = [-1, +1, 0, 0]
DC = [0, 0, +1, -1]

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.distance = None # for A*

class Algorithm:
    def __init__(self, grid:list[list[int]], start:tuple[int, int], goal:tuple[int, int]):
        self.grid = grid
        self.start = start
        self.goal = goal
        
        self.cost = 0
        self.finished = False
        self.current_node:Node = None
        self.solution:list[tuple[int, int]] = []
        
    def prepare_solution(self):
        node = self.current_node
        while node:
            self.solution.insert(0, node.state)
            node = node.parent
        
class BFS(Algorithm):
    def __init__(self, grid:list[list[int]], start:tuple[int, int], goal:tuple[int, int]):
        super().__init__(grid, start, goal)
        
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.visited = [[False for _ in row] for row in grid]
        self.current_node:Node = Node(start)
        self.queue = deque((self.current_node, ))
        self.set_visited(start)
        self.found = False
        self.solution:list[tuple[int, int]] = []
        self.cost = 0
        
    def get_visited(self, state:tuple[int, int]):
        r, c = state
        return self.visited[r][c]
    
    def get_visited_n(self, node:Node):
        return self.get_visited(node.state)
    
    def set_visited(self, state:tuple[int, int], visited=True):
        r, c = state
        self.visited[r][c] = visited
    
    def set_visited_n(self, node:Node, visited=True):
        return self.set_visited(node.state, visited)
    
    def is_visitable(self, state:tuple[int, int]):
        r, c = state
        if r < 0 or c < 0 or r >= self.rows or c >= self.cols or self.grid[r][c] == 1 or self.get_visited((r, c)):
            return False
        
        return True
    
    def solve_instant(self):
        while not self.found and len(self.queue) > 0:
            self.solve()
            
        if self.found:
            self.solution.clear()
            node = self.current_node
            while node:
                self.solution.append(node.state)
                node = node.parent
            print("Found")
                
        else:
            print("Not found")
            
    def add_neighbours(self):
        r, c = self.current_node.state
        for i in range(4):
            rr = r + DR[i]
            cc = c + DC[i]
            
            if self.is_visitable((rr, cc)):
                self.queue.append(Node((rr, cc), self.current_node))
                
                self.set_visited((rr, cc))
        
        if len(self.queue) == 0: self.finished = True
            

    def solve(self):
        if self.finished: return self.current_node
        
        self.current_node = self.queue.popleft()
        self.cost += 1
        if self.goal == self.current_node.state:
            self.prepare_solution()
            self.found = True
            self.finished = True
            return self.current_node
        
        self.add_neighbours()
        return self.current_node
            

class GBFS(Algorithm):
    def __init__(self, grid:list[list[int]], start:tuple[int, int], goal:tuple[int, int]):
        super().__init__(grid, start, goal)
        
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.visited = [[False for _ in row] for row in grid]
        self.current_node:Node = Node(start)
        self.current_node.distance = self.dist_n(self.current_node)
        self.queue = [self.current_node]
        self.set_visited(start)
        self.found = False
        self.solution:list[tuple[int, int]] = []
        
        self.cost = 0
    
    def dist(self, state:tuple[int, int]): # manhattan distance
        return  abs(self.goal[0] - state[0]) + abs(self.goal[1] - state[1])
        
    def dist_n(self, node:Node):
        return self.dist(node.state)
    
    def get_visited(self, state:tuple[int, int]):
        r, c = state
        return self.visited[r][c]
    
    def get_visited_n(self, node:Node):
        return self.get_visited(node.state)
    
    def set_visited(self, state:tuple[int, int], visited=True):
        r, c = state
        self.visited[r][c] = visited
    
    def set_visited_n(self, node:Node, visited=True):
        return self.set_visited(node.state, visited)
    
    def is_visitable(self, state:tuple[int, int]):
        r, c = state
        if r < 0 or c < 0 or r >= self.rows or c >= self.cols or self.grid[r][c] == 1 or self.get_visited((r, c)):
            return False
        
        return True
    
    def solve_instant(self):
        while not self.found and len(self.queue) > 0:
            self.solve()
            
        if self.found:
            self.solution.clear()
            node = self.current_node
            while node:
                self.solution.append(node.state)
                node = node.parent
            print("Found")
                
        else:
            print("Not found")
            
    def add_neighbours(self):
        r, c = self.current_node.state
        for i in range(4):
            rr = r + DR[i]
            cc = c + DC[i]
            
            if self.is_visitable((rr, cc)):
                node = Node((rr, cc), self.current_node)
                node.distance = self.dist_n(node)
                
                inserted = False
                for i in range(len(self.queue)):
                    _node = self.queue[i]
                    if node.distance < _node.distance:
                        self.queue.insert(i, node)
                        inserted = True
                        break
                
                if not inserted:
                    self.queue.append(node)    
                
                self.set_visited((rr, cc))
        if len(self.queue) == 0: self.finished = True
            

    def solve(self):
        if self.finished: return self.current_node
        
        self.current_node = self.queue.pop(0)
        self.cost += 1
        if self.goal == self.current_node.state:
            self.prepare_solution()
            self.found = True
            self.finished = True
            return self.current_node
        
        self.add_neighbours()
        return self.current_node
    
class AStar(Algorithm):
    def __init__(self, grid:list[list[int]], start:tuple[int, int], goal:tuple[int, int]):
        super().__init__(grid, start, goal)
        
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.visited = [[False for _ in row] for row in grid]
        self.current_node:Node = Node(start)
        self.current_node.distance = self.dist_n(self.current_node)
        self.queue = [self.current_node]
        self.set_visited(start)
        self.found = False
        self.solution:list[tuple[int, int]] = []
        
        self.cost = 0
    
    def path_cost(self, node:Node):
        cost = 0
        while node:
            node = node.parent
            cost += 1
        return cost
        
    def dist_n(self, node:Node):
        return abs(self.goal[0] - node.state[0]) + abs(self.goal[1] - node.state[1]) + self.path_cost(node)
    
    def get_visited(self, state:tuple[int, int]):
        r, c = state
        return self.visited[r][c]
    
    def get_visited_n(self, node:Node):
        return self.get_visited(node.state)
    
    def set_visited(self, state:tuple[int, int], visited=True):
        r, c = state
        self.visited[r][c] = visited
    
    def set_visited_n(self, node:Node, visited=True):
        return self.set_visited(node.state, visited)
    
    def is_visitable(self, state:tuple[int, int]):
        r, c = state
        if r < 0 or c < 0 or r >= self.rows or c >= self.cols or self.grid[r][c] == 1 or self.get_visited((r, c)):
            return False
        
        return True
    
    def solve_instant(self):
        while not self.found and len(self.queue) > 0:
            self.solve()
            
        if self.found:
            self.solution.clear()
            node = self.current_node
            while node:
                self.solution.append(node.state)
                node = node.parent
            print("Found")
                
        else:
            print("Not found")
            
    def add_neighbours(self):
        r, c = self.current_node.state
        for i in range(4):
            rr = r + DR[i]
            cc = c + DC[i]
            
            if self.is_visitable((rr, cc)):
                node = Node((rr, cc), self.current_node)
                node.distance = self.dist_n(node)
                
                inserted = False
                for i in range(len(self.queue)):
                    _node = self.queue[i]
                    if node.distance <= _node.distance:
                        self.queue.insert(i, node)
                        inserted = True
                        break
                
                if not inserted:
                    self.queue.append(node)    
                
                self.set_visited((rr, cc))
        if len(self.queue) == 0: self.finished = True
            

    def solve(self):
        if self.finished: return self.current_node
        
        self.current_node = self.queue.pop(0)
        self.cost += 1
        if self.goal == self.current_node.state:
            self.prepare_solution()
            self.found = True
            self.finished = True
            return self.current_node
        
        self.add_neighbours()
        return self.current_node