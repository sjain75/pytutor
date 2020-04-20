def addToCalendar(calendar, activity, time, day):
    """ will add a specific activity with a specific time to a calendar. Calendar will be a list of lists. The outer list
    will be length 7, each indices representing a different day. Each day will be a list that contain the schedules/activities
    in tuples."""
    if (day >= 7 and day <= 0):
        print("Day is not valid!")
    tempTuple = (activity, time)
    if (calendar[day] == "nothing so far!"):
        calendar[day] = tempTuple
    else:
        calendar[day].extend(tempTuple)

sophiaCalendar = ["nothing so far!"] * 7
ericCalendar = ["nothing so far!"] * 7

addToCalendar(ericCalendar, "Study cs!", "1:00 PM", 1)
print(ericCalendar)

# Will be mutable. Figure this out tomorrow.