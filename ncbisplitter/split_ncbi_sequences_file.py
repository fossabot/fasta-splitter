from exceptions import InvalidExtensionFileError, InvalidFormattedFastaFileError, InvalidNumberofArgumentsError
import os
import sys


def check_if_is_valid_number_of_arguments(number_of_arguments_provided: int):
    if number_of_arguments_provided != 2:
        invalid_number_of_arguments_message = "Invalid Number of Arguments Provided! \n" \
                                              "Expected: 1 Argument (NCBI Sequences File). \n" \
                                              "Provided: {0} Argument(s).".format(number_of_arguments_provided - 1)
        raise InvalidNumberofArgumentsError(invalid_number_of_arguments_message)


def check_if_is_valid_sequences_file(ncbi_sequences_file: str):
    if not os.path.isfile(ncbi_sequences_file):
        file_not_found_message = "NCBI Sequences File not Found!"
        raise FileNotFoundError(file_not_found_message)
    if ncbi_sequences_file.rsplit(".", 1)[1] != "fasta":
        invalid_format_file_message = "Only FASTA Extension Files (.fasta) are Allowed!"
        raise InvalidExtensionFileError(invalid_format_file_message)
    header_lines_count = 0
    invalid_header_lines_count = 0
    lines_count = 0
    sequences_start_token = ">"
    with open(ncbi_sequences_file, mode="r") as sequences_file:
        for line in sequences_file:
            if line.startswith(sequences_start_token):
                header_lines_count = header_lines_count + 1
            if line.startswith(sequences_start_token) and line.split(" ", 1)[0] == sequences_start_token:
                invalid_header_lines_count = invalid_header_lines_count + 1
            lines_count = lines_count + 1
    if header_lines_count == 0:
        invalid_formatted_fasta_file_message = "'{0}' Has Not Any Description Line!".format(str(ncbi_sequences_file))
        raise InvalidFormattedFastaFileError(invalid_formatted_fasta_file_message)
    if invalid_header_lines_count != 0:
        invalid_formatted_fasta_file_message = "'{0}' Contains {1} Line(s) With Invalid Description Format!" \
            .format(str(ncbi_sequences_file), str(invalid_header_lines_count))
        raise InvalidFormattedFastaFileError(invalid_formatted_fasta_file_message)
    if lines_count < 2:
        invalid_formatted_fasta_file_message = "'{0}' Seems a Empty Fasta File!".format(str(ncbi_sequences_file))
        raise InvalidFormattedFastaFileError(invalid_formatted_fasta_file_message)


def get_sequences_prefix_path_from_ncbi_sequences_file(ncbi_sequences_file: str):
    sequences_prefix_path = ""
    sequences_file_path_split = ncbi_sequences_file.rsplit("/", 1)
    if len(sequences_file_path_split) > 1:
        sequences_prefix_path = sequences_file_path_split[0] + "/"
    return sequences_prefix_path


def get_sequences_name_list_from_ncbi_sequences_file(ncbi_sequences_file: str):
    sequences_start_token = ">"
    sequences_name_list = []
    with open(ncbi_sequences_file, mode="r") as ncbi_sequences_file:
        for line in ncbi_sequences_file:
            line = line.strip()
            if line.startswith(sequences_start_token):
                sequence_name = line.split("|", 1)[0].replace(sequences_start_token, "").replace(" ", "")
                sequences_name_list.append(sequence_name)
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


def write_sequences_fasta_files_index_list_text_file(sequences_prefix_path: str, sequences_name_list: list):
    sequences_prefix_path = sequences_prefix_path.rsplit("/", 1)[0]
    if len(sequences_prefix_path) > 0:
        sequences_list_file_name = sequences_prefix_path + "_Sequences_List.txt"
        sequences_prefix_path = sequences_prefix_path + "/"
    else:
        sequences_list_file_name = "Sequences_List.txt"
    sequences_fasta_files_index_count = 0
    with open(sequences_list_file_name, mode="w") as sequences_list_file:
        for index_name in range(len(sequences_name_list)):
            sequence_name = sequences_name_list[index_name]
            sequence_file_name = sequences_prefix_path + sequence_name + ".fasta"
            sequences_list_file.write(sequence_file_name + "\n")
            sequences_fasta_files_index_count = sequences_fasta_files_index_count + 1


def main(argv: list):
    # BEGIN

    # GET NUMBER OF ARGUMENTS PROVIDED
    number_of_arguments_provided = len(argv)

    # VALIDATE NUMBER OF ARGUMENTS PROVIDED
    check_if_is_valid_number_of_arguments(number_of_arguments_provided)

    # GET NCBI SEQUENCES FILE
    ncbi_sequences_file = argv[1]

    # VALIDATE NCBI SEQUENCES FILE
    check_if_is_valid_sequences_file(ncbi_sequences_file)

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
    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv)
