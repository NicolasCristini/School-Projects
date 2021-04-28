"""
Created on Tue Feb 23 17:46:14 2021
Latest version on Tue Mar 2 16:36:23 2021


The game is called "GUESS WHAT?", and is a quizz-type game 
with multiple categories. We recommend you use Spyder 3.8 to
run the code, as this is what we tested it with. We also recommend
adjusting the IPython console to match the output formating of
the game for a better user experience.

Thank you for playing!

@authors: nicolas_cristini, bruno_rodrigues, nelfyenny
 
"""

import graphics as g

#Player selection variables
Y = ["Yes", "yes", "Y", "y" , "YES"]
N = ["No", "no", "N", "n" , "NO"]
A = ["A", "a"]
B = ["B", "b"]
C = ["C", "c"]
D = ["D", "d"]

#Initialization variables
name = None
skip = False
score = 0
total_score = 0
max_questions = int(10)

#Theme/topic tokens
topic_token = [False, False, False]


def presentation():
    global name
    
    g.figures("space")
    g.figures("title")
    g.figures("space")
    
    g.talk("Hello!\nWhat is your name?")
    name = input("\n")
    g.talk(f"\nHi {name}!")
    
def rules():
    
    g.figures("space")
    rule = None
    
    while (rule not in Y) and (rule not in N):
        
        g.talk("Before you start the quizz, would you like to read an overview of how the game works? (y/n)")
        rule = str(input("\n"))
        
        if rule in Y:
            g.figures("rules")
            g.talk("Here's an explanation of the game rules and how it works.")
            g.talk("This is a quiz game! You can choose among three themes: 'Science', 'History' and 'Entertainment'. In each theme, you can choose among three different categories according to what you like most. \nFor each question, there are four possible answers. \n\nTo complete the game you must answer to AT LEAST five questions of THREE categories, ONE for each theme! \nDuring the game, you are allowed to call the 'help' option. If you do so, you will enter a 'help menu' that will show you three help option: \n\n50:50 = two out of four possible answer will be deleted. \nhint = a hint to answer the question will be displayed to you. \nskip = you can skip the question and still gain a reasonable amount of points. \n\nYou can use each of the 'help options' only once per theme! \nAt the end of the game, your total score will be placed in the leader board. \nLater, you can start the game all over again and choose different categories to see how well you perform on different topics!. \nEnjoy!")
            g.delay(1)
            
        elif rule in N:
            g.talk("Ok, let's get straight to it then!")
            g.delay(1)
            
        else:
            g.talk("Invalid input. Please answer with (y/n).")
    
def introduction():
    
    g.figures("space")
    intro = None
    
    while (intro not in Y) and (intro not in N):
        
        intro = input(f"Are you ready to start the game, {name} (y/n)?\n")
        
        if intro in Y:
            g.talk("Let's start!")
        elif intro in N:
            g.talk("Come on, just give it a chance!")
        else:
            g.talk("\nInvalid input. Please answer with (y/n).")
        

def theme():
    global topic_token
    topic = None
    
    while topic not in (A + B + C):
        
        if False not in topic_token:
            g.talk("\nYou have completed all categories. Well done!")
            break
        
        g.figures("space")
        g.figures("category")
        g.talk("This is the category selection screen.")
        g.talk("\nChoose your topic among the following options: \n[A]:\tScience \n[B]:\tHistory \n[C]:\tEntertainment\n\n")
        topic = str(input("\n")).upper()
        g.figures("space")
        
        #TOPIC A - SCIENCE (Category 0,1,2)
        if (topic in A):
            if (topic_token[0] == False):
                g.figures("science")
                g.talk("\nChoose your category among the following options: \n[A]:\tBiology \n[B]:\tPhysics \n[C]:\tChemistry\n[D]:\tBack to topic selection\n")
                category = str(input("\n")).upper()
                
                if category in A:
                    world(0)
                elif category in B:
                    world(1)
                elif category in C:
                    world(2)
                elif category in D:
                    g.talk("Taking you back to topic selection\n")
                    topic = None
                    continue
                else:
                    #ERROR message
                    g.talk("\nInvalid input! Taking you back to topic selection.")
                    topic = None
                    continue
                
            else:
                g.talk("\nYou have already completed this topic! Please choose another.")
                topic = None
        
        #TOPIC B - HISTORY (Category 3,4,5)
        elif (topic in B):
            if (topic_token[1] == False):
                g.figures("history")
                g.talk("\nChoose your category among the following options: \n[A]:\tProgramming \n[B]:\tGeography \n[C]:\tPersonalities \n[D]:\tBack to topic selection\n")
                category = str(input("\n")).upper()
                
                if category in A:
                    world(3)
                elif category in B:
                    world(4)
                elif category in C:
                    world(5)
                elif category in D:
                    g.talk("Taking you back to topic selection\n")
                    topic = None
                    continue
                else:
                    #ERROR message
                    g.talk("\nInvalid input! Taking you back to topic selection.")
                    topic = None
                    continue
            else:
                g.talk("\nYou have already completed this topic! Please choose another.")
                topic = None

        #TOPIC C - ENTERTAINMENT (Category 6,7,8)
        elif (topic in C):
            if (topic_token[2] == False):
                g.figures("entertainment")
                g.talk("\nChoose your category among the following options: \n[A]:\tArt \n[B]:\tMovies \n[C]:\tMusic \n[D]:\tBack to topic selection\n\n")
                category = str(input("\n")).upper()
                
                if category in A:
                    world(6)
                elif category in B:
                    world(7)
                elif category in C:
                    world(8)
                elif category in D:
                    g.talk("Taking you back to topic selection\n")
                    topic = None
                    continue
                else:
                    #ERROR message
                    g.talk("\nInvalid input! Taking you back to topic selection.")
                    topic = None
                    continue
                
            else:
                g.talk("\nYou have already completed this topic! Please choose another.")
                topic = None
        
        
        else:
            g.talk("\nInvalid input. Please choose again.")
            

