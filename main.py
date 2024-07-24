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
    if text_entry[0] == '\"' and text_entry[-1] == '\"':
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

def create_comparison_pairs(table):    

    # find which column is the index column (named "index" in the title row)
    titles = title_row(table)
    for col_num,col in enumerate(titles):
        if col == "index":
            idx_col = col_num

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
    
    
                
            
    
def main():
    filename = project_name("Indexed Project List.txt")
    
    indexed_table = read_file_lines(filename)

    print_with_titles(indexed_table)
    
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
