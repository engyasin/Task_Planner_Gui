# -*- coding: utf-8 -*-
"""
Created on :
2016-06-18 11:48:33.352000

@author: Yasin_Yousif
"""

import sys, MySQLdb
from lgls import *

from PyQt4 import QtSql,QtGui

#from helper_funcs_lgls import *
#from Tasks import *

# Paragraph-vv
# creat Connection
def creatConnection():
    db = QtSql.QSqlDatabase.addDatabase('QMYSQL')
    db.setHostName('127.0.0.1')
    db.setDatabaseName('lgls')
    db.setUserName('root')
    db.setPassword('roben')
    db.open()
    print (db.lastError().text())

    return True

# Paragraph-yy

class MyForm(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent )
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # Table Model
        self.model = QtSql.QSqlTableModel(self)
        self.model.setTable('Tasks')
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.model.select()
        self.query = QtSql.QSqlQuery()
        # init Timesheet Model
        # change font
        fnt_obj = QtGui.QFont()
        fnt_obj.setPointSize(12);
        fnt_obj.setFamily('Arial');
        fnt_obj.setBold(1)

        self.modelq = QtSql.QSqlQueryModel(self)
        self.modelq.setQuery("select * from Timesheet")
        self.ui.tableView.setModel(self.modelq)
        self.ui.tableView.setFont(fnt_obj)
        self.ui.tableView.resizeColumnsToContents()

        # init combo box , and every thing:
        self.ui.comboBox.addItem('Works')
        self.ui.comboBox.addItem('Routin')
        self.ui.comboBox.addItem('Rest')
        self.ui.comboBox.addItem('Else')

        self.today_tasks = [];
        self.hardnesslist = [];

        for i in range(1,6):
            self.ui.hardness.addItem(str(i))

        # init List-View
        # chooseClass()
        QtCore.QObject.connect(self.ui.comboBox,
                               QtCore.SIGNAL('currentIndexChanged(QString)'),
                               self.chooseClass)

        QtCore.QObject.connect(self.ui.addnewtaskbtn,
                               QtCore.SIGNAL('clicked()'),
                               self.addNewTask)

        QtCore.QObject.connect(self.ui.deletetask,
                               QtCore.SIGNAL('clicked()'),
                               self.deletetask)

        QtCore.QObject.connect(self.ui.listWidget,
                               QtCore.SIGNAL('itemSelectionChanged()'),
                               self.editTask)

        QtCore.QObject.connect(self.ui.dotoday,
                               QtCore.SIGNAL('clicked()'),
                               self.orderTask)

        QtCore.QObject.connect(self.ui.tabWidget,
                               QtCore.SIGNAL('currentChanged(int)'),
                               self.initTableModel)

        QtCore.QObject.connect(self.ui.listhours,
                               QtCore.SIGNAL('currentRowChanged (int)'),
                               self.sycnListsHP)

        QtCore.QObject.connect(self.ui.listhardness,
                               QtCore.SIGNAL('currentRowChanged (int)'),
                               self.sycnListsPH)


        # producitivity buttons:
        QtCore.QObject.connect(self.ui.super5,
                    QtCore.SIGNAL('clicked()'),
                               lambda: self.setProdHours(5))

        QtCore.QObject.connect(self.ui.up4,
                    QtCore.SIGNAL('clicked()'),
                               lambda: self.setProdHours(4))

        QtCore.QObject.connect(self.ui.medium3,
                    QtCore.SIGNAL('clicked()'),
                               lambda: self.setProdHours(3))

        QtCore.QObject.connect(self.ui.down2,
                    QtCore.SIGNAL('clicked()'),
                               lambda: self.setProdHours(2))

        QtCore.QObject.connect(self.ui.tired1,
                    QtCore.SIGNAL('clicked()'),
                               lambda: self.setProdHours(1))

        QtCore.QObject.connect(self.ui.asleep0,
                    QtCore.SIGNAL('clicked()'),
                               lambda: self.setProdHours(0))

        # plan the day..
        QtCore.QObject.connect(self.ui.plan_the_day,
                    QtCore.SIGNAL('clicked()'),
                               self.plan_the_day)

        self.chooseClass()


    def chooseClass(self):
        self.ui.listWidget.clear()
