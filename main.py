import sys
import SQLiteHelper
import Diff

def HelpInfo():
    print '[Expected database file path] [Actual database file path] [Ignore list]'
    print 'Ignore tables with indicated columns:'
    print '\t[TableName1:IgnoreColumn1,IgnoreColumn2] [TableName2:IgnoreColumn1,IgnoreColumn2]'
    print 'Ignore all table:'
    print '\t[TableName3]'

if len(sys.argv) < 2 or len(sys.argv) == 2 and sys.argv[1] == '--help':
    HelpInfo()
    exit()

expected = SQLiteHelper.SQLiteHelper(sys.argv[1]) 
actual = SQLiteHelper.SQLiteHelper(sys.argv[2]) 
    
# Get same table between two DB
expectedTableName = expected.GetAllTableNames()
actualTableName = actual.GetAllTableNames()
tableNames = None
if expectedTableName != actualTableName:
    tableNames = [i for i in actualTableName if i in expectedTableName]
else:
    tableNames = expectedTableName
tableNames = [i[0] for i in tableNames]

def PrintCompareResult(tableName):
    print "\n***Start to compare table [" + tableName + "]***"
    print "---Compare schema---"
    diff = Diff.Diff(expected.GetTableSchemaInfo(tableName), actual.GetTableSchemaInfo(tableName))
    print diff.OutputResult()
        
    print "---Compare data---"
    diff = Diff.Diff(expected.GetDataFromTable(tableName), actual.GetDataFromTable(tableName))
    print diff.OutputResult()
    
# Compare two DB without ignored tables
if len(sys.argv) == 3:
    print "***Start to compare the following tables***\n" + ', '.join(tableNames) + "\n"
    
    # Compare DB schema and data
    for tableName in tableNames:
        PrintCompareResult(tableName)
    exit()
    
# Compare two DB with ignored tables and columns
if len(sys.argv) > 3:
    ignoreList = sys.argv[3:]
    ignoreDic = {}
    for i in ignoreList:
        if ':' in i:
            ignoreDic[i.split(':')[0]] = i.split(':')[1]
        else:
            ignoreDic[i] = ''
    
    for tableName in tableNames:
        if tableName not in ignoreDic:
            PrintCompareResult(tableName)
        elif ignoreDic[tableName]=='':
            continue
        else:
            print "\n***Start to compare table [" + tableName + "]***"
            print "---Compare schema---"
            diff = Diff.Diff(expected.GetTableSchemaInfo(tableName), actual.GetTableSchemaInfo(tableName))
            print diff.OutputResult()
                
            print "---Compare data---"
            diff = Diff.Diff(
                             expected.GetDataFromTable(tableName, *ignoreDic[tableName].split(',')), 
                             actual.GetDataFromTable(tableName, *ignoreDic[tableName].split(',')))
            print diff.OutputResult()
            
            
            
            