# This script is to extract first 10,000 review data from the shuffled amazon review data (totally 120,000 instances)

input_file = 'dataset/amz_data_shuffled.dat'
output_file = 'dataset/amz_data_shuffled_start_10k_lines.dat'

with open(input_file, 'r', encoding='utf-8') as fin, open(output_file, 'w', encoding='utf-8') as fout:
    line_written = 0
    for line in fin:
        if line_written == 10000: break
        fout.write(line)
        line_written += 1

# Check the output data
with open(output_file, 'r', encoding='utf-8') as f:
    for i in range(10):
        print(f.readline())
