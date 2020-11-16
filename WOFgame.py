import libdw.sm as sm
import random
import time
import math

   
class Wheel():
    def __init__(self):
        self.inwheel = ['BANKRUPT','$500','$1000','FREE PLAY','$800','$300','$700','LOSE A TURN']
        self.count = [-math.inf,500,1000,500,800,300,700,0]
        self.length = len(self.inwheel)
        
    def display(self):
        wheelstr = '| '
        for i in range(11):
            for j in range(self.length):
                try:
                    wheelstr += '{} | '.format(self.inwheel[j][i])
                except:
                    wheelstr += '  | '
            wheelstr += '\n| '
        wheelstr = wheelstr[:-3]
        print(wheelstr)
    
    def spin(self):
        pos = random.randrange(2,self.length*4,4)
        print('\nSpinning the Wheel...')
        for i in range(2):
            for j in range(self.length*4 + 2):
                if j == pos and i == 1:
                    print('^\n')
                    return self.count[int((pos-2)/4)] , self.inwheel[int((pos-2)/4)]
                else:
                    print('.',end = '')
                    time.sleep(0.1)
            print('')           

class Player(sm.SM):
    def __init__(self,name):
        self.name = name
        self.state = 0
        self.thisround = 0
        self.balance = 0
    
    def get_next_values(self,state,inp):
        if type(inp) == type(0):
            self.thisround += inp
            ns = 0
            out = self.thisround
        elif inp == 'win':
            self.balance += self.thisround
            self.thisround = 0
            ns = 0
            out = self.balance 
        elif inp == 'lose':
            self.thisround = 0
            ns = 0
            out = self.balance
        return ns,out
    
    def __str__(self):
        return self.name

def GenerateWL():
    wordlist = open ('wordlist.txt','r')
    biglst = []
    theme = []
    for line in wordlist:
        if line == '\n':
            if theme != []:
                biglst.append(theme)
                theme = []
        else:
            word = line.strip('\n')
            theme.append(word)
    wordlist.close()
    biglst.append(theme)
    if [] in biglst:
        biglst.remove([])
    return biglst



