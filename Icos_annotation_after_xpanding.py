# Change the xpand processed virus particle structure into right format.
# The output of xpand makes wrong ATOM numbers and wrong chain ID.

file = '/home/zqq/lip/FCV/qzh/highresolution_fit/highresolution_fit_coot/fix_the_secondary_structure/xpanded2280.pdb'
output_file = '/home/zqq/code/workscript/fcv/output.pdb'

with open(file) as file_obj:
    obj_list = file_obj.readlines()

line_list = []
n = 0
ATOM_n = 1
change_happens_count = 0
MODEL_n = 1

for line in obj_list:
    line_list.append(line)
    with open(output_file, 'a') as file_output:

        # Change the lines with a 'ATOM' head

        if 'ATOM' in line_list[n]:

            if 'ATOM' not in line_list[n - 1]:
                change_happens_count = 1

            if 'ATOM' not in line_list[n - 1] and 'ATOM' in line_list[n]:
                change_happens_count = 0
                MODEL_n += 1
                ATOM_n = 1

            elif int(line_list[n][23:25]) < int(line_list[n - 1][23:25]):
                change_happens_count += 1

            if change_happens_count > 2:
                change_happens_count = 0

            # Class A (change_happens_count == 0), B (1), C (2) options

            space_number = 11 - len(str(ATOM_n)) - 4
            space = " " * space_number

            if change_happens_count == 0:
                file_output.write(('ATOM%s%s' % (space, str(ATOM_n))) +
                                  line[11:])

            elif change_happens_count == 1:
                file_output.write(('ATOM%s%s' % (space, str(ATOM_n))) +
                                  line[11:20] + ' B' + line[22:])

            elif change_happens_count == 2:
                file_output.write(('ATOM%s%s' % (space, str(ATOM_n))) +
                                  line[11:20] + ' C' + line[22:])

            ATOM_n += 1
            # print(ATOM_n)

        elif ('HELIX' in line_list[n]) or ('SHEET' in line_list[n]):
            file_output.write(line)

        elif 'REMARK Z' in line_list[n]:
            # file_output.write(line)
            space_number_MODEL = 14 - len(str(MODEL_n)) - 5
            space_MODEL = " " * space_number_MODEL
            if n < 1000:
                file_output.write(
                    'MODEL%s%s\n' %
                    (space_MODEL,
                     str(MODEL_n))) # To save the XPAND default output
            else:
                file_output.write('ENDMDL\n' + 'MODEL%s%s\n' %
                                  (space_MODEL, str(MODEL_n)))
            # file_output.write(line)

        elif 'TER' in line_list[n]:
            file_output.write(line)

    n += 1
