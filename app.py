from cmd import Cmd
import argparse
import getpass
import ibm_db
import os


class Db2Prompy(Cmd):
    def __init__(self, conn):
        Cmd.__init__(self)
        self.prompt = 'db2prompy> '
        self.intro = "Welcome! Type ? to list commands"
        self.conn = conn

    def emptyline(self):
        pass

    def do_exit(self, args):
        return True

    def help_exit(self):
        print('exit the application. Shorthand: Ctrl-D.')

    def do_ls(self, args):
        print("SQL files available:")
        for f in os.listdir("sqls/"):
            if not f.startswith('.'):
                print("- {}".format(f))

    def help_ls(self):
        print('List SQL files avaiable to execute.')

    def do_execf(self, arg):
        stmt = None
        try:
            with open("sqls/{}".format(arg), "r") as f:
                stmt = f.read()
        except Exception:
            print(
                "Could not open file sqls/{}. Check available files with command ls".format(arg))

        try:
            if stmt:
                res = ibm_db.exec_immediate(self.conn, stmt)
                if stmt is not None:
                    row = ibm_db.fetch_tuple(res)
                    while (row):
                        for col in row:
                            print(col, end="\t")
                        print("")
                        row = ibm_db.fetch_tuple(res)
        except Exception:
            print("Execution of sqls/{} failed".format(arg))

    def help_execf(self):
        print("Execute a file from directory sqls/")

    def do_commit(self, arg):
        try:
            ibm_db.commit(self.conn)
        except:
            print("Failed to commit.")

    def help_commit(self):
        print('Commit last transactions.')

    def do_rollback(self, arg):
        try:
            ibm_db.rollback(self.conn)
        except:
            print("Failed to rollback.")

    def help_rollback(self):
        print('Rollback last transactions.')

    def default(self, arg):
        print("Command not found. Type ? to list commands.")

    do_EOF = do_exit
    help_EOF = help_exit


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-H", "--host", help="Database hostname", default="127.0.0.1")
    parser.add_argument("-p", "--port", help="Database port", default="50000")
    parser.add_argument(
        "-d", "--dbname", help="Database name", default="sample")
    parser.add_argument(
        "-u", "--user", help="Database user", default="db2inst1")
    parser.add_argument("-n", "--program",
                        help="Program name", default="DB2PROMPY")

    args = parser.parse_args()
    return args


def create_connection(args: dict, passwd: str):
    options = {
        ibm_db.SQL_ATTR_INFO_PROGRAMNAME: args.program,
        ibm_db.SQL_ATTR_INFO_WRKSTNNAME: args.program,
        ibm_db.SQL_ATTR_INFO_ACCTSTR: args.program,
        ibm_db.SQL_ATTR_INFO_APPLNAME: args.program,
        ibm_db.SQL_ATTR_AUTOCOMMIT: ibm_db.SQL_AUTOCOMMIT_OFF
    }
    connection_string = "DATABASE={};HOSTNAME={};PORT={};PROTOCOL=TCPIP;UID={};PWD={};".format(
        args.dbname, args.host, args.port, args.user, passwd)
    try:
        conn = ibm_db.pconnect(connection_string, "", "", options)
        print("Connected to {}:{}/{} as {}".format(args.host,
              args.port, args.dbname, args.user))
    except Exception as e:
        print("Could not connect to database")
        raise e
    return conn


if __name__ == '__main__':
    try:
        args = parse_arguments()
        dbpasswd = getpass.getpass(
            "Type password for user {}: ".format(args.user))
        conn = create_connection(args, dbpasswd)
        Db2Prompy(conn).cmdloop()
    except KeyboardInterrupt:
        pass
