'''
Problem 3 - Wedding Planner
(A) Abstraction:
  * State space - Set of tables with any combinations of persons
  * the successor function - generates a set of states where a person is added into the current state into one of the
    current tables or a new table
  * goal state - goal state is reached when the given state has all the person attending the wedding
  * initial state - A state with a single table and a single person
  * cost function - F() = G(), where G() is the number of tables currently used
  * Search Algorithm: A* search

(B) How The Search Algorithm Works:
    Initially it starts by placing single person in a single table to the fringe. Then, as long as there are states
    in the fringe, repeats: generates successors of a low priority fringe element and for each of this success state
    check if the goal has reached and return the tables, else add this state to the fringe and continue.

(C) Successor Function:
    Successor Function tries to generate states by adding a person in different combinations so as to it doesn't
    violate the friendship property. Another optimization it does is to put the persons with more number of friends
    in the beginning to quickly ramp up the total number of tables to the optimal number of tables.

(D) Design and assumptions:
    This search guarantees 100% optimal solution(minimum number of tables).

(E) Other Designs tried:
    Design 1:Tried to implement another version of the code which does BFS or DFS, and starts by generating states from
    the beginning(empty tables and empty person). It generates all the combinations by placing the persons in
    different tables in different orders, which guarantees 100% optimal solution but runs much slower.
    Design 2: Initially it starts by placing all the persons in a single table to the fringe. Then, as long as there are states
    in the fringe, repeats: generates successors of a high priority fringe element and for each of this success state check
    if the goal has reached and return the tables, else add this state to the fringe and continue.

'''
import sys
import os.path
import copy
import heapq
import time


class WeddingPlanner:

    def __init__(self, friends_file, seats_per_table):
        self.friends_file = friends_file
        self.seats_per_table = int(seats_per_table)
        self.friends_map = dict()
        self.persons_list = []
        self.generated_tables = []
        self.least_tables = None
        self.read_friends_file()
        start_time = time.clock()
        self.solve()
        print("Time:", time.clock() - start_time)
        self.print_output(self.least_tables)

    def print_output(self, tables):
        output_string = str(len(tables))+" "
        for table in tables:
            for p_index, person in enumerate(table):
                output_string += person
                if p_index < len(table)-1:
                    output_string += ","
            output_string += " "
        print(output_string)

    def read_friends_file(self):

        if not os.path.exists(self.friends_file):
            return False
        with open(self.friends_file) as f:
            for friends_line in f.readlines():
                friends_line = friends_line.strip('\n')
                person = friends_line.split(" ")[0]
                if person not in self.friends_map.keys():
                    self.friends_map[person] = set()
                for friend in friends_line.split(" ")[1:]:
                    self.add_friend_to_person(person, friend)
                    self.add_friend_to_person(friend, person)

            friends_pr_queue = PriorityQueue()
            for person in self.friends_map:
                friends_pr_queue.push(person, -len(self.friends_map[person]))
            while(len(friends_pr_queue) > 0):
                self.persons_list.append(friends_pr_queue.pop())

    def add_friend_to_person(self, person, friend):
        if person not in self.friends_map:
            self.friends_map[person] = set()

        friends_list = self.friends_map[person]
        for friend_person in friends_list:
            if friend_person == friend:
                return
        self.friends_map[person].add(friend)
        return

    def is_goal(self, tables, num_of_persons):
        if num_of_persons == len(self.persons_list):
            self.least_tables = tables
            return True
        return False

    def is_friend(self, current_person, new_person):
        if new_person in self.friends_map[current_person]:
            return True
        return False

    def has_no_friends(self, table, person):
        for cur_person in table:
            if person != cur_person and self.is_friend(person, cur_person):
                return False
        return True

    def add_person(self, tables, person):
        new_tables_list = []
        for table_index, table in enumerate(tables):
            if len(table) < self.seats_per_table:
                if self.has_no_friends(table, person):
                    new_tables = copy.deepcopy(tables)
                    new_tables[table_index].add(person)
                    new_tables_list.append(new_tables)
        new_tables = copy.deepcopy(tables)
        new_table_set = set()
        new_table_set.add(person)
        new_tables.append(new_table_set)
        new_tables_list.append(new_tables)
        return new_tables_list

    def solve(self):
        fringe = PriorityQueue()
        table = set()
        table.add(self.persons_list[0])
        tables = [table]
        fringe.push((tables, 1), 1)
        while len(fringe) > 0:
            tables_tuple = fringe.pop()
            for s in self.add_person(tables_tuple[0], self.persons_list[tables_tuple[1]]):
                if self.is_goal(s, tables_tuple[1]+1):
                    return True
                fringe.push((s, tables_tuple[1]+1), len(s))

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def __len__(self):
        return len(self._queue)

    def push(self, item, priority):
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]

if len(sys.argv) == 3:
    friends_file = sys.argv[1]
    seats_per_table = sys.argv[2]
    WeddingPlanner(friends_file, seats_per_table)
else:
    print("Usage: python wedding.py [friends-file] [seats-per-table]")





