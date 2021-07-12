from pathlib import Path
import fastasplitter.exceptions
import fastasplitter.split_fasta_sequences_file
import os
import pytest
import runpy
import shutil
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


def test_when_fasta_sequences_file_not_exists_then_throws_file_not_found_exception():
    inexistent_sequences_file = Path("inexistent_sequences.fasta")
    with pytest.raises(FileNotFoundError) as pytest_wrapped_e:
        fastasplitter.split_fasta_sequences_file.check_if_is_valid_fasta_sequences_file(str(inexistent_sequences_file))
    file_not_found_message = "FASTA Sequences File not Found!"
    assert pytest_wrapped_e.type == FileNotFoundError
    assert str(pytest_wrapped_e.value) == file_not_found_message


def test_when_sequences_file_is_fasta_extension_then_return_extension():
    sequences_file_extension_expected = "fasta"
    temporary_sequences_file = Path("sequences.fasta")
    temporary_sequences_file_str = str(temporary_sequences_file)
    with open(os.path.join(temporary_sequences_file), mode="w"):
        pass
    sequences_file_extension_returned = fastasplitter.split_fasta_sequences_file \
        .get_sequences_file_extension(temporary_sequences_file_str)
    os.remove(temporary_sequences_file)
    assert sequences_file_extension_returned == sequences_file_extension_expected


def test_when_sequences_file_is_not_fasta_extension_then_throws_invalid_extension_file_exception():
    temporary_sequences_file = Path("sequences.txt")
    with open(os.path.join(temporary_sequences_file), mode="w"):
        pass
    temporary_sequences_file_str = str(temporary_sequences_file)
    with pytest.raises(fastasplitter.exceptions.InvalidExtensionFileError) as pytest_wrapped_e:
        fastasplitter.split_fasta_sequences_file.check_if_is_valid_fasta_sequences_file(temporary_sequences_file_str)
    invalid_format_file_message = "Only FASTA Extension Files (.fa, .faa, .fasta, .ffn, .fna or .frn) are Allowed!"
    assert pytest_wrapped_e.type == fastasplitter.exceptions.InvalidExtensionFileError
    assert str(pytest_wrapped_e.value) == invalid_format_file_message
    os.remove(temporary_sequences_file)


def test_when_fasta_sequences_file_has_not_any_description_line_then_throws_invalid_formatted_fasta_file_exception():
    temporary_sequences_file = Path("sequences.fasta")
    with open(os.path.join(temporary_sequences_file), mode="w") as sequences_file:
        sequences_file.write("AAA\n")
        sequences_file.write("CCC\n")
        sequences_file.write("GGG\n")
    temporary_sequences_file_str = str(temporary_sequences_file)
    with pytest.raises(fastasplitter.exceptions.InvalidFormattedFastaFileError) as pytest_wrapped_e:
        fastasplitter.split_fasta_sequences_file.check_if_is_valid_fasta_sequences_file(temporary_sequences_file_str)
    invalid_formatted_fasta_file_message = "'{0}' Has Not Any Description Line!".format(str(temporary_sequences_file))
    assert pytest_wrapped_e.type == fastasplitter.exceptions.InvalidFormattedFastaFileError
    assert str(pytest_wrapped_e.value) == invalid_formatted_fasta_file_message
    os.remove(temporary_sequences_file)


def test_when_fasta_sequences_file_has_invalid_description_lines_then_throws_invalid_formatted_fasta_file_exception():
    temporary_sequences_file = Path("sequences.fasta")
    with open(os.path.join(temporary_sequences_file), mode="w") as sequences_file:
        sequences_file.write("> InvalidDescription1\nAAA\n")
        sequences_file.write(">ValidDescription1 |text1\nCCC\n")
        sequences_file.write(">ValidDescription2|text2\nGGG\n")
        sequences_file.write("> InvalidDescription2|text2\nTTT\n")
    temporary_sequences_file_str = str(temporary_sequences_file)
    with pytest.raises(fastasplitter.exceptions.InvalidFormattedFastaFileError) as pytest_wrapped_e:
        fastasplitter.split_fasta_sequences_file.check_if_is_valid_fasta_sequences_file(temporary_sequences_file_str)
    invalid_formatted_fasta_file_message = "'{0}' Contains {1} Line(s) With Invalid Description Format!" \
        .format(str(temporary_sequences_file), str(2))
    assert pytest_wrapped_e.type == fastasplitter.exceptions.InvalidFormattedFastaFileError
    assert str(pytest_wrapped_e.value) == invalid_formatted_fasta_file_message
    os.remove(temporary_sequences_file)


