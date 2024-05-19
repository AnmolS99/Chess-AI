import unittest
from chess_board import ChessBoard
from fen_converter import FENConverter
from gui import ChessGUI

def move_sim(game: ChessBoard, ui, curr_depth: int, final_depth: int):

    if curr_depth == final_depth:
        return 1
    else:
        org_game = game.copy()
        num_positions = 0
        for move in org_game.get_all_legal_moves():

            game_with_move = org_game.copy()
            game_with_move.move_piece(move)
            num_positions_given_move = move_sim(game_with_move, ui, curr_depth + 1, final_depth)
            num_positions += num_positions_given_move
        return num_positions
    

class TestPerft(unittest.TestCase):
    """ Test positions are taken from here: https://www.chessprogramming.org/Perft_Results """
    
    def test_initial_position(self):
        game = ChessBoard()
        game.reset_board()
        
    
        ui = ChessGUI(game)
        self.assertEqual(move_sim(game, ui, 0, 1), 20)
        self.assertEqual(move_sim(game, ui, 0, 2), 400)
    
    def test_position2(self):
        fen_converter = FENConverter()
        game = ChessBoard()
        game.reset_board()
        
        fen_converter.to_game_state(game, "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - ")
    
        ui = ChessGUI(game)
        self.assertEqual(move_sim(game, ui, 0, 1), 48)
        self.assertEqual(move_sim(game, ui, 0, 2), 2039)
        self.assertEqual(move_sim(game, ui, 0, 3), 97862)

    def test_position3(self):
        fen_converter = FENConverter()
        game = ChessBoard()
        game.reset_board()
        
        fen_converter.to_game_state(game, "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - -")
    
        ui = ChessGUI(game)
        self.assertEqual(move_sim(game, ui, 0, 1), 14)
        self.assertEqual(move_sim(game, ui, 0, 2), 191)
        self.assertEqual(move_sim(game, ui, 0, 3), 2812)
        self.assertEqual(move_sim(game, ui, 0, 4), 43238)
    
    def test_position4(self):
        fen_converter = FENConverter()
        game = ChessBoard()
        game.reset_board()
        
        fen_converter.to_game_state(game, "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1")
    
        ui = ChessGUI(game)
        self.assertEqual(move_sim(game, ui, 0, 1), 6)
        self.assertEqual(move_sim(game, ui, 0, 2), 264)
        self.assertEqual(move_sim(game, ui, 0, 3), 9467)

    def test_position5(self):
        fen_converter = FENConverter()
        game = ChessBoard()
        game.reset_board()
        
        fen_converter.to_game_state(game, "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8")
    
        ui = ChessGUI(game)
        self.assertEqual(move_sim(game, ui, 0, 1), 44)
        self.assertEqual(move_sim(game, ui, 0, 2), 1486)
        self.assertEqual(move_sim(game, ui, 0, 3), 62379)

    def test_position6(self):
        fen_converter = FENConverter()
        game = ChessBoard()
        game.reset_board()
        
        fen_converter.to_game_state(game, "r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10")
    
        ui = ChessGUI(game)
        self.assertEqual(move_sim(game, ui, 0, 1), 46)
        self.assertEqual(move_sim(game, ui, 0, 2), 2079)
        self.assertEqual(move_sim(game, ui, 0, 3), 89890)
    
        
if __name__ == '__main__':
    unittest.main()