from pathlib import Path
import fastasplitter.exceptions
import fastasplitter.split_fasta_sequences_file
import pytest
import runpy
import sys


def test_when_number_of_arguments_equals_two_then_ok():
    number_of_arguments_provided = 2
    assert fastasplitter.split_fasta_sequences_file \
           .check_if_is_valid_number_of_arguments(number_of_arguments_provided) is None


def test_when_number_of_arguments_not_equals_two_then_throws_invalid_number_of_arguments_exception():
    number_of_arguments_provided = 3
    with pytest.raises(fastasplitter.exceptions.InvalidNumberofArgumentsError) as pytest_wrapped_e:
        fastasplitter.split_fasta_sequences_file.check_if_is_valid_number_of_arguments(number_of_arguments_provided)
    invalid_number_of_arguments_message = "Invalid Number of Arguments Provided! \n" \
                                          "Expected: 1 Argument (FASTA Sequences File). \n" \
                                          "Provided: {0} Argument(s).".format(number_of_arguments_provided - 1)
    assert pytest_wrapped_e.type == fastasplitter.exceptions.InvalidNumberofArgumentsError
    assert str(pytest_wrapped_e.value) == invalid_number_of_arguments_message


def test_when_sequences_file_not_exists_then_throws_file_not_found_exception():
    inexistent_sequences_file = Path("inexistent_sequences.fasta")
    with pytest.raises(FileNotFoundError) as pytest_wrapped_e:
        fastasplitter.split_fasta_sequences_file.check_if_sequences_file_exists(inexistent_sequences_file)
    file_not_found_message = "FASTA Sequences File not Found!"
    assert pytest_wrapped_e.type == FileNotFoundError
    assert str(pytest_wrapped_e.value) == file_not_found_message


def test_when_sequences_file_exists_then_return_sequences_file_extension():
    sequences_file_extension_expected = ".fasta"
    temporary_sequences_file = Path("sequences.fasta")
    with open(temporary_sequences_file, mode="w"):
        pass
    sequences_file_extension_returned = fastasplitter.split_fasta_sequences_file \
        .get_sequences_file_extension(temporary_sequences_file)
    assert sequences_file_extension_returned == sequences_file_extension_expected
    temporary_sequences_file.unlink()


def test_when_sequences_file_has_no_fasta_extension_then_throws_invalid_extension_file_exception():
    temporary_sequences_file = Path("sequences.txt")
    with open(temporary_sequences_file, mode="w"):
        pass
    with pytest.raises(fastasplitter.exceptions.InvalidExtensionFileError) as pytest_wrapped_e:
        fastasplitter.split_fasta_sequences_file.check_if_sequences_file_has_fasta_extension(temporary_sequences_file)
    invalid_format_file_message = "Only FASTA Extension Files (.fa, .faa, .fasta, .ffn, .fna or .frn) are Allowed!"
    assert pytest_wrapped_e.type == fastasplitter.exceptions.InvalidExtensionFileError
    assert str(pytest_wrapped_e.value) == invalid_format_file_message
    temporary_sequences_file.unlink()


def test_when_description_line_is_parsed_then_return_description_lines_count():
    description_line_count_expected = 1
    line = ">ValidDescription1 |text1\n"
    sequences_start_token = ">"
    description_lines_count_returned = 0
    description_lines_count_returned = fastasplitter.split_fasta_sequences_file \
        .parse_description_line(line, sequences_start_token, description_lines_count_returned)
    assert description_lines_count_returned == description_line_count_expected


def test_when_invalid_description_line_is_parsed_then_return_invalid_description_lines_count():
    invalid_description_lines_count_expected = 1
    line = "> InvalidDescription1\n"
    sequences_start_token = ">"
    invalid_description_lines_count_returned = 0
    invalid_description_lines_count_returned = fastasplitter.split_fasta_sequences_file \
        .parse_invalid_description_line(line, sequences_start_token, invalid_description_lines_count_returned)
    assert invalid_description_lines_count_returned == invalid_description_lines_count_expected


def test_when_sequences_file_is_parsed_then_return_sequences_file_counter():
    description_lines_count_expected = 2
    invalid_description_lines_count_expected = 1
    lines_count_expected = 4
    temporary_sequences_file = Path("sequences.fasta")
    with open(temporary_sequences_file, mode="w") as sequences_file:
        sequences_file.write("> InvalidDescription1\nAAA\n")
        sequences_file.write(">ValidDescription1 |text1\nCCC\n")
    description_lines_count_returned, invalid_description_lines_count_returned, lines_count_returned = \
        fastasplitter.split_fasta_sequences_file.get_sequences_file_counters(temporary_sequences_file)
    assert description_lines_count_returned == description_lines_count_expected
    assert invalid_description_lines_count_returned == invalid_description_lines_count_expected
    assert lines_count_returned == lines_count_expected
    temporary_sequences_file.unlink()