#       chosenTaskClass = str(Qtext)
        chosenTaskClass = str(self.ui.comboBox.itemText(
            self.ui.comboBox.currentIndex()))
        self.model.setFilter("Task_class='%s'"%chosenTaskClass)
        # self.model.select()
        for d in range(self.model.rowCount()):
            Task = self.model.record(d)
            self.ui.listWidget.addItem(Task.value('Task_title').toString())


    def addNewTask(self):

        if self.scan4Task():
            self.updateDbWithNewTask(self.current_task)
            self.chooseClass()

    def scan4Task(self):
        try:
            # Take all Task properties:
            Task_class = self.ui.comboBox.itemText(
                self.ui.comboBox.currentIndex())
            Task_title = self.ui.tasktitle.text()
            Task_shortcut = self.ui.taskshortcut.text()
            isurg = int(self.ui.isurgent.isChecked())
            isimp = int(self.ui.isimportant.isChecked())
            isInst = int(not(self.ui.isextended_g.isChecked()))
            if not(isInst):
                Task_period = int(self.ui.period.text())
                Task_start = self.ui.starttime.time().toString()
                Task_end = self.ui.endtime.time().toString()
            else:
                Task_period = 1;
                Task_start = self.ui.starttime.time().toString();
                Task_end = Task_start;
            Task_hardness = self.ui.hardness.currentIndex()+1;
            Task_notes = self.ui.tasknotes.toPlainText()
            new_task_list = [str(Task_class),
                            str(Task_title),
                            str(Task_shortcut),
                            isurg,isimp,
                            isInst,Task_period,
                            str(Task_start),
                            str(Task_end),
                            Task_hardness,
                            str(Task_notes)]

            self.current_task = new_task_list;
            return True
        except:
            reply = QtGui.QMessageBox.warning(
                self, 'Warning',
                "Please enter a valid values in all the inputs!",
                QtGui.QMessageBox.Ok,
                QtGui.QMessageBox.Ok)
            return False

#        query = QtSql.QSqlQuery()
#        query.exec_("insert into Tasks values {}".format( tuple(new_task_list)))


    def updateDbWithNewTask(self,new_task):
        # query = QtSql.QSqlQuery()
        print new_task
        # w = input('paues: ')

#       ntask = QtSql.QSqlRecord();
#       ntask.setValue("Task_class", new_task[0]);
#       ntask.setValue("Task_title", new_task[1]);
#       ntask.setValue("Task_shortcut", new_task[2]);
#       ntask.setValue("Task_isUrg", new_task[3]);
#       ntask.setValue("Task_isImp", new_task[4]);
#       ntask.setValue("Task_isInsatnce", new_task[5]);
#       ntask.setValue("Task_period", new_task[6]);
#       ntask.setValue("Task_start", new_task[7]);
#       ntask.setValue("Task_end", new_task[8]);
#       ntask.setValue("Task_hardness", new_task[9]);
#       ntask.setValue("Task_notes", new_task[10]);


        #print ntask
        # print '--up is record? -----'
        print self.model.rowCount()
        res = self.query.exec_("insert into tasks"+\
                         " values{}".format(tuple(new_task)))
        # res = self.model.updateRowInTable(0,ntask)

        if res:
            print '------tasks written --------'
        else:
            print self.model.lastError().text()
            print 'error in inserting rows : rolling back'
            self.query.exec_("rollback")


    def initTableModel(self):
        ind = self.ui.tabWidget.currentIndex()
        if ind==0:
            self.initFirstTab()
        elif ind==1 :
            self.initSecondTab()
        elif ind==2:
            if not(len(self.hardnesslist)):
                self.initSecondTab()

