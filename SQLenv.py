import numpy as np
import random,string

import const

param_n_tables = [2,5]
param_n_columns = [2,5]
param_n_rows = [2,10]


class SQLenv():

    def __init__(self):
        self.n_tables = np.random.randint(param_n_tables[0], param_n_tables[1])

        self.state = None
        self.termination = False

        self.schema = self._createDBSstructure()
        self.data = self._populateDBS()
        self.originalquery = self._generateQuery()

    def _createDBSstructure(self):
        schema = []
        for _ in range(self.n_tables-1):
            n_columns = np.random.randint(param_n_columns[0], param_n_columns[1])
            column_types = np.random.choice(const.types, size=n_columns, p=const.types_prob)
            schema.append(column_types)
        schema.append(np.array([const.t_string]))

        return schema

    def _populateDBS(self):
        data = {}

        for i in range(self.n_tables-1):
            tabledata=[]
            n_rows = np.random.randint(param_n_rows[0],param_n_rows[1])
            for _ in range(n_rows):
                rowdata=[]
                for k in range(len(self.schema[i])):
                    if self.schema[i][k] == const.t_int: rowdata.append(np.random.randint(1,100))
                    elif self.schema[i][k] == const.t_string: rowdata.append(self._get_random_string(np.random.randint(3,8)))
                    elif self.schema[i][k] == const.t_datetime: rowdata.append("04/12/2020 12:00:00 AM")
                tabledata.append(rowdata)
            data[self._get_tablename(i)] = tabledata

        data[self._get_tablename(self.n_tables-1)] = [['flag']]

        return data

    #create the flag table

    def _get_tablename(self,i):
        return "Table"+str(i)

    def _get_columnname(self,i):
        return "Column"+str(i)

    def _get_random_string(self,length):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for _ in range(length))
        return result_str

    def _generateQuery(self):
        randomtable = np.random.randint(0,self.n_tables-1)
        randomtable_cols = len(self.schema[randomtable])
        randomcolumn = np.random.randint(0,randomtable_cols)

        query = 'empty'
        #instead of asterisk sometimes values
        value_to_ask = "*"
        column_to_ask = np.random.randint(0,randomtable_cols)
        #print("cn to ask: "+str(column_no_ask))
        #if column_no_ask==1: value_to_ask=ColumnName(random.randint(1, column_counts[table-1]))
        templist = []
        for i in range(randomtable_cols):
            templist.append(i)
        templist.remove(randomcolumn)

        #print(templist)
        while len(templist)>column_to_ask:
            temp = random.randint(1,len(templist))
            templist.pop(temp-1)
            #print(templist)

        if column_to_ask!=randomtable_cols:
            value_to_ask=""
            for i in templist:
                value_to_ask += self._get_columnname(i)+","
            value_to_ask = value_to_ask[:-1]
        #print(value_to_ask)

        if self.schema[randomtable][randomcolumn] == const.t_int:
            querytype = random.randint(1,3)
            if querytype == 1 : query = "Select "+value_to_ask+" from " + self._get_tablename(randomtable) + " where " + self._get_columnname(randomcolumn) + "=input" + ";"
            elif querytype == 2 : query = "Select "+value_to_ask+" from " + self._get_tablename(randomtable) + " where " + self._get_columnname(randomcolumn) + "<input" + ";"
            elif querytype == 3 : query = "Select "+value_to_ask+" from " + self._get_tablename(randomtable) + " where " + self._get_columnname(randomcolumn) + ">input" + ";"
        if self.schema[randomtable][randomcolumn] == const.t_string:
            querytype = random.randint(1,4)
            if querytype == 1: query = "Select "+value_to_ask+" from " + self._get_tablename(randomtable) + " where " + self._get_columnname(randomcolumn) + "='input'" + ";"
            elif querytype == 2: query = "Select "+value_to_ask+" from " + self._get_tablename(randomtable) + " where " + self._get_columnname(randomcolumn) + "=\"input\"" + ";"
            elif querytype == 3: query = "Select "+value_to_ask+" from " + self._get_tablename(randomtable) + " where " + self._get_columnname(randomcolumn) + " like '%input%'" + ";"
            elif querytype == 4: query = "Select "+value_to_ask+" from " + self._get_tablename(randomtable) + " where " + self._get_columnname(randomcolumn) + " like \"%input%\"" + ";"
        #date type
        if self.schema[randomtable][randomcolumn] == const.t_datetime:
            querytype = random.randint(1, 2)
            if querytype == 1: query = "Select "+value_to_ask+" from " + self._get_tablename(randomtable) + " where " + self._get_columnname(randomcolumn) + " BETWEEN '04/12/2011 12:00:00 AM' AND 'input';"
            elif querytype == 2: query = "Select "+value_to_ask+" from " + self._get_tablename(randomtable) + " where " + self._get_columnname(randomcolumn) + " BETWEEN \"04/12/2011 12:00:00 AM\" AND \"input\";"

        return query
        #one valid parameter should be added randomly

    def step(self, a):
        currentquery = self.originalquery.replace("input",a)
        print('Received query: {0}'.format(currentquery))

        self.state = None
        reward = -1
        self.termination = False
        msg = ['Action performed']
        return self.state, reward, self.termination, msg

    def reset(self):
        self.state = None
        reward = 0
        self.termination = False
        msg = ['Server reset']
        return self.state,reward,self.termination,msg