def test_when_fasta_sequences_file_has_not_any_description_line_then_throws_invalid_formatted_fasta_file_exception():
    temporary_sequences_file = Path("sequences.fasta")
    with open(temporary_sequences_file, mode="w") as sequences_file:
        sequences_file.write("AAA\n")
        sequences_file.write("CCC\n")
        sequences_file.write("GGG\n")
    description_lines_count_returned, invalid_description_lines_count_returned, lines_count_returned = \
        fastasplitter.split_fasta_sequences_file.get_sequences_file_counters(temporary_sequences_file)
    with pytest.raises(fastasplitter.exceptions.InvalidFormattedFastaFileError) as pytest_wrapped_e:
        fastasplitter.split_fasta_sequences_file \
            .check_if_sequences_file_has_any_description_line(temporary_sequences_file,
                                                              description_lines_count_returned)
    invalid_formatted_fasta_file_message = "'{0}' Has Not Any Description Line!".format(str(temporary_sequences_file))
    assert pytest_wrapped_e.type == fastasplitter.exceptions.InvalidFormattedFastaFileError
    assert str(pytest_wrapped_e.value) == invalid_formatted_fasta_file_message
    temporary_sequences_file.unlink()


def test_when_fasta_sequences_file_has_invalid_description_lines_then_throws_invalid_formatted_fasta_file_exception():
    temporary_sequences_file = Path("sequences.fasta")
    with open(temporary_sequences_file, mode="w") as sequences_file:
        sequences_file.write("> InvalidDescription1\nAAA\n")
        sequences_file.write(">ValidDescription1 |text1\nCCC\n")
        sequences_file.write(">ValidDescription2|text2\nGGG\n")
        sequences_file.write("> InvalidDescription2|text2\nTTT\n")
    description_lines_count_returned, invalid_description_lines_count_returned, lines_count_returned = \
        fastasplitter.split_fasta_sequences_file.get_sequences_file_counters(temporary_sequences_file)
    with pytest.raises(fastasplitter.exceptions.InvalidFormattedFastaFileError) as pytest_wrapped_e:
        fastasplitter.split_fasta_sequences_file \
            .check_if_sequences_file_has_any_invalid_description_line(temporary_sequences_file,
                                                                      invalid_description_lines_count_returned)
    invalid_formatted_fasta_file_message = "'{0}' Contains {1} Line(s) With Invalid Description Format!" \
        .format(str(temporary_sequences_file), str(2))
    assert pytest_wrapped_e.type == fastasplitter.exceptions.InvalidFormattedFastaFileError
    assert str(pytest_wrapped_e.value) == invalid_formatted_fasta_file_message
    temporary_sequences_file.unlink()


def test_when_fasta_sequences_file_has_no_data_then_throws_invalid_formatted_fasta_file_exception():
    temporary_sequences_file = Path("sequences.fasta")
    with open(temporary_sequences_file, mode="w") as sequences_file:
        sequences_file.write(">ValidDescription1\n")
    description_lines_count_returned, invalid_description_lines_count_returned, lines_count_returned = \
        fastasplitter.split_fasta_sequences_file.get_sequences_file_counters(temporary_sequences_file)
    with pytest.raises(fastasplitter.exceptions.InvalidFormattedFastaFileError) as pytest_wrapped_e:
        fastasplitter.split_fasta_sequences_file.check_if_sequences_file_has_no_data(temporary_sequences_file,
                                                                                     lines_count_returned)
    invalid_formatted_fasta_file_message = "'{0}' Seems a Empty Fasta File!".format(str(temporary_sequences_file))
    assert pytest_wrapped_e.type == fastasplitter.exceptions.InvalidFormattedFastaFileError
    assert str(pytest_wrapped_e.value) == invalid_formatted_fasta_file_message
    temporary_sequences_file.unlink()


def test_when_fasta_sequences_file_has_all_valid_lines_then_ok():
    temporary_sequences_file = Path("sequences.fasta")
    with open(temporary_sequences_file, mode="w") as sequences_file:
        sequences_file.write(">ValidDescription1|text1\nAAA\n")
        sequences_file.write(">ValidDescription2 |text2\nCCC\n")
        sequences_file.write(">ValidDescription3\nGGG\n")
    assert fastasplitter.split_fasta_sequences_file \
           .check_if_is_valid_fasta_sequences_file(temporary_sequences_file) is None
    temporary_sequences_file.unlink()


