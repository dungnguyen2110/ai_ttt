# Làm việc với ma trận
import numpy as np

# cur_state: trạng thái hiện tại của người chơi
# remain_time: thời gian còn lại để thực hiên nước đi
def select_move(cur_state, remain_time):
    # Lấy nước đi hộp lê
    valid_moves = cur_state.get_valid_moves
    
    # Nếu có ít nhất 1 nước đi hợp lệ, hàm sẽ chọn ngẫu nhiên 1 nước đi từ danh sách
    if len(valid_moves) != 0:
        return np.random.choice(valid_moves)
    return None

# Tham khảo
# Code File _1813518_1812558_1812658.py thắng 10/10 so với file random_agent.py
# Code File minimax.py thắng 10/10 lần so với file _1813518_1812558_1812658.py
# Code File player.py thắng 10/10 lần so với file  minimax.py 
