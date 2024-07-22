
#store and return project list location
def project_name():
    file_location = "C:\\Users\\Tyler\\Documents\\Audio exports\\Zig Zag"
    txttitle = "Project List.txt"
    filepath = file_location + "\\" + txttitle
    return filepath

#parse file into a list of tuples
def read_file_lines(path_to_file):
    with open(path_to_file, "r") as f:
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
        val_string = row[2].strip('"')
        if val_string == str(bpm_val):
            query += [row]

    return query

def main():
    filename = project_name()
    full_list = read_file_lines(filename)
    
    # print as table

    col_name = full_list[0]
    print(col_name[0], col_name[1], col_name[2])
    data_rows = full_list[1:]
    for item in data_rows:
        print(item[0], item[1], item[2])

        
    print("all 130 songs:")
    oneTHIRTYquery = find_bpm(data_rows, 130)

    for row in oneTHIRTYquery:
        print(row)

    
    return

if __name__ == "__main__":
    main()
