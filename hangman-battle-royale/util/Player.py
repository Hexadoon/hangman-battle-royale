class Player:
    #TODO add server compatibility
    
    def __init__(self, word, player_num):
        self._parts = 0
        self._id = player_num
        self._word = word
        self._guessed = set([])
        
    def get_id(self):
        return self._id

    def get_guessed(self):
        return ''.join(sorted(list(self._guessed - set(self._word)))) 
    
    def guess_letter(self, char):
        """ Takes a guessed character, checks if it's in the word
            returns -1 if character has already been guessed or is otherwise invalid
                     0 if character is not in the word
                     1 if character is in the word and not guessed """
    
        
        if char.isalpha() == False:
            return -1

        char.lower()
        if char in self._guessed:
            return -1
        
        self._guessed.add(char)

        if char in self._word:
            return 1
        else:
            return 0

    def get_word_status(self):
        """ returns the word with underscores in place of unguessed characters """
        status = ''
        for c in self._word:
            if c.isalpha() == False:
                status += c
            elif c in self._guessed:
                status += c
            else:
                status += '_'
        
        return ' '.join(list(status))
    
        """ TODO once servers are set up, implement some concept of a turn happening 
            ie one character chooses a letter and another character and calls other.guess_letter(char)"""

    def is_dead(self):
        """ Returns true or false if the character is dead """
        if self._parts == 6 or (set(self._word) - self._guessed) == set():
            return True

        return False
