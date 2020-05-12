import yaml
import csv

def return_region(x, y):

    if x > 40 and x < 1800+40 and y > 75 and y < 190+75:
        return '0'

    if x > 20 and x < 800+20 and y > 308 and y < 115+308:
        return '1'

    if x > 20 and x < 800+20 and y > 424 and y < 125+424:
        return '2'

    if x > 20 and x < 800+20 and y > 550 and y < 125+550:
        return '3'

    if x > 20 and x < 800+20 and y > 675 and y < 125+675:
        return '4'

    return None

# ucitavanje vremena svakog pitanja korisnika i konverzija u sekunde
with open("question_time.csv") as f:
    reader = csv.reader(f, delimiter=",", quotechar='"')
    next(reader, None)  # skip the headers
    data_read = []

    for row in reader:
        helper = []
        for time_ in row[1:]:
            time_ = time_.split(':')
            helper.append(60*int(time_[0]) + int(time_[1]) + int(time_[2])/1000)
        data_read.append(helper)

# ucitavanje podataka is eye tracker-a, mapiranje na regione i upisivanje u novi fajl
with open('out_question_region_data.csv', 'w') as out:
    for user in range (3,26):
        k = 1
        q_start_t = data_read[user-3][0]
        q_end_t = data_read[user-3][k]
        with open('00' + str(user) + '-user.yml') as f:
            my_dict = yaml.safe_load(f)
            data_list = my_dict['Data']

            out_data = []
            regs = []
            for event in data_list:
                if event['BPOGV'] != 1:
                    continue
                
                if event['TIME'] < q_start_t:
                    continue

                if event['TIME'] > q_end_t:
                    print('Question ', k, 'finished; time_start: ', q_start_t, 'time_end', q_end_t)
                    print(regs)
                    out.write('\n')
                    out_data.append(regs)
                    regs = []
                    k = k + 1
                    q_start_t = q_end_t
                    q_end_t = data_read[user-3][k]

                reg = return_region(event['BPOGX']*1920, event['BPOGY']*1920)

                if reg is not None:
                    if len(regs) == 0:
                        out.write(reg)
                        
                    out.write(',' + reg)
                    regs.append(reg)
                    

            print(len(out_data))
            print()
            print()
            print('New user:')



        