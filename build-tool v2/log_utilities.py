from datetime import date
import os

root = os.path.dirname(os.path.realpath(__file__))

#simple function to get the current date 
def getDate() -> str:
    cur_date = date.today().strftime('%d_%m_%Y')
    return cur_date

#simple function to format the file name
def getLogName(log_pre_name):
    return log_pre_name + '-' + getDate() + '.txt'


def format_log(parts, part_names, prices) -> list:

    #Total cost
    total = sum(float(price.get()) for price in prices if price.get())
    
    #the log that we return to the user
    final_log = [str("Total: " + str(total) + '\n')]

    for part, part_name, price in zip(parts, part_names, prices):
        final_log.append(str('<'+part+'> ' + '<'+part_name.get()+'> ' + '<'+str(price.get())+'>\n'))

    return final_log


#function to create the log file
def save(log_text, log_name: str = 'log-file'):
    #Move to the logs directory
    log_path = root + '\logs'
    print(log_path)
    os.chdir(root)
    try:
        os.chdir(log_path)
    except FileNotFoundError:
        os.mkdir('logs')
        os.chdir(log_path)

    with open(getLogName(log_name) if log_name=='' else log_name+'.txt', 'w') as new_log:
        for line in log_text:
            new_log.write(line)

    os.chdir(root)

def deformatLog(log_text : list):
    parts = []
    part_names = []
    prices = []

    for i in range(1, len(log_text)):
        try:
            l = [s.strip(' <').strip('>') for s in log_text[i].strip().split('>')]
        except Exception:
            pass
        parts.append(l[0])
        part_names.append(l[1])
        try:
            prices.append(float(l[2]))
        except Exception:
            prices.append('')
        
    return [part_names, prices]

def load(log_file_name = 'N/A'):
    os.chdir(root)
    #change work space to the logs directory
    try:
        log_path = root + '\logs'
        os.chdir(log_path)
    except FileNotFoundError:
        return None
    
    #find the log_file_name in dirs
    if log_file_name:
        for r, dirs, files in os.walk('.'):
            if log_file_name in files:
                break
        else:
            return None
    else:
        #if the log_file_name is undefined then default it to the last file 
        log_file_name = files[-1]
            
    fin = open(log_file_name, 'r')
    l = fin.readlines()
    fin.close()
    os.chdir(root)
    return deformatLog(l)