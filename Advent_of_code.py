import numpy as np
import re

class color:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW= '\033[93m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def importFile(path_to_file:str)->list:
    cleaned_lines = []
    with open(path_to_file) as input:
        for line in input.readlines():
            cleaned_lines.append(line.replace("\n",""))
    return cleaned_lines

def count_calories(file_content:list)->dict:
    elf_iterator = 0
    elves = {}
    for line in file_content:
        if line == "\n":
            
            elf_iterator += 1
        else:
            elf_name = "elf" + str(elf_iterator)
            
            try:
                elves[elf_name] += int(line)
            except KeyError:
                elves[elf_name] = int(line)
    return elves

def find_max(elves:dict)->None:
    max = [0,0,0]
    for elf in elves:
        
        if elves[elf] > max[0]:
            max[2] = max[1]
            max[1] = max[0] 
            max[0] = elves[elf]
            
        elif elves[elf] > max[1]:
            max[2] = max[1]
            max[1] = elves[elf]

        elif elves[elf] > max[2]:
            max[2] = elves[elf]
        
    print(sum(max))

"""
A: Rock     1
B: Paper    2
C: Scissor  3
X: Lose     0
Y: Draw     3
Z: Win      6
"""
def rockPaperScossor(Strat_guide:list)->None:
    
    my_points = 0
    
    for game in Strat_guide:
        game = game.replace("\n","").split(" ")
        their_play = game[0]
        game_end = game[1]
        if their_play == "A":
            if game_end == "X":
                my_points += 0
                my_points += 3
            elif game_end == "Y":
                my_points += 3
                my_points += 1
            elif game_end == "Z":
                my_points += 6
                my_points += 2

        elif their_play == "B":
            if game_end == "X":
                my_points += 0
                my_points += 1
            elif game_end == "Y":
                my_points += 3
                my_points += 2
            elif game_end == "Z":
                my_points += 6
                my_points += 3

        elif their_play == "C":
            if game_end == "X":
                my_points += 0
                my_points += 2
            elif game_end == "Y":
                my_points += 3
                my_points += 3
            elif game_end == "Z":
                my_points += 6                
                my_points += 1                

    print(my_points)

def find_common_item(file_content)->None:
    points = 0
    elf_counter = 0
    rucksack_container = [0,0,0]

    for rucksack in file_content:
        rucksack_container[elf_counter] = rucksack
        elf_counter += 1
        if elf_counter == 3:
            for item in rucksack_container[0]:
                if rucksack_container[1].find(item) != -1:  
                    if rucksack_container[2].find(item) != -1:  
                        
                        break
            elf_counter = 0
            partly_point = ord(item)-96
            if partly_point <= 0:
                partly_point = ord(item)-65+27
            points += partly_point
    print(points)

def find_overlapping_sections(file_content):
    elf = [{},{}]
    elf_pairs = 0
    for pair in file_content:
        elf[0]["lowest"] = int(pair.split(",")[0].split("-")[0])
        elf[0]["highest"] = int(pair.split(",")[0].split("-")[1])

        elf[1]["lowest"] = int(pair.split(",")[1].split("-")[0])
        elf[1]["highest"] = int(pair.split(",")[1].split("-")[1])
        array_length = max(elf[0]["highest"],elf[1]["highest"])
        range_of_numbers = ["."]*(array_length+1)

        for j in range(elf[0]["lowest"],elf[0]["highest"]+1):
            range_of_numbers[j] = "x"
        for j in range(elf[1]["lowest"],elf[1]["highest"]+1):
            
            if range_of_numbers[j] == "x":
                range_of_numbers[j] = "y"
                elf_pairs += 1
                break
    print(elf_pairs,len(file_content))
            

def move_crate(stacks, start, end,number_of_crates_to_move):
    bottom_position = len(stacks[start])-number_of_crates_to_move
    stacks[end]    += stacks[start][bottom_position:]
    stacks[start]   = stacks[start][:bottom_position]   
    return stacks

def print_stacks(stacks):
    for stack in stacks:
        print(stack,stacks[stack])

def rearrange_crates(file_content):
    stacks = {}
    for idx,line in enumerate(file_content):
        if line[:2] == " 1":
            for stack in line.split("   "):
                stacks[int(stack)] = ""
            break
    for line in reversed(file_content[:idx]):
        
        for stack in stacks:
            pattern = re.compile(r"(\[(?P<Container>\w*)\])")
            found_reg_string = re.finditer(pattern,line)

            if found_reg_string is not None:
                for match in found_reg_string:
                    found_container = match.group().replace("[","").replace("]","")
                    if match.span()[0] < stack*4-1 <= match.span()[1]:
                        stacks[stack] += found_container
        
    print_stacks(stacks)
    print()
        

    for line in file_content[idx+2:]:
        pattern = re.compile(r"move (?P<number>\w*) from (?P<start>\w*) to (?P<end>\w*)")
        number_of_crates_to_move = int(re.match(pattern,line).group("number"))
        starting_stack = int(re.match(pattern,line).group("start"))
        ending_stack = int(re.match(pattern,line).group("end"))
        
        stacks = move_crate(stacks,starting_stack,ending_stack,number_of_crates_to_move)
        
    
    for stack in stacks:
        print(stacks[stack][-1],end="")    
    print()
    print_stacks(stacks)

def check_characters(characters:str)->bool:
    
    for i in characters:
        if characters.count(i)>1:
            return False
    return True

def find_start_marker(file_content:list,distinct_chars:int):
    
    for data_stream in file_content:
        print(data_stream,end=": ")
        idx = distinct_chars
        while (idx <= len(data_stream)):
            char = data_stream[idx-1]                                 
            if check_characters(data_stream[idx-distinct_chars:idx]):
                print(idx)
                break

            idx += 1


def run1(file_content:list):
    elves = count_calories(file_content)
    find_max(elves)

def run2(file_content:list):
    rockPaperScossor(file_content)

def run3(file_content:list):
    find_common_item(file_content)

def run4(file_content:list):
    find_overlapping_sections(file_content)

def run5(file_content:list):
    rearrange_crates(file_content)

def run6(file_content:list):
    find_start_marker(file_content,14)

if __name__ == "__main__":
    file_content = importFile("input.txt")
    run6(file_content)