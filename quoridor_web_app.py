from flask import *
from quoridor import *
from pymongo import *

app = Flask(__name__)
client = MongoClient('127.0.0.1', 27017)
db = client.ship_database
coordinates = db.coordinates


q = QuoridorGame()
@app.route('/') 
def root():
       fences = q.return_fences()
       grid = q.return_board()
       turn = q.return_turn()
       return render_template('main.html', grid=grid, turn=turn, fences=fences, visibility="hidden")

@app.route('/addfence', methods = ["POST"])
def add_fence():
   
       data = request.form
       x = int(data['X'])
       y = int(data['Y'])
       align = data['alignment']
       q.add_fence(x, y, align)
       fences = q.return_fences()
       print(fences)
       grid = q.return_board()
       turn = q.return_turn()
       return render_template('main.html', grid=grid, turn=turn, fences=fences, visibility="hidden") 
   

@app.route('/movepawn', methods = ["POST"])
def move_pawn():
       data = request.form
       x = int(data['X'])
       y = int(data['Y'])
       q.movePawn(x, y)
       fences = q.return_fences()
       turn = q.return_turn()
       grid = q.return_board()
       if q.check_winner():
              winner = q.return_game_state
              return render_template('won.html', winner=winner)  
       return render_template('main.html', grid=grid, turn=turn, fences=fences, visibility="hidden") 

@app.route('/show_instruction', methods = ["POST"])
def show_instructions():
       fences = q.return_fences()
       turn = q.return_turn()
       grid = q.return_board()
       return render_template('main.html', grid=grid, turn=turn, fences=fences, visibility="visible")

@app.route('/hide_instruction', methods = ["POST"])
def hide_instructions():
       fences = q.return_fences()
       turn = q.return_turn()
       grid = q.return_board()
       return render_template('main.html', grid=grid, turn=turn, fences=fences, visibility="hidden") 
       
         
if __name__ == '__main__':
       app.run(port = 6789, debug = True)
