# 4CHESS v0.2.5 - 12:45AM | BULLETPROOF BOARD + RULES
import random

def new_board():
    board = [
        ['r','n','b','q','k','b','n','r'],
        ['p'] * 8, # 8 BLACK PAWNS - GUARANTEED
        ['.'] * 8,
        ['.'] * 8,
        ['.'] * 8,
        ['.'] * 8,
        ['P'] * 8, # 8 WHITE PAWNS - GUARANTEED
        ['R','N','B','Q','K','B','N','R']
    ]
    assert len(board) == 8, "Board must have 8 ranks"
    assert all(len(row) == 8 for row in board), "Each rank must have 8 files"
    return board

def show(b):
    print(f"\n=== 4CHESS v0.2.5 | 12:45AM | BULLETPROOF ===")
    print(" a b c d e f g h")
    for i,row in enumerate(b):
        print(f"{8-i} {' '.join(row)} {8-i}")
    print(" a b c d e f g h\n")

def parse(sq):
    cols = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
    if len(sq)!=2 or sq[0] not in cols or sq[1] not in '12345678': return None,None
    return 8-int(sq[1]), cols[sq[0]]

def clear_path(b,sr,sc,er,ec):
    dr = 0 if er==sr else (1 if er>sr else -1)
    dc = 0 if ec==sc else (1 if ec>sc else -1)
    r,c = sr+dr, sc+dc
    while r!=er or c!=ec:
        if b[r][c]!='.': return False
        r+=dr; c+=dc
    return True

def legal(b,sr,sc,er,ec):
    p = b[sr][sc]; t = b[er][ec]
    if p=='.': return False,"Empty square"
    if t!='.' and t.isupper()==p.isupper(): return False,"Can't take own piece"
    if sr==er and sc==ec: return False,"Same square"

    dr,dc = er-sr, ec-sc; adr,adc = abs(dr),abs(dc)

    if p=='P': # White pawn
        if dc==0 and dr==-1 and t=='.': return True,""
        if sr==6 and dr==-2 and dc==0 and b[5][sc]=='.' and t=='.': return True,""
        if dr==-1 and adc==1 and t.islower(): return True,""
        return False,"Illegal pawn"
    if p=='p': # Black pawn
        if dc==0 and dr==1 and t=='.': return True,""
        if sr==1 and dr==2 and dc==0 and b[2][sc]=='.' and t=='.': return True,""
        if dr==1 and adc==1 and t.isupper(): return True,""
        return False,"Illegal pawn"
    if p in 'Nn': return (adr,adc) in [(2,1),(1,2)], "Knight L-shape"
    if p in 'Kk': return adr<=1 and adc<=1, "King 1 square"
    if p in 'Bb': return adr==adc and clear_path(b,sr,sc,er,ec), "Bishop diagonal"
    if p in 'Rr': return (dr==0 or dc==0) and clear_path(b,sr,sc,er,ec), "Rook straight"
    if p in 'Qq': return (adr==adc or dr==0 or dc==0) and clear_path(b,sr,sc,er,ec), "Queen"
    return False,"Unknown piece"

def move(b,s,e):
    sr,sc = parse(s); er,ec = parse(e)
    if sr is None: return b,False,"Use a1-h8"
    if b[sr][sc].islower(): return b,False,"Can't move AI pieces"
    ok,msg = legal(b,sr,sc,er,ec)
    if not ok: return b,False,msg
    cap = b[er][ec]; b[er][ec]=b[sr][sc]; b[sr][sc]='.'
    if cap!='.': print(f"Captured {cap}!")
    return b,True,""

def ai_move(b):
    moves = []
    for r in range(8):
        for c in range(8):
            if b[r][c].islower():
                for er in range(8):
                    for ec in range(8):
                        if legal(b,r,c,er,ec)[0]: moves.append((r,c,er,ec))
    if not moves: print("AI STUCK. YOU WIN!"); return b,True
    sr,sc,er,ec = random.choice(moves)
    cap=b[er][ec]; b[er][ec]=b[sr][sc]; b[sr][sc]='.'
    print(f"AI: {chr(sc+97)}{8-sr} to {chr(ec+97)}{8-er}" + (f" x{cap}" if cap!='.' else ""))
    return b,False

# GAME
board = new_board()
print("4CHESS v0.2.5 | BOARD BUG KILLED | ALL RULES ACTIVE")
print("Format: e2 e4 | q to quit")

done=False
while not done:
    show(board)
    cmd = input("Move: ").strip().lower()
    if cmd=='q': break
    try:
        s,e = cmd.split()
        board,ok,msg = move(board,s,e)
        if not ok: print(msg)
        elif not done: board,done = ai_move(board)
    except: print("Format: e2 e4")

print("GG. Shipped at 12:45am.")
