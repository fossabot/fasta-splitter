from pathlib import Path
import fastasplitter.exceptions
import sys


def check_if_is_valid_number_of_arguments(number_of_arguments_provided: int):
    if number_of_arguments_provided != 2:
        invalid_number_of_arguments_message = "Invalid Number of Arguments Provided! \n" \
                                              "Expected: 1 Argument (FASTA Sequences File). \n" \
                                              "Provided: {0} Argument(s).".format(number_of_arguments_provided - 1)
        raise fastasplitter.exceptions.InvalidNumberofArgumentsError(invalid_number_of_arguments_message)


def check_if_sequences_file_exists(sequences_file_path: Path):
    if not sequences_file_path.is_file():
        file_not_found_message = "FASTA Sequences File not Found!"
        raise FileNotFoundError(file_not_found_message)


def get_sequences_file_extension(sequences_file_path: Path):
    return sequences_file_path.suffix


def check_if_sequences_file_has_fasta_extension(sequences_file_path: Path):
    if get_sequences_file_extension(sequences_file_path) not in [".fa", ".faa", ".fasta", ".ffn", ".fna", ".frn"]:
        invalid_format_file_message = "Only FASTA Extension Files (.fa, .faa, .fasta, .ffn, .fna or .frn) are Allowed!"
        raise fastasplitter.exceptions.InvalidExtensionFileError(invalid_format_file_message)


def parse_description_line(line: str,
                           sequences_start_token: str,
                           description_lines_count: int):
    if line.startswith(sequences_start_token):
        description_lines_count = description_lines_count + 1
    return description_lines_count


def parse_invalid_description_line(line: str,
                                   sequences_start_token: str,
                                   invalid_description_lines_count: int):
    if line.startswith(sequences_start_token) and line.split(" ", 1)[0] == sequences_start_token:
        invalid_description_lines_count = invalid_description_lines_count + 1
    return invalid_description_lines_count


def parse_sequences_file_line(line: str,
                              description_lines_count: int,
                              invalid_description_lines_count: int,
                              lines_count: int):
    sequences_start_token = ">"
    description_lines_count = parse_description_line(line,
                                                     sequences_start_token,
                                                     description_lines_count)
    invalid_description_lines_count = parse_invalid_description_line(line,
                                                                     sequences_start_token,
                                                                     invalid_description_lines_count)
    lines_count = lines_count + 1
    return description_lines_count, invalid_description_lines_count, lines_count


def get_sequences_file_counters(sequences_file_path: Path):
    description_lines_count = 0
    invalid_description_lines_count = 0
    lines_count = 0
    with open(sequences_file_path, mode="r") as sequences_file:
        for line in sequences_file:
            description_lines_count, invalid_description_lines_count, lines_count = \
                parse_sequences_file_line(line,
                                          description_lines_count,
                                          invalid_description_lines_count,
                                          lines_count)
    return description_lines_count, invalid_description_lines_count, lines_count


def check_if_sequences_file_has_any_description_line(sequences_file_path: Path,
                                                     description_lines_count: int):
    if description_lines_count == 0:
        invalid_formatted_fasta_file_message = "'{0}' Has Not Any Description Line!" \
            .format(str(sequences_file_path))
        raise fastasplitter.exceptions.InvalidFormattedFastaFileError(invalid_formatted_fasta_file_message)


def check_if_sequences_file_has_any_invalid_description_line(sequences_file_path: Path,
                                                             invalid_description_lines_count: int):
    if invalid_description_lines_count != 0:
        invalid_formatted_fasta_file_message = "'{0}' Contains {1} Line(s) With Invalid Description Format!" \
            .format(str(sequences_file_path), str(invalid_description_lines_count))
        raise fastasplitter.exceptions.InvalidFormattedFastaFileError(invalid_formatted_fasta_file_message)


def check_if_sequences_file_has_no_data(sequences_file_path: Path,
                                        lines_count: int):
    if lines_count < 2:
        invalid_formatted_fasta_file_message = "'{0}' Seems a Empty Fasta File!".format(str(sequences_file_path))
        raise fastasplitter.exceptions.InvalidFormattedFastaFileError(invalid_formatted_fasta_file_message)


def check_if_is_valid_fasta_sequences_file(sequences_file_path: Path):
    check_if_sequences_file_exists(sequences_file_path)
    check_if_sequences_file_has_fasta_extension(sequences_file_path)
    description_lines_count, invalid_description_lines_count, lines_count = \
        get_sequences_file_counters(sequences_file_path)
    check_if_sequences_file_has_any_description_line(sequences_file_path, description_lines_count)
    check_if_sequences_file_has_any_invalid_description_line(sequences_file_path, invalid_description_lines_count)
    check_if_sequences_file_has_no_data(sequences_file_path, lines_count)