def world(q):
    global points, score, total_score, name_category, max_questions, question_text1, question_text2, question_number, alpha, beta, gamma, delta, right, topic_token, help_token, exclude, hint
    import graphics as g
    g.figures("space")

    #world specific variable for help tokens
    help_token = [True, True, True]
    
    #early end control variable
    early_end = False
    
    #-------------------------------------------------------------------------#
    #-------------------------  Question Properties  -------------------------#
    #-------------------------------------------------------------------------#
    
    import csv
    
    data = []
    filename = "%s.txt" % f"category_{q}"
    with open(filename, newline='', encoding='utf8') as inputfile:
        for row in csv.reader(inputfile):
            data.append(row)
    
    name_category = data[0]        
    question_text1 = data[1]
    question_text2 = data[2]
    alpha = data[3]
    beta = data[4]
    gamma = data[5]
    delta = data[6]
    answers = data[7]
    points = data[8]
    exclude1 = data[9]
    exclude2 = data[10]
    hint = data[11]
    
    exclude = [None]*max_questions
    right = [None]*max_questions
    for l in range(max_questions):
        exclude[l] = [exclude1[l],exclude2[l]]
        right[l] =  eval(answers[l])
        
    
    #-------------------------------------------------------------------------#
    
    g.figures(f"{name_category[0]}")
    g.talk(f"\nWelcome to the {name_category[0]} category.\n")
    g.delay(1)
    g.talk("Are you ready? Press [ENTER] to start")
    input("")
    
    for k in range(max_questions):
        g.countdown()
        question_display(k)
        answer(k)
        g.delay(1)
        g.talk("Press enter to move to the next question")
        input("\n")
        
        #Premature end of category script
        if k+1 == 5:
            stop = None
            while (stop not in Y) and (stop not in N):
                g.talk(f"\nYou have completed {k+1} questions from this category, {name}. Would you like to stop here? (y/n)?)")
                stop = input("\n")
                if stop in Y:
                    g.talk("\nLet's stop here then. You have completed this category.")
                    if q in [0,1,2]:
                        topic_token[0] = True
                    elif q in [3,4,5]:
                        topic_token[1] = True
                    elif q in [6,7,8]:
                        topic_token[2] = True
                    early_end = True
                elif stop in N:
                    g.talk("\nOk! Let's continue. Good luck.")
                else:
                    g.talk("\nInvalid input. Please answer with (y/n).")
                    
        if (early_end == True):
            break
    
    if (early_end == False):
        #Topic Token designator
        if q in [0,1,2]:
            topic_token[0] = True
            print("\nYou have completed all questions in this category, well done.")
        elif q in [3,4,5]:
            topic_token[1] = True
            print("\nYou have completed all questions in this category, well done.")
        elif q in [6,7,8]:
            topic_token[2] = True
            print("\nYou have completed all questions in this category, well done.")
        else:
            #ERROR message
            print("\nDesignator variable q is not valid!")

    #return to category selection function once this one is completed
    theme()

def question_display(k):
    #Question and answer display formating
    print('\n{:^75}\n'.format('QUESTION ' + str(k+1)))
    print('╭───────────────────────────────────────────────────────────────────────────╮\n')
    print('{:^75}\n'.format(question_text1[k]))
    print('{:^75}\n'.format(question_text2[k]))
    print('╰───────────────────────────────────────────────────────────────────────────╯\n')
    print('{:<5}{:<35}{:<5}{:<10}'.format('[A]',alpha[k],'[B]', beta[k]))
    print('{:<5}{:<35}{:<5}{:<10}'.format('[C]',gamma[k],'[D]', delta[k]))