def test_when_fasta_sequences_file_has_no_data_then_throws_invalid_formatted_fasta_file_exception():
    temporary_sequences_file = Path("sequences.fasta")
    with open(os.path.join(temporary_sequences_file), mode="w") as sequences_file:
        sequences_file.write(">ValidDescription1\n")
    temporary_sequences_file_str = str(temporary_sequences_file)
    with pytest.raises(fastasplitter.exceptions.InvalidFormattedFastaFileError) as pytest_wrapped_e:
        fastasplitter.split_fasta_sequences_file.check_if_is_valid_fasta_sequences_file(temporary_sequences_file_str)
    invalid_formatted_fasta_file_message = "'{0}' Seems a Empty Fasta File!".format(str(temporary_sequences_file))
    assert pytest_wrapped_e.type == fastasplitter.exceptions.InvalidFormattedFastaFileError
    assert str(pytest_wrapped_e.value) == invalid_formatted_fasta_file_message
    os.remove(temporary_sequences_file)


def test_when_fasta_sequences_file_has_all_valid_lines_then_ok():
    temporary_sequences_file = Path("sequences.fasta")
    with open(os.path.join(temporary_sequences_file), mode="w") as sequences_file:
        sequences_file.write(">ValidDescription1|text1\nAAA\n")
        sequences_file.write(">ValidDescription2 |text2\nCCC\n")
        sequences_file.write(">ValidDescription3\nGGG\n")
    temporary_sequences_file_str = str(temporary_sequences_file)
    assert fastasplitter.split_fasta_sequences_file \
           .check_if_is_valid_fasta_sequences_file(temporary_sequences_file_str) is None
    os.remove(temporary_sequences_file)


def test_when_fasta_sequences_file_has_no_prefix_path_then_return_empty_prefix_path_string():
    sequences_prefix_path_expected = ""
    temporary_sequences_file = Path("sequences.fasta")
    with open(os.path.join(temporary_sequences_file), mode="w"):
        pass
    temporary_sequences_file_str = str(temporary_sequences_file)
    sequences_prefix_path_returned = fastasplitter.split_fasta_sequences_file \
        .get_sequences_prefix_path_from_fasta_sequences_file(temporary_sequences_file_str)
    assert sequences_prefix_path_returned == sequences_prefix_path_expected
    os.remove(temporary_sequences_file)


def test_when_fasta_sequences_file_has_prefix_path_then_return_prefix_path_string():
    sequences_prefix_path_expected = "sequences_directory/"
    temporary_sequences_directory_name = "sequences_directory"
    os.mkdir(temporary_sequences_directory_name)
    temporary_sequences_file = temporary_sequences_directory_name + "/" + "sequences.fasta"
    with open(os.path.join(temporary_sequences_file), mode="w"):
        pass
    temporary_sequences_file_str = str(temporary_sequences_file)
    sequences_prefix_path_returned = fastasplitter.split_fasta_sequences_file \
        .get_sequences_prefix_path_from_fasta_sequences_file(temporary_sequences_file_str)
    assert sequences_prefix_path_returned == sequences_prefix_path_expected
    shutil.rmtree(temporary_sequences_directory_name)


