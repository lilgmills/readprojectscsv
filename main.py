
#store and return project list location
def project_name():
    file_location = "C:\\Users\\Tyler\\Documents\\Audio exports\\Zig Zag"
    txttitle = "Project List.txt"
    filepath = file_location + "\\" + txttitle
    return filepath

#parse file into a list of tuples
def read_file_lines(path_to_file):
    with open(path_to_file, "r") as f:
        # line[:-1] used here to stop before newline while reading
        list_of_entries = [line[:-1] for line in f]

    
    values = [line.split(",") for line in list_of_entries]
    tuples_list = []
    for line in values:
        new_tuple = (line[0], line[1], line[2])        
        tuples_list += [new_tuple]

    return tuples_list
    
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
        formatrow += row_element
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
    

def create_indexkeys(table):
    indexed_rows = {}
    for i in range(len(table)):
        indexed_rows[i] = table[i]

    return indexed_rows

def create_new_indexed_table(keys_dict):
    data_rows = [[str(idx)] + list(keys_dict[idx]) for idx in keys_dict.keys()]
    
    return data_rows
    
def main():
    filename = project_name()
    
    full_list = read_file_lines(filename)

    index_keys_dicts = create_indexkeys(full_list)

    indexed_table = create_new_indexed_table(index_keys_dicts)

    print_with_titles(indexed_table)
    
    return

if __name__ == "__main__":
    main()
