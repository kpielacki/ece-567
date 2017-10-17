import datetime
import pexpect
import getpass
import numpy as np
import pandas as pd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from blade_health_parser import BladeHealthParser


TIMEOUT = 90
# blade_prompt = ':~\$'
blade_prompt = r'\$'


server = Flask('CRAN Script', static_folder='assets')
server.config['SECRET_KEY'] = 'fbbc945de4075d6ab2f128c7a1997d457b95bc3dc45e7802'
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
server.config['SQLALCHEMY_ECHO'] = False
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(server)


def cm_check():
    cmd = 'bash /home/tb-user/cran-monitor/bin/cm-check.sh'
    return run_command(cmd)


def dus_check():
    cmd = 'bash /home/tb-user/cran-monitor/bin/dus-check.sh'
    return run_command(cmd)


def metric_check():
    cmd = 'bash /home/tb-user/cran-monitor/bin/metrics-check.sh'
    return run_command(cmd)


def ping_check():
    # Stupid hack from laziness.
    fname = '/home/ekevpie/cran-monitor/bin/device-status.sh'
    ping_script_template = '\n'.join([
        'echo "=============================================================="',
        'echo "Date"',
        'date',
        'echo "=============================================================="',
        'echo "=============================================================="',
        'echo "Hostname"',
        'hostname',
        'echo "=============================================================="',
        '{__ping_cmds__}',
    ])
    ping_template = '\n'.join([
        'output=$(ping {} -c 1)',
        'echo "=============================================================="',
        'echo "{}"',
        'echo "$output" | grep "packet loss"',
        'echo "=============================================================="',
    ])

    query = """
    SELECT DISTINCT id, device_ip
    FROM device;
    """
    df = pd.read_sql(query, db.engine)

    pings = []
    for idx, row in df.iterrows():
        ping = ping_template.format(row.device_ip, row.id)
        pings.append(ping)

    ping_script = ping_script_template.format(__ping_cmds__='\n'.join(pings))
    with open(fname, 'w') as f:
        f.write(ping_script)
    return run_command('bash ' + fname)


def run_command(cmd):
    child = pexpect.spawn(cmd)
    child.setecho(False)
    try:
        child.sendline(cmd)
        child.expect(pexpect.EOF, timeout=TIMEOUT)
        result = child.before
        child.close()
        return result
    except Exception as e:
        print e.message
        child.close()
        return None


def insert_df(df, table):
    """Upsert df results to table SQL table."""
    col_list = map(lambda x: x.lower().replace(' ', '_'),
        list(df.columns))
    
    # Assemble the upsert query
    start_string = 'INSERT INTO ' + table + ' (`' \
        + '`, `'.join(col_list) + '`)'
    values_string = ' VALUES( ' + ', '.join(
        [':i{}'.format(i) for i in range(len(col_list))]) + ' );'
    
    # Combine the parts
    final_query = start_string + values_string
    
    # Run the upsert query on the database
    data_list = df.values.tolist()
    num_rows_result = db.engine.execute(final_query, data_list)
    db.session.commit()


checks = (
    (cm_check, 'cm', 'cm_data'),
    (ping_check, 'device', 'device_status'),
    (dus_check, 'dus', 'dus_status'),
    (metric_check, 'metrics', 'metrics'),
)


if __name__ == '__main__':
    for f, parse_type, table in checks:
        result = f()
    
        if result is None:
            print 'No result found'
            continue
    
        parser = BladeHealthParser(result)
        if parse_type == 'cm':
            parser.parse_cm()
        elif parse_type == 'device':
            parser.parse_device()
        elif parse_type == 'dus':
            parser.parse_dus()
        elif parse_type == 'metrics':
            parser.parse_metrics()

        try:
            df = pd.DataFrame(parser.results)
        except:
            print 'Bad print for {}'.format(parse_type)
            continue
        if df.empty:
            print 'No result returned for {}'.format(parse_type)
            continue
        
        insert_df(df, table)
