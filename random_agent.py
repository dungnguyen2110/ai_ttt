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
