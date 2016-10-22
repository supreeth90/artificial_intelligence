import sys
import os.path
from pprint import pprint
import copy
from operator import itemgetter

class WeddingPlanner:


    def __init__(self, friends_file, seats_per_table):
        self.friends_file = friends_file
        self.seats_per_table = seats_per_table
        self.friends_map = dict()
        self.persons_list = []
        self.generated_tables = []
        self.least_tables = None
        self.read_friends_file()
        print("Printing Friends graph")
        # pprint(self.friends_map)
        self.solve()


    def read_friends_file(self):

        if not os.path.exists(self.friends_file):
            return False

        with open(self.friends_file) as f:
            for friends_line in f.readlines():
                friends_line = friends_line.strip('\n')
                person = friends_line.split(" ")[0]
                if person not in self.friends_map.keys():
                    self.friends_map[person] = []
                for friend in friends_line.split(" ")[1:]:
                    self.add_friend_to_person(person, friend)
                    self.add_friend_to_person(friend, person)

            for person in self.friends_map:
                self.persons_list.append(person)

    def add_friend_to_person(self, person, friend):
        if person not in self.friends_map:
            self.friends_map[person] = []

        friends_list = self.friends_map[person]
        for friend_person in friends_list:
            if friend_person == friend:
                return
        self.friends_map[person].append(friend)
        return

    def is_goal(self, tables):
        if self.has_all_persons(tables):
            if self.least_tables:
                if len(tables) < len(self.least_tables):
                    self.least_tables = tables
            else:
                self.least_tables = tables
            return True
        return False

    def has_all_persons(self, tables):
        all_persons_dict = dict()
        for person in self.persons_list:
            all_persons_dict[person] = 0

        for table in tables:
            for person in table:
                all_persons_dict[person] = 1

        for person in all_persons_dict:
            if all_persons_dict[person] == 0:
                return False
        return True

    def is_friend(self, current_person, new_person):
        for person in self.friends_map[current_person]:
            if person == new_person:
                return True
        return False

    def is_person_exists(self, person, tables):
        for table in tables:
            for cur_person in table:
                if cur_person == person:
                    return True
        return False

    def add_person(self, person, tables):
        new_tables = copy.deepcopy(tables)
        if not self.is_person_exists(person, tables):
            for table in new_tables:
                if len(table) >= int(self.seats_per_table):
                    continue
                for current_person in table:
                    # Eliminate all persons which doesn't meet these criteria
                    # they cannot sit together
                    if not self.is_friend(current_person, person):
                        table.append(person)
                        table = self.sort_table(table)
                        return self.sort_tables(new_tables), True

            # person has to placed in a new table
            new_tables.append([person])
            new_tables = sorted(new_tables, key=itemgetter(0))
            return new_tables, True
        else:
            return new_tables, False

    # This needs to be optimized
    def check_generated_states(self, new_tables):
        table_valid_flag = True
        for tables in self.generated_tables:

            # Compare sizes
            if len(new_tables) == len(tables):
                for i in range(0, len(new_tables)):
                    if not table_valid_flag:
                        table_valid_flag = True
                        break
                    table = tables[i]
                    new_table = new_tables[i]

                    if len(table) == len(new_table):
                        for j in range(0, len(new_table)):
                            if table[j] != new_table[j]:
                                table_valid_flag = False
                                break

                if i == len(new_tables):
                    return True
        return False



    def sort_table(self, table):
        return list.sort(table)

    def sort_tables(self, tables):
        return sorted(tables, key=itemgetter(0))

    def successors(self, tables):
        new_tables_list = []
        for i in range(0, len(self.persons_list)):
            new_tables, added_bool = self.add_person(self.persons_list[i], tables)
            if added_bool and not self.check_generated_states(new_tables):
                self.generated_tables.append(new_tables)
                new_tables_list.append(new_tables)
        return new_tables_list


    def solve(self):
        tables = []
        fringe = [tables]
        while len(fringe) > 0:
            for s in self.successors(fringe.pop()):
                if self.is_goal(s):
                    continue
                    # return (s)
                fringe.append(s)
        pprint(self.least_tables)

if len(sys.argv) == 3:
    friends_file = sys.argv[1]
    seats_per_table = sys.argv[2]
    WeddingPlanner(friends_file, seats_per_table)
else:
    print("Usage: python wedding.py [friends-file] [seats-per-table]")





