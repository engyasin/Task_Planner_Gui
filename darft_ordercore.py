#                           [str(Task_class),
#                           str(Task_title),
#                           str(Task_shortcut),
#                           isurg,isimp,
#                           isInst,Task_period,
#                           str(Task_start),
#                           str(Task_end),
#                           Task_hardness,
#                           str(Task_notes)]

from helper_funcs_lgls import *
from Tasks import *

T1 = ['Works', 'Task3c11', 'TK41', 1, 0, 0, 80, '12:00:00',
 '15:00:00', 1, 'A Formal job to test.. c0']

T2 = ['Works', 'Task3c10', 'TK40', 1, 0, 0, 80, '11:00:00',
 '16:00:00', 2, 'A Formal job to test.. c0']

T3 = ['Works', 'Task3c9', 'TK39', 1, 0, 0, 80, '10:00:00',
 '17:00:00', 3, 'A Formal job to test.. c0']

T4 = ['Works', 'Task3c8', 'TK38', 1, 1, 0, 80, '10:00:00',
 '18:00:00', 4, 'A Formal job to test.. c0']

T5 = ['Works', 'Task3c7', 'TK37', 1, 0, 0, 80, '09:00:00',
 '19:00:00', 5, 'A Formal job to test.. c0']

T6 = ['Works', 'Task3c6', 'TK36', 1, 1, 0, 80, '08:00:00',
 '19:00:00', 3, 'A Formal job to test.. c0']

T7 = ['Works', 'Task3c5', 'TK35', 1, 0, 1, 80, '07:00:00',
 '17:30:00', 5, 'A Formal job to test.. c0']

T8 = ['Works', 'Task3c4', 'TK34', 1, 0, 0, 80, '06:00:00',
 '20:00:30', 5, 'A Formal job to test.. c0']

T9 = ['Works', 'Task3c3', 'TK33', 1, 1, 0, 80, '05:00:00',
 '21:00:00', 2, 'A Formal job to test.. c0']

T10 = ['Works', 'Task3c2', 'TK32', 1, 0, 0, 80, '04:00:00',
 '22:20:00', 1, 'A Formal job to test.. c0']

T11= ['Works', 'Task3c1', 'TK31', 0, 0, 0, 80, '03:00:00',
 '23:10:00', 4, 'A Formal job to test.. c0']

#-----tasks written --------
#--ind 4 currenttab is---1

#--ind 4 currenttab is---2



T12 = ['Routin', 'Iftarc0', 'IF0', 0, 1, 0, 30, '20:00:00', '21:00:00', 1,
 'Eating in ramadan , should be short and fullfilment.c0']

T13 = ['Routin', 'Iftarc1', 'IF1', 1, 1, 1, 30, '10:00:00', '21:00:00', 2,
 'Eating in ramadan , should be short and fullfilment.c0']

T14= ['Routin', 'Iftarc2', 'IF2', 1, 0, 0, 30, '15:00:00', '21:00:00', 3,
 'Eating in ramadan , should be short and fullfilment.c0']

T15= ['Routin', 'Iftarc3', 'IF3', 1, 1, 0, 30, '15:00:00', '21:00:00', 2,
 'Eating in ramadan , should be short and fullfilment.c0']

T16= ['Routin', 'Iftarc4', 'IF4', 1, 1, 0, 30, '16:00:00', '21:00:00', 1,
 'Eating in ramadan , should be short and fullfilment.c0']

T17= ['Routin', 'Iftarc5', 'IF5', 1, 1, 0, 30, '17:00:00', '21:00:00', 4,
 'Eating in ramadan , should be short and fullfilment.c0']

#today_tasks = [ T1, T2, T3, T4, T5, T6, T7, T8, T9, T10, T11, T12, T13, T14,
#              T15, T16, T17];
#today_tasks = [  T2, T3, T4,  T11, T12,  T14]
today_tasks = [ T2, T4, T15, T10, T11, T13, T17]
# today_tasks = [T11,T6,T17]
print '======================'
print len(today_tasks)

#-----tasks written --------
#--ind 4 currenttab is---1
hardness = [0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 3, 3, 3, 2, 2, 2, 2, 3, 4, 4, 3,
            4, 3, 2]
#--ind 4 currenttab is---2
#--ind 4 currenttab is---0

Tasks_list = []
for T in today_tasks:
    if T[5]:
        pass
    else:
        Tasks_list.append(T)

#T_highst_hard = Task_list[0][9];
Tasks_list  = sorted(Tasks_list , key=lambda Task : Task[9], reverse = True)

# now we need to take first the important then the urget
# , but execute reverse

Tasks_list  = sorted(Tasks_list , key=lambda Task : Task[3], reverse = True)
Tasks_list  = sorted(Tasks_list , key=lambda Task : Task[4], reverse = True)


#print Tasks_list

# turn into lists:
for i,T in enumerate(Tasks_list):
    Tasks_list[i] = Task(T)

hardness_details = [];

for h in hardness  :
    # [hardnes, hour , diff of hardness]
    hardness_details += [h]*60

hardness_details = [[1]*1440,hardness_details,hardness_details];

# print hardness_details

# as start

y = 'y';
while True:
    [ret,hardness_result,Tasks_planned] = schedule_tasks(
        Tasks_list, hardness_details)
    if ret:
        break
    ans = input('subtract 1 of hardness or edit tasks manully?(y/n) ');
    if ans == 'y':
        isbottomed = 1;
        for i,T in enumerate(Tasks_list):
            if T.hardness > 1 :
                isbottomed = 0;
                Tasks_list[i].hardness -= 1;
        if isbottomed:
            print 'You should now change periods ,i will multiply by 0.75'
            for i,T in enumerate(Tasks_list):
                Tasks_list[i].period = int(T.period * 0.75)



for T in today_tasks:
    if T[5]:
        Task = Task(T)
        Tasks_planned.append(Task)

print '---------------------------'
print hardness_result

print '--------Total diff of hardness per hour---------'
print ((hardness_result[2].sum())-(hardness_result[1].sum()))/60.0


print '-------- while hardness average per hour---------'
print sum(hardness)/24.0
