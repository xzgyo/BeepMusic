import csv

 
def generate_senbonzakura():
    melody = [
        ('D4', .75), ('D4', .25), ('D4', .5), ('C4', .5),
        ('D4', .5), ('F4', .5), ('F4', .5), ('G4', .5),
        ('D4', .75), ('D4', .25), ('D4', .5), ('C4', .5),
        ('D4', .75), ('D4', .25), ('D4', .5), ('C4', .5),
        ('D4', .5)
    ]

    with open('music.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(melody)
    print("music.csv")

if __name__ == "__main__":
    generate_senbonzakura()