from dateutil.parser import parse
import requests
import datetime
import calendar

def check_string_year(year):
    if(not year):
        return True
    if(len(year)!=4):
        return False
    if(not str(year).isnumeric()):
        return False
    if(int(year) > datetime.datetime.now().year):
        return False
    return True

def check_string_year_month(year,month):
    if(not year or not month):
        return True
    # Check year validity first
    if( not check_string_year(year)):
        return False
    # Check Month 
    if(len(month)!=2):
        return False
    if(not str(month).isnumeric()):
        return False
    if(int(month) < 1 or int(month) >12 ):
        return False
    return True

def check_string_year_month_day(year,month,day):
    # 
    if(not year or not month or not day):
        return True
    # Check Year
    if(not check_string_year(year)):
        return False
    # Check Year and Month
    if(not check_string_year_month(year,month)):
        return False
    # Check year month day 
    if(len(day)!=2):
        return False
    if(not str(day).isnumeric()):
        return False
    if(int(day) < 1 or int(day) > calendar.monthrange(year,month)[1]):
        return False
    return True

def check_string_query_validity(type,since=False,upto=False):
    # Check if the format is correct 
    # C
    if type=="year":
        if(not check_string_year(since) or not(check_string_year(upto))):
            return False
        if(not since and not upto):
            if(int(since)>int(upto)):
                return False
    
    return True
        
def check_param_date_range(item1,item2):
    since = parse(item1.replace('.','-'))
    upto = parse(item2.replace('.','-'))
    if(since.timestamp()>upto.timestamp()):
        return False
    return True
            