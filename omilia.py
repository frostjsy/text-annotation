#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 19:28:17 2018

@author: stephanosarampatzes
"""

# pip install -U spacy
# python -m spacy download en


import re
import spacy
import en_core_web_sm as en
nlp = en.load()

class Banking():
    
    def __init__(self, user_input):
        self.user_input = user_input
        
    def __repr__(self):
        return("We are on the way to serve your demand...")
    
    # separate utterances into groups
    def search_group(self):
        pattern = re.compile(r"(apply|application|open)|(balance|how much)|(activate|activation|cancel|close|terminate|passed away)|(credit(?!\scard)|limit|available balance)|(payment|pay)|(pin)")
        if pattern.search(self.user_input) is not None:
            return(pattern.search(self.user_input))
        else:
            return('cannot process your demand, please type again!')
        
    def print_result(self):
        # apply/open cards
        if result.group() in ['apply', 'application', 'open']:
            if 'personal' in self.user_input:
                return('Apply for personal')
            elif 'business' in self.user_input:
                return('Apply for Business card')
            else:
                return('Apply for card')
        
        # balance/transfer
        elif result.group() in ['balance', 'how much']:
            if 'transfer' in self.user_input:
                return('Balance Transfer')
            # overlapping regular expressions
            elif 'credit' in self.user_input:
                return('Available Credit') # returns an intent from "Available credit" group
            else:
                return('Balance Inquiry')
        
        # activate/cancel cards
        elif result.group() in ['activate', 'activation', 'cancel', 'close', 'terminate', 'passed away']:
            if 'activate' in self.user_input or 'activation' in self.user_input:
                return('Activate card')
            else:
                return('Cancel-Close card')
        
        # available credit & limits
        elif result.group() in ['credit', 'limit', 'available balance']:
            limits = ['increase', 'decrease', 'change']
            if any(lt in self.user_input for lt in limits):
                return('Change Limit')
            elif 'limit' in self.user_input:
                return('Limit Inquiry')
            else:
                return('Available Credit')
        
        # Payment
        elif result.group() in ['payment', 'pay']:
            if 'minimum' in self.user_input:
                return('minimum payment')
            else:
                return('Payment')
        
        # PIN issues
        elif result.group() == 'pin':
            return('PIN issues')
    
    def annotations(self):
        if any(act in self.user_input for act in ['open','apply','activate','cancel', 'close', 'terminate', 'order','make']):
            annotation = 'ACTION'
        elif 'pay' in self.user_input:
            if re.search(r"pay\?", self.user_input):
                annotation = 'other'
            elif re.search(r"pay\b", self.user_input):
                annotation = 'ACTION'
            else:
                annotation = 'other'
        elif any(mod in self.user_input for mod in ['change', 'increase', 'decrease']):
            annotation = 'MODIFIER'
        else:
            annotation = 'other'
        # store info of utternace in a dictionary
        # annotation/ span start-end/ POS tagging/ Name Entity Recognition
        text = nlp(self.user_input)
        annot = {}
        annot[text] = [annotation, result.span(), [word.pos_ for word in text], [word.label_ for word in text.ents]]
        return(annot)


if __name__ == '__main__':
    while True:
        # customer input
        input_ = input('How can I help you? \n')
        
        if input_.lower() in ['bye', 'goodbye', 'see you']:
            print('Goodbye, hope to see you again!')
            break
        else:
            b = Banking(input_.lower())
            print(b,'\n')
            result = b.search_group()
            if type(result) != str: 
                print('Intent: {}'.format(b.print_result()))
                print('Annotations: {}'.format(b.annotations()))
            else:
                print(result)
