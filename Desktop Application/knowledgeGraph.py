import logging
import sys

from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable


class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    @staticmethod
    def enable_log(level, output_stream):
        handler = logging.StreamHandler(output_stream)
        handler.setLevel(level)
        logging.getLogger("neo4j").addHandler(handler)
        logging.getLogger("neo4j").setLevel(level)

    def initialize_knowledge_graph(self):
        with self.driver.session() as session:
            query = (
                """
                CREATE (s:Stroke{Name:'Stroke',QName:'Stroke'}),(rf:RiskFactor{Name:'Risk Factor',QName:'RiskFactor'})-[:DESCRIBES]->(s),(mrf:MedicalRiskFactor{Name:'Medical Risk Factor',QName:'MedicalRiskFactor'})-[:PART_OF]->(rf),(nmrf:NonMedicalRiskFactor{Name:'Non-Medical Risk Factor',QName:'NonMedicalRiskFactor'})-[:PART_OF]->(rf)
                
                CREATE (age:Age{Name:'Age',QName:'Age'})-[:IS_A]->(nmrf),(marriage:MarriageCategory{Name:'Marriage',QName:'Marriage'})-[:IS_A]->(nmrf),(residenceType:ResidenceCategory{Name:'Residence Type',QName:'ResidenceType'})-[:IS_A]->(nmrf),(smokingStatus:SmokingCategory{Name:'Smoking Status',QName:'SmokingStatus'})-[:IS_A]->(nmrf),(workType:WorkCategory{Name:'Work Type',QName:'WorkType'})-[:IS_A]->(nmrf),(gender:GenderCategory{Name:'Gender',QName:'Gender'})-[:IS_A]->(nmrf)

                CREATE (yes:MarriageCategory{Name:'Yes',QName:'Marriage:Yes'})-[:CATEGORY_OF]->(marriage), (no:MarriageCategory{Name:'No',QName:'Marriage:No'})-[:CATEGORY_OF]->(marriage)
                CREATE (urban:ResidenceCategory{Name:'Urban',QName:'ResidenceType:Urban'})-[:CATEGORY_OF]->(residenceType), (rural:ResidenceCategory{Name:'Rural',QName:'ResidenceType:Rural'})-[:CATEGORY_OF]->(residenceType)
                CREATE (neverSmoked:SmokingCategory{Name:'Never',QName:'SmokingStatus:Never'})-[:CATEGORY_OF]->(smokingStatus), (formerlySmoked:SmokingCategory{Name:'Formerly',QName:'SmokingStatus:Formerly'})-[:CATEGORY_OF]->(smokingStatus), (smoking:SmokingCategory{Name:'Smoking',QName:'SmokingStatus:Smoking'})-[:CATEGORY_OF]->(smokingStatus),(unknown:SmokingCategory{Name:'Unknown',QName:'SmokingStatus:Unknown'})-[:CATEGORY_OF]->(smokingStatus)
                CREATE (private:WorkCategory{Name:'Private',QName:'WorkType:Private'})-[:CATEGORY_OF]->(workType), (selfEmployed:WorkCategory{Name:'Self Employed',QName:'WorkType:SelfEmployed'})-[:CATEGORY_OF]->(workType), (children:WorkCategory{Name:'Children',QName:'WorkType:Children'})-[:CATEGORY_OF]->(workType), (governmentJob:WorkCategory{Name:'Government Job',QName:'WorkType:GovernmentJob'})-[:CATEGORY_OF]->(workType), (neverWorked:WorkCategory{Name:'Never Worked',QName:'WorkType:NeverWorked'})-[:CATEGORY_OF]->(workType)
                CREATE (male:GenderCategory{Name:'Male',QName:'Gender:Male'})-[:CATEGORY_OF]->(gender), (female:GenderCategory{Name:'Female',QName:'Gender:Female'})-[:CATEGORY_OF]->(gender)
                
                CREATE (avg:AverageGlucoseLevel{Name:'Average Glucose Level',QName:'AverageGlucoseLevel'})-[:IS_A]->(mrf),(bmi:BMI{Name:'BMI',QName:'BMI'})-[:IS_A]->(mrf),(heart:HeartDiseaseCategory{Name:'Heart Disease',QName:'HeartDisease'})-[:IS_A]->(mrf),(hypertension:HypertensionCategory{Name:'Hypertension',QName:'Hypertension'})-[:IS_A]->(mrf)
                
                CREATE (yesHeart:HeartDiseaseCategory{Name:'Yes',QName:'HeartDisease:Yes'})-[:CATEGORY_OF]->(heart), (noHeart:HeartDiseaseCategory{Name:'No',QName:'HeartDisease:No'})-[:CATEGORY_OF]->(heart)
                CREATE (yesHyper:HypertensionCategory{Name:'Yes',QName:'Hypertension:Yes'})-[:CATEGORY_OF]->(hypertension), (noHyper:HypertensionCategory{Name:'No',QName:'Hypertension:No'})-[:CATEGORY_OF]->(hypertension)
                """
            )
            session.run(query)

    def initialize_risk_factors_explanations(self):
        with self.driver.session() as session:
            ageQuery = (
                """
                MATCH (n) WHERE n.QName = 'Age' SET 
                n.Explanation = 'Aging is the most robust non-modifiable risk factor for incident stroke, which doubles every 10 years after age 55 years. Approximately three-quarters of all strokes occur in persons aged ≥65 years.'
                ,n.MedicalDetails = 
                'Aging and cerebral vasculature. The complex network of the adult brain vasculature measures approximately 370 miles, receives about 20% of total cardiac output, and exchanges 20% of total blood glucose and oxygen. With aging, both cerebral micro- and macro-circulations undergo structural and functional alterations. Age-related microcirculatory changes are presumably mediated by endothelial dysfunction and impaired cerebral autoregulation and neurovascular coupling. Whereas endothelial dysfunction promotes neuro-inflammation, impaired cerebral autoregulation may lead to microvascular injury, and impaired neurovascular coupling fosters a decline in cortical function, all potential targets for future therapeutic interventions. Aging, in otherwise healthy individuals, is associated with numerous noticeable changes in human intracranial and extracranial cerebral arteries that predict the risk of future stroke. Aging and silent cerebrovascular disease. Silent cerebrovascular disease represents structural abnormalities, presumed vascular etiology, on neuroimaging not supported by clinically recognized stroke symptoms. The prevalence of silent cerebrovascular disease increases with advancing age and is recognizable as the following parenchymal lesions: 1) Silent infarcts (silent strokes), prevalence 6% and 28%, exceeds symptomatic stroke by a ratio of 10:1, 2) white matter hyperintensity or hypodensity on neuroimaging represent microvascular disease occurring in 20% to 94% older adults, and 3) cerebral microbleeds indicate silent intracerebral hemorrhages in 38% of general population aged >80 years. These conditions are age dependent and forecast increased risk of future symptomatic strokes'
                """
            )
            session.run(ageQuery)

            marriageQuery = (
                """
                MATCH (n) WHERE n.QName = 'Marriage:Yes' OR n.QName='Marriage:No' SET 
                n.Explanation = 'According to a study with more than 2 million participants [Wong CW, Kwok CS, Narain A, et alMarital status and risk of cardiovascular diseases: a systematic review and meta-analysisHeart 2018;104:1937-1948.], unmarried participants were 1.4 times more likely to develop CVD with a slight increase in the odds of developing CHD , but no difference was observed for incident stroke compared with married participants '
                ,n.MedicalDetails =''
                """
            )
            session.run(marriageQuery)

            residenceQuery = (
                """
                MATCH (n) WHERE n.QName = 'ResidenceType:Rural' OR n.QName = 'ResidenceType:Urban' SET 
                n.Explanation = 'According to a study with 23,280 participants [Howard, George et al. “Contributors to the Excess Stroke Mortality in Rural Areas in the United States.” Stroke vol. 48,7 (2017): 1773-1778. doi:10.1161/STROKEAHA.117.017089]. The estimated risk of incident stroke is 23% higher in large rural cities/towns, and 30% higher in small rural towns or isolated regions (compared to urban areas).'
                ,n.MedicalDetails = ''
                """
            )
            session.run(residenceQuery)

            smokingQuery = (
                """
                MATCH (n) WHERE n.Name = 'Smoking Status' SET 
                n.Explanation = 'Aging is the most robust non-modifiable risk factor for incident stroke, which doubles every 10 years after age 55 years. Approximately three-quarters of all strokes occur in persons aged ≥65 years.'
                ,n.MedicalDetails = ''
                """
            )
            session.run(smokingQuery)

            # workQuery = (
            #     """
            #     MATCH (n:NonMedicalRiskFactor) WHERE n.Name = 'Age' SET
            #     n.Explanation = 'Aging is the most robust non-modifiable risk factor for incident stroke, which doubles every 10 years after age 55 years. Approximately three-quarters of all strokes occur in persons aged ≥65 years.'
            #     ,n.MedicalDetails =
            #     'Aging and cerebral vasculature. The complex network of the adult brain vasculature measures approximately 370 miles, receives about 20% of total cardiac output, and exchanges 20% of total blood glucose and oxygen. With aging, both cerebral micro- and macro-circulations undergo structural and functional alterations. Age-related microcirculatory changes are presumably mediated by endothelial dysfunction and impaired cerebral autoregulation and neurovascular coupling. Whereas endothelial dysfunction promotes neuro-inflammation, impaired cerebral autoregulation may lead to microvascular injury, and impaired neurovascular coupling fosters a decline in cortical function, all potential targets for future therapeutic interventions. Aging, in otherwise healthy individuals, is associated with numerous noticeable changes in human intracranial and extracranial cerebral arteries that predict the risk of future stroke. Aging and silent cerebrovascular disease. Silent cerebrovascular disease represents structural abnormalities, presumed vascular etiology, on neuroimaging not supported by clinically recognized stroke symptoms. The prevalence of silent cerebrovascular disease increases with advancing age and is recognizable as the following parenchymal lesions: 1) Silent infarcts (silent strokes), prevalence 6% and 28%, exceeds symptomatic stroke by a ratio of 10:1, 2) white matter hyperintensity or hypodensity on neuroimaging represent microvascular disease occurring in 20% to 94% older adults, and 3) cerebral microbleeds indicate silent intracerebral hemorrhages in 38% of general population aged >80 years. These conditions are age dependent and forecast increased risk of future symptomatic strokes'
            #     """
            # )

            # session.run(workQuery)

    def clear_knowledge_graph(self):
        with self.driver.session() as session:
            query = (
                "MATCH (n) DETACH DELETE n"
            )
            session.run(query)

    def getExplanation(self, riskFactor):
        with self.driver.session() as session:
            query = (
                """
                MATCH (n) WHERE n.QName = $riskFactor RETURN n
                """
            )
            result = session.run(query, riskFactor=riskFactor)
            return result.single()

    def modifyExplanation(self, riskFactor,
    explanation, medicalDetails):
        with self.driver.session() as session:
            query = (
                """
                MATCH (n) WHERE n.QName = $riskFactor SET 
                n.Explanation = $explanation
                ,n.MedicalDetails = $medicalDetails
                """
            )
            session.run(query, riskFactor=riskFactor, explanation=explanation, medicalDetails=medicalDetails)