#           self.modelq = QtSql.QSqlQueryModel(self)
#           self.model.setQuery("select * from Timesheet")
#           self.ui.tableView.setModel(self.modelq)
            pass
        print '---ind 4 currenttab is---'+str(ind)


    def orderTask(self):
        self.scan4Task();
        self.today_tasks.append(self.current_task)
        self.ui.todaytasks.addItem(self.current_task[1])
        pass

    def editTask(self):
        task2edit = str(self.ui.listWidget.currentItem().text())

        self.model.setFilter("Task_title='%s'"%task2edit)
        # self.model.select()

        try:
            Task = self.model.record(0)
            self.ui.tasktitle.setText(Task.value('Task_title').toString())
            self.ui.taskshortcut.setText(Task.value('Task_shortcut').toString())
            self.ui.isurgent.setCheckState(Task.value('Task_isUrg').toBool()*2)
            self.ui.isimportant.setCheckState(
                Task.value('Task_isImp').toBool()*2)
            inst = Task.value('Task_isInsatnce').toBool()*2;
            self.ui.isextended_g.setChecked(not(inst))
            self.ui.starttime.setTime(Task.value('Task_start').toTime())
            hardness = Task.value('Task_hardness').toInt()[0];
            self.ui.hardness.setCurrentIndex(hardness-1)
            self.ui.tasknotes.setPlainText(Task.value('Task_notes').toString())
            if not(inst):
                self.ui.period.setText(Task.value('Task_period').toString())
                self.ui.endtime.setTime(Task.value('Task_end').toTime())

        except:
            pass
            print 'sth wrong'


    def setProdHours(self,prod):
        row = self.ui.listhours.currentRow()
        hour = str(self.ui.listhours.currentItem().text());
        print hour
        self.ui.listhardness.takeItem(row)
        self.ui.listhardness.insertItem(row,str(prod))
        self.hardnesslist[row] = prod
        res = self.query.exec_(
            "update prodictivty "+\
            "set hardness={0} where hours='{1}'".format(int(prod),hour))

        if res:
            print '------data written --------'
        else:
            print self.model.lastError().text()
            print 'error in Updating rows : rolling back'
            self.query.exec_("rollback")
        pass


    def sycnListsHP(self):
        row = self.ui.listhours.currentRow()
        self.ui.listhardness.setCurrentRow(row)

    def sycnListsPH(self):
        row = self.ui.listhardness.currentRow()
        self.ui.listhours.setCurrentRow(row)

    def deletetask(self):
        try:
            task2delet = str(self.ui.listWidget.currentItem().text())
            # confime message
            reply = QtGui.QMessageBox.question(
                self, 'Warning',
            "Are you sure you want to delete task?",
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.Cancel,
                QtGui.QMessageBox.Cancel)
            if reply == QtGui.QMessageBox.Yes:
                res = self.query.exec_("delete from tasks where Task_title='%s'"%task2delet)
                if res:
                    print 'deleting sucsess'
                else :
                    print 'sth went wrong in deletion -- rolling back'
                    self.query.exec_("rollback")
                self.chooseClass()
            else:
                pass
        except:
            try:
                row2delet = self.ui.todaytasks.currentRow()
                self.ui.todaytasks.takeItem(row2delet)
                self.today_tasks.pop(row2delet)
                print " --- {} task for today---".format(len(self.today_tasks))
            except:
                pass
            pass

    def initFirstTab(self):
        self.model.clear()
        self.model.setTable('Tasks')
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.model.select()

    def initSecondTab(self):
        self.model.clear()
        self.model.setTable('prodictivty')
        self.model.select()
        if  not(self.ui.listhours.count()):
            for d in range(self.model.rowCount()):
                Hour_mode = self.model.record(d)
                self.ui.listhours.addItem(
                    Hour_mode.value('hours').toString())
                self.ui.listhardness.addItem(
                    Hour_mode.value('hardness').toString())
                self.hardnesslist.append(
                    Hour_mode.value('hardness').toInt()[0])


    def plan_the_day(self):

        Tasks_planned = self.planahead();
        if len(Tasks_planned):
            self.showTimesheet(Tasks_planned)


    def showTimesheet(self,Tasks_planned):
        """
        Show the tasks in timesheet
        and insert rows in database..
        Warning: no undos once created..

        YY_2016
        """

        import time

        new_day = [0]*24

        timeOfSleep = 0;
        for i,h in enumerate(self.hardnesslist):
            if not(h):
                timeOfSleep += 1;
                new_day[i] = 'Sleep.. Zzz'


        for T in Tasks_planned:
            if not(T.isinst):
                time_str = str(int(T.s_task/60)) + ':' + str(int(T.s_task%60));
                str2add = '[ '+' - '+T.shortcut+' '+time_str+'->'
                if not(new_day[int(T.s_task/60)]):
                    new_day[T.s_task/60] = str2add;
                else:
                    try:
                        currt = int(new_day[T.s_task/60][-4:-2]);
                    except ValueError :
                        currt = int(new_day[T.s_task/60][-3:-2]);

                    if currt > (T.s_task%60):
                        new_day[T.s_task/60]=str2add+new_day[T.s_task/60]
                    else:
                        new_day[T.s_task/60] += str2add;
                endt = T.s_task + T.period;
                time_str = str(endt/60) + ':' + str(endt%60);
                str2add = '<--'+T.shortcut+' - '+time_str+' ]'
                if not(new_day[endt/60]):
                    new_day[endt/60] = str2add;
                else:
                    try:
                        currt = int(new_day[endt/60][-4:-2]);
                    except ValueError :
                        currt = int(new_day[endt/60][-3:-2]);

                    if currt > (endt%60):
                        new_day[endt/60]=str2add+new_day[endt/60]
                    else:
                        new_day[endt/60] += str2add;

                for x in range((T.s_task/60)+1,(endt/60)):
                    new_day[x] = '--- '+T.title+' ---';
            else:
                # inst Tasks
                time_str = str(T.s_task/60) + ':' + str(T.s_task%60);
                str2add = '[ '+'- '+T.shortcut+time_str+' ]'
                if not(new_day[T.s_task/60]):
                    new_day[T.s_task/60] = str2add;
                else:
                    try:
                        currt = int(new_day[T.s_task/60][-4:-2]);
                    except ValueError :
                        currt = 0;

                    if currt > (T.s_task%60):
                        new_day[T.s_task/60]=str2add+new_day[T.s_task/60]
                    else:
                        new_day[T.s_task/60] += str2add;

            pass
        pass

        timeOfWork = sum([T.period for T in Tasks_planned])/60.0
        spareTime = 24 - timeOfSleep - timeOfWork;

        msg = 'You do have -\n'' - '+str(timeOfWork)+' hour of work..\n'+\
            ' - '+ str(timeOfSleep)+' hour of sleep..\n'+\
            ' - '+ str(spareTime)+' of spare time..';

        QtGui.QMessageBox.information(self,'Info',msg,
                                    QtGui.QMessageBox.Ok,
                                    QtGui.QMessageBox.Ok)
        for i in range(len(new_day)):
            if not(new_day[i]):
                new_day[i] = '-- Empty Time [???]-'

        # adjust and prpare to display..
        new_day = new_day[8:] + new_day[:8];
        new_day = [time.strftime("%a - %d%b")] + new_day;

        res = self.query.exec_("insert into timesheet"+\
                         " values{}".format(tuple(new_day)))
        # res = self.model.updateRowInTable(0,ntask)

        if res:
            print '------ Plan written --------'
            self.modelq.setQuery("select * from Timesheet")
            self.ui.tableView.setModel(self.modelq)