def get_sequences_file_path_parents(sequences_file_path: Path):
    return Path(sequences_file_path.parents[0])


def get_sequences_file_path_parents_underscored(sequences_file_path_parents: Path):
    sequences_file_path_parents_underscored = str(sequences_file_path_parents) \
        .replace("/", "_").replace("\\", "_").replace(".", "")
    return sequences_file_path_parents_underscored


def get_sequences_name_list(sequences_file_path: Path):
    sequences_start_token = ">"
    sequences_name_list = []
    with open(sequences_file_path, mode="r") as fasta_sequences_file:
        for line in fasta_sequences_file:
            line = line.strip()
            if line.startswith(sequences_start_token):
                sequence_name = line.split("|", 1)[0].replace(sequences_start_token, "").replace(" ", "")
                sequences_name_list.append(sequence_name)
    return sequences_name_list


def get_sequences_data_list(sequences_file_path: Path):
    sequences_start_token = ">"
    sequences_data_list = []
    current_sequence_data = []
    with open(sequences_file_path, mode="r") as sequences_file:
        for line in sequences_file:
            line = line.strip()
            if line.startswith(sequences_start_token) and current_sequence_data:
                sequences_data_list.append(current_sequence_data[:])
                current_sequence_data = []
            current_sequence_data.append(line)
        sequences_data_list.append(current_sequence_data)
    return sequences_data_list


def write_sequences_fasta_files_from_sequences_lists(sequences_file_path_parents: Path,
                                                     sequences_file_extension: str,
                                                     sequences_name_list: list,
                                                     sequences_data_list: list):
    wrote_sequences_fasta_files_count = 0
    for index_name in range(len(sequences_name_list)):
        sequence_file_name = sequences_name_list[index_name] + sequences_file_extension
        with open(sequences_file_path_parents.joinpath(sequence_file_name), mode="w") as sequence_file:
            sequence_data = sequences_data_list[index_name]
            for index_data in range(len(sequence_data)):
                sequence_file.write(sequence_data[index_data] + "\n")
        wrote_sequences_fasta_files_count = wrote_sequences_fasta_files_count + 1


def write_sequences_fasta_files_index_list_text_file(sequences_file_path_parents: Path,
                                                     sequences_file_extension: str,
                                                     sequences_name_list: list):
    sequences_file_path_parents_underscored = get_sequences_file_path_parents_underscored(sequences_file_path_parents)
    if len(sequences_file_path_parents_underscored) > 0:
        sequences_list_file_name = sequences_file_path_parents_underscored + "_Sequences_List.txt"
    else:
        sequences_list_file_name = "Sequences_List.txt"
    sequences_fasta_files_index_count = 0
    with open(Path(sequences_list_file_name), mode="w") as sequences_list_file:
        for index_name in range(len(sequences_name_list)):
            sequence_file_name = sequences_name_list[index_name] + sequences_file_extension
            sequences_list_file.write(str(Path(sequences_file_path_parents, sequence_file_name)) + "\n")
            sequences_fasta_files_index_count = sequences_fasta_files_index_count + 1


def main(argv: list):
    # BEGIN

    # GET NUMBER OF ARGUMENTS PROVIDED
    number_of_arguments_provided = len(argv)

    # VALIDATE NUMBER OF ARGUMENTS PROVIDED
    check_if_is_valid_number_of_arguments(number_of_arguments_provided)

    # GET SEQUENCES FILE PATH
    sequences_file_path = Path(argv[1])

    # VALIDATE SEQUENCES FILE (AS FASTA FORMATTED FILE)
    check_if_is_valid_fasta_sequences_file(sequences_file_path)

    # GET SEQUENCES FILE PATH PARENTS
    sequences_file_path_parents = get_sequences_file_path_parents(sequences_file_path)

    # GET SEQUENCES FILE EXTENSION
    sequences_file_extension = get_sequences_file_extension(sequences_file_path)

    # READ SEQUENCES FILE AND GET SEQUENCES NAME LIST
    sequences_name_list = get_sequences_name_list(sequences_file_path)

    # READ SEQUENCES FILE AND GET SEQUENCES DATA LIST
    sequences_data_list = get_sequences_data_list(sequences_file_path)

    # WRITE SEQUENCES FASTA FILES (SPLITTING ORIGINAL FASTA SEQUENCES FILE INTO INDIVIDUAL SEQUENCES FILES)
    write_sequences_fasta_files_from_sequences_lists(sequences_file_path_parents,
                                                     sequences_file_extension,
                                                     sequences_name_list,
                                                     sequences_data_list)

    # WRITE SEQUENCES FASTA FILES INDEX LIST (INDEX OF INDIVIDUAL SEQUENCES FILES)
    write_sequences_fasta_files_index_list_text_file(sequences_file_path_parents,
                                                     sequences_file_extension,
                                                     sequences_name_list)

    # END
    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv)
