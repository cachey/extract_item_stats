import os, sys, re, collections, csv

from string import ascii_uppercase as ucase

class ItemAnalysis:
    def __init__(self, n):
        self.number = n

    def __str__(self):
        return """
        ITEM %d\n\tDIF: %f\n\tRPB: %f\n\tCRPB: %f\n\tRBIS: %f\n\tCRBIS: %f\n\tISI: %f\n\t%s
        """% (self.number, self.DIF, self.RPB, self.CRPB, self.RBIS, self.CRBIS, self.IRI, item.key_dict)



def analyse_and_write_file(file):
    try:
        items = []

        with open(file, "r") as f:
            read_data = f.read()
            read_data = iter(read_data.split("\n"))

        # process the file
        for line in read_data:
            #  "ITEM   8: DIF=0.969, RPB=  0.185, CRPB=  0.157 (95% CON=  0.071, 0.240)"
            m =  re.match(r'ITEM\s+(\d+):\s+DIF=(\d+\.\d+)\,\s+RPB=\s+(\d+\.\d+),\s+CRPB=\s+(\d+\.\d+)', line)
            if m:
                item = ItemAnalysis(int(m.group(1)))
                item.DIF = float(m.group(2))
                item.RPB = float(m.group(3))
                item.CRPB = float(m.group(4))

                #                      RBIS= 0.160, CRBIS= 0.060, IRI=0.059
                l2 = read_data.next()
                m = re.match(r'\s+RBIS=\s+(\d+\.\d+),\s+CRBIS=\s+(\d+\.\d+),\s+IRI=(\d+\.\d+)', l2)
                item.RBIS = float(m.group(1))
                item.CRBIS = float(m.group(2))
                item.IRI = float(m.group(3))

                #    GROUP   N   INV   NF  OMIT     A       B       C       D*      E       F       G       H
                l3 = read_data.next()
                # find the answer with a "*"
                m = re.match('.*(\w\*).*', l3)
                indicated_correct_answer =  m.group(1)
                # strip off the star
                item.correct_key_only = indicated_correct_answer[0]
                # replace in l3 and create dict of used keys
                line_items = l3.replace(indicated_correct_answer, item.correct_key_only).split()
                used_keys = line_items[5:]
                item.last_key = line_items[-1]

                # create dict of all keys with default values of 0 (zero)
                item.key_dict = collections.OrderedDict(((k, 0) for k in ucase))

                # TOTAL  509    0    0    0    0.02    0.92    0.00    0.00    0.00    0.06
                l4 = read_data.next()
                line_items = l4.split()

                # get the total number answering this question
                item.number_answering = line_items[1]

                # update the key dict with proportions
                key_proportions = line_items[5:]
                for key, proportion in zip(used_keys, key_proportions):
                    item.key_dict[key] = proportion

                items.append(item)

        # write to csv file - rename with .csv extension
        name, ext = os.path.splitext(file)
        outfile_name = name + ".csv"

        with open(outfile_name, 'w') as csvfile:
            itemwriter = csv.writer(csvfile, dialect = 'excel')
            itemwriter.writerow(['ITEM', 'Number Answering', 'Correct Answer', 'DIF', 'RPB', 'CRPB', 'RBIS', 'CRBIS', 'ISI'] + list(ucase) + ['LAST KEY IN DATA'])
            for item in items:
                data = (item.number, item.number_answering, item.correct_key_only, item.DIF, item.RPB, item.CRPB, item.RBIS, item.CRBIS, item.IRI) + tuple(item.key_dict.values())
                data += (item.last_key,)
                itemwriter.writerow(data)
    except Exception as e:
        print sys.exc_info()


# get the files in the selected directory
path = './raw_data'
for file in os.listdir(path):
    current = os.path.join(path, file)
    if os.path.isfile(current):
        analyse_and_write_file(current)