#           for i,x in enumerate(new_day):
#               self.ui.tableView.setColumnWidth(i,len(x)*6)

        else:
            print 'error in inserting rows : rolling back'
            self.query.exec_("rollback")

        print '----new_day----'
        print new_day

    def planahead(self):
        """
        orgnize the hardest , the important,
        the urgent, respictivly..
        in the best time of the day to achive.
        """



        Tasks_list = []
        for T in self.today_tasks:
            if T[5]:
                pass
            else:
                Tasks_list.append(T)

        # hardest first
        Tasks_list  = sorted(Tasks_list , key=lambda Task : Task[9],
                             reverse = True)

        # now we need to take first the important then the urget
        # , but execute reverse

        Tasks_list  = sorted(Tasks_list , key=lambda Task : Task[3],
                             reverse = True)
        Tasks_list  = sorted(Tasks_list , key=lambda Task : Task[4],
                             reverse = True)


        # turn into classes:
        for i,T in enumerate(Tasks_list):
            Tasks_list[i] = self.Task(T)

        hardness_details = [];
        for h in self.hardnesslist  :
            # [hardnes, hour , diff of hardness]
            hardness_details += [h]*60

        hardness_details = [[1]*1440,hardness_details,hardness_details];

        while True:
            [ret,hardness_result,Tasks_planned] = self.schedule_tasks(
                Tasks_list, hardness_details)
            if ret:
                break

            reply = QtGui.QMessageBox.question(
                    self, 'Confirm',
                "subtract 1 of hardness or edit tasks manually (Cancel)?",
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.Cancel,
                    QtGui.QMessageBox.Cancel)

            if reply == QtGui.QMessageBox.Yes:
                isbottomed = 1;
                for i,T in enumerate(Tasks_list):
                    if T.hardness > 1 :
                        isbottomed = 0;
                        Tasks_list[i].hardness -= 1;
                if isbottomed:
                    msg = 'The limit is reashed, you may'+\
                            ' consider decreasing the periods';
                    QtGui.QMessageBox.information(self,'Note',msg,
                                                QtGui.QMessageBox.Ok,
                                                QtGui.QMessageBox.Ok)
                    # out_now
                    return []
            else:
                return []

        for T in self.today_tasks:
            if T[5]:
                Task = self.Task(T)
                Tasks_planned.append(Task)

        return Tasks_planned




    def schedule_tasks (self,Tasks_list,hardness_details):
        """
        func to fit the tasks..
        YY_2016
        """
        import numpy as np
        hardness_details = np.array(hardness_details)
        for i,T in enumerate(Tasks_list):
            best_diff = -1;
            # hit with availabilty line
            hardness_details[1] = hardness_details[0] * hardness_details[1]
            # start the loop for perfect place for Task :
            s_jmp = T.starttime;
            for s in range(T.starttime,T.endtime - T.period):
                if s_jmp > (T.endtime - T.period):
                    break
                # check if the period able to work in.
                notperiodable = (hardness_details[1][s_jmp:s_jmp+T.period]<T.hardness)
                if notperiodable.any():
                    s_jmp += len(notperiodable)- (notperiodable[::-1].argmax());
                    # s_jmp += notperiodable.argmax()+1;
                    continue
                    # to check again..untile period is good.
                h_diff=(hardness_details[1][s_jmp:s_jmp+T.period]-T.hardness).sum()
                if h_diff > best_diff:
                    best_diff = h_diff;
                    s_still = s_jmp;
                    hardness_details[0][:] = 1;
                    hardness_details[0][s_jmp:s_jmp+T.period] = 0;
                s_jmp += 1;

            if best_diff == -1 :
                # Task didn't fit.
                # ask the user to edit ..
                # or just return , False as op stat..
                print "Sorry, some task didn\'t fit .."
                return False,hardness_details,Tasks_list
            else:
                # the task find a space..
                print " Task: " + T.title + " scehualled !"
                print " at this time: " + str(s_still/60.0)
                Tasks_list[i].s_task = s_still;
                hardness_details[2][s_still:s_still+T.period] -= T.hardness;

                pass
        # here we end
        return True, hardness_details, Tasks_list

## Calsses declreation:
    class Task :
        """
        calss for cearting new tasks
        """
        def __init__(self,T=[]):
            if len(T)==11:
                self.taskclass = str(T[0])
                self.title = str(T[1])
                self.shortcut = str(T[2])
                self.isurg = bool(T[3])
                self.isimp = bool(T[4])
                self.isinst = bool(T[5])
                self.period = int(T[6])
                self.starttime = int(T[7][:2])*60 + int(T[7][3:5])
                self.endtime = int(T[8][:2])*60 + int(T[8][3:5])
                self.hardness = int(T[9])
                self.notes = str(T[10])
                if T[5]:
                    self.s_task = int(T[7][:2])*60 + int(T[7][3:5])
            else:
                pass



#        query.exec_("UPDATE Tasks set Task_class '{0}',Task_title '{1}' ,\
#                                       Task_shortcut '{2}' ,\
#                                    Task_type {3}{4},\
#                                    Task_isInsatnce {5},\
#                                    Task_period {6},\
#                                    Task_start '{7}',\
#                                    Task_end '{8}',\
#                                    Task_hardness {9},\
#                                    Task_notes '{10}'".format(new_task))
#        query.finish()

# Paragraph-zz
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    if not creatConnection():
        sys.exit(1)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())


