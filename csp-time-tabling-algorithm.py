import sys

# global attributes
input_file_name = sys.argv[1]
output_file_name = sys.argv[2]
subjects = []
subject_timeslots = {}
subject_modes = {}
all_timeslots = []
rooms = []
timeslot_subjects = {}

# insert time slots to all timeslots array
def insertTimeslots(timeslots):
    for timeslot in timeslots:
        if timeslot not in all_timeslots:
            all_timeslots.append(timeslot)

# read from input file
def readFromInputFile():
    fo = open(input_file_name, "r")
    lines = fo.readlines()
    fo.close()

    for line in lines[:-1]:
        subject, mode, *timeslots = line.strip().split(",")
        while '' in timeslots: timeslots.remove('')
        subjects.append(subject)
        subject_timeslots[subject] = timeslots
        subject_modes[subject] = mode
        insertTimeslots(timeslots)

    rooms.extend(lines[-1].strip().split(","))
    while '' in rooms: rooms.remove('')

    for timeslot in all_timeslots: 
        timeslot_subjects[timeslot] = []

# write to output file
def writeToOutputFile():
    fo = open(output_file_name, "w")
    for timeslot in timeslot_subjects.keys():
        i = 0
        for subject in timeslot_subjects[timeslot]:
            if subject != -1:
                fo.write(subject+", "+timeslot+", R"+ str(i+1)+"\n")
            i += 1
    fo.close()

def assignTimeslot(subject):
    # check whether a timeslot is assigned to the subject
    assigned = False
    for timeslot in timeslot_subjects.keys():
        if subject in timeslot_subjects[timeslot]:
            assigned = True
    
    # if not, assign the first possible timeslot
    if assigned == False:
        for timeslot in subject_timeslots[subject]:
            if subject_modes[subject] == "c" and len(timeslot_subjects[timeslot]) < 1:
                timeslot_subjects[timeslot].append(subject)
                return True
            elif subject_modes[subject] == "o" and len(timeslot_subjects[timeslot]) < len(rooms):
                state = True
                for s in timeslot_subjects[timeslot]:
                    if s != subject and subject_modes[s] == "c":
                        state = False
                        break
                if state:
                    timeslot_subjects[timeslot].append(subject)
                    return True

    # if yes, assign the next possible timeslot
    if assigned == True:
        reset = False
        for timeslot in subject_timeslots[subject]:
            if reset == False and subject in timeslot_subjects[timeslot]:
                timeslot_subjects[timeslot].remove(subject)
                reset = True
                continue
            if reset == True:
                if subject_modes[subject] == "c" and len(timeslot_subjects[timeslot]) < 1:
                    timeslot_subjects[timeslot].append(subject)
                    return True
                elif subject_modes[subject] == "o" and len(timeslot_subjects[timeslot]) < len(rooms):
                    state = True
                    for s in timeslot_subjects[timeslot]:
                        if s != subject and subject_modes[s] == "c":
                            state = False
                            break
                    if state:
                        timeslot_subjects[timeslot].append(subject)
                        return True

    # else return false
    return False

# set a timeslot for subject
def setSubject(i):
    if i >= len(subjects): 
        return
    else:
        subject = subjects[i]
        # if can be set go to next subject
        if assignTimeslot(subject):
            setSubject(i+1)
        # if can't be set go to previous subject
        else:
            setSubject(i-1)
        return

readFromInputFile()
try:
    setSubject(0)
except:
    print("Can't assign a time table!")
else:
    writeToOutputFile()
    print("Time table assigned successfully!")