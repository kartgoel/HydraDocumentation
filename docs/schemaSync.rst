schema_sync
===================

This file initiates schema sync through backing up the database. It retrieves the list of tables in each database and compares the schemas between databases A and B. 

.. code-block:: python

    bkcmd="mysqldump -u "+db_b_user+" -p -h "+db_b_host+" "+db_b_name+" > DB_b_bkup.sql"
    print(bkcmd)
    try:
        process = subprocess.Popen(bkcmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if stderr:
            raise Exception(stderr.decode())
    except Exception as e:
        print("Error backing up database: "+str(e))
        exit(1)

    print("BACKUP COMPLETE. Beginning schema sync...")

    # get the list of tables in each database
    cursor_a = db_a.cursor()
    cursor_a.execute("SHOW TABLES")
    tables_a = [table[0] for table in cursor_a.fetchall()]

    cursor_b = db_b.cursor()
    cursor_b.execute("SHOW TABLES")
    tables_b = [table[0] for table in cursor_b.fetchall()]

    # loop through each table and compare the schemas
    for table in tables_a:
        if table not in tables_b:
            print("Table {} is in database A but not in database B.".format(table))
            # get the schema of the table in database A
            cursor_a.execute("SHOW CREATE TABLE {}".format(table))
            create_table = cursor_a.fetchone()[1]
            print("  A: {}".format(create_table))
            # create the table with the same schema in database B
            cursor_b.execute(create_table)
        
            # get the column names and types for the new table in database B
            cursor_b.execute("DESCRIBE {}".format(table))
            columns_b = cursor_b.fetchall()
            column_names_b = [col[0] for col in columns_b]
        
            # get the AUTO_INCREMENT and DEFAULT values for each column in database A
            cursor_a.execute("SELECT COLUMN_NAME, EXTRA, COLUMN_DEFAULT FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{}' AND TABLE_SCHEMA = '{}'".format(table, db_a_name))
            extra_defaults_a = cursor_a.fetchall()
            extra_defaults_dict_a = {col[0]: (col[1], col[2]) for col in extra_defaults_a}
        
            # add AUTO_INCREMENT and DEFAULT values to any missing columns in database B
            for col_a in columns_a:
                if col_a[0] not in column_names_b:
                    col_name = col_a[0]
                    col_type = col_a[1]
                    col_extra, col_default = extra_defaults_dict_a.get(col_name, ("", None))
                    alter_table = "ALTER TABLE {} ADD COLUMN {} {}{}{}".format(table, col_name, col_type, col_extra, " DEFAULT '{}'".format(col_default) if col_default is not None else "")
                    print("  Adding column {} to database B".format(col_name))
                    cursor_b.execute(alter_table)

            # set any missing keys in database B
            cursor_a.execute("SHOW KEYS FROM {}".format(table))
            keys_a = cursor_a.fetchall()
            key_statements = []
            for key in keys_a:
                if key[2] not in column_names_b:
                    continue
                key_type = "PRIMARY KEY" if key[2] == "PRIMARY" else "{} KEY".format(key[3])
                key_name = key[2]
                key_columns = [col[1] for col in key_statements if col[0] == key_name] + [key[2]]
                key_columns.sort(key=column_names_b.index)
                key_statements.append((key_name, key_type, key_columns))
            for key_name, key_type, key_columns in key_statements:
                add_key = "ALTER TABLE {} ADD {} ({})".format(table, key_type, ",".join(key_columns))
                print("  Adding {} {} to database B".format(key_type, key_name))
                cursor_b.execute(add_key)

            # set AUTO_INCREMENT value for table in database B
            cursor_a.execute("SELECT AUTO_INCREMENT FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{}' AND TABLE_SCHEMA = '{}'".format(table, db_a_name))
            auto_increment = cursor_a.fetchone()[0]
            if auto_increment is not None:
                set_auto_increment = "ALTER TABLE {} AUTO_INCREMENT = {}".format(table, auto_increment)
                cursor_b.execute(set_auto_increment)

            print("Table {} has been synced.".format(table))
            continue
            
        cursor_a.execute("SHOW CREATE TABLE {}".format(table))
        cursor_b.execute("SHOW CREATE TABLE {}".format(table))
        
        schema_a = cursor_a.fetchone()[1]
        schema_b = cursor_b.fetchone()[1]
        schema_a="\n".join(schema_a.split("\n")[:-1]) 
        schema_b="\n".join(schema_b.split("\n")[:-1]) 

        if schema_a != schema_b:
            print("Schema for table {} is different between databases A and B.".format(table))

            columns_a = [line.strip() for line in schema_a.split('\n')[1:-1]]
            columns_b = [line.strip() for line in schema_b.split('\n')[1:-1]]

            if len(columns_a) != len(columns_b):

                print("  A has {} columns, B has {} columns.".format(len(columns_a), len(columns_b)))
                if len(columns_a) > len(columns_b):
                    missing_columns = [col.split()[0] for col in columns_a if col not in columns_b]
                    print("  Table {} is missing the following columns: {}".format(table, ", ".join(missing_columns)))
                    for col_a in columns_a:
                        col_name = col_a.split()[0]
                        if col_name in missing_columns:
                            print("col_a:",col_a)
                            col_a = col_a.rstrip(',')  # remove trailing comma
                            print("ALTER TABLE {} ADD COLUMN {}".format(table, col_a))
                            cursor_b.execute("ALTER TABLE {} ADD COLUMN {}".format(table, col_a))
                            print("  Adding column {} to database B".format(col_name))

                            # get the AUTO_INCREMENT and DEFAULT values for the new column in database A
                            cursor_a.execute("SELECT EXTRA, COLUMN_DEFAULT FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{}' AND COLUMN_NAME = '{}' AND TABLE_SCHEMA = '{}'".format(table, col_name, db_a_name))
                            extra_default_a = cursor_a.fetchone()
                            col_extra, col_default = extra_default_a if extra_default_a is not None else ("", None)

                            # add AUTO_INCREMENT and DEFAULT values to the new column in database B
                            alter_table = "ALTER TABLE {} MODIFY COLUMN {} {}{}{}".format(table, col_name, col_a.split()[1], col_extra, " DEFAULT '{}'".format(col_default) if col_default is not None else "")
                            cursor_b.execute(alter_table)
                    
                            # check if column is part of any keys or indexes in database A
                            cursor_a.execute("SELECT INDEX_NAME, SEQ_IN_INDEX FROM INFORMATION_SCHEMA.STATISTICS WHERE TABLE_NAME = '{}' AND COLUMN_NAME = '{}' AND TABLE_SCHEMA = '{}'".format(table, col_name, db_a_name))
                            key_indexes_a = cursor_a.fetchall()
                            for key_index_a in key_indexes_a:
                                key_name = key_index_a[0]
                                seq_in_index = key_index_a[1]
                                cursor_a.execute("SELECT NON_UNIQUE FROM INFORMATION_SCHEMA.STATISTICS WHERE TABLE_NAME = '{}' AND INDEX_NAME = '{}' AND TABLE_SCHEMA = '{}'".format(table, key_name, db_a_name))
                                non_unique = cursor_a.fetchone()[0]
                                key_type = "KEY" if non_unique else "UNIQUE KEY"
                                cursor_a.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.STATISTICS WHERE TABLE_NAME = '{}' AND INDEX_NAME = '{}' AND SEQ_IN_INDEX < {} AND TABLE_SCHEMA = '{}' ORDER BY SEQ_IN_INDEX".format(table, key_name, seq_in_index, db_a_name))
                                key_columns = [col[0] for col in cursor_a.fetchall()] + [col_name]
                                key_columns.sort(key=column_names_b.index)
                                add_key = "ALTER TABLE {} ADD {} `{}` ({})".format(table, key_type, key_name, ",".join(key_columns))
                                print("  Adding {} `{}` to database B".format(key_type, key_name))
                                cursor_b.execute(add_key)

                            # check if column is part of primary key in database A
                            cursor_a.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_NAME = '{}' AND CONSTRAINT_NAME = 'PRIMARY' AND TABLE_SCHEMA = '{}'".format(table, db_a_name))
                            primary_key_columns_a = cursor_a.fetchall()
                            if (col_name,) in primary_key_columns_a:
                                cursor_b.execute("ALTER TABLE {} ADD PRIMARY KEY ({})".format(table, ",".join(primary_key_columns_b)))
                                print("  Adding PRIMARY KEY to database B")

                else:
                    missing_columns = [col.split()[0] for col in columns_b if col not in columns_a]
                    print("  Table {} has extra columns: {}".format(table, ", ".join(missing_columns)))
            
            
            print("ensuring column definitions are the same...")
            for column_a in columns_a:
                col_name_a, col_def_a = column_a.split(maxsplit=1)
                for column_b in columns_b:
                    col_name_b, col_def_b = column_b.split(maxsplit=1)
                    if col_name_a == col_name_b:
                        if col_def_a != col_def_b:
                            print("Column '{}' in table '{}' has a different definition in table B:".format(col_name_a, table))
                            print("  A: {}".format(col_def_a))
                            print("  B: {}".format(col_def_b))
                            update_b_q="ALTER TABLE {} MODIFY COLUMN {} {}".format(table, col_name_a, col_def_a.rstrip(','))
                            print(update_b_q)
                            cursor_b.execute(update_b_q)
                            print("  Updated column definition in table B.")
