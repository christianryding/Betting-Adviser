import csv

# calculate sum of all completed  bets in "bets_summary.csv"
def calc_sum():
    with open("bets_summary.csv", "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        sum = 0
        for line in csv_reader:
            sum = sum + float(line[7]) - float(line[6])
        print("sum is = {}".format(sum))