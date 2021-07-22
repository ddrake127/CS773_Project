import datetime

FILE_CORRELATION_THRESHOLD = 0.5 # two users are considered to access the same group of files if 50% of their accesses are exactly the same

class User:
    def __init__(self, uid):
        self.user_id = uid
        self.num_records = 0
        self.total_time = 0
        self.longest_day = 0
        self.total_ave_proc = 0
        self.max_proc = 0
        self.total_max_proc = 0
        self.machines = []
        self.logins = []
        self.logouts = []
        self.total_chars_typed = 0
        self.max_chars_typed = 0
        self.total_cpu = 0
        self.max_cpu = 0
    
    def inc_records(self):
        self.num_records += 1
        
    def inc_total_time(self, time):
        self.total_time += time
        if time > self.longest_day:
            self.longest_day = time

    def inc_ave_proc(self, ave_proc):
        self.total_ave_proc += ave_proc
        
    def inc_max_proc(self, max_proc):
        self.total_max_proc += max_proc
        if max_proc > self.max_proc:
            self.max_proc = max_proc
    
    def add_machine(self, machine):
        self.machines.append(machine)
        
    def add_login(self, login):
        self.logins.append(login)
        
    def add_logout(self, logout):
        self.logouts.append(logout)
        
    def inc_chars_typed(self, chars_typed):
        self.total_chars_typed += chars_typed
        if chars_typed > self.max_chars_typed:
            self.max_chars_typed = chars_typed
            
    def inc_cpu(self, cpu):
        self.total_cpu += cpu
        if cpu > self.max_cpu:
            self.max_cpu = cpu

class Resource:
    def __init__(self, uid):
        self.user_id = uid
        self.num_records = 0
        self.accesses = 0
        self.printed = 0
        self.machines = []
        self.start_times = []
        self.durations = []
        self.programs = []
        self.files = []
        self.printers = []
    def addMachine(self, machine):
        self.machines.append(machine)
    def addStartTime(self, st):
        self.start_times.append(st)
    def addDuration(self, dr):
        self.durations.append(dr)
    def addProgram(self, prg):
        self.programs.append(prg)
    def addFile(self, f):
        self.files.append(f)
    def addPrinter(self, p):
        self.printers.append(p)
    def incNumRecord(self):
        self.num_records += 1
    def incNumPrintRecord(self):
        self.printed += 1
    def incNumAccessRecord(self):
        self.accesses += 1
            
            
def secondsToFormattedTime(time):
    hours = time // 3600
    time -= hours * 3600
    minutes = time // 60
    time -= minutes * 60
    return (str(int(hours)) + ":" + str(int(minutes)) + ":" + str(int(time)))
        
