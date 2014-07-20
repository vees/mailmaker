import json
import csv
import os
import os.path as path
import time
import csv
import codecs
import mechanize
import StringIO

class CodeEnforcementReport:
    """Baltimore County Code Enforcement Report Representation"""
    def __init__(self, cachedir=None, max_age=None):
        if cachedir != None:
            self._cachedir = cachedir
        else:
            self._cachedir = os.getcwd()
        
        if max_age != None:
            self._max_age = max_age
        else:
            self._max_age = 60 * 60 * 24
        
        self.addresses = {}

    def convert_row_to_hash(row):
        pass
    
    def load(self):
        data_cache = self._cachedir + '/bacodata.txt'
        try:
            baco_data_age = time.time()-path.getmtime(data_cache)
        except:
            baco_data_age = self._max_age + 1
        s = ''
        if baco_data_age > self._max_age:
            try:
                print "Grabbing new version"
                br=mechanize.Browser()
                br.set_handle_robots(False)
                br.open("http://www.baltimorecountymd.gov/Agencies/permits/codeenforcement/complaintreports.html")
                br.follow_link(text="Code Enforcement Complaints (CSV)")
                s= br.response().get_data()
                with open(data_cache, "w") as text_file:
                    text_file.write(s)
            except:
                s = ''
        if s == '':
            with open (data_cache, "r") as myfile:
                s=myfile.read()
        
        self._property_data = s 
        self._baco_data_age = baco_data_age

    def process(self):
        s = self._property_data
        f = StringIO.StringIO(s)
        reader = csv.reader(f, delimiter=',', quotechar='"')
        headers = reader.next()
        complained = {}
        for x in reader:
            address_key = x[0][:-1].upper()
            if len(address_key) < 3:
                #print "Didn't load address key '%s' in  %s" % (address_key, x)
                continue
            x = x[1:]
            if address_key in complained:
                complained[address_key].append(x)
            else:
                complained[address_key] = [x]
        
        output = { 
            'string': s, 
            'Source': 'Downloaded file %s seconds old' % int(self._baco_data_age), 
            "Complaints": complained,
        }
        
        self._complaints = complained

    def search(self, address):
        #print self._complaints.keys()
        if address in self._complaints.keys():
            return self._complaints[address]
        else:
            return None

    def dump(self):
        self.display_list(self._complaints.keys())

    def filter_by_list(self, property_list, excludestatus=[]):
        return {x: [y for y in self._complaints[x] if y[5] not in excludestatus] 
            for x in property_list if x in self._complaints.keys()}

    def display_list(self, complaints_by_address):
        for address in complaints_by_address:
            if len(complaints_by_address[address]) == 0:
                continue;
            print address
            for complaint in complaints_by_address[address]:
                print complaint
            print "=" * 35

    def output_html(self, complaints_by_address):
        output = "<ul>"
        for address in complaints_by_address:
            if len(complaints_by_address[address]) == 0:
                continue;
            output += "<li>%s\n" % address
            for complaint in complaints_by_address[address]:
                case, opened, updated = complaint[0], complaint[2], complaint[4]
                output += "<br/>Case %s" % case
                if (len(updated)>0):
                    output += " updated %s" % updated                
                elif (len(opened)>0):
                    output += " opened %s" % opened
                output += "</li>\n";
        output += "</ul>\n"
        return output

if __name__ == "__main__":
    cer = CodeEnforcementReport()
    cer.load()
    cer.process()
    #print cer.search("7502 OLD HARFORD RD")
    #cer.dump()
    cer.display_list(cer.filter_by_list(['7502 OLD HARFORD RD']))
