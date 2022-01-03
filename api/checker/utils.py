from dateutil.parser import parse
import datetime
import calendar

def check_string_year(item):
    year = item
    if(not year):
        return True
    if not check_param_year(year):
        return False
    return True

def check_string_year_month(item):
    if('.' not in str(item)):
        return False
    year,month = str(item).split('.')
    if(not year or not month):
        return True
    # Check year validity first
    if( not check_param_year(year)):
        return False
    # Check Month 
    if not check_param_month(month):
        return False
    return True

def check_string_year_month_day(item):
    if('.' not in str(item)):
        return False
    year,month,day = str(item).split('.')    
    if(not year or not month or not day):
        return True
    # Check Year
    if(not check_param_year(year)):
        return False
    # Check Month
    if(not check_param_month(month)):
        return False
    # Check day 
    if not check_param_day(year,month,day):
        return False
    return True

def check_param_year(year):
    if(len(year)!=4):
        return False
    if(not str(year).isnumeric()):
        return False
    if(int(year) > datetime.datetime.now().year):
        return False
    return True    

def check_param_month(month):
    if(len(month)!=2):
        return False
    if(not str(month).isnumeric()):
        return False
    if(int(month) < 1 or int(month) >12 ):
        return False
    return True    

def check_param_day(year,month,day):
    if(len(day)!=2):
        return False
    if(not str(day).isnumeric()):
        return False
    if(int(day) < 1 or int(day) > calendar.monthrange(int(year),int(month))[1]):
        return False
    return True    
        
def check_param_date_range(item1,item2):
    since = parse(item1.replace('.','-'))
    upto = parse(item2.replace('.','-'))
    if(since.timestamp()>upto.timestamp()):
        return False
    return True

def keys_exists(element, *keys):
    '''
    Check if *keys (nested) exists in `element` (dict).
    '''
    if not isinstance(element, dict):
        raise AttributeError('keys_exists() expects dict as first argument.')
    
    if len(keys) == 0:
        raise AttributeError('keys_exists() expects at least two arguments, one given.')

    _element = element
    for key in keys:
        try:
            _element = _element[key]
        except KeyError:
            return False
    return True            