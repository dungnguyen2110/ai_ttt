import numpy as np

# 2 lớp Ultimate TTT_Move, State
# 1 lớp kế thừa State_2

# Lớp UltimateTTT_Move đại diện cho 1 nước đi trong trò chơi Tic-tac-toe
class UltimateTTT_Move:
    def __init__(self, index_local_board, x_coordinate, y_coordinate, value):
        # Chỉ số của bảng cục bộ (local board) trong trò chơi
        self.index_local_board = index_local_board
        # Tọa độ x của nước đi
        self.x = x_coordinate
        # Tọa độ y của nước đi
        self.y = y_coordinate
        #Gía tri (1 là X đi, -1 là O đi, 0 là ô trống)
        self.value = value
    

    def __repr__(self):
        return "local_board:{0}, (x:{1} y:{2}), value:{3}".format(
                self.index_local_board,
                self.x,
                self.y,
                self.value       
            )

        
class State:
    # Gía trị đại diện cho X là O
    X = 1
    O = -1
    
    # Biến cho biết liệu có "NƯỚC ĐI TỰ DO" không
    free_move = False
    
    def __init__(self, state = None): # init with 0 arg or 1 arg (state)
        # Lần đánh đầu tiên, khới tạo bảng
        if not state:
            # Mảng 9 phần tử: Bảng to
            self.global_cells = np.zeros(9)
            
            # Mảng 3x3: Bảng nhỏ
            self.blocks = np.array([np.zeros((3, 3)) for x in range(9)])
            
            # Người chơi hiện tại là X hay O, mặc định là player_1 đi trước
            self.player_to_move: int = 1
            
            # Nước đi trước đó
            self.previous_move:  UltimateTTT_Move = None
            
        # Các lần sau, copy bảng cũ, đánh tiếp
        else:
            self.global_cells = np.copy(state.global_cells)
            self.blocks = np.copy(state.blocks)
            self.player_to_move: int = state.player_to_move
            self.previous_move: UltimateTTT_Move = state.previous_move
    
    
    # In ro player đánh vào chỗ nào, trạng thái sao khi đánh
    def __repr__(self):        
        return '''player: {0} \n\nmove: {1} \n\nafter move:\n\n+ global cells: 
                \n\n{2}\n+ blocks:\n\n{3}
                \n#############################################\n'''.format(
                self.player_to_move * -1,
                self.previous_move,
                self.global_cells.reshape(3, 3),
                self.blocks
            )
    
    
    # game result on single board (local or global)
    # Kết quả trên bảng (bảng nhỏ hoặc bảng to)
    # X WIN => Tổng hàng || Tổng cột || Tổng đường chéo = 3
    # O WIN => Tổng hàng || Tổng cột || Tổng đường chéo = 3
    def game_result(self, board):
        row_sum = np.sum(board, 1)
        col_sum = np.sum(board, 0)
        diag_sum_topleft = board.trace()
        diag_sum_topright = board[::-1].trace()
        
        player_one_wins = any(row_sum == 3) + any(col_sum == 3)
        player_one_wins += (diag_sum_topleft == 3) + (diag_sum_topright == 3)
        
        if player_one_wins:
            return self.X

        player_two_wins = any(row_sum == -3) + any(col_sum == -3)
        player_two_wins += (diag_sum_topleft == -3) + (diag_sum_topright == -3)

        if player_two_wins:
            return self.O
        
        # Hòa
        if np.all(board != 0):
            return 0.
        
        # if not over
        # Chưa kết thúc
        return None
        
    # Kiểm tra xem trò chơi đã kết thúc chưa
    @property    
    def game_over(self):
        return self.game_result(self.global_cells.reshape(3,3)) != None
    
    # Trả về danh sách các nước đi hợp lê
    @property
    def get_valid_moves(self):
        # Xác định bước tiếp theo phải đi vào block nào nếu có người đánh trước đó
        if self.previous_move != None:
            index_local_board = self.previous_move.x * 3 + self.previous_move.y
            
        # Ngược lại, khởi tạo bảng ban đầu, return
        else: 
            temp_blocks = np.zeros((3, 3))
            indices = np.where(temp_blocks == 0)
            ret = []
            for i in range(9):
                ret += [UltimateTTT_Move(i, index[0], index[1], self.player_to_move)
                        for index in list(zip(indices[0], indices[1]))
                    ]
            return ret
            
        # Chuyển đến blcok cần đánh để đánh
        local_board = self.blocks[index_local_board]
        # Lấy các ô trống trên bảng cần đánh
        indices = np.where(local_board == 0)
        
        # Nếu còn ô trống thì đánh, trả về các ô trống
        if(len(indices[0]) != 0):
            self.free_move = False
            return [UltimateTTT_Move(index_local_board, index[0], 
                                     index[1], self.player_to_move)
                    for index in list(zip(indices[0], indices[1]))
                ]
        # chosen board is full   
        # Ngược lại, đi tự do vào bất kỳ chỗ nào trên bảng, trả về các ô trống   
        self.free_move = True        
        ret = []
        for i in range(9):
            if not np.all(self.blocks[i] != 0):
                indices = np.where(self.blocks[i] == 0)
                ret += [UltimateTTT_Move(i, index[0], index[1], self.player_to_move)
                        for index in list(zip(indices[0], indices[1]))
                    ]
        return ret
        
    # Kiểm tra các nước đi có hợp lệ không
    def is_valid_move(self, move: UltimateTTT_Move): 
        # Kiểm tra xem giá trị nước đi có phù hợp với người đi hiện tại
        # X phải là 1, O phải là 0    
        if move.value != self.player_to_move:
            return False
        
        # Tọa độ của x và y phải < 3 
        if move.x not in range(3) or move.y not in range(3):
            return False
        
        # Mếu có nước đi trước đó và nước đi hiên tại không phải là nước đi tự do
        # Nước đi hiện tại có nằm trong local_board không
        if self.previous_move and (not self.free_move):
            if(move.index_local_board != (self.previous_move.x * 3 + self.previous_move.y)):
                return False

        # Kiểm tra lại nước đã đánh có phải vào ô trống hay không
        board_to_move = self.blocks[move.index_local_board]
        return board_to_move[move.x, move.y] == 0 # check if board field not occupied yet
    
    # Thực hiện nuwocs đi và cập nhật trạng thái của trò chơi
    def act_move(self, move: UltimateTTT_Move):
        #  Kiểm tra nước đi hợp lệ, nếu không hợp lệ, ném lỗi
        if not self.is_valid_move(move):
            raise ValueError(
                "move {0} on local board is not valid".format(move)
            )
            
        # Đánh và lưu giá trị
        local_board = self.blocks[move.index_local_board]
        local_board[move.x, move.y] = move.value
        
        self.player_to_move *= -1          
        self.previous_move = move
        
        if self.global_cells[move.index_local_board] == 0: # not 'X' or 'O'
            if self.game_result(local_board):
                self.global_cells[move.index_local_board] = move.value
                
        # print(self)
    
    # Đếm số lượng X và O trên bảng to
    @property
    def count_X(self):
        return len((np.where(self.global_cells == 1))[0])
    
    @property
    def count_O(self):
        return len((np.where(self.global_cells == -1))[0])
        
  
