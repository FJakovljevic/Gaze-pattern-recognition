import csv
import random

def to_seq_30(line):
    # prebroj broj uzastopnih pojavljivanja sekvence
    counted = []
    section = line[0]
    counter = 0
    for s in line:
        if section != s:
            counted.append([section, counter])
            section = s
            counter = 0
            
        counter += 1
    counted.append([section, counter])

    # izbaci neke koji su suvise krati i predstavljaju sum
    new = []
    for s in counted:
        if not s[1] <= 3:
            new.append(s)

    # ponovo prebroji i grupise bez tih sumova
    counted = new
    refined_counted = []
    i = 0
    new_len = 0        
    while i < len(counted)-1:
        helper = counted[i]
        i = i + 1
        
        for j in range(i, len(counted)):
            if helper[0] == counted[j][0]:
                helper[1] = helper[1] + counted[j][1]
            else:
                i = j
                break
        
        new_len = new_len + helper[1]
        refined_counted.append(helper)

    # odredi njihov udeo u sekvenci
    to_ret = ''
    for s in refined_counted:
        to_ret += round((30*s[1])/new_len) * s[0]

    # ispravi greske u racunu
    if len(to_ret) > 30:
        for _ in range(len(to_ret) - 30):
            x = random.randint(0, len(to_ret)-1)
            to_ret = to_ret[0:x] + to_ret[x+1:]
    
    if len(to_ret) < 30:
        for _ in range(30 - len(to_ret)):
            x = random.randint(0, len(to_ret)-1)
            to_ret = to_ret[0:x] + to_ret[x] + to_ret[x:]

    return to_ret    


with open("out_question_region_data.csv") as f:
    reader = csv.reader(f, delimiter=",", quotechar='"')
    data_read = [row for row in reader]

print('Number of inputs: ', len(data_read))

with open('scaled_data.txt', 'w') as out:
    for q in data_read:
        q_size = len(q)

        if q_size <= 30:
            print('Discarded because to short')
            continue

        ret = to_seq_30(q)
        print('Sequence: ', ret, 'len: ', len(ret))
        out.write(ret + '\n')

        
