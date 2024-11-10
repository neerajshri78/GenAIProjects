from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
load_dotenv()


template= """
You are an intelligent assistant that helps convert natural language queries into SQL queries or provide schema details based on information provided. #

IMPORTANT:
At every run, please definitely follow these below steps, do not add any prefix or suffic charcter such as single quotes in the SQL
- Please return the SQL query wherever applicable.
- Ensure the SQL query is clean and without any additional symbols, text, or commentary.

You are working with  table below with list of column mames:
Schema Name : OMOP
Table Name: person
Column Names:
1. person_id: Integer. A unique identifier for each person, treated independently.
2. gender_concept_id: Integer. Captures the biological sex at birth of the person; not for studying gender identity.
3. year_of_birth: Integer. The year of birth used to compute age.
4. month_of_birth: Integer. The month of birth of the person.
5. day_of_birth: Integer. The day of birth of the person.
6. birth_datetime: Datetime. The full date and time of birth of the person.
7. race_concept_id: Integer. Captures the race or ethnic background of the person.
8. ethnicity_concept_id: Integer. Captures ethnicity as defined by the OMB, distinguishing “Hispanic” and “Not Hispanic”.
9. location_id: Integer. Refers to the last known physical address of the person.
10. provider_id: Integer. Refers to the last known primary care provider associated with the person.
11. care_site_id: Integer. Refers to where the provider typically provides primary care.
12. person_source_value: String. Links back to persons in the source data for error checking of ETL logic.
13. gender_source_value: String. Stores the biological sex from the source data; for reference only.
14. gender_source_concept_id: Integer. Typically zero due to a limited number of options.
15. race_source_value: String. Stores the race from the source data; for reference only.
16. race_source_concept_id: Integer. Typically zero due to a limited number of options.
17. ethnicity_source_value: String. Stores the ethnicity from the source data; for reference only.
18. ethnicity_source_concept_id: Integer. Typically zero due to a limited number of options.

Table Name: visit_detail

1. visit_detail_id: Integer. Use this to identify unique interactions between a person and the health care system. This identifier links across the other CDM event tables to associate events with a visit detail.
2. person_id: Integer. Links to the PERSON table.
3. visit_detail_concept_id: Integer. Contains a concept ID representing the kind of visit detail (e.g., inpatient or outpatient). All concepts in this field should be standard and belong to the Visit domain. Foreign Key: CONCEPT (Visit).
4. visit_detail_start_date: Date. The date of the start of the encounter; may or may not be equal to the date of the associated visit.
5. visit_detail_start_datetime: Datetime. The specific start date and time of the encounter.
6. visit_detail_end_date: Date. The end date of the patient-provider interaction.
7. visit_detail_end_datetime: Datetime. The specific end date and time of the encounter.
8. visit_detail_type_concept_id: Integer. Understand the provenance of the visit detail record, indicating where the record comes from. Foreign Key: CONCEPT (Type Concept).
9. provider_id: Integer. There will only be one provider per visit record, indicating how they were chosen (e.g., attending, admitting). This is important as multiple visit detail records can be associated with a single visit occurrence. Foreign Key: PROVIDER.
10. care_site_id: Integer. Provides information about the Care Site where the Visit Detail took place. Foreign Key: CARE_SITE.
11. visit_detail_source_value: String. Houses the verbatim value from the source data representing the kind of visit detail (e.g., inpatient, outpatient, emergency).
12. visit_detail_source_concept_id: Integer. Concept ID from the source data; Foreign Key: CONCEPT.
13. admitting_source_value: String. Represents the source of admission.
14. admitting_source_concept_id: Integer. Indicates where the patient was admitted from, part of the visit domain (e.g., from a long-term care facility). Foreign Key: CONCEPT (Visit).
15. discharge_to_source_value: String. Represents where the patient was discharged to.
16. discharge_to_concept_id: Integer. Indicates where the patient was discharged to after a visit detail record (e.g., home or long-term care facility). Foreign Key: CONCEPT (Visit).
17. preceding_visit_detail_id: Integer. Finds the visit detail that occurred prior to the given visit detail record. Foreign Key: VISIT_DETAIL.
18. visit_detail_parent_id: Integer. Finds the visit detail that subsumes the given visit detail record, used for nested relationships beyond the VISIT_OCCURRENCE/VISIT_DETAIL relationship. Foreign Key: VISIT_DETAIL.
19. visit_occurrence_id: Integer. Links the VISIT_DETAIL record to its VISIT_OCCURRENCE. Foreign Key: VISIT_OCCURRENCE.


Now, based on the information provided, convert the following natural language question into an SQL query.

Ensure that you return only the SQL query, with no additional explanations, commentary, or noise.
 
Question: {question}
"""

prompt=ChatPromptTemplate.from_template(template)

#llm=ChatOllama(temprature=0,model="llama3.2") 

llm = ChatOpenAI(temperature=0.7, model="gpt-4o")

chain=prompt|llm

response=chain.invoke({"question":"Give me the table names in OMOP schema provided"})
print(response.content)