def test_when_fasta_sequences_file_has_no_path_parents_then_return_empty_path_parents_underscored_string():
    sequences_file_path_parents_underscored_expected = ""
    temporary_sequences_file = Path("sequences.fasta")
    with open(temporary_sequences_file, mode="w"):
        pass
    sequences_file_path_parents_returned = fastasplitter.split_fasta_sequences_file \
        .get_sequences_file_path_parents(temporary_sequences_file)
    sequences_file_path_parents_underscored_returned = fastasplitter.split_fasta_sequences_file \
        .get_sequences_file_path_parents_underscored(sequences_file_path_parents_returned)
    assert sequences_file_path_parents_underscored_returned == sequences_file_path_parents_underscored_expected
    temporary_sequences_file.unlink()


def test_when_fasta_sequences_file_has_path_parents_then_return_path_parents_underscored_string():
    sequences_file_path_parents_underscored_expected = "sequences_directory"
    temporary_sequences_directory = Path("sequences_directory")
    temporary_sequences_directory.mkdir()
    temporary_sequences_file = temporary_sequences_directory.joinpath("sequences.fasta")
    with open(temporary_sequences_file, mode="w"):
        pass
    sequences_file_path_parents_returned = fastasplitter.split_fasta_sequences_file \
        .get_sequences_file_path_parents(temporary_sequences_file)
    sequences_file_path_parents_underscored_returned = fastasplitter.split_fasta_sequences_file \
        .get_sequences_file_path_parents_underscored(sequences_file_path_parents_returned)
    assert sequences_file_path_parents_underscored_returned == sequences_file_path_parents_underscored_expected
    temporary_sequences_file.unlink()
    temporary_sequences_directory.rmdir()


def test_when_fasta_sequences_file_valid_then_return_sequences_name_list():
    sequences_name_list_expected = ["Sequence1", "Sequence2", "Sequence3"]
    temporary_sequences_file = Path("sequences.fasta")
    with open(temporary_sequences_file, mode="w") as sequences_file:
        sequences_file.write(">Sequence1|text1\nAAA\n")
        sequences_file.write(">Sequence2 |text2\nCCC\n")
        sequences_file.write(">Sequence3\nGGG\n")
    sequences_name_list_returned = fastasplitter.split_fasta_sequences_file \
        .get_sequences_name_list(temporary_sequences_file)
    for index in range(len(sequences_name_list_returned)):
        assert sequences_name_list_returned[index] == sequences_name_list_expected[index]
    temporary_sequences_file.unlink()


def test_when_fasta_sequences_file_valid_then_return_sequences_data_list():
    sequences_data_list_expected = ["AAA", "CCC", "GGG"]
    temporary_sequences_file = Path("sequences.fasta")
    with open(temporary_sequences_file, mode="w") as sequences_file:
        sequences_file.write(">Sequence1|text1\nAAA\n")
        sequences_file.write(">Sequence2 |text2\nCCC\n")
        sequences_file.write(">Sequence3\nGGG\n")
    sequences_data_list_returned = fastasplitter.split_fasta_sequences_file \
        .get_sequences_data_list(temporary_sequences_file)
    for index in range(len(sequences_data_list_returned)):
        assert sequences_data_list_returned[index][1] == sequences_data_list_expected[index]
    temporary_sequences_file.unlink()


def test_when_fasta_sequences_file_valid_then_split_sequences_and_write_to_disk():
    sequence1_file_expected = Path("Sequence1.fasta")
    sequence2_file_expected = Path("Sequence2.fasta")
    sequence3_file_expected = Path("Sequence3.fasta")
    temporary_sequences_file = Path("sequences.fasta")
    with open(temporary_sequences_file, mode="w") as sequences_file:
        sequences_file.write(">Sequence1|text1\nAAA\n")
        sequences_file.write(">Sequence2 |text2\nCCC\n")
        sequences_file.write(">Sequence3\nGGG\n")
    sequences_file_path_parents_returned = fastasplitter.split_fasta_sequences_file \
        .get_sequences_file_path_parents(temporary_sequences_file)
    sequences_file_extension_returned = fastasplitter.split_fasta_sequences_file \
        .get_sequences_file_extension(temporary_sequences_file)
    sequences_name_list_returned = fastasplitter.split_fasta_sequences_file \
        .get_sequences_name_list(temporary_sequences_file)
    sequences_data_list_returned = fastasplitter.split_fasta_sequences_file \
        .get_sequences_data_list(temporary_sequences_file)
    fastasplitter.split_fasta_sequences_file \
        .write_sequences_fasta_files_from_sequences_lists(sequences_file_path_parents_returned,
                                                          sequences_file_extension_returned,
                                                          sequences_name_list_returned,
                                                          sequences_data_list_returned)
    assert sequence1_file_expected.exists()
    assert sequence2_file_expected.exists()
    assert sequence3_file_expected.exists()
    sequence1_file_expected.unlink()
    sequence2_file_expected.unlink()
    sequence3_file_expected.unlink()
    temporary_sequences_file.unlink()


