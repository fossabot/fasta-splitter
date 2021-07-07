import sys


def get_sequences_prefix_path_from_ncbi_sequences_file(ncbi_sequences_file: str):
    sequences_prefix_path = ""
    sequences_file_path_split = ncbi_sequences_file.rsplit("/", 1)
    if len(sequences_file_path_split) > 1:
        sequences_prefix_path = sequences_file_path_split[0] + "/"
    return sequences_prefix_path


def get_sequences_name_list_from_ncbi_sequences_file(ncbi_sequences_file: str):
    sequences_name_list = []
    with open(ncbi_sequences_file, mode="r") as ncbi_sequences_file:
        for line in ncbi_sequences_file:
            line = line.strip()
            if ">" in line:
                sequence_name = line.split(" ")[0].replace(">", "")
                sequences_name_list.append(sequence_name)
    print("Sequences Name List Length: {0}".format(str(len(sequences_name_list))))
    return sequences_name_list


def get_sequences_data_list_from_ncbi_sequences_file(ncbi_sequences_file: str):
    sequences_start_token = ">"
    sequences_data_list = []
    current_sequence_data = []
    with open(ncbi_sequences_file, mode="r") as ncbi_sequences_file:
        for line in ncbi_sequences_file:
            line = line.strip()
            if line.startswith(sequences_start_token) and current_sequence_data:
                sequences_data_list.append(current_sequence_data[:])
                current_sequence_data = []
            current_sequence_data.append(line)
        sequences_data_list.append(current_sequence_data)
    print("Sequences Data List Length: {0}".format(str(len(sequences_data_list))))
    return sequences_data_list


def write_sequences_fasta_files_from_sequences_lists(sequences_prefix_path: str,
                                                     sequences_name_list: list,
                                                     sequences_data_list: list):
    wrote_sequences_fasta_files_count = 0
    for index_name in range(len(sequences_name_list)):
        sequence_name = sequences_name_list[index_name]
        sequence_file_name = sequences_prefix_path + sequence_name + ".fasta"
        with open(sequence_file_name, mode="w") as sequence_file:
            sequence_data = sequences_data_list[index_name]
            for index_data in range(len(sequence_data)):
                sequence_file.write(sequence_data[index_data] + "\n")
        wrote_sequences_fasta_files_count = wrote_sequences_fasta_files_count + 1
    print("Wrote {0} Sequences Fasta Files.".format(str(wrote_sequences_fasta_files_count)))


def write_sequences_fasta_files_index_list_text_file(sequences_prefix_path: str, sequences_name_list: list):
    sequences_list_file_name = sequences_prefix_path.rsplit('/', 1)[0] + "_Sequences_List.txt"
    sequences_fasta_files_index_count = 0
    with open(sequences_list_file_name, mode="w") as sequences_list_file:
        for index_name in range(len(sequences_name_list)):
            sequence_name = sequences_name_list[index_name]
            sequence_file_name = sequences_prefix_path + sequence_name + ".fasta"
            sequences_list_file.write(sequence_file_name + "\n")
            sequences_fasta_files_index_count = sequences_fasta_files_index_count + 1
    print("{0}'s Index Contains {1} Sequences Fasta Files.".format(str(sequences_list_file_name),
                                                                   str(sequences_fasta_files_index_count)))


def main():
    # BEGIN
    if len(sys.argv) != 2:
        raise ValueError("Wrong number of arguments...")

    # GET NCBI SEQUENCES FILE PATH ARGUMENT
    ncbi_sequences_file = sys.argv[1]

    # READ NCBI SEQUENCES FILE AND GET SEQUENCES NAME LIST
    sequences_name_list = get_sequences_name_list_from_ncbi_sequences_file(ncbi_sequences_file)

    # READ NCBI SEQUENCES FILE AND GET SEQUENCES DATA LIST
    sequences_data_list = get_sequences_data_list_from_ncbi_sequences_file(ncbi_sequences_file)

    # GET SEQUENCES PREFIX PATH
    sequences_prefix_path = get_sequences_prefix_path_from_ncbi_sequences_file(ncbi_sequences_file)

    # WRITE SEQUENCES FASTA FILES (SPLITTING ORIGINAL NCBI SEQUENCES FILE INTO INDIVIDUAL SEQUENCES FILES)
    write_sequences_fasta_files_from_sequences_lists(sequences_prefix_path, sequences_name_list, sequences_data_list)

    # WRITE SEQUENCES FASTA FILES INDEX LIST (INDEX OF INDIVIDUAL SEQUENCES FILES)
    write_sequences_fasta_files_index_list_text_file(sequences_prefix_path, sequences_name_list)

    # END
    sys.exit()


if __name__ == "__main__":
    main()
