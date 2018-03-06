#!/usr/bin/python3

import sys
import re

# Referred from https://docs.python.org/2/library/sets.html
# Calculate jaccard distance based on character similarity
def jaccard_char(str1, str2):
    chars1 = set(str1)
    chars2 = set(str2)
    jaccard = len(chars1 & chars2) / len(chars1 | chars2)
    return jaccard 

# Referred from https://docs.python.org/2/library/sets.html
# Calculate jaccard distance based on word similarity
def jaccard_word(str1, str2):
    words1 = set(str1.split())
    words2 = set(str2.split())
    #words1 = set(re.split(' |\|', str1))
    #words2 = set(re.split(' |\|', str2))
    jaccard = len(words1 & words2) / len(words1 | words2)
    return jaccard

# Count the number of distinct courses where two courses are considered to be distinct if their similarity
# is less than the specified value
def count_courses(file_name, similarity_threshold):
    courses = []
    course = []
    duplicate_courses = []
    
    with open(file_name) as input_file:
        line = input_file.readline()
        while line is not '':
            line = line.split('-', 1)[1].strip()
            course = line.split('|')
            for c in course:
                courses.append(c)
            line = input_file.readline()

    courses = sorted(courses)
    
    n = len(courses)
    for i in range(n):
        for j in range(i+1, n):
            if(jaccard_char(courses[i], courses[j]) >= similarity_threshold):
                duplicate_courses.append(courses[i])
                break

    num_of_courses = len(courses) - len(duplicate_courses)    
    print("Number of distinct courses are: {}\nHere, the courses having jaccard distance > {} are considered to be similar and hence do not contribute to the set of distinct courses\n".format(num_of_courses, similarity_threshold))
    #for i in items_to_remove:
        #print(i)

# List all the courses taught by the professor specified
def list_course(file_name, professor_name):
    courses = []

    if ',' in professor_name:
        professor_name = professor_name.split(',', 1)[0].title()
    elif ' ' in professor_name:
        professor_name = professor_name.split()[-1:][0].title()
    elif '.' in professor_name:
        professor_name = professor_name.split('.')[-1:][0].title()

    with open(file_name) as input_file:
        line  = input_file.readline()
        while line.split('-')[0].strip() != professor_name and line is not '':
            line = input_file.readline()
        if line is '':
            print("Professor {} not found in the catalog\n".format(professor_name))
            return
        line = line.split('-', 1)[1].strip()
        courses = line.split('|')

    print("The courses taught by Prof. {} are:".format(professor_name))
    for i in range(len(courses) - 1):
        print("'{}', ".format(courses[i]), end = "")
    print("'{}'\n".format(courses[-1:][0]))

# Find 2 professors having the most aligned teaching interests based on course titles using jaccard distance as the similarity measure
def find_common_interests(file_name):
    course_catalog = []
    professor = []
    course = []
    prof_course = []
    
    with open(file_name) as input_file:
        line = input_file.readline()
        course_catalog.append(line.strip())
        while line is not '':
            line = input_file.readline()
            course_catalog.append(line.strip())
    
    number_of_splits = 1
    course_threshold = 5
    
    for i in range(len(course_catalog)):
        if course_catalog[i].count('|') >= course_threshold - 1:
            professor.append(course_catalog[i].split('-', number_of_splits)[0].strip())
            course.append(course_catalog[i].split('-', number_of_splits)[1].strip().split('|'))

    for i in range(len(course)):
        for j in range(i+1, len(course)):
            jaccard_sum = 0
            for k in range(len(course[i])):
                for l in range(len(course[j])):
                    jaccard_sum = jaccard_sum + jaccard_word(course[i][k], course[j][l])
                    # print("{}, {} = {}".format(course[i][k], course[j][l], jaccard_sum))
            prof_course_similarity = []
            prof_course_similarity.append(professor[i])
            prof_course_similarity.append(professor[j])
            prof_course_similarity.append(jaccard_sum)
            prof_course.append(prof_course_similarity)
            # print("{}, {} = {}".format(professor[i], professor[j], jaccard_sum))

    # Referred from https://stackoverflow.com/questions/39748916/find-maximum-value-and-index-in-a-python-list
    # Selecting the 2 professors having maximum similarity between their courses
    n = max(prof_course, key=lambda item: item[2])
    print("The professors with the most aligned teaching interests are Prof. {} and Prof. {}\n".format(n[0], n[1]))

def main(*args):
    if len(args) != 2:
        print("Incorrect arguments. Please pass the name of a cleaned file and the name of a professor")
        sys.exit()
    
    file_name = args[0]
    professor_name_p = args[1]

    similarity_threshold = 0.8

    count_courses(file_name, similarity_threshold)
    list_course(file_name, professor_name_p)
    find_common_interests(file_name)

if __name__ == "__main__": main(*sys.argv[1:])