class State_2(State):
    def __init__(self, state = None):
        super().__init__(state)
    
    @property
    def get_valid_moves(self):
        # Kiểm tra kỹ hơn, nếu ô đang đánh mà thuộc block đã có kết quả thì không được đánh
        
        is_occupied = False
        if self.previous_move != None:
            index_local_board = self.previous_move.x * 3 + self.previous_move.y
            if self.global_cells[index_local_board] != 0:
                is_occupied = True
        else:
            temp_blocks = np.zeros((3, 3))
            indices = np.where(temp_blocks == 0)
            ret = []
            for i in range(9):
                ret += [UltimateTTT_Move(i, index[0], index[1], self.player_to_move)
                        for index in list(zip(indices[0], indices[1]))
                    ]
            return ret
        
        local_board = self.blocks[index_local_board]
        indices = np.where(local_board == 0)
        
        # Nếu block đó còn ô trống và block đó chưa biết thắng thua thì đánh được
        # Ngược lại "Đánh tự do"
        if (len(indices[0]) != 0) and (not is_occupied):
            self.free_move = False
            return [UltimateTTT_Move(index_local_board, index[0], 
                                     index[1], self.player_to_move)
                    for index in list(zip(indices[0], indices[1]))
                ]
        # chosen block is full or occupied (1 or -1)      
        self.free_move = True        
        ret = []
        for i in range(9):
            if (self.global_cells[i] == 0) and (not np.all(self.blocks[i] != 0)):
                indices = np.where(self.blocks[i] == 0)
                ret += [UltimateTTT_Move(i, index[0], index[1], self.player_to_move)
                        for index in list(zip(indices[0], indices[1]))
                    ]
        return ret