def answer(k):
    global score, total_score, points, right, skip
    g.figures("space")
    #validity check variables
    attempts = int(1)
    answer_player = None
    while (answer_player not in right[k]) and (attempts <= 3):
        #Player input is either one of the question letters or the help options - upper case forced
        
        if skip == True:
            break
        
        g.talk("Please type in your answer: (A/B/C/D)\n[for help, type \"Help\".]\n\nMake your choice:")
        answer_player = input("\n").upper()
        
        if answer_player in (A + B + C + D): #It is a valid answer
            if answer_player in right[k]:
                g.figures("correct")
                g.figures("space")
                
                #score calculation
                if attempts == 1:
                    score = int(points[k])
                elif attempts == 2:
                    score = int(points[k])*0.5
                elif attempts == 3: 
                    score = int(points[k])*0.25
            else:
                
                attempts += 1
                g.figures("wrong")
                
                if (attempts <= 3):
                
                    print("\nTry again!")
                    g.figures("space")
                    
                    #OPTIONAL EXCLUSION SCRIPT
                    if answer_player in A:
                        alpha[k] = ''
                    if answer_player in B:
                        beta[k] = ''
                    if answer_player in C:
                        gamma[k] = ''
                    if answer_player in D:
                        delta[k] = ''
                    
                    question_display(k)
                    
                
        elif (answer_player == 'HELP'):
            help_menu(k)
        else:
            #Any other input is rejected and goes back to asking for valid input
            g.talk("That is not a valid input. Please try again.")
     
    
    if skip == True:
        score = int(points[k])*0.75
        total_score += score
        g.figures("score")
        score_string_skip = f"Nonetheless, you get {score} points!"
        g.talk(score_string_skip)
        skip = False # reset skip token
        
    else:
        if attempts == 4:
            g.talk("You exausted the number of attempts. You got 0 points")
        else:
            g.figures("score")
            g.talk(f"Question completed after {attempts} attempt(s). You got {score} points!")
            total_score += score
        
    g.talk(f"\nCurrent overall score: {total_score}")
    g.figures("space")
    
def help_menu(k):
    global alpha, beta, gamma, delta, help_token, exclude, hint, skip
    
    g.figures("space")
    g.figures("help")
    g.talk("Welcome to the help menu.\n")
    
    used = ['','','']
    help_input = None
    
    for n in range(3):
        if help_token[n] == False:
            used[n] = str('(used)')
            
    while help_input not in (A + B + C + D):
        
        help_menu = f"[A]:\t50:50 {used[0]}\n[B]:\tSkip {used[1]}\n[C]:\tHint {used[2]}\n[D]:\tExit help menu.\n"
        g.talk(help_menu)
        g.talk("Make your choice:")
        help_input = input("\n").upper()
        
        if (help_input in A) and (help_token[0] == False):
            g.talk("You can no longer make use of the 50:50 option. Please select from the help options that remain.\n")
            help_input = None
        elif (help_input in A) and (help_token[0] == True):
            
            #50:50 EXCLUSION SCRIPT
            if 'A' in exclude[k]:
                alpha[k] = ''
            if 'B' in exclude[k]:
                beta[k] = ''
            if 'C' in exclude[k]:
                gamma[k] = ''
            if 'D' in exclude[k]:
                delta[k] = ''
            
            g.talk("Two of the options have been excluded. You can still select them however, so don't make a mistake!\n")
            help_token[0] = False
        
        elif (help_input in B) and (help_token[1] == False):
            g.talk("You can no longer make use of the skip question option. Please select from the help options that remain.\n")
            help_input = None
        elif (help_input in B) and (help_token[1] == True):
            
            skip = True #token to skip question
            g.talk(f"\nVery well, you have skipped question {k+1}.\n")
            help_token[1] = False
            break
            
        elif (help_input in C) and (help_token[2] == False):
            g.talk("You can no longer make use of the hint option. Please select from the help options that remain.\n")
            help_input = None
        elif (help_input in C) and (help_token[2] == True):
            
            hint_text = f"Ok, here's a hint for you:\n{hint[k]}"
            print(hint_text)
            help_token[2] = False
            
        elif (help_input in D):
            g.talk("Exiting help menu.")
        else:
            g.talk("That is not a valid input.")
            continue
            
        question_display(k)


def board():

    import pandas as pd
    import os
    
    from datetime import date
    today = date.today()
    
    board = pd.read_csv("leader_board.csv", names = ["SCORE", "NAME", "DATE"])

    personal_score = pd.DataFrame({"SCORE": [total_score], "NAME": [name], "DATE": [today]})

    leader_board = board.append(personal_score)
    leader_board = leader_board.sort_values(by = ["SCORE"], ascending = False)
      
    path = str(os.getcwd()) + str("/leader_board.csv")
    leader_board.to_csv(path, index = False, header=False)
        
    g.talk("Do you want to see the leader board? (y/n)")
    decision = input("\n")
    if str(decision) in Y: 
        g.figures("leader_board")
        print("\n\n")
        print(leader_board.head())            

def farewell():
    g.figures("space")
    print(f"Farewell, {name}. Thank you for playing.")


#MAIN BODY/FUNCTION ORDER
    
presentation()
rules()
introduction()
theme()
board()
farewell()
