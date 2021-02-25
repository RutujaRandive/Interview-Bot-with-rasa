from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.executor import CollectingDispatcher
import webbrowser
from db_conn import DataUpdate,RetrieveQuestion,QuestionHistory,RetrieveCandidateId,UpdateSimilarity
from answer_evaluation import Similarity
import random

class ActionVideo(Action):
    def name(self) -> Text:
        return "action_video"

    async def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        video_url="https://youtu.be/jj4BL9o3Q7o"
        dispatcher.utter_message("wait... Playing your video.")
        webbrowser.open(video_url)
        return []

class ValidateRestaurantForm(Action):
    def name(self) -> Text:
        return "user_details_form"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        required_slots = ["name","lname", "number", "branch","cgpa","email","lang"]

        for slot_name in required_slots:
            if tracker.slots.get(slot_name) is None:
                # The slot is not filled yet. Request the user to fill this slot next.
                return [SlotSet("requested_slot", slot_name)]

        # All slots are filled.
        return [SlotSet("requested_slot", None)]

class ActionSubmit(Action):
    def name(self) -> Text:
        return "action_submit"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        # cid=DataUpdate(tracker.get_slot("name"),tracker.get_slot("number"),tracker.get_slot("lname"),tracker.get_slot("branch"),tracker.get_slot("cgpa"),tracker.get_slot("email"),tracker.get_slot("lang"))
        # print(cid)
        # SlotSet("cid",cid)

        dispatcher.utter_message(template="utter_details_thanks",
                                 FName=tracker.get_slot("name"),
                                 LName=tracker.get_slot("lname"),
                                 Branch=tracker.get_slot("branch"),
                                 CGPA=tracker.get_slot("cgpa"),
                                 Email=tracker.get_slot("email"),
                                 Coding_Language=tracker.get_slot("lang"),
                                 Mobile_number=tracker.get_slot("number"),
                                 Candidate_id=tracker.get_slot("cid"))

        # return(SlotSet("cid",cid))

        DataUpdate(tracker.get_slot("name"),tracker.get_slot("number"),tracker.get_slot("lname"),tracker.get_slot("branch"),tracker.get_slot("cgpa"),tracker.get_slot("email"),tracker.get_slot("lang"))

class Candidate_id(Action):
    def name(self):
        return "get_cand_id"

    def run(self,dispatcher,tracker,domain):
        cid = RetrieveCandidateId(tracker.get_slot("email"))
        return [SlotSet("cid",cid)]


class question(Action):
    def name(self) -> Text:
        return "first_question"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:

        q = RetrieveQuestion(tracker.get_slot("cid"))

        if len(q)==2 and q[1]=='stop':

            dispatcher.utter_message(template="utter_ask_question",
                                    qu=q[1])
        else:
            dispatcher.utter_message(template="utter_ask_question",
                                    qu=q[1])

            QuestionHistory(tracker.get_slot("cid"),q[0],q[3],q[4],0.5)

        return [SlotSet("question", tracker.latest_message['text'])]

class Candidate_id(Action):
    def name(self):
        return "get_sim"

    def run(self,dispatcher,tracker,domain):
        sim = Similarity(tracker.get_slot("question"))
        # print("actions",sim)
        if sim != -1:
            UpdateSimilarity(sim,tracker.get_slot("cid"))