class Game(sm.SM):
    def __init__(self):
        self.playernum, self.allnames = self.intro()
        self.player1 = Player(self.allnames[0])
        self.player2 = Player(self.allnames[1])
        self.player3 = Player(self.allnames[2])
        
        self.sequence = [self.player1,self.player2,self.player3]
        self.humans = self.sequence[0:self.playernum]
        random.shuffle(self.sequence)
        
        self.qnbank = GenerateWL()
        self.theme = ''
        self.qn = ''
        self.word = ''
        self.vowels = list('AEIOU')
        self.alphabets = list('BCDFGHJKLMNPQRSTVWXYZ')
        self.rounds = 0
        
        self.start_state = 0
        
    def get_next_values(self,state,inp):
        
        if inp == 'start':
            self.theme, self.qn, self.word = self.generateqn()
            out = self.sequence[state]
            ns = state
            self.vowels = list('AEIOU')
            self.alphabets = list('BCDFGHJKLMNPQRSTVWXYZ')
            self.rounds += 1

        else:
            if self.sequence[state] in self.humans:
                name = 'you'
                pronoun = 'have'
            else:
                name = self.sequence[state].name
                pronoun = 'has'
                
            inp = inp.upper()
            if inp == 'S': #player chooses to spin
                if self.sequence[state] not in self.humans: #informing player of move of AI
                    print('--{} chose to spin!--\n'.format(self.sequence[state].name))
                    time.sleep(1)
                    
                Wheel().display()
                money,display = Wheel().spin()
                time.sleep(1)
                
                if money > 0:
                    #prompt a guess if its human or guess a random letter if it is computer
                    if self.sequence[state] in self.humans:
                        print('--You spin {}--'.format(display))
                        time.sleep(1)
                        print('\nQn - {} : '.format(self.theme),end = '')
                        print(''.join(self.word))
                        
                        if display == 'FREE PLAY':
                            guess = input('Guess a consonant or vowel. \n>>>')
                            guess = guess.upper()
                            #error message
                            while (len(guess) != 1):
                                guess = input('This is not a valid input. Please input a consonant or vowel.\n>>>')
                                guess = guess.upper()
                        else:
                            guess = input('Guess a consonant. \n>>>')   
                            guess = guess.upper()
                            #error message
                            while (len(guess) != 1 or guess in list('AEIOU')):
                                guess = input('This is not a valid input. Please input a consonant.\n>>>')
                                guess = guess.upper()
                        
                    else:
                        if display == 'FREE PLAY':
                            total = self.vowels + self.alphabets
                            guess = total[random.randrange(len(total))]
                            if guess in self.vowels:
                                money = 0
                        else:
                            guess = self.alphabets[random.randrange(len(self.alphabets))]
                            
                        print('--{} spin {}--\n'.format(self.sequence[state].name,display))
                        time.sleep(1)
                        print('--{} guessed the letter {}--'.format(self.sequence[state].name,guess))
                        time.sleep(1)
                    
                    #what to do with guess
                    #error message if guess is in word displayed
                    if guess in self.word and self.sequence[state] in self.humans:
                        while guess not in self.alphabets:
                            if len(guess) > 1 or guess.isalpha() == False:
                                if display == 'FREE PLAY':
                                    guess = input('This is not a valid input. Please input a consonant or vowel.\n>>>')
                                else:
                                    guess = input('This is not a valid input. Please input a consonant.\n>>>')
                            elif guess in self.word:
                                guess = input('This letter is already revealed. Please input another letter\n>>>')
                            elif display != 'FREE PLAY' and guess in list('AEIOU'):
                                guess = input('This is not a valid input. Please input a consonant.\n>>>')
                            else:
                                break
                            guess = guess.upper()
                            
                            
                    #after making sure guess is not already displayed
                    if guess in self.alphabets:
                        self.alphabets.remove(guess)
                    elif guess in self.vowels:
                        self.vowels.remove(guess)
                    
                    ns = 'check'
                            
                else:
                    ns = state + 1
                    print('--Oh no! {} spin {}--'.format(name.capitalize(),display))
                    time.sleep(1)
                    
            elif inp in list('AEIOU'):
                money = -250
                display = ''
                if self.sequence[state].thisround < 250:
                    if self.sequence[state] in self.humans:
                        print('\n--You have ${}-- \n--You do not have enough money to buy a vowel-- \n--Please spin instead--'.format(self.sequence[state].thisround))
                        time.sleep(1)
                        ns = state
                        
                elif inp in self.qn:
                    if inp in self.vowels:
                        self.vowels.remove(inp)
                        
                    guess = inp           
                    ns = 'check'                    
                    
                elif inp not in self.qn:
                    if inp in self.vowels:
                        self.vowels.remove(inp)
                        
                    guess = inp     
                    ns = 'check'

                    
            elif inp == self.qn:
                print('\n{} solved the question!\n'.format(self.sequence[state].name))
                time.sleep(1)
                print ('The answer is {}.\n'.format(self.qn))
                time.sleep(1)
                print('Congratulations! {} has won ${} this round. \n'.format(self.sequence[state].name,self.sequence[state].thisround))
                time.sleep(1)
                for x in self.sequence:
                    if x == self.sequence[state]:
                        x.step('win')
                    else:
                        x.step('lose')
                print('''Now tallying everyone's score...\n''')
                time.sleep(2)
                print('{} : ${} \n{} : ${} \n{} : ${}'.format(self.player1.name,self.player1.balance,self.player2.name,self.player2.balance,self.player3.name,self.player3.balance))
                time.sleep(2)
                ns = 'next'
                
            elif len(inp) == len(self.qn):
                print('\n--You guessed {}-- \n'.format(inp))
                time.sleep(1)
                print('--That is not the answer--')
                time.sleep(2)
                print('''\n--{}'s turn ended with ${}--'''.format(self.sequence[state].name,self.sequence[state].thisround))
                time.sleep(2)
                ns = state + 1
                
            else:
                print('\nThis is an invalid input')
                time.sleep(1)
                ns = state 
            
           
                
        if ns == 'check':
            if guess in self.qn:
                ns = state
                count = 0
                for i in range(len(self.qn)):
                    if self.qn[i] == guess:
                        self.word[int(2*i)] = guess
                        count += 1
                print('\nQn - {} : '.format(self.theme),end = '')
                print(''.join(self.word))
                time.sleep(1)
                
                if guess in list('AEIOU'):
                    if display == 'FREE PLAY':
                        money = 0
                    self.sequence[state].thisround += money
                else:    
                    self.sequence[state].thisround += count * money
                
                print('\n--The question has {} {}(s)--\n'.format(count,guess))
                time.sleep(2)
                print('--{} {} ${} this round--\n'.format(name.capitalize(),pronoun,self.sequence[state].thisround))
                time.sleep(2)
                        
                if self.sequence[state] in self.humans:
                    print('What would you like to do?')
                    time.sleep(1)
                    
            elif guess not in self.qn:
                if display == 'FREE PLAY':
                    ns = state
                    print('\n--There are no {} s in the question--\n'.format(guess))
                    time.sleep(2)
                    print('--Luckily, {} landed on FREE PLAY--\n'.format(name))
                    time.sleep(1)
                    print('''--It's still {}'s turn--\n'''.format(self.sequence[state].name))
                    time.sleep(1)
                    
                else:
                    ns = state + 1
                    print('\n--There are no {} s in the question--\n'.format(guess))
                    time.sleep(2)
                    print('''--{}'s turn ended with ${}--'''.format(self.sequence[state].name,self.sequence[state].thisround))
                    time.sleep(2)
                
        
        if ns == 'next':
            out = False
            ns = self.start_state + 1
            
        elif inp != 'start':
            out = True            
            
        if ns == len(self.sequence):
            ns = 0
            
        if ns != state and out == True:
            print('''.\n.\n.\nIt's {}'s turn!'''.format(self.sequence[ns].name))
            time.sleep(1)
            print('\nQn - {} : '.format(self.theme),end = '')
            print(''.join(self.word),end = '\n\n')
            time.sleep(1)      
            
        return ns,out
    
    def intro(self):
        names = ['Erik','Jessica']
        playernum = input('Enter the number of players (1-3)\n>>>')
        playernames = []
        
        while playernum not in ['1','2','3']:
            playernum = input('This is an invalid input. Please input either 1, 2 or 3\n>>> ')
            
        playernum = int(playernum)
            
        for i in range (playernum):
            playernames.append(input('''Enter Player {}'s name\n>>>'''.format(i+1)).capitalize())  
            
        for j in range(3-playernum):
            playernames.append(names[j])
        
        print('\nWelcome to Wheel of Fortune!\n')
        time.sleep(1)
        print('There will be 3 rounds of game, at the end of which the player with the highest score wins!\n')
        time.sleep(2)
        print('Let us welcome our contestants for the night : {}, {} and {}!'.format(playernames[0],playernames[1],playernames[2]))
        time.sleep(1)
        return playernum, playernames
    
    def generateqn(self):
        randtheme = random.randint(0,len(self.qnbank)-1)
        randqn = random.randint(1,len(self.qnbank[randtheme])-1)
        currtheme = self.qnbank[randtheme][0]
        currqn = self.qnbank[randtheme][randqn]
        
        print('''.\n.\n.\n.\nStarting a new round...\n''')
        time.sleep(2)
        print('''The theme for this round is {}. \n'''.format(currtheme))
        time.sleep(1)
        print('''Here's the question : ''')
        word = ''
        for letter in currqn:
            if letter == ' ':
                word += '  '
            else:
                word += '_ '
        print(word,end='\n\n')
        time.sleep(2)
        self.qnbank[randtheme].remove(currqn)
        
        return currtheme,currqn,list(word)
            
    def duringround(self,player):
        if set(list('AEIOU')).union((set(list(self.qn))-set(self.word[::2]))) == set(list('AEIOU')):
            if player:
                playermove = input('''*Input a vowel (AEIOU) to buy it for $250 \n*Input the answer to solve.\n\n>>>''')
                while playermove not in list('AEIOU') or len(playermove) != len(self.qn):
                    playermove = input('''This is an invalid input.\n\nYou can:\n*Input a vowel (AEIOU) to buy it for $250 \n*Input the answer to solve.\n\n>>>''')
                out = self.step(playermove) 
            else:
                out = self.step(self.qn) 
        else:                             
            if player:
                playermove = input('''*Input 'S' to spin \n*Input a vowel (AEIOU) to buy it for $250 \n*Input the answer to solve.\n\n>>>''')
                out = self.step(playermove)
            else:
                out = self.step('S')
            
        return out
    
    def getwinner(self):
        scores = []
        highscore = -1
        for x in self.sequence:
            scores.append(x.balance)
        for a,b in enumerate(scores):
            if b == highscore:
                winner.append(a)
            elif b == max(scores):
                highscore = b
                winner = [a]
        print('.\n.\n.\n.\nThe games for tonight have been completed.\n')
        time.sleep(1)
        
        for i in range(len(winner)):
            if i == 0:
                print('And the winner is ... ',end = '')
                time.sleep(2)
                print('{} with a total of ${}. Congratulations!\n'.format(self.sequence[winner[i]],highscore))
                time.sleep(2)
            else:
                print('And surprise!\n')
                time.sleep(2)
                print('{} also won with a total of ${}. Congratulations!\n'.format(self.sequence[winner[i]],highscore))
                time.sleep(2)
                
    def run(self):
        self.start()
        playing = True
        rounds = 0
        while playing: 
            rounds += 1
            if rounds == 1:
                playing = False
                
            start_player = self.step('start')
            print('{} shall start this round\n'.format(start_player.name))
            time.sleep(2)
            
            if start_player in self.humans:
                player = True
            else:
                player = False
                
            while self.duringround(player):
                if self.sequence[self.state] in self.humans:
                    player = True
                else:
                    player = False
        
        self.getwinner()
                
        
Game().run()
        
        
            
            
        


