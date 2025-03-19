import random
import copy
import json

# Default Tetris pieces (tetrominos) and their rotations
SHAPES = {
    'I': [
        [[0, 0, 0, 0],
         [1, 1, 1, 1],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
        [[0, 0, 1, 0],
         [0, 0, 1, 0],
         [0, 0, 1, 0],
         [0, 0, 1, 0]]
    ],
    'J': [
        [[1, 0, 0],
         [1, 1, 1],
         [0, 0, 0]],
        [[0, 1, 1],
         [0, 1, 0],
         [0, 1, 0]],
        [[0, 0, 0],
         [1, 1, 1],
         [0, 0, 1]],
        [[0, 1, 0],
         [0, 1, 0],
         [1, 1, 0]]
    ],
    'L': [
        [[0, 0, 1],
         [1, 1, 1],
         [0, 0, 0]],
        [[0, 1, 0],
         [0, 1, 0],
         [0, 1, 1]],
        [[0, 0, 0],
         [1, 1, 1],
         [1, 0, 0]],
        [[1, 1, 0],
         [0, 1, 0],
         [0, 1, 0]]
    ],
    'O': [
        [[0, 0, 0, 0],
         [0, 1, 1, 0],
         [0, 1, 1, 0],
         [0, 0, 0, 0]]
    ],
    'S': [
        [[0, 1, 1],
         [1, 1, 0],
         [0, 0, 0]],
        [[0, 1, 0],
         [0, 1, 1],
         [0, 0, 1]]
    ],
    'T': [
        [[0, 1, 0],
         [1, 1, 1],
         [0, 0, 0]],
        [[0, 1, 0],
         [0, 1, 1],
         [0, 1, 0]],
        [[0, 0, 0],
         [1, 1, 1],
         [0, 1, 0]],
        [[0, 1, 0],
         [1, 1, 0],
         [0, 1, 0]]
    ],
    'Z': [
        [[1, 1, 0],
         [0, 1, 1],
         [0, 0, 0]],
        [[0, 0, 1],
         [0, 1, 1],
         [0, 1, 0]]
    ]
}

# Color theme presets
COLOR_THEMES = {
    'classic': {
        'I': '#00FFFF',  # Cyan
        'J': '#0000FF',  # Blue
        'L': '#FFA500',  # Orange
        'O': '#FFFF00',  # Yellow
        'S': '#00FF00',  # Green
        'T': '#800080',  # Purple
        'Z': '#FF0000'   # Red
    },
    'pastel': {
        'I': '#A5D8FF',  # Light Blue
        'J': '#A5B4FF',  # Light Purple
        'L': '#FFD8A5',  # Light Orange
        'O': '#FFFFA5',  # Light Yellow
        'S': '#A5FFA5',  # Light Green
        'T': '#D8A5FF',  # Light Pink
        'Z': '#FFA5A5'   # Light Red
    },
    'neon': {
        'I': '#00FFFF',  # Neon Cyan
        'J': '#4D4DFF',  # Neon Blue
        'L': '#FF8000',  # Neon Orange
        'O': '#FFFF00',  # Neon Yellow
        'S': '#00FF00',  # Neon Green
        'T': '#FF00FF',  # Neon Pink
        'Z': '#FF0000'   # Neon Red
    },
    'monochrome': {
        'I': '#FFFFFF',  # White
        'J': '#E0E0E0',  # Light Gray
        'L': '#C0C0C0',  # Silver
        'O': '#A0A0A0',  # Medium Gray
        'S': '#808080',  # Gray
        'T': '#606060',  # Dark Gray
        'Z': '#404040'   # Very Dark Gray
    },
    'dark': {
        'I': '#00AAAA',  # Dark Cyan
        'J': '#0000AA',  # Dark Blue
        'L': '#AA5500',  # Dark Orange
        'O': '#AAAA00',  # Dark Yellow
        'S': '#00AA00',  # Dark Green
        'T': '#AA00AA',  # Dark Purple
        'Z': '#AA0000'   # Dark Red
    }
}

# Scoring systems
SCORING_SYSTEMS = {
    'standard': {
        1: 100,   # 1 line: 100 points
        2: 300,   # 2 lines: 300 points
        3: 500,   # 3 lines: 500 points
        4: 800    # 4 lines (Tetris): 800 points
    },
    'modern': {
        1: 100,   # 1 line: 100 points
        2: 300,   # 2 lines: 300 points
        3: 500,   # 3 lines: 500 points
        4: 800,   # 4 lines (Tetris): 800 points
        'soft_drop': 1,  # 1 point per cell for soft drop
        'hard_drop': 2   # 2 points per cell for hard drop
    },
    'competitive': {
        1: 100,   # Base points for 1 line
        2: 300,   # Base points for 2 lines
        3: 500,   # Base points for 3 lines
        4: 800,   # Base points for 4 lines (Tetris)
        'combo_multiplier': 1.5,  # Multiplier for consecutive line clears
        'back_to_back': 1.5,      # Multiplier for back-to-back Tetrises
        'soft_drop': 1,           # 1 point per cell for soft drop
        'hard_drop': 2            # 2 points per cell for hard drop
    }
}

# Speed levels (milliseconds per drop)
SPEED_LEVELS = {
    1: 1000,  # Beginner: 1 second per drop
    2: 750,   # Easy: 0.75 seconds per drop
    3: 500,   # Medium: 0.5 seconds per drop
    4: 300,   # Hard: 0.3 seconds per drop
    5: 100    # Expert: 0.1 seconds per drop
}

class TetrisGame:
    def __init__(self, width=10, height=20, speed_level=1, scoring_system='standard', color_theme='classic'):
        self.width = width
        self.height = height
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.current_piece = None
        self.current_x = 0
        self.current_y = 0
        self.current_rotation = 0
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.game_over = False
        self.next_piece = None
        self.combo_count = 0
        self.last_clear_was_tetris = False
        self.speed_level = speed_level
        self.scoring_system = scoring_system
        self.color_theme = color_theme
        self.new_piece()
    
    def new_piece(self):
        """Generate a new random piece"""
        if self.next_piece:
            self.current_piece = self.next_piece
        else:
            self.current_piece = random.choice(list(SHAPES.keys()))
        
        self.next_piece = random.choice(list(SHAPES.keys()))
        self.current_rotation = 0
        self.current_x = self.width // 2 - len(SHAPES[self.current_piece][0][0]) // 2
        self.current_y = 0
        
        # Check if the new piece can be placed
        if not self.is_valid_position():
            self.game_over = True
    
    def rotate(self):
        """Rotate the current piece"""
        if not self.game_over:
            old_rotation = self.current_rotation
            self.current_rotation = (self.current_rotation + 1) % len(SHAPES[self.current_piece])
            if not self.is_valid_position():
                self.current_rotation = old_rotation
    
    def move_left(self):
        """Move the current piece left"""
        if not self.game_over:
            self.current_x -= 1
            if not self.is_valid_position():
                self.current_x += 1
    
    def move_right(self):
        """Move the current piece right"""
        if not self.game_over:
            self.current_x += 1
            if not self.is_valid_position():
                self.current_x -= 1
    
    def move_down(self):
        """Move the current piece down"""
        if not self.game_over:
            self.current_y += 1
            if not self.is_valid_position():
                self.current_y -= 1
                self.lock_piece()
                self.clear_lines()
                self.new_piece()
                return False
            
            # Add points for soft drop in modern and competitive scoring
            if self.scoring_system in ['modern', 'competitive']:
                self.score += SCORING_SYSTEMS[self.scoring_system]['soft_drop']
                
            return True
    
    def drop(self):
        """Drop the current piece to the bottom"""
        if not self.game_over:
            drop_distance = 0
            while True:
                self.current_y += 1
                if not self.is_valid_position():
                    self.current_y -= 1
                    break
                drop_distance += 1
            
            # Add points for hard drop in modern and competitive scoring
            if self.scoring_system in ['modern', 'competitive'] and drop_distance > 0:
                self.score += drop_distance * SCORING_SYSTEMS[self.scoring_system]['hard_drop']
                
            self.lock_piece()
            self.clear_lines()
            self.new_piece()
    
    def is_valid_position(self):
        """Check if the current piece position is valid"""
        shape = SHAPES[self.current_piece][self.current_rotation]
        for y in range(len(shape)):
            for x in range(len(shape[0])):
                if shape[y][x] == 0:
                    continue
                
                board_x = self.current_x + x
                board_y = self.current_y + y
                
                if (board_x < 0 or board_x >= self.width or 
                    board_y < 0 or board_y >= self.height or 
                    self.board[board_y][board_x] != 0):
                    return False
        return True
    
    def lock_piece(self):
        """Lock the current piece in place"""
        shape = SHAPES[self.current_piece][self.current_rotation]
        for y in range(len(shape)):
            for x in range(len(shape[0])):
                if shape[y][x] == 1:
                    self.board[self.current_y + y][self.current_x + x] = self.current_piece
    
    def clear_lines(self):
        """Clear completed lines and update score"""
        lines_cleared = 0
        y = self.height - 1
        while y >= 0:
            if all(self.board[y]):
                lines_cleared += 1
                # Move all lines above down
                for y2 in range(y, 0, -1):
                    self.board[y2] = copy.deepcopy(self.board[y2-1])
                # Clear the top line
                self.board[0] = [0 for _ in range(self.width)]
            else:
                y -= 1
        
        if lines_cleared > 0:
            # Update total lines cleared
            self.lines_cleared += lines_cleared
            
            # Update level every 10 lines
            self.level = (self.lines_cleared // 10) + 1
            
            # Calculate score based on scoring system
            if self.scoring_system == 'standard':
                if lines_cleared in SCORING_SYSTEMS['standard']:
                    self.score += SCORING_SYSTEMS['standard'][lines_cleared] * self.level
            
            elif self.scoring_system == 'modern':
                if lines_cleared in SCORING_SYSTEMS['modern']:
                    self.score += SCORING_SYSTEMS['modern'][lines_cleared] * self.level
            
            elif self.scoring_system == 'competitive':
                base_score = SCORING_SYSTEMS['competitive'][lines_cleared] * self.level
                
                # Apply combo multiplier
                if self.combo_count > 0:
                    base_score *= (1 + (self.combo_count * 0.1))
                
                # Apply back-to-back bonus for Tetrises
                if lines_cleared == 4:
                    if self.last_clear_was_tetris:
                        base_score *= SCORING_SYSTEMS['competitive']['back_to_back']
                    self.last_clear_was_tetris = True
                else:
                    self.last_clear_was_tetris = False
                
                self.score += int(base_score)
                self.combo_count += 1
        else:
            # Reset combo if no lines were cleared
            self.combo_count = 0
    
    def get_game_state(self):
        """Return the current game state as a dictionary"""
        # Create a copy of the board for rendering
        render_board = copy.deepcopy(self.board)
        
        # Add the current piece to the render board
        if not self.game_over:
            shape = SHAPES[self.current_piece][self.current_rotation]
            for y in range(len(shape)):
                for x in range(len(shape[0])):
                    if shape[y][x] == 1:
                        board_y = self.current_y + y
                        board_x = self.current_x + x
                        if 0 <= board_y < self.height and 0 <= board_x < self.width:
                            render_board[board_y][board_x] = self.current_piece
        
        # Convert board to colors for rendering based on selected theme
        color_board = []
        for row in render_board:
            color_row = []
            for cell in row:
                if cell == 0:
                    color_row.append(None)
                else:
                    color_row.append(COLOR_THEMES[self.color_theme][cell])
            color_board.append(color_row)
        
        # Get next piece preview
        next_shape = SHAPES[self.next_piece][0]
        next_piece_preview = []
        for row in next_shape:
            preview_row = []
            for cell in row:
                if cell == 0:
                    preview_row.append(None)
                else:
                    preview_row.append(COLOR_THEMES[self.color_theme][self.next_piece])
            next_piece_preview.append(preview_row)
        
        return {
            'board': color_board,
            'score': self.score,
            'level': self.level,
            'lines_cleared': self.lines_cleared,
            'game_over': self.game_over,
            'next_piece': next_piece_preview,
            'combo_count': self.combo_count,
            'speed_level': self.speed_level,
            'scoring_system': self.scoring_system,
            'color_theme': self.color_theme
        }
