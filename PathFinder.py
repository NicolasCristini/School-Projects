# Import libraries

import numpy as np
import random

import tkinter as tk   
from itertools import permutations


# Main class for the application window
class GUI:
    
    # init function for the app window
    def __init__(self,parent):
        
        self.parent = parent
        
        #Initial grid size
        self.size=4
        self.totalscore = 0
        self.solution_path= []
        self.window_width = 480
        self.window_height = 480
        self.gridsquare_size = int(self.window_width/(self.size))

        #Introduction Label
        self.intro=tk.Label(self.parent, width = 90, height=6, fg = "black", text = """
                            
                            Find the path from the Start (S) to the Goal (G) on which the sum of the numbers on the visited 
                            fields is the highest. But, you are only allowed to step upwards ⬆︎ and to the right ➡︎.
                            
                                So, what is the maximal sum that can be gained this way, and through which path?
                            
                            """, font=("Arial", 10, "bold"))
        self.intro.pack(side = "top")
        
        
        #Score label
        self.info=tk.Label(self.parent, width=60, height=1, fg='black', text="Click \"Find best path\" to see the maximum score.", background="white", font=('Arial',10))
        self.info.pack(side="top")
                        
        #Draw canvas for the grid
        self.draw_canvas()
        
        #Create grid data (numpy array) and draw grid numbers and horizontal and vertical gridlines
        self.grid = self.create_grid()
        self.draw_grid() 
        self.draw_gridlines()
        
        #Create the the and the buttons and the guess container
        self.draw_buttons(self.parent)
        self.guess_score()

        #Get the max_score and solution for the actual grid by calling the solve() function
        self.max_score, self.solution = self.solve()

    
## CREATION OF THE OBJECTS IN THE WINDOW ##
    def draw_canvas(self):

        #Canvas
        self.window = tk.Canvas(self.parent, width=self.window_width, height=self.window_height, bg='white', bd=0, highlightthickness=0)
        self.window.pack(side = "top")
        
        #Draw square background and start and finish tiles
        self.window.create_rectangle(0,0,self.window_width,self.window_height, fill="white")
        self.window.create_rectangle(self.window_width-self.gridsquare_size,0,self.window_width,self.gridsquare_size, fill="orange", outline="orange")
        self.window.create_rectangle(0,self.window_height,self.gridsquare_size,self.window_width-self.gridsquare_size, fill="lightblue",  outline="lightblue")
 

    def draw_gridlines(self):

        #draw horizontal grid lines
        for k in range(0, self.window_width, self.gridsquare_size):
            self.window.create_line(0, k, self.window_width, k)

        
        # draw vertical grid lines lines
        for k in range(0, self.window_height, self.gridsquare_size):
                self.window.create_line(k, 0, k, self.window_height)

    def create_grid(self):
        #Create a random array of numbers to place in the grid
        grid = np.array([random.choice(range(1,10)) for i in range (0,self.size*self.size)]).reshape(self.size,self.size)
        grid[0,len(grid[:,0])-1]=0
        grid[len(grid[0,:])-1,0]=0    
        return grid     
    
         
    def draw_grid(self):
        #Write the previously created numbers in the grid.
        fontsize=10
        
        padx= self.gridsquare_size/2-11
        pady= self.gridsquare_size/2-11
        
                
        for i in range(len(self.grid[:,0])):
            for j in range(len(self.grid[0,:])):
                
                #Adds the starting label in the bottom left
                if i == len(self.grid[:,0])-1 and j == 0:
                    self.e = tk.Label(self.window,  text="S", width=2, height=1, font=('Arial',fontsize, 'bold'),  background="lightblue")
                    self.e.grid(row=i, column=j, padx = padx, pady = pady)
                    
                    
                #Adds the finish label in the bottom left
                elif j == len(self.grid[:,0])-1 and i == 0:
                    self.e = tk.Label(self.window, text="F",  width=2, height=1, font=('Arial',fontsize, 'bold'), background ="orange")
                    self.e.grid(row=i, column=j, padx = padx, pady = pady)
                
                #Adds all the other numbers in the grid
                else:
                    self.e = tk.Label(self.window, text=self.grid[i,j], width=2, height=1, font=('Arial',fontsize), background= "white" )
                    self.e.grid(row=i, column=j,  padx = padx, pady = pady)
    
    
    def draw_buttons(self, parent): 
        
        #Button Container
        self.container = tk.Frame(parent)
        self.container.pack(side="bottom")
        self.colwidth = 20
        
        ###Create and pack the menu buttons.###
        #Pathfinding button
        self.findbest_btn = tk.Button(self.container,text="Find best path", width=self.colwidth, command=self.draw_solution)
        self.findbest_btn.pack(side="left")
        
        self.size_scale = tk.Scale(self.container, from_=3, to=6, orient=tk.HORIZONTAL, width=18)
        self.size_scale.set(4)
        self.size_scale.pack(side="left", ipady=9)
  
        
        #New grid button
        self.newfield_btn = tk.Button(self.container,text="Create new grid", width=self.colwidth, command=self.new_grid)
        self.newfield_btn.pack(side="left")
        
        #Exit program button
        self.exit_btn = tk.Button(self.container,text="Exit" , width=self.colwidth, command = parent.destroy)
        self.exit_btn.pack(side="left")




