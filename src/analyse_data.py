import chess.pgn
import json
import pandas as pd
from io import StringIO

def load_games(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def parse_pgn(pgn_string):
    game_io = StringIO(pgn_string)
    return chess.pgn.read_game(game_io)

def analyze_game(game):
    board = game.board()
    moves = []
    for move in game.mainline_moves():
        moves.append(board.san(move))
        board.push(move)
    return moves

if __name__ == "__main__":
    games_data = load_games('../data/raw/games.json')
    analysis_results = []

    for game_data in games_data:
        game_pgn = game_data['pgn']
        parsed_game = parse_pgn(game_pgn)
        moves = analyze_game(parsed_game)
        
        analysis_results.append({
            "white": game_data.get('players', {}).get('white', {}).get('user', {}).get('name'),
            "black": game_data.get('players', {}).get('black', {}).get('user', {}).get('name'),
            "moves": moves,
            "result": game_data.get('status'),
            "white_rating": game_data.get('players', {}).get('white', {}).get('rating'),
            "black_rating": game_data.get('players', {}).get('black', {}).get('rating'),
        })

    df = pd.DataFrame(analysis_results)
    df.to_csv('../data/processed/game_analysis.csv', index=False)
    print("Analysis complete and saved to processed/game_analysis.csv")
