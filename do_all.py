import glob
import os

#print(glob.glob("./raw/*.pdf"))

print("""
************
** STRART **
************
""")

files_list = glob.glob("./raw/*.pdf")

dest_dir = "./out/"
in_dir = './raw/'

chapter_list = []
# ottieni nome capitolo
for file in files_list:
    file = file.split('-')[0]
    chapter_list.append(file)

print(chapter_list)

# chapter name uniques
chapter_uniques = list(set(chapter_list))

print(chapter_uniques)

for chapter in chapter_uniques:
    file_name = chapter.split('/')[-1]
    print("Chapter: {}".format(file_name))

    even = in_dir + file_name + "-pari.pdf"
    odd = in_dir + file_name + "-dispari.pdf"

    out_file = dest_dir + file_name + ".pdf"

    print(odd, even)


    # python3 pdf-merger.py gastrointeriti_dispari.pdf  gastrointeriti_dispari.pdf gastrointeriti.pdf
    command = "python3.7 pdf-merger.py {} {} {}".format(odd, even, out_file)
    #print(command)
    os.system(command)

print("""
************
** END **
************
""")
