import datetime
import json
import re
from itertools import groupby
from collections import defaultdict


def get_val(line):
    return line.split(':', 1)[-1].strip()


def remove_ansi(text):
    ansi_pat = re.compile(r'\x1b[^m]*m')
    return ansi_pat.sub('', text)


class BladeHealthParser:

    results = dict()
    """Parsed results dictionary."""

    simple_fields = (
        'Date',
        'Hostname',
        'SW Version',
        'Config',
    )
    """One line simple to parse fields."""

    dus_pat = re.compile('DUS\d\d\d')
    """Regex pattern for DUS fields."""

    def __init__(self, contents):
        self.contents = contents.split('\n')

    def get_blocks(self):
        return groupby(self.contents, lambda x: '=========' in x)
    
    def parse_field(self, field, contents):
        if field in self.simple_fields:
            return self.simple_parse(contents)
        else:
            return self.ping_parse(contents)

    def simple_parse(self, contents):
        return contents[0].strip().strip('/').strip('\r')

    def ping_parse(self, contents):
        if '1 packets transmitted, 1 received,' in contents[0]:
            return True
        return False

    def parse_cm(self):
        results = defaultdict(list)
        block_iter = self.get_blocks()
        for k, block in block_iter:
            if k: continue
            block_contents = list(block)
            field = block_contents[0].strip('\r')
            if field == '': continue
            field_contents = block_contents[1:]
            value = self.parse_field(field, field_contents)
            if value is not None:
                value = value.strip('\r')
            results[field].append(value)

        results['Date'] = map(self.format_dt, results['Date'])
        self.results = results

    def parse_device(self):
        date = None
        hostname = None
        results = {
            'Date': [],
            'Hostname': [],
            'Device ID': [],
            'Reachable': [],
        }
        block_iter = self.get_blocks()
        for k, block in block_iter:
            if k: continue
            block_contents = list(block)
            field = block_contents[0].strip('\r')
            if field == '': continue
            field_contents = block_contents[1:]
            value = self.parse_field(field, field_contents)
            if field == 'Date':
                date = self.format_dt(value.replace('  ', ' '))
            elif field == 'Hostname':
                hostname = value
            else:
                results['Device ID'].append(field)
                results['Reachable'].append(value)

        self.fill_info(results, date, hostname, len(results['Device ID']))
        self.results = dict(results)

    def get_temps(self, contents):
         for line in contents:
             if 'Temperature min/max/avg (C)' in line:
                 temps = line.split(':', 1)[-1].split(' from')[0].strip()
                 return map(float, temps.split('/'))
         return (None, None, None)

    def get_cpris(self, contents):
         cpris = [None, None, None, None, None, None]
         cpri_map = ((0, 'CPRI A'),
                     (1, 'CPRI B'),
                     (2, 'CPRI C'),
                     (3, 'CPRI D'),
                     (4, 'CPRI E'),
                     (5, 'CPRI F'))

         cpri_contents = []
         for idx, line in enumerate(contents):
             if 'CPRI port status' in line:
                 try:
                     cpri_contents = contents[idx+3:idx+9]
                 except IndexError:
                     return cpris

         # Probably a better way to do this all
         for line in cpri_contents:
             port, status = line.split(':')
             port = port.strip().strip(':')
             status = status.rsplit('\t', 1)[-1].strip()
             status = remove_ansi(status)
 
             for idx, name in cpri_map:
                 if name == port:
                     cpris[idx] = status
                     continue

         return cpris

    def get_tns(self, contents):
         tns = [None, None, None]
         tn_map = ((0, 'TNA'),
                   (1, 'TNB'),
                   (2, 'TNC'))

         tn_contents = []
         for idx, line in enumerate(contents):
             if 'PORT | LINK |' in line:
                 try:
                     tn_contents = contents[idx+2:idx+5]
                 except IndexError:
                     return tns

         # Probably a better way to do this all
         for line in tn_contents:
             port, status = line.split('|', 1)
             port = port.strip()
             status = status.split('|', 1)[0].strip()
             status = remove_ansi(status)
 
             for idx, name in tn_map:
                 if name == port:
                     tns[idx] = status
                     continue

         return tns

    def get_sync(self, contents):
         for line in contents:
             if 'Netsync status' in line:
                 sync = line.split(':', 1)[-1].strip()
                 return remove_ansi(sync)
         return None

    def fill_info(self, data, date, hostname, count):
       for x in xrange(count):
           data['Date'].append(date)
           data['Hostname'].append(hostname)

    def format_dt(self, date_str):
        if date_str is None: return None

        timezones = ('EDT', 'EST', 'PDT', 'PST', 'CDT', 'CST', 'CEST')
        for timezone in timezones:
            date_str = date_str.replace(' ' + timezone, '')
        try:
            dt = datetime.datetime.strptime(date_str, '%a %b %d %H:%M:%S %Y')
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            print e.message
            return None

    def parse_dus(self):
        dus_field_pat = re.compile('DUS\d{3}')
        date = None
        hostname = None
        results = {
            'Date': [],
            'Hostname': [],
            'DUS': [],
            'Temp Min': [],
            'Temp Max': [],
            'Temp Avg': [],
            'CPRI A Link': [],
            'CPRI B Link': [],
            'CPRI C Link': [],
            'CPRI D Link': [],
            'CPRI E Link': [],
            'CPRI F Link': [],
            'TN A Link': [],
            'TN B Link': [],
            'TN C Link': [],
            'Netsync': [],
        }
        block_iter = self.get_blocks()
        for k, block in block_iter:
            if k: continue
            block_contents = list(block)
            field = block_contents[0].strip('\r')
            field_contents = block_contents[1:]
 
            if field == '': continue
            elif field == 'Date':
                date = self.parse_field(field, field_contents)
                date = date.replace('  ', ' ')
            elif field == 'Hostname':
                hostname = self.parse_field(field, field_contents)
            elif re.match(dus_field_pat, field):
                temp_min, temp_max, temp_avg = self.get_temps(field_contents)
                cpris = self.get_cpris(field_contents)
                tns = self.get_tns(field_contents)
                sync = self.get_sync(field_contents)
                results['DUS'].append(field)
                results['Temp Min'].append(temp_min)
                results['Temp Max'].append(temp_max)
                results['Temp Avg'].append(temp_avg)
                results['CPRI A Link'].append(cpris[0])
                results['CPRI B Link'].append(cpris[1])
                results['CPRI C Link'].append(cpris[2])
                results['CPRI D Link'].append(cpris[3])
                results['CPRI E Link'].append(cpris[4])
                results['CPRI F Link'].append(cpris[5])
                results['TN A Link'].append(tns[0])
                results['TN B Link'].append(tns[1])
                results['TN C Link'].append(tns[2])
                results['Netsync'].append(sync)
            else:
                print 'Unknown field {}'.format(field)
 
        self.fill_info(results, date, hostname, len(results['DUS']))
        results['Date'] = map(self.format_dt, results['Date'])
        self.results = results

    def parse_gui_print(self, contents, results):
        split_pat = re.compile('\s{2,}')
        for line in contents:
            try:
                _, rx, metric, val, _ = re.split(split_pat, line)
                rx = rx.strip()
                metric = metric.strip()
                val = val.strip()
                if val == 'Empty': val = None
            except Exception as e:
                print 'Bad line for metric parse: {}'.format(e.message)
                rx = None
                metric = None
                val = None
            results['RX'].append(rx)
            results['Metric'].append(metric)
            results['Value'].append(val)
        return results

    def parse_metrics(self):
        """Parse metric output from gui.py
        
        For new metrics add dictionary entry. 
        """
        dus_field_pat = re.compile('DUS\d{3}')
        date = None
        hostname = None
        results = {
            'Date': [],
            'Hostname': [],
            'RX': [],
            'Metric': [],
            'Value': [],
        }
        block_iter = self.get_blocks()
        for k, block in block_iter:
            if k: continue
            block_contents = list(block)
            field = block_contents[0].strip('\r')
            field_contents = block_contents[1:]

            if field == '': continue
            elif field == 'Date':
                date = self.parse_field(field, field_contents)
                date = date.replace('  ', ' ')
            elif field == 'Hostname':
                hostname = self.parse_field(field, field_contents)
            else:
                results = self.parse_gui_print(field_contents, results)
 
        self.fill_info(results, date, hostname, len(results['RX']))
        results['Date'] = map(self.format_dt, results['Date'])
        self.results = results

    def results_to_json(self):
        return json.dumps(self.results)


if __name__ == '__main__':
    with open('test.txt', 'r') as f:
        contents = f.read()
    parser = BladeHealthParser(contents)
    parser.parse_cm()
    results = parser.results_to_json()
    with open('results.txt', 'w') as f: f.write(str(results))


    with open('test_radio.txt', 'r') as f:
        contents = f.read()
    parser = BladeHealthParser(contents)
    parser.parse_radio()
    results = parser.results_to_json()
    with open('results_radio.txt', 'w') as f: f.write(str(results))


    with open('test_dus.txt', 'r') as f:
        contents = f.read()
    parser = BladeHealthParser(contents)
    parser.parse_dus()
    results = parser.results_to_json()
    with open('results_dus.txt', 'w') as f: f.write(str(results))