def test_when_fasta_sequences_file_valid_then_return_sequences_name_list():
    sequences_name_list_expected = ["Sequence1", "Sequence2", "Sequence3"]
    temporary_sequences_file = Path("sequences.fasta")
    with open(os.path.join(temporary_sequences_file), mode="w") as sequences_file:
        sequences_file.write(">Sequence1|text1\nAAA\n")
        sequences_file.write(">Sequence2 |text2\nCCC\n")
        sequences_file.write(">Sequence3\nGGG\n")
    temporary_sequences_file_str = str(temporary_sequences_file)
    sequences_name_list_returned = fastasplitter.split_fasta_sequences_file \
        .get_sequences_name_list_from_fasta_sequences_file(temporary_sequences_file_str)
    for index in range(len(sequences_name_list_returned)):
        assert sequences_name_list_returned[index] == sequences_name_list_expected[index]
    os.remove(temporary_sequences_file)


def test_when_fasta_sequences_file_valid_then_return_sequences_data_list():
    sequences_data_list_expected = ["AAA", "CCC", "GGG"]
    temporary_sequences_file = Path("sequences.fasta")
    with open(os.path.join(temporary_sequences_file), mode="w") as sequences_file:
        sequences_file.write(">Sequence1|text1\nAAA\n")
        sequences_file.write(">Sequence2 |text2\nCCC\n")
        sequences_file.write(">Sequence3\nGGG\n")
    temporary_sequences_file_str = str(temporary_sequences_file)
    sequences_data_list_returned = fastasplitter.split_fasta_sequences_file \
        .get_sequences_data_list_from_fasta_sequences_file(temporary_sequences_file_str)
    for index in range(len(sequences_data_list_returned)):
        assert sequences_data_list_returned[index][1] == sequences_data_list_expected[index]
    os.remove(temporary_sequences_file)


def test_when_fasta_sequences_file_valid_then_split_sequences_and_write_to_disk():
    sequence1_file_expected = Path("Sequence1.fasta")
    sequence2_file_expected = Path("Sequence2.fasta")
    sequence3_file_expected = Path("Sequence3.fasta")
    temporary_sequences_file = Path("sequences.fasta")
    with open(os.path.join(temporary_sequences_file), mode="w") as sequences_file:
        sequences_file.write(">Sequence1|text1\nAAA\n")
        sequences_file.write(">Sequence2 |text2\nCCC\n")
        sequences_file.write(">Sequence3\nGGG\n")
    temporary_sequences_file_str = str(temporary_sequences_file)
    sequences_prefix_path_returned = fastasplitter.split_fasta_sequences_file \
        .get_sequences_prefix_path_from_fasta_sequences_file(temporary_sequences_file_str)
    sequences_file_extension_returned = fastasplitter.split_fasta_sequences_file \
        .get_sequences_file_extension(temporary_sequences_file_str)
    sequences_name_list_returned = fastasplitter.split_fasta_sequences_file \
        .get_sequences_name_list_from_fasta_sequences_file(temporary_sequences_file_str)
    sequences_data_list_returned = fastasplitter.split_fasta_sequences_file \
        .get_sequences_data_list_from_fasta_sequences_file(temporary_sequences_file_str)
    fastasplitter.split_fasta_sequences_file \
        .write_sequences_fasta_files_from_sequences_lists(sequences_prefix_path_returned,
                                                          sequences_file_extension_returned,
                                                          sequences_name_list_returned,
                                                          sequences_data_list_returned)
    assert sequence1_file_expected.exists()
    assert sequence2_file_expected.exists()
    assert sequence3_file_expected.exists()
    os.remove(sequence1_file_expected)
    os.remove(sequence2_file_expected)
    os.remove(sequence3_file_expected)
    os.remove(temporary_sequences_file)


