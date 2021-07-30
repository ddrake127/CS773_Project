import datetime
import numpy as np
import statistics
import math
import copy


class User:
    def __init__(self, uid):
        self.user_id = uid
        self.num_records = 0
        self.total_time = 0
        self.longest_day = 0
        self.total_ave_proc = 0
        self.ave_procs = []
        self.max_proc = 0
        self.max_proc_l = []
        self.total_max_proc = 0
        self.machines = []
        self.logins = []
        self.logouts = []
        self.total_chars_typed = 0
        self.chars_typed = []
        self.max_chars_typed = 0
        self.total_cpu = 0
        self.cpus = []
        self.max_cpu = 0
        self.days_worked = [] # days of week worked. Monday = 0
        self.times = []
        for i in range(0, 7):
            self.days_worked.append(0)
        
    
    def inc_records(self):
        self.num_records += 1
        
    def inc_total_time(self, time):
        self.total_time += time
        self.times.append(time)
        if time > self.longest_day:
            self.longest_day = time

    def inc_ave_proc(self, ave_proc):
        self.ave_procs.append(ave_proc)
        self.total_ave_proc += ave_proc
        
    def inc_max_proc(self, max_proc): 
        self.total_max_proc += max_proc
        self.max_proc_l.append(max_proc)
        if max_proc > self.max_proc:
            self.max_proc = max_proc
    
    def add_machine(self, machine):
        self.machines.append(machine)
        
    def add_login(self, login):
        self.logins.append(login)
        self.days_worked[login.weekday()] += 1
        
    def add_logout(self, logout):
        self.logouts.append(logout)
        
    def inc_chars_typed(self, chars_typed):
        self.chars_typed.append(chars_typed)
        self.total_chars_typed += chars_typed
        if chars_typed > self.max_chars_typed:
            self.max_chars_typed = chars_typed
            
    def inc_cpu(self, cpu):
        self.cpus.append(cpu)
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

class Email:
    def __init__(self, uid):
        self.user_id = uid
        self.machines = []
        self.start_times = []
        self.email_programs = []
        self.emails = [] # addresses; S/R
        self.bytes = []
        self.attachments = 0
        self.count = 0
    def addMachine(self, machine):
        self.machines.append(machine)
    def addStartTime(self, st):
        self.start_times.append(st)
    def addEmailProgram(self, prog):
        self.email_programs.append(prog)
    def addBytes(self, b):
        self.bytes.append(b)
    def incCount(self):
        self.count += 1
    def addEmail(self, em):
        self.emails.append(em)
            
          
          
# ---------------------------------------------------------------------------------
#       HELPER FUNCTIONS

def secondsToFormattedTime(time):
    hours = time // 3600
    time -= hours * 3600
    minutes = time // 60
    time -= minutes * 60
    return (str(int(hours)) + ":" + str(int(minutes)) + ":" + str(int(time)))

def removeOutliers(data):
    data.sort()
    upper = []
    lower = []
    if len(data) % 2 == 0:
        lower = data[:int(len(data) / 2)]
        upper = data[int(len(data) / 2):]
    else:
        lower = data[:int(len(data) / 2)]
        upper = data[int(len(data) / 2) + 1:]
    q1 = statistics.median(lower)
    q3 = statistics.median(upper)
    iqr = q3-q1
    lower = q1 - (iqr * 1.5)
    upper = q3 + (iqr * 1.5)
    ret_val = []
    for d in data:
        if d >= lower and d <= upper:
            ret_val.append(d)
    return ret_val
    
# data is a list of integers
def normalize_list(data):
    _max = max(data)
    _min = min(data)
    ret_val = []
    for d in data:
        ret_val.append((d - _min) / (_max - _min))
    return ret_val
    
# data is a list of lists; normalize based on position in the second list
# so if you have [a1,b1,c1] and [a2,b2,c2] where a, b, c are attributes,
# all a's, b's and c's will be normalized seperately
def normalize(data):
    for i in range(len(data[0])):
        values = []
        for j in range(len(data)):
            values.append(data[j][i])
        values = normalize_list(values)
        for j in range(len(data)):
            data[j][i] = values[j]
    return data
    
def distance(ref, values):
    if len(ref) != len(values):
        return -1
    _sum = 0
    for i in range(len(values)):
        _sum += (ref[i] - values[i])**2
    return math.sqrt(_sum)
    
    
def centroid(points):
    point = []
    for i in range(len(points[0])):
        val = 0
        for j in range(len(points)):
            val += points[j][i]
        point.append(val / len(points))
    return point

# points are what we are trying to cluster, ref_points are what we are using as the starting centroids
def k_meansCluster(points, ref_points):
    num_groups = len(ref_points)
    groups = []
    for i in range(num_groups):
        groups.append([])
        groups[i].append(ref_points[i])
    for p in points:
        closest = ref_points[0]
        for ref in ref_points:
            if distance(ref, p) < distance(closest, p):
                closest = ref
        for g in groups:
            if g[0] == closest:
                g.append(p)
    for g in groups:
        if len(g) > 1:
            g[0] = centroid(g[1:])
    return groups