def test_when_fasta_sequences_file_has_no_path_parents_then_write_sequences_list_file_to_disk():
    sequences_list_file_expected = Path("Sequences_List.txt")
    temporary_sequences_file = Path("sequences.fasta")
    with open(temporary_sequences_file, mode="w") as sequences_file:
        sequences_file.write(">Sequence1|text1\nAAA\n")
        sequences_file.write(">Sequence2 |text2\nCCC\n")
        sequences_file.write(">Sequence3\nGGG\n")
    sequences_file_path_parents_returned = fastasplitter.split_fasta_sequences_file \
        .get_sequences_file_path_parents(temporary_sequences_file)
    sequences_file_path_parents_underscored_returned = fastasplitter.split_fasta_sequences_file \
        .get_sequences_file_path_parents_underscored(sequences_file_path_parents_returned)
    sequences_file_extension_returned = fastasplitter.split_fasta_sequences_file \
        .get_sequences_file_extension(temporary_sequences_file)
    sequences_name_list_returned = fastasplitter.split_fasta_sequences_file \
        .get_sequences_name_list(temporary_sequences_file)
    fastasplitter.split_fasta_sequences_file \
        .write_sequences_fasta_files_index_list_text_file(sequences_file_path_parents_underscored_returned,
                                                          sequences_file_extension_returned,
                                                          sequences_name_list_returned)
    assert sequences_list_file_expected.exists()
    sequences_list_file_expected.unlink()
    temporary_sequences_file.unlink()


def test_when_fasta_sequences_file_has_path_parents_then_write_sequences_list_file_to_disk():
    sequences_list_file_expected = Path("sequences_directory_Sequences_List.txt")
    temporary_sequences_directory = Path("sequences_directory")
    temporary_sequences_directory.mkdir()
    temporary_sequences_file = temporary_sequences_directory.joinpath("sequences.fasta")
    with open(temporary_sequences_file, mode="w") as sequences_file:
        sequences_file.write(">Sequence1|text1\nAAA\n")
        sequences_file.write(">Sequence2 |text2\nCCC\n")
        sequences_file.write(">Sequence3\nGGG\n")
    sequences_file_path_parents_returned = fastasplitter.split_fasta_sequences_file \
        .get_sequences_file_path_parents(temporary_sequences_file)
    sequences_file_path_parents_underscored_returned = fastasplitter.split_fasta_sequences_file \
        .get_sequences_file_path_parents_underscored(sequences_file_path_parents_returned)
    sequences_file_extension_returned = fastasplitter.split_fasta_sequences_file \
        .get_sequences_file_extension(temporary_sequences_file)
    sequences_name_list_returned = fastasplitter.split_fasta_sequences_file \
        .get_sequences_name_list(temporary_sequences_file)
    fastasplitter.split_fasta_sequences_file \
        .write_sequences_fasta_files_index_list_text_file(sequences_file_path_parents_underscored_returned,
                                                          sequences_file_extension_returned,
                                                          sequences_name_list_returned)
    assert sequences_list_file_expected.is_file()
    sequences_list_file_expected.unlink()
    temporary_sequences_file.unlink()
    temporary_sequences_directory.rmdir()


def test_when_execute_main_function_with_valid_fasta_sequences_file_then_return_successful_termination_code():
    sequence1_file_expected = Path("Sequence1.fasta")
    sequence2_file_expected = Path("Sequence2.fasta")
    sequence3_file_expected = Path("Sequence3.fasta")
    sequences_list_file_expected = Path("Sequences_List.txt")
    temporary_sequences_file = Path("sequences.fasta")
    with open(temporary_sequences_file, mode="w") as sequences_file:
        sequences_file.write(">Sequence1|text1\nAAA\n")
        sequences_file.write(">Sequence2 |text2\nCCC\n")
        sequences_file.write(">Sequence3\nGGG\n")
    sys.argv = ["", temporary_sequences_file]
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        runpy.run_path("fastasplitter/split_fasta_sequences_file.py", run_name="__main__")
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0
    sequence1_file_expected.unlink()
    sequence2_file_expected.unlink()
    sequence3_file_expected.unlink()
    sequences_list_file_expected.unlink()
    temporary_sequences_file.unlink()
