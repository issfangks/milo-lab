#!/usr/bin/python

import logging
import re


def NormalizeNames(name_str):
    """Normalize a KEGG-style list of names."""
    all_names = name_str.replace('\t', '').split(';')
    return [n.strip() for n in all_names]


class EntryDictWrapper(dict):
    
    def GetStringField(self, field_name, default_value=None):
        if field_name not in self:
            if default_value:
                return default_value
            raise Exception("Missing obligatory field: " + field_name)
            
        return self[field_name]
    
    def GetStringListField(self, field_name, default_value=None):
        val = self.GetStringField(field_name, default_value=False)
        
        if val == False:
            if default_value == None:
                raise Exception("Missing obligatory field: " + field_name)
            return default_value
        return val.split()
        
    def GetBoolField(self, field_name, default_value=True):
        val = self.GetStringField(field_name, default_value=False)
        
        if val == False:
            if default_value == None:
                raise Exception("Missing obligatory field: " + field_name)
            return default_value
        elif val.upper() == 'TRUE':
            return True
        elif val.upper() == 'FALSE':
            return False
    
    def GetFloatField(self, field_name, default_value=None):
        val = self.GetStringField(field_name, default_value=False)
        
        if val == False:
            if default_value == None:
                raise Exception("Missing obligatory field: " + field_name)
            return default_value
        return float(val)
    
    def GetVFloatField(self, field_name, default_value=()):
        val = self.GetStringField(field_name, default_value=False)
        
        if val == False:
            if default_value == None:
                raise Exception("Missing obligatory field: " + field_name)
            return default_value
        return [float(x) for x in val.split()]
    

class ParsedKeggFile(dict):
    """A class encapsulating a parsed KEGG file."""

    def __init__(self):
        """Initialize the ParsedKeggFile object."""
        pass
        
    def _AddEntry(self, entry, fields):
        """Protected helper for adding an entry from the file.
        
        Args:
            entry: the entry key.
            fields: the fields for the entry.
        """
        if entry in self:
            logging.warning('Overwriting existing entry for %s', entry)
        self[entry] = EntryDictWrapper(fields)


    @staticmethod
    def FromKeggFile(filename, verbose=False):
        """Parses a file from KEGG.
    
        Args:
            filename: the name of the file to parse.
        
        Returns:
            A dictionary mapping entry names to fields.
        """
        kegg_file = open(filename, 'r')
        parsed_file = ParsedKeggFile()
    
        curr_field = ""
        field_map = {}
        line_counter = 0
        line = kegg_file.readline()
    
        while line:
            field = line[0:12].strip()
            value = line[12:].strip()
    
            if field == "///":
                entry = re.split('\s\s+', field_map['ENTRY'])[0]
                parsed_file._AddEntry(entry, field_map)
                field_map = {}
            else:
                if field != "":
                    curr_field = field
                if curr_field in field_map:
                    field_map[curr_field] = field_map[curr_field] + "\t" + value
                else:
                    field_map[curr_field] = value
    
            line = kegg_file.readline()
            line_counter += 1
        
        kegg_file.close()
        return parsed_file