## CREATE A NEW GRID TO REPEAT THE GAME ##

#This chunck of code destroy the old canvas and create a new canvas, grid, gridlines, 
#taking the selected size from the slider into account, from min 3x3 grid to max 6x6 grid.
#This function is executed as a command for the self.newfield_btn
    
    def new_grid(self):
        
        #Get size from the slider and set the size of a square depending on the amount of squares in the grid.
        self.size = self.size_scale.get()
        self.gridsquare_size = int(self.window_width/(self.size))
        
        #Destroy the old canvas
        self.window.destroy()
        
        #Create a new canvas and draw a new grid on it.
        self.draw_canvas()
        self.grid = self.create_grid()
        self.draw_grid()
        self.draw_gridlines()
        self.info["text"]="Click on Find best path to view the score!"
        
        #Recompute the solution for the new grid
        self.max_score, self.solution = self.solve()
        
    

## CALCULATE THE SOLUTION ##

#Creates a function to solve the enigma and return the class
#the maximum score and the solution grid.    
    
    def solve(self):

        #Create all possible combinations.
        commands = (["up"] * (self.size-1)) + (["right"] * (self.size-1))
        combinations = (list(set(permutations(commands))))


        #Make a dictionaire and keep track of all the path and relative scores.
        sol = {}
        for comb in combinations:
         
            score = 0
            solution = np.zeros_like(self.grid)
            solution[len(self.grid[:,0])-1,0]=1 
            #Initialize the coordinates, starting form the borrom left corner.
            i_up = int(self.size)-1 
            i_right = 0

            for move in comb:
                
                if move == "up":
                    #Move the index one up
                    i_up -= 1
                    solution[i_up,i_right]=1
                    if self.grid[i_up][i_right] != ("G" or "S"):
                        score += int(self.grid[i_up][i_right])
                       

                if move == "right":
                    #Move the index one right
                    i_right += 1
                    solution[i_up,i_right]=1
                    if self.grid[i_up][i_right] != ("G" or "S"):
                        score += int(self.grid[i_up][i_right]) 
                      

            #Pairs the score with the solution array
            sol[score] = solution
          
            
        #Find the highest scores and the related solution    
        max_score = max(sol.keys())
        solution = sol[max_score]
        
        #return the max_score and the solution as the set of moves
        return max_score, solution
   
    
    def draw_solution(self):
        #Draw the solution on the grid

        self.info["text"]=f"Maximum possible score:{self.max_score}"    
        halfsquare = self.gridsquare_size/2    
        
        #Creates a list with the same x coordinates as the grid
        x = [k for k in range(0, self.window_height, self.gridsquare_size)]
        y = [k for k in range(0, self.window_height, self.gridsquare_size)]
        
        #For each row and coloumn draw the line according to the solution
        for i in range(len(self.solution[:,0])):
            for j in range(len(self.solution[0,:])):
                                            
                
                if i == len(self.solution[:,0])-1 and j == len(self.solution[0,:])-1:
                     pass
            
                #If the next number in the correct path is up, draw a vertical line.
                if self.solution[i,j] == 1 and i != 0 and self.solution[i-1,j] ==1:
                    self.window.create_line(
                            x[j]+halfsquare,
                            y[i]-halfsquare,
                            x[j]+halfsquare,
                            y[i]-halfsquare+self.gridsquare_size,
                            fill="green",
                            width=3)

                #In other cases (next number in the correct path is right), draw a horizontal line.
                elif self.solution[i,j] == 1 and j<len(self.solution[0,:])-1 and self.solution[i,j+1] ==1:
                    self.window.create_line(
                            x[j]+halfsquare,
                            y[i]+halfsquare,
                            x[j]+halfsquare+self.gridsquare_size,
                            y[i]+halfsquare,
                            fill="green",
                            width=3)
                    

## GUESS THE MAXIMUM SCORE OF THE GRID ##

#We ask to the user to guess the max score and to insert it as entry
#By cliking the check button it will say if the guess is right or wrong. 

    def guess_score(self):
            self.guess_container = tk.Frame(self.parent)
            self.guess_container.pack(side="bottom")

            #Create the solution field
            self.solution_text = tk.Label(self.guess_container)
            self.solution_text.configure(text = "Guess !", background = "white")
            self.solution_text.pack(side = "right")

            #Create an entry field
            self.guess = tk.StringVar()
            self.guess_entry = tk.Entry(self.guess_container, textvariable = self.guess)
            self.guess_entry.pack(side = "left")

            #Create a Check buttton
            self.Check_button = tk.Button(self.guess_container)
            self.Check_button["text"] = "Check"
            self.Check_button.pack() #to make it visible
            self.Check_button.bind("<Button-1>", self.check_button_click)
   
    def check_button_click(self, event):
        #Show result
        try:
            self.guess_number = int(self.guess.get())
            if self.guess_number < self.max_score:
                self.solution_text.configure(text = f"{self.guess_number} is too little")
            elif self.guess_number > self.max_score:
                self.solution_text.configure(text = f"{self.guess_number} is too large")
            else:
                self.solution_text.configure(text = "Correct!")
        except:
             self.solution_text.configure(text = "Invalid input")
            

## MAIN ##

root = tk.Tk()
root.title('Pathfinder')
app = GUI(root)

root.mainloop()