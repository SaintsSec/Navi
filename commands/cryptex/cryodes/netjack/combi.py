file1 = "./gen/adjectives.txt"
file2 = "./gen/nouns.txt"
# file3 = "./gen/numbers.txt"
file4 = "./wldb/netgear_list.txt"

with open(file1, 'rt') as f:
  file1_content = f.read().strip('\n').split('\n')
with open(file2, 'rt') as f:
  file2_content = f.read().strip('\n').split('\n')

out = []
for file1_line in file1_content:
  for file2_line in file2_content:
      out.append(file1_line.strip() + file2_line.strip())

with open(file4, 'wt') as f:
  f.write('\n'.join(out))