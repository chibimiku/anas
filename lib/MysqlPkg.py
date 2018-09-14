import mysql.connector

class MysqlPkg:
    def __init__(self, config):
        self._config = config
        self.cnx = mysql.connector.connect(**config)
        self.cursor = self.cnx.cursor()
        
    def close(self):
        self.cnx.close()
        
    def fetch_first(self, sql, data = []):
        self.cursor.execute(sql, data)
        row = self.cursor.fetchone()
        columns = self.cursor.description
        result_row = {columns[index][0]:column for index, column in enumerate(row)}
        return result_row
        
    def query(self, sql, data = []):
        self.cursor.execute(sql, data)
        results = self.cursor.fetchall()
        columns = self.cursor.description
        return_list = []
        for value in results:
            row = {columns[index][0]:column for index, column in enumerate(value)}
            return_list.append(self._fix_row(row))
        return results

    def insert_update(self, table_name, in_data, in_data_on_dup = {}):
        self.insert(table_name, in_data, ignore = True)
        
    #TODO: 更新 ON DUPLICATE 时候的处理
    def insert(self, table_name, in_data, ignore = False, on_update = False, in_data_on_dup = {}):
        #根据输入in_data拼接
        insert_stmt_arr = ['INSERT INTO ' , table_name , ' (']
        if(ignore):
            insert_stmt_arr = ['INSERT IGNORE INTO ' , table_name , ' (']
        keys_arr = []
        values_arr = []
        values_type_arr = []
        for k,v in in_data.items():
            keys_arr.append(k)
            values_arr.append(v)
            values_type_arr.append('%s')
        
        insert_stmt_arr.append(",".join(keys_arr))
        insert_stmt_arr.append(" ) VALUES (")
        insert_stmt_arr.append(",".join(values_type_arr))
        insert_stmt_arr.append(")")
        self._execute("".join(insert_stmt_arr), values_arr)
        
    def update(self, table_name, in_data, cond, cond_data = []):
        update_str = ''
        tmp = []
        tmp_value_arr = [] 
        for (k, v) in in_data.items():
            v = str(v)
            tmp.append("=".join([k,'%s']))
            tmp_value_arr.append(v)
        #sql = 'UPDATE %s SET %s WHERE %s' % (tablename, update_str, condition)
        sql = "".join(['UPDATE ', table_name, ' SET ', ",".join(tmp), ' WHERE ', cond])
        exec_var = tmp_value_arr + cond_data
        exec_result = self._execute(sql, exec_var)
        return exec_result

    def insert_id(self):
        return self.cursor.lastrowid
        
    def _execute(self, sql, data = {}):
        try:
            rs = self.cursor.execute(sql, data)
            self.cnx.commit()
            return rs
        except Exception as e:
            print (e)
            return False
            
    def _fix_row(self, rs):
        for k,v in rs.items():
            if(isinstance(v, bytearray) or isinstance(v, bytes)):
                rs[k] = v.decode(self._config["charset"])
        return rs