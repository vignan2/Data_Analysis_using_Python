#!/usr/bin/python3

import sys

def main(*args):
    if len(args) != 1:
        print("Incorrect arguments. Please pass the name of the file to be cleaned")
        sys.exit()
    file_name = args[0]  # 'class.txt'
    out_file_name = 'cleaned.txt'
    
    count = 0
    
    course_catalog = []
    professor = []
    course = []
    duplicates = []
    
    # Referred from http://stackabuse.com/read-a-file-line-by-line-in-python/
    with open(file_name) as input_file:
        line = input_file.readline()
        course_catalog.append(line.strip())
        while line:
            line = input_file.readline()
            count = count + 1
            course_catalog.append(line.strip())
    
    number_of_splits = 1
    
    for i in range(count):
        professor.append(course_catalog[i].split('-', number_of_splits)[0].strip())
        course.append(course_catalog[i].split('-', number_of_splits)[1].strip().split('|'))
    
    for i in range(count):
        if ',' in professor[i]:
            professor[i] = professor[i].split(',', number_of_splits)[0].title()
        elif ' ' in professor[i]:
            professor[i] = professor[i].split()[-1:][0].title()
        elif '.' in professor[i]:
            professor[i] = professor[i].split('.')[-1:][0].title()
    
    for i in range(count):
        for j in range(len(course[i])):
            course[i][j] = course[i][j].title()
    
    for i in range(count):
        for j in range(i+1, count):
            if(professor[i] == professor[j]):
                for c in course[j]:
                    course[i].append(c)
                if j not in duplicates:
                    duplicates.append(j)
                #print("Line {} {}: {}".format(i, j, professor[j]))
    
    duplicates = sorted(duplicates, reverse = True)
    
    for d in duplicates:
        del professor[d]
        del course[d]
        #print(d)
    
    for c in course:
        c.sort()
    
    # Referred from http://interactivepython.org/runestone/static/pythonds/SortSearch/TheBubbleSort.html
    for i in range(len(professor)-1, 0, -1):
            for j in range(i):
                if professor[j] > professor[j+1]:
                    temp = professor[j]
                    professor[j] = professor[j+1]
                    professor[j+1] = temp
                    temp = course[j]
                    course[j] = course[j+1]
                    course[j+1] = temp
    
    with open(out_file_name, 'w') as output_file:
        for i in range(len(professor)):
            output_file.write("{}  - ".format(professor[i]))
            for j in range(len(course[i]) - 1):
                output_file.write("{}|".format(course[i][j]))
            output_file.write("{}\n".format(course[i][-1:][0]))

    print("Successfully cleaned the file '{}' and generated 'cleaned.txt' file".format(args[0]))

if __name__ == "__main__": main(*sys.argv[1:])
