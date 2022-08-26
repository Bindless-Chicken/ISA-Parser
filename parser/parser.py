import tabula
import re

# dfs = tabula.convert_into('data/RDNA2_Shader_ISA_November2020.pdf', 'output.tsv', pages='110-243', output_format="tsv")
# print(dfs)

def is_all_caps(s):
    return all(char.isupper() for char in s)

regex_good_line = r"^([0-9]+)\s{1}([A-Z_0-9]*?)\s{1}(.+)$"
regex_description_only = r"^(\"\")\t\t(.+)$"
regex_opcode_description_only = r"^\"\"\s{1}(\S+?)?\s{1}(.+)$"
regex_header = r"^Opcode\t(Name)[\t, ]Description$"
regex_trailing_opcode_with_desc = r"^\"\"\t([A-Z_0-9]*?)\t(.*?)$"
regex_description_catch_all = r"^\"\"\t(.*?)$"
regex_malformed_opcode_line = r"^([0-9]+)\s{1}\"([A-Z_0-9]*?)$"
regex_end_of_malformed_opcode_line = r"([A-Z_0-9]*?)\"\t(.*)$"


valid_lines = list()
invalid_lines = list()

with open('output.tsv', 'r') as f:
    lines = f.readlines()

    previous_line = list()

    for line in lines[:]:
        # Good line (right amount of cell)
        matches = re.search(regex_good_line, line, re.MULTILINE)
        if matches:
            # Push the previous line, it's complete now
            if len(previous_line) == 3:
                valid_lines.append(previous_line)
                previous_line = list()

            # Cache the current
            previous_line = [matches.group(1), matches.group(2).replace('"', ''), matches.group(3).replace('"', '')]
            continue

        # Description only line
        # (append to previous line)
        matches = re.search(regex_description_only, line, re.MULTILINE)
        if matches:
            previous_line[2] += " "
            previous_line[2] += matches.group(2).replace('"', '')
            continue

        # Trailing opcode only line
        # (append to previous line)
        matches = re.search(regex_trailing_opcode_with_desc, line, re.MULTILINE)
        if matches:
            previous_line[1] += matches.group(1).replace('"', '')

            if matches.group(2):
                previous_line[2] += " "
                previous_line[2] += matches.group(2).replace('"', '')
            continue

        # Malformed opcode line
        matches = re.search(regex_malformed_opcode_line, line, re.MULTILINE)
        if matches:
            # Push the previous line, it's complete now
            if len(previous_line) == 3:
                valid_lines.append(previous_line)
                previous_line = list()

            # Cache the current
            previous_line = [matches.group(1), matches.group(2).replace('"', ''), '']
            continue

        # End of malformed line
        # (append to previous line)
        matches = re.search(regex_end_of_malformed_opcode_line, line, re.MULTILINE)
        if matches:
            previous_line[1] += matches.group(1).replace('"', '')

            if matches.group(2):
                previous_line[2] += " "
                previous_line[2] += matches.group(2).replace('"', '')
            continue

        # Description catch all (must run last)
        # (append to previous line)
        matches = re.search(regex_description_catch_all, line, re.MULTILINE)
        if matches:
            previous_line[2] += " "
            previous_line[2] += matches.group(1).replace('"', '')
            continue

        # Header line
        matches = re.search(regex_header, line, re.MULTILINE)
        if matches:
            # Push the previous line, it's complete now
            if len(previous_line) == 3:
                valid_lines.append(previous_line)
                previous_line = list()

            valid_lines.append(['', '', ''])
            valid_lines.append(['#####', '', ''])
            continue

        # No tab lines, jsut append to desc
        if line.find('\t') == -1 and len(previous_line) == 3:
            previous_line[2] += " "
            previous_line[2] += line[:-1]
            continue

        # Fallthrough case
        invalid_lines.append(line)

with open('valid.tsv', 'w') as f:
    for line in valid_lines:
        f.writelines(line[0] + '\t' + line[1] + '\t' + line[2] + '\n')

with open('valid.csv', 'w') as f:
    for line in valid_lines:
        f.writelines(line[0] + ',' + line[1] + ',"' + line[2] + '"\n')

with open('invalid.tsv', 'w') as f:
    for line in invalid_lines:
        f.writelines(line + '\n')

