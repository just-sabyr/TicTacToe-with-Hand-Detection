SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 800

from positions_boxes import positions
from cli_game import convert_3x3, one_dim_to_3x3, game_winner

# length of a box (1 of 9)
BOX_LENGTH = 200
BOX_1_x, BOX_1_y = 500, 50
box_positions = positions(box_1_x=BOX_1_x, box_1_y=BOX_1_y, box_length=BOX_LENGTH)
box_positions = [i for i in box_positions]
alpha = 0.5 # used to combine overlay imgs with the frames


def next_player(current_player):
    return ('x' if current_player == 'o' else 'o')

import cv2
import mediapipe as mp
import time




mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1,
                    min_detection_confidence=.9, min_tracking_confidence=.5)

mp_drawing = mp.solutions.drawing_utils

print("The Game Begins\n\n\n\n\n")

continue_playing = True

while continue_playing:
    cv2.namedWindow("blended", cv2.WINDOW_AUTOSIZE) 
  
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 10)   

    # initialize the board
    board = [i for i in range(9)]
    board = convert_3x3(board)

    tile = -1
    winner = 0
    free_tiles = [i for i in range(9)]
    current_player = 'x'

    while free_tiles: # if free tiles is empty then no more moves meaning game ended a tie

        chosen = -1 
        ret, frame = cap.read()
        if not ret:
            break

        # flip the screen horizontally
        frame = cv2.flip(frame, 1)

        # resize the screen to make it more visible
        frame = cv2.resize(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(image_rgb)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
                pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]


                is_hand_index = (
                    index_finger_tip.y < thumb_tip.y and
                    middle_finger_tip.y > thumb_tip.y and
                    ring_finger_tip.y > thumb_tip.y and
                    pinky_tip.y > thumb_tip.y
                )

                is_hand_pistol = (
                    index_finger_tip.y < thumb_tip.y and
                    middle_finger_tip.y < thumb_tip.y and
                    abs(middle_finger_tip.y - index_finger_tip.y) < 30 and
                    ring_finger_tip.y > thumb_tip.y and
                    pinky_tip.y > thumb_tip.y
                )

                if is_hand_index:
                    # the choosing of a tile part is here
                    
                    for i in range(9):
                        iftx = SCREEN_WIDTH * index_finger_tip.x
                        ifty = SCREEN_HEIGHT * index_finger_tip.y
                        bx = box_positions[i][0]
                        by = box_positions[i][1]

                        if (iftx > bx and iftx < bx+BOX_LENGTH) and (ifty > by and ifty < by+BOX_LENGTH):
                            tile = i
                            break

                if is_hand_pistol:
                    # the choosing of XorO part is here
                    if tile in free_tiles:
                        chosen = tile
                        tile = -1

        # Create a copy of the frame to draw the grid on
        overlay = frame.copy()

        # Draw vertical lines
        for i in range(1, 3):
            x = BOX_1_x + i * BOX_LENGTH
            cv2.line(overlay, (x, BOX_1_y), (x, BOX_1_y + 3 * BOX_LENGTH), (200, 200, 200), 10)

        # Draw horizontal lines
        for j in range(1, 3):
            y = BOX_1_y + j * BOX_LENGTH
            cv2.line(overlay, (BOX_1_x, y), (BOX_1_x + 3 * BOX_LENGTH, y), (200, 200, 200), 10)

        # Perform alpha blending
        blended = cv2.addWeighted(overlay, alpha, frame, 1-alpha, 0)
        
        # change the color of the chosen tile 
        if tile != -1: 
            tile_overlay = frame.copy()
            red_or_blue = [150, 0, 0] if current_player == "x" else [0, 0, 150]
            cv2.rectangle(tile_overlay, (box_positions[tile][0], box_positions[tile][1]), (box_positions[tile][0] + BOX_LENGTH, box_positions[tile][1] + BOX_LENGTH), red_or_blue, -1)
            blended = cv2.addWeighted(tile_overlay, 0.3, blended, 1-0.3, 0)

        if chosen != -1:
            free_tiles.remove(chosen)
            row, col = one_dim_to_3x3(chosen+1)
            board[row][col] = current_player
            winner = game_winner(board)
            
            if winner != 0:
                blue_or_red = 'blue' if current_player == 'x' else 'red'
                print(f"{blue_or_red} has won")
                break                
            current_player = next_player(current_player)
            
        # show the the current board 
        board_overlay = frame.copy()
        for i in range(9):
            row, col = one_dim_to_3x3(i+1)
            x_or_o_on_the_board = board[row][col]
            if x_or_o_on_the_board == 'x':
                cv2.rectangle(board_overlay, (box_positions[i][0], box_positions[i][1]), (box_positions[i][0] + BOX_LENGTH, box_positions[i][1] + BOX_LENGTH), [200, 0, 0], cv2.FILLED)
                blended = cv2.addWeighted(board_overlay, 0.3, blended, 1-0.3, 0)
            elif x_or_o_on_the_board == 'o':
                cv2.rectangle(board_overlay, (box_positions[i][0], box_positions[i][1]), (box_positions[i][0] + BOX_LENGTH, box_positions[i][1] + BOX_LENGTH), [0, 0, 200], cv2.FILLED)
                blended = cv2.addWeighted(board_overlay, 0.3, blended, 1-0.3, 0)

        cv2.imshow('blended', blended)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            continue_playing = False
            break


    # change the screen from the game and display the winner or draw images
    if tile:
        winner_or_tie_img_path = 'blue_won.png' if blue_or_red == 'blue' else 'red_won.png'
    else:
        winner_or_tie_img_path = 'tie.png'
    winner_or_tie_img = cv2.imread(winner_or_tie_img_path)

    for _ in range(150): 
        cv2.imshow('blended', winner_or_tie_img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            continue_playing = False
            break

    cv2.destroyWindow('blended')
    cap.release()
    time.sleep(1)