def k_meansClusterFull(refs, points):
    res = k_meansCluster(points, refs)
    new_refs = []
    for i in range(len(res)):
        new_refs.append(res[i][0])
    while refs != new_refs:
        res = k_meansCluster(points, new_refs)
        refs = new_refs
        new_refs = []
        for i in range(len(res)):
            new_refs.append(res[i][0])
    
    # res now has the groups with the centroids
    groups = []
    for i in range(len(refs)):
        groups.append([])
    for i in range(len(points)):
        for j in range(len(groups)):
            if points[i] in res[j]:
                groups[j].append("U" + str(i + 1))
    return groups
    
def rm_dup(lst):
    res = []
    [res.append(x) for x in lst if x not in res]
    return res
    
# ---------------------------------------------------------------------------------
    
def main():
    # file = open("Z:\CS 773 Data Mining\Project\sorted-proj-data.csv")
    file = open("sorted-proj-data.csv")
    lines = file.readlines()
    
    type_one_users = []
    resources = []
    emails = []
    for i in range(1, 10):
        type_one_users.append(User("U0"+str(i)))
        resources.append(Resource("U0"+str(i)))
        emails.append(Email("U0"+str(i)))
    for i in range(10, 20):
        type_one_users.append(User("U"+str(i)))
        resources.append(Resource("U"+str(i)))
        emails.append(Email("U"+str(i)))

    

    
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
        elif parts[0] == '2':
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
        elif parts[0] == '3':
            uid = parts[1]
            machine = parts[2]
            raw_date = parts[3]
            raw_st = parts[4]
            program = parts[5]
            em = parts[6]
            sent_rec = parts[7]
            bites = parts[8] # since bytes is a reserved word
            attachments = parts[9]
            start_time = datetime.datetime(int(raw_date[4:]) + 2000, int(raw_date[0:2]), int(raw_date[2:4]),
            int(raw_st[0:2]), int(raw_st[2:4]), int(raw_st[4:]))

            email = emails[int(uid[1:]) - 1]
            email.addMachine(machine)
            email.addStartTime(start_time)
            email.addEmailProgram(program)
            email.addBytes(bites)
            email.incCount()
            email.addEmail(em + ":" + sent_rec)
      
                
        
    print("Average time worked:")
    average_time_worked = []
    for user in type_one_users:
        with_outliers = user.total_time / user.num_records
        without_outliers = int(sum(removeOutliers(user.times)) / user.num_records)
        average_time_worked.append(without_outliers)
        print(user.user_id + ": " + secondsToFormattedTime(with_outliers) + ", " + str(secondsToFormattedTime(without_outliers)))
        
    print("Longest day:")
    longest_day = []
    for user in type_one_users:
        longest_day.append(user.longest_day)
        print(user.user_id + ": " + secondsToFormattedTime(user.longest_day))

    print("Average processes, average:")
    for user in type_one_users:
        without_outliers = sum(removeOutliers(user.ave_procs)) / len(removeOutliers(user.ave_procs))
        print(user.user_id + ": " + str(user.total_ave_proc / user.num_records) + ", " + str(without_outliers))

    print("Max processes, average:")
    for user in type_one_users:
        without_outliers = sum(removeOutliers(user.max_proc_l)) / len(removeOutliers(user.max_proc_l))
        print(user.user_id + ": " + str(user.total_max_proc / user.num_records) + ", " + str(without_outliers))

    print("Max processes, max:")
    for user in type_one_users:
        print(user.user_id + ": " + str(user.max_proc))

    print("Average characters typed:")
    for user in type_one_users:
        without_outliers = sum(removeOutliers(user.chars_typed)) / len(removeOutliers(user.chars_typed))
        print(user.user_id + ": " + str(user.total_chars_typed / user.num_records) + ", " + str(without_outliers))

    print("Average CPU:")
    for user in type_one_users:
        without_outliers = sum(removeOutliers(user.cpus)) / len(removeOutliers(user.cpus))
        print(user.user_id + ": " + str(user.total_cpu / user.num_records) + ", " + str(without_outliers))

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
    average_start_time = []
    for user in type_one_users:
        s = 0
        stimes = 0
        start_times_seconds = []
        for st in user.logins:
            tmpdt = datetime.datetime(st.year, st.month, st.day, 0, 0, 0)
            diff = (st - tmpdt).total_seconds() # gets the time without day, month or year attached
            start_times_seconds.append(diff)
            stimes += diff
            s += 1
        l = removeOutliers(start_times_seconds)
        average_start_time.append(int(sum(l) / len(l)))
        print(user.user_id + ": " + str(secondsToFormattedTime(stimes / s)) + ", " + str(secondsToFormattedTime(sum(l) / len(l))))


    print("Average end time:")
    average_end_time = []
    for user in type_one_users:
        s = 0
        etimes = 0
        end_times_seconds = []
        for et in user.logouts:
            tmpdt = tmpdt = datetime.datetime(et.year, et.month, et.day, 0, 0, 0)
            diff = (et - tmpdt).total_seconds()
            end_times_seconds.append(diff)
            etimes += diff
            s += 1
        l = removeOutliers(end_times_seconds)
        average_end_time.append(int(sum(l) / len(l)))
        print(user.user_id + ": " + str(secondsToFormattedTime(etimes / s)) + ", " + str(secondsToFormattedTime(sum(l) / len(l))))


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

    print("Days worked")
    for user in type_one_users:
        print(user.user_id + ":")
        print("\t" + "Sunday: " + str(user.days_worked[6]))
        print("\t" + "Monday: " + str(user.days_worked[0]))
        print("\t" + "Tuesday: " + str(user.days_worked[1]))
        print("\t" + "Wednesday: " + str(user.days_worked[2]))
        print("\t" + "Thursday: " + str(user.days_worked[3]))
        print("\t" + "Friday: " + str(user.days_worked[4]))
        print("\t" + "Saturday: " + str(user.days_worked[5]))
        
    print("\n\nAverage pages printed, per user")
    pages_printed = []
    [pages_printed.append([x.split(':')[1] for x in r.printers]) for r in resources]
    [print(str(sum([int(x) for x in p]) / len(p)) + ", " + str(sum(removeOutliers([int(x) for x in p])) / len(removeOutliers([int(x) for x in p])))) for p in pages_printed]

    print("\n\n\n\n\n\n\n\nEnd of statistics...beginning of correlation and clustering\n\n\n")
    
    
    print("Cluster based on login information\n\n\n")
    
    points = []
    for i in range(len(type_one_users)):
        l = []
        l.append(average_time_worked[i])
        l.append(longest_day[i])
        l.append(average_start_time[i])
        l.append(average_end_time[i])
        points.append(l)
    points = normalize(points)
    
    print("k=2\n")
    
    refs = [[0,0,0,0],[1,1,1,1]]
    print(k_meansClusterFull(refs, points))
    
    print("k=3\n")
    refs = [[0,0,0,0],[.5,.5,.5,.5],[1,1,1,1]]
    print(k_meansClusterFull(refs, points))
    
    print("k=4\n")
    refs = [[0,0,0,0],[.3,.3,.3,.3],[.6,.6,.6,.6],[1,1,1,1]]
    print(k_meansClusterFull(refs, points))
    
    print("k=5\n")
    refs = [[0,0,0,0],[.25,.25,.25,.25],[.5,.5,.5,.5],[.75,.75,.75,.75],[1,1,1,1]]
    print(k_meansClusterFull(refs, points))
    
    points = []
    for u in type_one_users:
        l = []
        l.append(sum(removeOutliers(u.ave_procs)) / len(removeOutliers(u.ave_procs)))
        l.append(sum(removeOutliers(u.max_proc_l)) / len(removeOutliers(u.max_proc_l)))
        l.append(sum(removeOutliers(u.chars_typed)) / len(removeOutliers(u.chars_typed)))
        l.append(sum(removeOutliers(u.cpus)) / len(removeOutliers(u.cpus)))
        points.append(l)
    print(points)
        
    points = normalize(points)
    
    print("Cluster based on program access\n\n\n")
    
    refs = [[0,0,0,0],[1,1,1,1]]
    print("k=2\n")
    print(k_meansClusterFull(refs, points))
    
    refs = [[0,0,0,0],[.5,.5,.5,.5],[1,1,1,1]]
    print("k=3\n")
    print(k_meansClusterFull(refs, points))
    
    refs = [[0,0,0,0],[.3,.3,.3,.3],[.6,.6,.6,.6],[1,1,1,1]]
    print("k=4\n")
    print(k_meansClusterFull(refs, points))
    
    refs = [[0,0,0,0],[.25,.25,.25,.25],[.5,.5,.5,.5],[.75,.75,.75,.75],[1,1,1,1]]
    print("k=5\n")
    print(k_meansClusterFull(refs, points))
    
    FILE_CORRELATION_THRESHOLD = 0.5 
    while FILE_CORRELATION_THRESHOLD <= 1:
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
        #print("Percent Similar Matrix")
        #print(percent_similar_matrix)
        print("Percent Similar: " + str(FILE_CORRELATION_THRESHOLD * 100) + "%")

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
        FILE_CORRELATION_THRESHOLD += .1
        print()
        
    print("File accesses subsets")
    print(file_accesses)
    cnt = 1
    for f in file_accesses:
        print(f, end=": ")
        dict1 = file_accesses[f]
        for g in file_accesses:
            dict2 = file_accesses[g]
            if f != g:
                subset = True
                for key in dict1:
                    if key not in dict2:
                        subset = False
                    if key in dict2 and dict1[key] != dict2[key]:
                        subset = False
                if subset:
                    print(g, end = ", ")
        print()

    prnts = []
    [prnts.append([x.split(':')[0] for x in r.printers]) for r in resources]
    for i in range(len(prnts)):
        prnts[i] = rm_dup(prnts[i])
    [print(p) for p in prnts] # prints the printers each user used without duplicates
    
    
        
    
    
            
            
                 
	
if __name__ == "__main__":
    main()
