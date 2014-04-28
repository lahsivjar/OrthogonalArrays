# GUI

from Tkinter import *
from os import listdir
from os.path import isfile, join
from numpy import matrix
from OA import OA
from mutation import mutation_t1, mutation_t2
from crossover import one_point_crossover
from threading import Thread
from collections import Counter

import random
import utilities as util
import tkMessageBox as mb
import os
import re
import time


class Basic_Gui(Frame):
    
    def __init__(self, master):
        self.data_path = os.path.join(util.module_path(), "..\data")
        self.dump_path = os.path.join(util.module_path(), "..\dump")
        Frame.__init__(self, master)
        self.grid()
        self.create_elements()
        
    def create_elements(self):
        """ Put the elements of the GUI """

        # Run Option Menu
        Label(self, text = "Runs :").grid(row = 0, column = 0, columnspan = 1, sticky = W)
        self.run = StringVar()
        self.choices = self.scan_data()
        self.run_menu = OptionMenu(self, self.run, command = self.select_runsize, *self.choices)
        self.run_menu.config(width = 2)
        self.run_menu.grid(row = 0, column =1, columnspan = 1, padx = 5, pady = 5, sticky = W)

        # Mutation Check Button
        self.mutation1 = IntVar()
        self.mutation2 = IntVar()
        self.mutation_button1 = Checkbutton(self, text= "Mutation Type1", variable = self.mutation1, command = self.update_mutation1)
        self.mutation_button1.grid(row = 0, column = 2, columnspan = 1, padx = 5, pady = 5, sticky = W)
        self.mutation_button2 = Checkbutton(self, text= "Mutation Type2", variable = self.mutation2, command = self.update_mutation2)
        self.mutation_button2.grid(row = 1, column = 2, columnspan = 1, padx = 5, pady = 5, sticky = W)

        # Mutation Rate Field
        self.mutation_rate1 = Entry(self)
        self.mutation_rate2 = Entry(self)
        self.mutation_rate1.grid(row = 0, column = 3, columnspan = 1, padx = 5, pady = 5, sticky = W)
        self.mutation_rate2.grid(row = 1, column = 3, columnspan = 1, padx = 5, pady = 5, sticky = W)
        self.mutation_rate1.config(width = 5)
        self.mutation_rate2.config(width = 5)
        self.mutation_rate1.config(state = "disabled")
        self.mutation_rate2.config(state = "disabled")

        # Crossover Rate
        Label(self, text = "Crossover Rate: ").grid(row = 0, column = 4, columnspan = 2, padx = 5, pady = 5, sticky = W)
        self.crossover_rate = Entry(self)
        self.crossover_rate.grid(row = 0, column = 6, columnspan = 1, padx = 5, pady = 5, sticky = W)
        self.crossover_rate.config(width = 5)

        # Population Size
        Label(self, text = "Population Size: ").grid(row = 1, column = 4, columnspan = 2, padx = 5, pady = 5, sticky = W)
        self.population_size = Entry(self)
        self.population_size.grid(row = 1, column = 6, columnspan = 1, padx = 5, pady = 5, sticky = W)
        self.population_size.config(width = 5)

        # Update the run menu
        self.update_button = Button(self, text = "Update OA Data", command = self.update_run_menu)
        self.update_button.grid(row = 1, column = 0, columnspan = 2, padx = 5, pady = 5, sticky = W)

        # Begin Stop GA Button
        self.begin_button = Button(self, text = "Begin", command = self.begin_stop_ga)
        self.begin_button.grid(row = 0, column = 7, columnspan = 1, padx = 5, pady = 5, sticky = W)
        self.begin_button.config(width = 6)

        # Show current population fitness value
        self.show_button = Button(self, text = "Show", command = self.show_curr_fitness)
        self.show_button.grid(row = 1, column = 7, columnspan = 1, padx = 5, pady = 5, sticky = W)
        self.show_button.config(width = 6)
        self.show_button.config(state = "disabled")

        # Console
        Label(self, text = "Console: ").grid(row = 2, column = 0, columnspan = 3, padx = 5, pady = 5, sticky = W)
        self.console = Text(self, width = 70, height = 10, wrap = WORD)
        self.console.grid(row = 3, column = 0, columnspan = 8, padx = 5, pady = 5, sticky = W)
        self.console.config(state = "disabled")
        self.console_scroll = Scrollbar(self)
        self.console.config(yscrollcommand = self.console_scroll.set)
        self.console_scroll.config(command = self.console.yview)
        
    def begin_stop_ga(self):
        if self.begin_button["text"]=="Begin":
            if self.run.get() == "" :
                mb.showerror("Error", "Run Size not set")
                return
            if self.crossover_rate.get() == "":
                mb.showerror("Error", "Crossover rate not set")
                return
            if self.mutation1.get() == 1 and self.mutation_rate1.get() == "":
                mb.showerror("Error", "Type 1 mutation rate not set")
                return
            if self.mutation2.get() == 1 and self.mutation_rate2.get() == "":
                mb.showerror("Error", "Type 2 mutation rate not set")
                return
            if self.population_size.get() == "":
                mb.showerror("Error", "Population size not set")
                return
            try:
                if int(self.population_size.get()) <= len(self.initial_oa_population):
                    raise ValueError
            except ValueError:
                mb.showerror("Error", "Invalid Population Size")
                self.population_size.delete(0, "end")
                return
            
            self.show_button.config(state = "normal")
            self.run_menu.config(state = "disabled")
            self.mutation_button1.config(state = "disabled")
            self.mutation_button2.config(state = "disabled")
            self.mutation_rate1.config(state = "disabled")
            self.mutation_rate2.config(state = "disabled")
            self.crossover_rate.config(state = "disabled")
            self.population_size.config(state = "disabled")
            self.update_button.config(state = "disabled")
            self.begin_button["text"] = "Stop"

            self.load_and_run()
        else:
            self.show_button.config(state = "disabled")
            self.run_menu.config(state = "normal")
            self.mutation_button1.config(state = "normal")
            self.mutation_button2.config(state = "normal")
            if self.mutation1.get() == 1:
                self.mutation_rate1.config(state = "normal")
            if self.mutation2.get() == 1:
                self.mutation_rate2.config(state = "normal")
            self.crossover_rate.config(state = "normal")
            self.population_size.config(state = "normal")
            self.update_button.config(state = "normal")
            self.begin_button["text"] = "Begin"

            self.runFlag = False
            
    def show_curr_fitness(self):
        temp = '\n[ '
        for i in self.initial_oa_population:
            temp += str(i.get_fitness_value()) + " , "
        temp = temp.rstrip(', ') + " ]"

        self.set_in_console(temp)
        
    def select_runsize(self, runsize):
        ''' Scans the data directory for OA's of selected runsize and loads them as members of initial population'''
        if (runsize == ""):
            return
        self.initial_oa_population = []
        load_data = [i for i, word in enumerate(self.all_files) if re.search('^' + str(runsize) + ',' + '.*', word)]
        self.set_in_console("Loading ...")

        for i in load_data:
            print self.all_files[i]
            file1 = open(join(self.data_path, self.all_files[i]), 'r')
            ar = ''
            for j in file1.readlines():
                ar += j.rstrip(',\n') + ';'
            ar = ar.rstrip(';')
            self.initial_oa_population.append(OA(self.all_files[i].split('.')[0], matrix(ar)))
        self.initial_population_size = len(load_data)
        
        for i in self.initial_oa_population:
            print i.get_fitness_value()
            
        self.set_in_console("Loaded " + str(self.initial_population_size) + " OA's of run size " + str(runsize))
        
    def update_mutation1(self):
        if self.mutation1.get() == 1:
            self.mutation_rate1.config(state = "normal")
        elif self.mutation1.get() == 0:
            self.mutation_rate1.config(state = "disabled")

    def update_mutation2(self):
        if self.mutation2.get() == 1:
            self.mutation_rate2.config(state = "normal")
        elif self.mutation2.get() == 0:
            self.mutation_rate2.config(state = "disabled")

    def update_run_menu(self):
        self.set_in_console("Loading ...")
        options = self.scan_data()
        menu = self.run_menu["menu"]
        menu.delete(0, "end")
        for itm in options:
            menu.add_command(label = itm,
                             command = lambda value = itm: self.util_1(value))
        self.set_in_console("Loaded OA's of " + str(len(options) - 1) + " different run size")
        self.run.set("")

    def util_1(self, value):
        self.run.set(value)
        self.select_runsize(value)

    def set_in_console(self, text):
        text += "\n"
        self.console.config(state = "normal")
        self.console.insert(END, text)
        self.console.config(state = "disabled")
        self.console.yview_moveto(1.0)

    def load_and_run(self):
        ''' Load parameters and call run_ga '''
        try:
            num_run = int(self.run.get())
            num_population = int(self.population_size.get())
            num_crossover_rate = float(self.crossover_rate.get())
            if self.mutation1.get() == 0:
                num_mutation_rate1 = 0
            else:
                num_mutation_rate1 = float(self.mutation_rate1.get())
            if self.mutation2.get() == 0:
                num_mutation_rate2 = 0
            else:
                num_mutation_rate2 = float(self.mutation_rate2.get())

            self.runFlag = True
            Thread(target = self.run_ga, args = [self.initial_oa_population, self.initial_population_size,
                                                 num_population, num_crossover_rate, num_mutation_rate1,
                                                 num_mutation_rate2]).start()
        except ValueError:
            mb.showerror("Error", "Invalid Input")
            self.begin_stop_ga()

    def run_ga(self, initial_oa_population, initial_population_size, num_population,
               num_crossover_rate, num_mutation_rate1, num_mutation_rate2):
        ''' Run Genetic Algorithm '''
        current_generation = 0
        while(self.runFlag):
            # Select two OA's for crossover
            index_1 = random.randint(0, len(initial_oa_population) - 1)
            index_2 = random.randint(0, len(initial_oa_population) - 1)

            # Perform crossover
            [oa1, oa2] = one_point_crossover([initial_oa_population[index_1], initial_oa_population[index_2]], num_crossover_rate)

            # After Crossover perform mutation
            if num_mutation_rate1 > 0:
                oa1 = mutation_t1(oa1, num_mutation_rate1)
                oa2 = mutation_t1(oa2, num_mutation_rate1)
            if num_mutation_rate2 > 0:
                oa1 = mutation_t2(oa1, num_mutation_rate2)
                oa2 = mutation_t2(oa2, num_mutation_rate2)

            # Perform check to see if oa1 and oa2 are eligible to gain spot in population
            self.check_eligible([oa1, oa2], initial_oa_population, initial_population_size, num_population)

            print "Current gen: " + str(current_generation) + ' :: ' + 'Total_pop_size: ' + str(len(initial_oa_population))
            tapu = ''
            for i in initial_oa_population:
                tapu += ': ' + str(i.get_fitness_value())
            print tapu + '\n'
            for i in initial_oa_population:
                print i.string + '  :  ' + str(i.get_fitness_value())
            print "\n\nOA's:\n"
            print oa1.string + '  :  ' + str(oa1.get_fitness_value())
            print oa2.string + '  :  ' + str(oa2.get_fitness_value())
            print 'END\n'

            # Update current_generation
            current_generation += 1
            time.sleep(0.01)

        # Dump all information to a dump file
        self.dump_info(initial_oa_population)
        

    def check_eligible(self, oa, population, initial_population, max_population):
        ''' Check if 2 oa's given by a list are eligible for getting accepted in current_population '''
        # Return the index at which to put the oa if index = -1 then don't put it in population
        max_fit = population[-1].get_fitness_value()
        current_population = len(population)
        for i in oa:
            if len(i.factors) <= 1:
                continue
            acceptFlag = True
            temp1 = Counter(i.factors)
            for j in range(0, initial_population):
                temp2 = Counter(population[j].factors)

                # Accept an oa if and only if it's factors are not a subset of any OA in initial data
                if not temp1 - temp2:
                    acceptFlag = False
                    break

            if acceptFlag:
                lastFlag = False
                for j in range(current_population, initial_population - 1, -1):
                    j -= 1
                    # if fit_val is greater than 0 i is better else not better than population's jth OA
                    if j == initial_population - 1:
                        lastFlag = True
                    fit_val = population[j].get_fitness_value() - i.get_fitness_value()

                    if (fit_val < 0 or lastFlag) and current_population < max_population:
                        population.insert(j + 1, i)
                        current_population = len(population)
                        break
                    elif (fit_val < 0 or lastFlag):
                        # Now we insert our value oa after deleting one member of population
                        population.insert(j + 1, i)
                        del population[-1]
                        current_population = len(population)
                        break
                    elif fit_val >= 0:
                        # If i is same as jth member(factors same) but better fitness then remove j
                        if Counter(i.factors) == Counter(population[j].factors):
                            del population[j]
                            current_population = len(population)
                        # If factors not same continue with next value of j
                #If i oa is not acceptable don't put it in population
            
    def scan_data(self):
        ''' Scan and return a list of run sizes available in data directory '''
        return_list = ["",]
        self.all_files = [f for f in listdir(self.data_path) if isfile(join(self.data_path, f))]
        self.all_files.sort(key = lambda x: int(x.split(',')[0]))

        for i in self.all_files:
            temp = i.split(',')[0]
            if temp not in return_list:
                return_list.append(temp)

        return return_list

    def dump_info(self, population):
        ''' Dump all the GA parameters and current population to a dump file '''
        print "Arrays in population: "
        for i in population:
            print "\t" + i.string + " : " + str(i.get_fitness_value())
            dmp = os.path.join(self.dump_path, i.string)
            i.print_array(dmp)
            
        ######### Also create a function to load dump files ##########

        
root = Tk()
root.title("MSc. Project")
root.geometry("577x305")
root.resizable(width = False, height = False)
app = Basic_Gui(root)

root.mainloop()
