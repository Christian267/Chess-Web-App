def validate_fen(fen):
    words = fen.split()
    pieceName = {'p': 'pawns',
                 'r': 'rooks',
                 'b': 'bishops',
                 'q': 'queens',
                 'k': 'king',
                 'n': 'knight'}
    currentRank = 1
    res = {}
    res['isValid'] = False
    res['error_count'] = 0 # error count, error messages
    res['error_messages'] = []
    if len(words) != 6:
        res['error_count'] += 1
        res['error_messages'].append('fen must be composed of 6 space separated strings.')
        return res
    # Validate chessboard position
    pieceCount = {}
    validChars = '12345678rnbqkpRNBQKP/'
    currentFile = 0
    for ch in words[0]:
        if ch not in validChars:
            res['error_count'] += 1
            res['error_messages'].append('1st field: Invalid piece.')
        if ch not in pieceCount and ch.isalpha():
            pieceCount[ch] = 1
        elif ch.isalpha():
            pieceCount[ch] += 1
        if ch == '/':
            if currentFile != 8:
                res['error_count'] += 1
                res['error_messages'].append(f'1st field: Rank {currentRank} has {currentFile} files.')
            currentRank += 1
            currentFile = 0
        elif ch.isnumeric():
            currentFile += int(ch)
        else:
            currentFile += 1
    
    extraSpecialPieces = 0
    for piece, count in pieceCount.items():
        color = 'White' if piece.isupper() else 'Black'
        if ((piece.lower() in 'p' and pieceCount[piece] > 8) or 
            (piece.lower() in 'k' and pieceCount[piece] > 1)):
            res['error_count'] += 1
            res['error_messages'].append(f'1st field: {color} has {pieceCount[piece]} {pieceName[piece.lower()]}.')
        else:
            numPawns = pieceCount['P'] if color == 'White' else pieceCount['p']
            if ((piece.lower() == 'q' and pieceCount[piece] > 1 and (pieceCount[piece] + numPawns > 8)) or
                (piece.lower() in 'rnb' and pieceCount[piece] > 2 and (pieceCount[piece] + numPawns > 8))):
                res['error_count'] += 1
                res['error_messages'].append(
                    f'1st field: {color} has {pieceCount[piece]} {pieceName[piece.lower()]} and {numPawns} pawns, impossible.')

    if currentFile != 8:
        res['error_count'] += 1
        res['error_messages'].append(f'1st field: Rank {currentRank} has {currentFile} files.')

    if currentRank != 8:
        res['error_count'] += 1
        res['error_messages'].append(f'1st field: {currentRank} ranks.')

    if words[1] != 'w' and words[1] != 'b':
        res['error_count'] += 1
        res['error_messages'].append('2nd field: Invalid character.')

    castle = ['-', 'K', 'KQ', 'Kk', 'Kq', 'Qk', 'Qq', 'kq', 'KQk', 'KQq', 'KkQ', 'Kkq' 'Qkq', 'KQkq']
    if words[2] not in castle:
        res['error_count'] += 1
        res['error_messages'].append('3rd field: Invalid castle string, must follow order \'KQkq\' or \'-\' for none.')

    if words[3] != '-' and (words[3][0] not in 'abcdefgh' or words[3][2] not in '12345678'):
        res['error_count'] += 1
        res['error_messages'].append('4th field: Invalid square.')
    
    if not words[4].isnumeric() or int(words[4]) > 50:
        res['error_count'] += 1
        res['error_messages'].append('5th field: Invalid halfmove count, must be an integer between 0 and 50.')
        
    if not words[5].isnumeric() or int(words[5]) <= 0:
        res['error_count'] += 1
        res['error_messages'].append('6th field: Invalid move number, must be an integer greater than 0.')
    
    if res['error_count'] == 0:
        res['isValid'] = True
        return res
    return res

if __name__ == '__main__':
    fen = 'r1qkbr1/pp2np1p/3p1B2/2p1N3/2BnP3/3P4/PPP2PPP/R2bK2R w KQq - 1 0'
    print(fen.split())
    print(validate_fen(fen))