def main():
    # file = open("Z:\CS 773 Data Mining\Project\sorted-proj-data.csv")
    file = open("sorted-proj-data.csv")
    lines = file.readlines()
    
    type_one_users = []
    resources = []
    for i in range(1, 10):
        type_one_users.append(User("U0"+str(i)))
        resources.append(Resource("U0"+str(i)))
    for i in range(10, 20):
        type_one_users.append(User("U"+str(i)))
        resources.append(Resource("U"+str(i)))

    

    
    for line in lines:
        parts = line.split(',')
        if parts[0] == '1':
            # create a date-time object with the starting and ending times
            raw_date = parts[3]
            raw_st = parts[4]
            raw_et = parts[5]
            start_time = datetime.datetime(int(raw_date[4:]) + 2000, int(raw_date[0:2]), int(raw_date[2:4]),
            int(raw_st[0:2]), int(raw_st[2:4]), int(raw_st[4:]))
            end_time = datetime.datetime(int(raw_date[4:]) + 2000, int(raw_date[0:2]), int(raw_date[2:4]),
            int(raw_et[0:2]), int(raw_et[2:4]), int(raw_et[4:]))
            workday_len = end_time - start_time
            #get other useful info
            uid = parts[1]
            machine = parts[2]
            num_proc = int(parts[6])
            max_proc = int(parts[7])
            chars_typed = int(parts[8])
            cpu_use = int(parts[9])
            user_idx = int(uid[1:]) - 1
            user = type_one_users[user_idx]
            user.inc_records()
            user.inc_total_time((end_time - start_time).total_seconds())
            user.inc_ave_proc(num_proc)
            user.inc_max_proc(max_proc)
            user.add_machine(machine)
            user.add_login(start_time)
            user.add_logout(end_time)
            user.inc_chars_typed(chars_typed)
            user.inc_cpu(cpu_use)
        if parts[0] == '2':
            if "PR" in parts[9]:
                uid = parts[1]
                machine = parts[2]
                raw_date = parts[3]
                raw_st = parts[4]
                program = parts[5]
                raw_duration = parts[6]
                fle = parts[7]
                permissions = parts[8]
                printer = parts[9]
                pages = parts[10]
                start_time = datetime.datetime(int(raw_date[4:]) + 2000, int(raw_date[0:2]), int(raw_date[2:4]),
                int(raw_st[0:2]), int(raw_st[2:4]), int(raw_st[4:]))
                d_hours = raw_duration[0:2]
                d_min = raw_duration[2:4]
                d_sec = raw_duration[4:]
                total_dur_seconds = d_hours * 3600 + d_min * 60 + d_sec

                usr_idx = int(uid[1:]) - 1
                resource = resources[usr_idx]
                resource.incNumRecord()
                resource.incNumPrintRecord()
                resource.addMachine(machine)
                resource.addStartTime(start_time)
                resource.addDuration(total_dur_seconds)
                resource.addProgram(program)
                resource.addFile(fle + ":" + permissions)
                resource.addPrinter(printer + ":" + pages)
                
            elif parts[9] == "":
                uid = parts[1]
                machine = parts[2]
                raw_date = parts[3]
                raw_st = parts[4]
                program = parts[5]
                raw_duration = parts[6]
                fle = parts[7]
                permissions = parts[8]
                start_time = datetime.datetime(int(raw_date[4:]) + 2000, int(raw_date[0:2]), int(raw_date[2:4]),
                int(raw_st[0:2]), int(raw_st[2:4]), int(raw_st[4:]))
                d_hours = raw_duration[0:2]
                d_min = raw_duration[2:4]
                d_sec = raw_duration[4:]
                total_dur_seconds = d_hours * 3600 + d_min * 60 + d_sec

                usr_idx = int(uid[1:]) - 1
                resource = resources[usr_idx]
                resource.incNumRecord()
                resource.incNumAccessRecord()
                resource.addMachine(machine)
                resource.addStartTime(start_time)
                resource.addDuration(total_dur_seconds)
                resource.addProgram(program)
                resource.addFile(fle + ":" + permissions)
                

    print("Number of records:")
    for user in type_one_users:
        print(user.user_id + ": " + str(user.num_records))
        
    print("Average time worked:")
    for user in type_one_users:
        print(user.user_id + ": " + secondsToFormattedTime(user.total_time / user.num_records))
        
    print("Longest day:")
    for user in type_one_users:
        print(user.user_id + ": " + secondsToFormattedTime(user.longest_day))

    print("Average processes, average:")
    for user in type_one_users:
        print(user.user_id + ": " + str(user.total_ave_proc / user.num_records))

    print("Max processes, average:")
    for user in type_one_users:
        print(user.user_id + ": " + str(user.total_max_proc / user.num_records))

    print("Max processes, max:")
    for user in type_one_users:
        print(user.user_id + ": " + str(user.max_proc))

    print("Average characters typed:")
    for user in type_one_users:
        print(user.user_id + ": " + str(user.total_chars_typed / user.num_records))

    print("Average CPU:")
    for user in type_one_users:
        print(user.user_id + ": " + str(user.total_cpu / user.num_records))

    print("Max CPU:")
    for user in type_one_users:
        print(user.user_id + ": " + str(user.max_cpu))

    user_machines = []
    for l in range(19):
        tmp = []
        for i in range(30):
            tmp.append(0)
        user_machines.append(tmp)
        
    print("Usage per machine:")
    for user in type_one_users:
        uid = int(user.user_id[1:]) - 1
        for machine in user.machines:
            num = int(machine[1:]) - 1
            user_machines[uid][num] += 1

    for l in user_machines:
        for i in l:
            print(i, end=',')
        print()

    print("Average start time:")
    for user in type_one_users:
        s = 0
        stimes = 0
        for st in user.logins:
            tmpdt = datetime.datetime(st.year, st.month, st.day, 0, 0, 0)
            diff = (st - tmpdt).total_seconds()
            stimes += diff
            s += 1
        print(user.user_id + ": " + str(secondsToFormattedTime(stimes / s)))


    print("Average end time:")
    for user in type_one_users:
        s = 0
        etimes = 0
        for et in user.logouts:
            tmpdt = tmpdt = datetime.datetime(et.year, et.month, et.day, 0, 0, 0)
            diff = (et - tmpdt).total_seconds()
            etimes += diff
            s += 1
        print(user.user_id + ": " + str(secondsToFormattedTime(etimes / s)))


    print("File accesses and prints")
    for r in resources:
        print(r.user_id + ": " + str(r.accesses) + ", " + str(r.printed) + ", " + str(r.num_records))

    print("File accesses based on files")
    file_accesses = {}
    for r in resources:
        files = {}
        for f in r.files:
            if f not in files:
                files[f] = 1
            else:
                files[f] += 1
        print(r.user_id)
        print(files)
        file_accesses[r.user_id] = files

    print("\n\n\n\n\n\n\n\nEnd of statistics...beginning of correlation\n\n\n")
    percent_similar_matrix = []
    for files in file_accesses:
        this_one = file_accesses[files] # dictionary of files to number of accesses
        per_similars = []
        this_num_records = resources[int(files[1:]) - 1].num_records
        for f in file_accesses:
            similar = 0
            if files != f:
                other_one = file_accesses[f] # dictionary of files to number of accesses
                other_num_records = resources[int(f[1:]) - 1].num_records
                for accesses in this_one:
                    cnt = this_one[accesses]
                    othercnt = 0 if accesses not in other_one else other_one[accesses]
                    similar += min(cnt, othercnt)
                per_similars.append(similar / max(this_num_records, other_num_records))
            else:
                per_similars.append(-1)
        percent_similar_matrix.append(per_similars)
    print("Percent Similar Matrix")
    print(percent_similar_matrix)

    groups = []
    user_number_outer = 1
    for user_list in percent_similar_matrix:
        user_number_inner = 1
        print("U" + str(user_number_outer) + ": ", end="")
        for per in user_list:
            if per > FILE_CORRELATION_THRESHOLD:
                print("U" + str(user_number_inner), end = " ")
            user_number_inner += 1
        user_number_outer += 1
        print()
            
        
            
            
                 
	
if __name__ == "__main__":
    main()
