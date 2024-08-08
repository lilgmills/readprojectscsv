from random import choice
import json

#store and return project list location
def project_name(txttitle):
    file_location = "C:\\Users\\Tyler\\Documents\\Audio exports\\Zig Zag"
    filepath = file_location + "\\" + txttitle
    return filepath

def write_to_txt_file(mem_table):
    file_location = "C:\\Users\\Tyler\\Documents\\Audio exports\\Zig Zag"
    txttitle = "Indexed Project List.txt"
    filepath = file_location + "\\" + txttitle
    
    with open(filepath, "w+") as f:
        for row in mem_table:
            formatrow = ""
            for row_element in row:
                formatrow += str(row_element)
                formatrow+=","
            f.write(formatrow + '\n')

        print(f.read())
    return

def ignore_newlines_and_commas(list_of_textlines):
    formattedlist = []
    for row in list_of_textlines:
        if row != "" and row != "\n":
            #ignore newline
            row = row.strip("\n")
            #ignore terminal comma, if it exists
            if row[-1] == ",":
                row = row[:-1]

            formattedlist += [row]
        
    return formattedlist

def strip_quotes(text_entry):
    if not text_entry:
        # empty string
        return text_entry

    elif text_entry[0] == '\"' and text_entry[-1] == '\"':
        text_entry_stripped = text_entry[1:-1]
    else:
        return text_entry
    return text_entry_stripped

#parse file into a list of lists for csv row entries
def read_file_lines(path_to_file):
    
    with open(path_to_file, "r") as f:
        list_of_rows = f.readlines()
        format_rowlist = ignore_newlines_and_commas(list_of_rows)
        
    listed_row_values = [line.split(",") for line in format_rowlist]
    table_rows = []
    for value in listed_row_values:
        new_row = [strip_quotes(entry) for entry in value]        
        table_rows += [new_row]

    return table_rows
    
def find_bpm(data, bpm_val):
    query = []
    for row in data:
        # row[2] is bpm string, remove its double quote formatting
        # save as val_string
        val_string = row[2].strip('"')
        if val_string == str(bpm_val):
            query += [row]

    return query

def remove_title_row(table):
    data_rows = table[1:]

    return data_rows

def title_row(table):
    return table[0]

def print_row_format(data_row):
    # put elements of data_row (which is a list) into a string and print
    formatrow = ""
    for row_element in data_row:
        formatrow += str(row_element)
        formatrow+=","

    print(formatrow)
    

def print_data_rows(table):

    data_rows = remove_title_row(table)
    
    for row in data_rows:
        print_row_format(row)
    
    

def print_with_titles(table):
    print_row_format(title_row(table))
    print_data_rows(table)

    return
    

def create_new_indexed_table(table):

    

    data_rows = []
    for idx in range(len(table)):
        if idx != 0:
            data_rows += [[idx] + table[idx] ]
        else:
            data_rows += [["index"] + table[idx] ]
    return data_rows

def index_column_index(table):
    titles = title_row(table)
    idx_col = None
    for col_num,col in enumerate(titles):
        if col == "index":
            if not idx_col:
                idx_col = col_num
            else:
                print("Error: there is more than one \"index\" column")
    
    return idx_col

def title_column_index(table):
    titles = title_row(table)
    title_col = None
    for col_num,col in enumerate(titles):
        if col == "title":
            if not title_col:
                title_col = col_num
            else:
                print("Error: there is more than one \"title\" column")
    
    return title_col

def create_comparison_pairs(table):    
    # takes an in-memory table: a list of lists of row entries, with an initial row of titles
    # find which column is the index column (named "index" in the title row)
    idx_col = index_column_index(table)

    data_table = remove_title_row(table)
    index_pairs = []
    for i, row1 in enumerate(data_table):
        # start enumerating from i + 1 so we do not get 
        #     duplicates (self-comparison) inside the pair
        for j, row2 in enumerate(data_table[i+1:]):
            index_pairs += [(row1[idx_col], row2[idx_col])]


    return index_pairs

def interactive_comparison(serialized_file):
    better_than_partition = json.load(serialized_file)
    # if project list has more indices than the json file, we need to add them
    # if comparisons.json has indices that have been removed from the project list,
    #     we need to discard them
    # I don't know how to do all that yet
    # Problem: If list changes, the indices change. Should have an option to reset manually?

def target_row(table, target_idx):
    row_idx = None
    index_col = index_column_index(table)
    for row_num, row in enumerate(table):
        
        if row[index_col] == str(target_idx):
            if not row_idx:
                row_idx = row_num
            else:
                print("Error: there is more than one {} index".format(target_idx))
    if row_idx is None:
        print("There is not a {} index".format(target_idx))
        return
    return row_idx
    
    

