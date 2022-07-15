from dis import dis
import random
import string
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import csv
import re

class ActionReadCSV(Action):
    def name(self) -> Text:
         return "action_csv"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        id = tracker.get_slot('claim_id')
        with open('claimstatus.csv','r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[1]==id:
                    dispatcher.utter_message("Your claim is "+row[2]+"\n")
                    if(row[2]=="Approved"):
                        dispatcher.utter_message("Your claim amount is "+row[3]+"\n")
                        return[]
                    elif(row[2]=="Pending"):
                        dispatcher.utter_message("We ask that you check again in a few days\n")
                        return[]
                    elif(row[2]=="Rejected"):
                        dispatcher.utter_message("We are sorry but your damages are not covered under the policy that you purchased.\n")
                        return[]
        dispatcher.utter_message("Your entered name or id is incorrect, please type again.\n")
        return[]

    
    def name(self) -> Text:
         return "action_write_csv"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        id = random(6)
        name=tracker.get_slot('name')
        with open('claimstatus.csv','w') as file:
            writer = csv.writer(file)
            tup1={name,id,"Pending","0"}
            writer.writerow(tup1)
        dispatcher.utter_message("Your request has been accepted. Your Claim Id is "+id+".")
        dispatcher.utter_message("Please remember this unique claim id for future reference.")
        return[]

                        