def test_when_fasta_sequences_file_has_no_prefix_path_then_write_sequences_list_file_to_disk():
    sequences_list_file_prefix_expected = ""
    sequences_list_file_expected = Path(sequences_list_file_prefix_expected + "Sequences_List.txt")
    temporary_sequences_file = Path("sequences.fasta")
    with open(os.path.join(temporary_sequences_file), mode="w") as sequences_file:
        sequences_file.write(">Sequence1|text1\nAAA\n")
        sequences_file.write(">Sequence2 |text2\nCCC\n")
        sequences_file.write(">Sequence3\nGGG\n")
    temporary_sequences_file_str = str(temporary_sequences_file)
    sequences_prefix_path_returned = fastasplitter.split_fasta_sequences_file \
        .get_sequences_prefix_path_from_fasta_sequences_file(temporary_sequences_file_str)
    sequences_file_extension_returned = fastasplitter.split_fasta_sequences_file \
        .get_sequences_file_extension(temporary_sequences_file_str)
    sequences_name_list_returned = fastasplitter.split_fasta_sequences_file \
        .get_sequences_name_list_from_fasta_sequences_file(temporary_sequences_file_str)
    fastasplitter.split_fasta_sequences_file \
        .write_sequences_fasta_files_index_list_text_file(sequences_prefix_path_returned,
                                                          sequences_file_extension_returned,
                                                          sequences_name_list_returned)
    assert sequences_list_file_expected.exists()
    os.remove(sequences_list_file_expected)
    os.remove(temporary_sequences_file)


def test_when_fasta_sequences_file_has_prefix_path_then_write_sequences_list_file_to_disk():
    sequences_list_file_prefix_expected = "sequences_directory_"
    sequences_list_file_expected = Path(sequences_list_file_prefix_expected + "Sequences_List.txt")
    temporary_sequences_directory = "sequences_directory"
    os.mkdir(temporary_sequences_directory)
    temporary_sequences_file = temporary_sequences_directory + "/" + "sequences.fasta"
    with open(os.path.join(temporary_sequences_file), mode="w") as sequences_file:
        sequences_file.write(">Sequence1|text1\nAAA\n")
        sequences_file.write(">Sequence2 |text2\nCCC\n")
        sequences_file.write(">Sequence3\nGGG\n")
    temporary_sequences_file_str = str(temporary_sequences_file)
    sequences_prefix_path_returned = fastasplitter.split_fasta_sequences_file \
        .get_sequences_prefix_path_from_fasta_sequences_file(temporary_sequences_file_str)
    sequences_file_extension_returned = fastasplitter.split_fasta_sequences_file \
        .get_sequences_file_extension(temporary_sequences_file_str)
    sequences_name_list_returned = fastasplitter.split_fasta_sequences_file \
        .get_sequences_name_list_from_fasta_sequences_file(temporary_sequences_file_str)
    fastasplitter.split_fasta_sequences_file \
        .write_sequences_fasta_files_index_list_text_file(sequences_prefix_path_returned,
                                                          sequences_file_extension_returned,
                                                          sequences_name_list_returned)
    assert sequences_list_file_expected.exists()
    os.remove(sequences_list_file_expected)
    shutil.rmtree(temporary_sequences_directory)


def test_when_execute_main_function_with_valid_fasta_sequences_file_then_return_successful_termination_code():
    sequence1_file_expected = Path("Sequence1.fasta")
    sequence2_file_expected = Path("Sequence2.fasta")
    sequence3_file_expected = Path("Sequence3.fasta")
    sequences_list_file_prefix_expected = ""
    sequences_list_file_expected = Path(sequences_list_file_prefix_expected + "Sequences_List.txt")
    temporary_sequences_file = Path("sequences.fasta")
    with open(os.path.join(temporary_sequences_file), mode="w") as sequences_file:
        sequences_file.write(">Sequence1|text1\nAAA\n")
        sequences_file.write(">Sequence2 |text2\nCCC\n")
        sequences_file.write(">Sequence3\nGGG\n")
    temporary_sequences_file_str = str(temporary_sequences_file)
    sys.argv = ["", temporary_sequences_file_str]
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        runpy.run_path("fastasplitter/split_fasta_sequences_file.py", run_name="__main__")
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0
    os.remove(sequence1_file_expected)
    os.remove(sequence2_file_expected)
    os.remove(sequence3_file_expected)
    os.remove(sequences_list_file_expected)
    os.remove(temporary_sequences_file)
