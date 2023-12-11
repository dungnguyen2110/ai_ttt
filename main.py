from state import State, State_2
# Import từ file state.py
import time
# Đo lường thời gian đã trôi qua trong quá trình thực hiện nước đi
from importlib import import_module
# import các module của người chơi

# Người chới 1: X,  người chơi 2: O, 
# rule = 1: gọi State()
# rule = 2: gọi State_2()
  
def main(player_X, player_O, rule = 1):
    # Anhs xạ người chơi: X = 1; O = -1, chưa đánh = 0
    dict_player = {1: 'X', -1: 'O'}
    if rule == 1:
        cur_state = State()
    else:
        cur_state = State_2()
    # Theo dõi số ô đã được đánh, tối đa là 81 ô
    turn = 1    

    # Max bằng 81 ô
    limit = 81
    
    # Tổng thời gian tới đa của mỗi người chơi là 120s
    remain_time_X = 120
    remain_time_O = 120
    
    #Import các mô-đun của 2 người chơi
    player_1 = import_module(player_X)
    player_2 = import_module(player_O)
    
    # Còn ô còn đánh
    while turn <= limit:
        # In ra số ô đã đánh
        print("turn:", turn, end='\n\n')
        
        # CÓ người thắng, thì in ra
        if cur_state.game_over:
            print("winner:", dict_player[cur_state.player_to_move * -1])
            break
        
        # Đếm giờ
        start_time = time.time()
        
        # Lượt của ai thì lưu cho người đó
        if cur_state.player_to_move == 1:
            new_move = player_1.select_move(cur_state, remain_time_X)
            # Số thời gian đánh người 1
            elapsed_time = time.time() - start_time
            # Số thời gian còn lại người 1
            remain_time_X -= elapsed_time
        else:
            new_move = player_2.select_move(cur_state, remain_time_O)
            # Số thời gian đánh người 2
            elapsed_time = time.time() - start_time
            # Số thời gian còn lại người 2
            remain_time_O -= elapsed_time
        
        # Không có người đánh thì thoát    
        if new_move == None:
            break
        
        # Hết thời gian
        if remain_time_X < 0 or remain_time_O < 0:
            print("out of time")
            print("winner:", dict_player[cur_state.player_to_move * -1])
            break
                
        # Thời gian đánh > 10s, thoát
        if elapsed_time > 10.0:
            print("elapsed time:", elapsed_time)
            print("winner: ", dict_player[cur_state.player_to_move * -1])
            break
        
        # Lưu trạng thái đánh + in bàn cơ
        cur_state.act_move(new_move)
        print(cur_state)
        
        turn += 1
    
    # In số blcok mỗi bên thắng     
    print("X:", cur_state.count_X)
    print("O:", cur_state.count_O)

# Gọi tới hàm _MSSV.py và random_agent
# _MSSV.py là code mình càn hiện thực
# random_agent là đối thủ, đánh tự do
# Đánh với agent 10 lần: 50% điểm BTL

# Mặc định là ramdom_agent (đối thủ trong phần 1 của bài tập lớn) đi trước
main('random_agent', '_MSSV')

 