class ComparisonTable():
    def __init__(self, indexed_table):
        self.title_row = ["index","comparisons"]
        self.data_rows = self.initialize_comparison(indexed_table)
        self.index_list = self.get_all_indices(self.data_rows)
        # if comparisons are already stored in a file, we want to load those as well
        # # which could potentially be a complicated merge operation between the project list and the existing comparisons

        # for every index in project list:
        # case 1: index is also in comparisons -> case 1a. the "foreign key" index refers to the same project. no merge issue
        # case 1: index is also in comparisons -> case 1b. the foreign key index refers to a different project. !!merge issue!! 
        # case 2: index is not in comparisons -> !!merge issue!!

        # for every index in comparisons list:
        # case 1: index is also in project list -> case 1a. the "primary key" index refers to the same project. no merge issue
        # case 1: index is also in project list -> case 1b. the primary key index refers to a different project. !!merge issue!! 
        # case 2: index is not in project list -> !!merge issue!!
                        
    def initialize_comparison(self, table):
        # take the column that has all the indicies from indexed table, and initialize new comparisons
        index_column = []
        # it's a little crazy that I'm not using a class-native method to find this index column index. Refactor please!
        idx_col = index_column_index(table)
        data_rows = remove_title_row(table)
        for row in data_rows:
            index_column.append(row[idx_col])

        comparison_data = [[int(index_column[i]),[]] for i in range(len(data_rows))]
        return comparison_data
    
    def get_all_indices(self, data_rows):
        all_indices = []
        idx_col = self.column_num("index")
        for row in data_rows:
            all_indices.append(row[idx_col])

        return all_indices

    
    #returns the index of the given column title
    def column_num(self, col_name):
        col_idx = None
        for col_num, title in enumerate(self.title_row):
            if col_name == title:
                if not col_idx:
                    col_idx = col_num
                else:
                    print("Error: there is more than one {} column".format(col_name))

        if col_idx is None:
            print("There is no {} column".format(col_name))
            return
        return col_idx

    # returns the data_row list index of the given record index    
    def row_num(self, target_idx):
        row_idx = None
        index_col = self.column_num("index")
        for row_num, row in enumerate(self.data_rows):
            
            if row[index_col] == target_idx:
                if not row_idx:
                    row_idx = row_num
                else:
                    print("Error: there is more than one {} index".format(target_idx))
        if row_idx is None:
            print("There is not a {} index".format(target_idx))
            return
        return row_idx
    
    def check_index_exists(self, index):
        list_of_indices = [row[self.column_num("index")] for row in self.data_rows]
        exists_val = index in list_of_indices
        return exists_val

    def insert_comparison(self, index1, index2):
        # go to table row for index1
        if index1 == index2:
            print("Error: self-comparison on {}".format(index1))
            return
        if not self.check_index_exists(index2):
            print("{} is not a valid index".format(index2))
            return
        comparison_record = self.data_rows[self.row_num(index1)]
        comparisons_col = self.column_num("comparisons")
        comparisons = comparison_record[comparisons_col]
        if index2 not in comparisons:
            comparison_record[comparisons_col].append(index2)
        return

    def wrap_quotes(self, entry):
        if entry == []:
            return "\"\""
        else: return "\"{}\"".format(str(entry))
    
    def wrap_row_entries(self, row):
        return [self.wrap_quotes(entry) for entry in row]

    def __str__(self):
        titles_wrapped = self.wrap_row_entries(self.title_row)
        title_string = ",".join(titles_wrapped)
        string_self = title_string + ",\n"
        index_col = self.column_num("index")
        comp_col = self.column_num("comparisons")
        for row in self.data_rows:
            csv_comparisons = ",".join([str(entry) for entry in row[comp_col]])
            string_self += self.wrap_quotes(row[index_col])
            string_self +=","
            string_self += self.wrap_quotes(csv_comparisons)
            string_self +=",\n"
            
            
        return string_self
    
    def comparison_pair(self):
        # not worth overthinking. just choose 2 indices that aren't the same. a small chance this will require re-samples but who cares, runs in O(1) worst case either way
        index1 = choice(self.index_list)
        index2 = index1
        while index2 == index1:
            index2 = choice(self.index_list)

        return (index1, index2)
    
    def title(self, index, primary_table):
        title_col = title_column_index(primary_table)
        index_row = target_row(primary_table, index)

        
        return primary_table[index_row][title_col]
        

    
    def run_interactive_comparison(self, primary_table):
        idx_pair = self.comparison_pair()
        comp1 = idx_pair[0]
        comp2 = idx_pair[1]
        title1 = self.title(comp1, primary_table)
        title2 = self.title(comp2, primary_table)
        print(title1)
        print(title2)
        get_input = None
        while (get_input != "1" and get_input != "2"):
            get_input = input("Which song is better?\n>")

            if (get_input != "1" and get_input != "2"):
                print("error: Type a 1 or a 2\n")


        if get_input == "1":
            self.insert_comparison(comp1, comp2)
        elif get_input == "2":
            self.insert_comparison(comp2, comp1)

        return



            




    
def main():
    filename = project_name("The Short List.txt")
    
    indexed_table = read_file_lines(filename)

    print_with_titles(indexed_table)

    comparison_object = ComparisonTable(indexed_table)

    print(comparison_object)
    
    for i in range(3):
        comparison_object.run_interactive_comparison(indexed_table)

    print(comparison_object)

    # comparison_idxs = create_comparison_pairs(indexed_table)

##    interactive_comparison('index_comparisons.json')
##    
##
##    for i in range(3):
##        random_index_pair = choice(comparison_idxs)
##        pair_first = random_index_pair[0]
##        pair_second = random_index_pair[1]
##        title_col = 2
##        print(indexed_table[pair_first][title_col])
##        print(indexed_table[pair_second][title_col])
##
##        get_input = None
##        while (get_input != "1" and get_input != "2"):
##            get_input = input("Which song is better? Type a 1 or a 2\n")
##        
##        if get_input == "1":
##            if pair_first not in better_than_partition.keys():
##                better_than_partition[pair_first] = set()       
##            better_than_partition[pair_first].add(pair_second)
##        else:
##            if pair_second not in better_than_partition.keys():
##                better_than_partition[pair_second] = set()       
##            better_than_partition[pair_second].add(pair_first)
##
##    for k in better_than_partition.keys():
##        print(indexed_table[k][title_col], "is better than:")
##        print([indexed_table[x][title_col] for x in better_than_partition[k]])
    
        
    
    return

if __name__ == "__main__":
    main()
