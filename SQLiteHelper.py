import sqlite3

class SQLiteHelper:
    def __init__(self, databaseFilePath):
        self.databaseFilePath = databaseFilePath
    
    def GetDataFromTable(self, tableName, *ignoreColumns):
        if len(ignoreColumns) == 0:
            return self.PopulateDataFromDB("select * from %s" % tableName)
        else:
            self.GetAllColumnName(tableName)
            filteredColumns = [i for i in self.GetAllColumnName(tableName) if i not in ignoreColumns]
            return self.PopulateDataFromDB("select %s from %s" % (",".join(filteredColumns), tableName))
    
    def PopulateDataFromDB(self, searchScript):
        with sqlite3.connect(self.databaseFilePath) as con:
            cur = con.execute(searchScript)
            rows = cur.fetchall()
        return rows
    
    def GetTableSchemaInfo(self, tableName):
        return self.PopulateDataFromDB("PRAGMA table_info('%s')" % tableName)
    
    def GetAllColumnName(self, tableName):
        return [i[1] for i in self.GetTableSchemaInfo(tableName)]
    
    def GetAllTableNames(self):
        return self.PopulateDataFromDB("SELECT name FROM sqlite_master WHERE type='table'")

if __name__ == "__main__":
    db = SQLiteHelper("d:\library.db")
    print db.GetDataFromTable("probe_format_map", "probe_format", "file_format_id")
    print db.GetAllTableNames()