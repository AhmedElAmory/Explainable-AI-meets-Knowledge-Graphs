# %% Imports
from utils import DataLoader
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, accuracy_score
from interpret.blackbox import LimeTabular
from interpret import show
import pandas as pd 

class Model():
        def loadData(self):
                # %% Load and preprocess data
                self.data_loader = DataLoader()
                self.data_loader.load_dataset()
                self.data_loader.preprocess_data()
                # Split the data for evaluation
                self.X_train, self.X_test, self.y_train, self.y_test = self.data_loader.get_data_split()
                # Oversample the train data
                self.X_train, self.y_train = self.data_loader.oversample(self.X_train, self.y_train)

        def train(self):
                # %% Fit blackbox model
                self.rf = RandomForestClassifier(random_state=42)
                self.rf.fit(self.X_train, self.y_train)
                self.y_pred = self.rf.predict(self.X_test)
                print(f"F1 Score {f1_score(self.y_test, self.y_pred, average='macro')}")
                print(f"Accuracy {accuracy_score(self.y_test, self.y_pred)}")

        def explainCase(self,data):
                self.caseValues=data
                # Convert the dictionary into DataFrame 
                df = pd.DataFrame([data])
                data_pred=self.rf.predict(df)
                # print(df)
                print(data_pred[0])

                # Initilize Lime for Tabular data
                lime = LimeTabular(predict_fn=self.rf.predict_proba, 
                                data=self.X_train, 
                                random_state=1)

                self.lime_local = lime.explain_local(df[-1:], 
                                                data_pred[-1:], 
                                                name='Stroke Probability')
                show(self.lime_local)
                print(self.lime_local.data(0))

        def getFeatures(self):
                switcher = {
                'gender_Female':'Gender:Female',
                'gender_Male':'Gender:Male',
                'ever_married_No':'Marriage:No',
                'ever_married_Yes':'Marriage:Yes',
                'work_type_Govt_job':'WorkType:GovernmentJob',
                'work_type_Never_worked':'WorkType:NeverWorked',
                'work_type_Private':'WorkType:Private',
                'work_type_Self-employed':'WorkType:SelfEmployed',
                'work_type_children':'WorkType:Children',
                'Residence_type_Rural':'ResidenceType:Rural',
                'Residence_type_Urban':'ResidenceType:Urban',
                'smoking_status_Unknown':'SmokingStatus:Unknown',
                'smoking_status_formerly smoked':'SmokingStatus:Formerly',
                'smoking_status_never smoked':'SmokingStatus:Never',
                'smoking_status_smokes':'SmokingStatus:Smoking',
                'hypertension_Yes':'Hypertension:Yes',
                'hypertension_No':'Hypertension:No',
                'heart_disease_No':'HeartDisease:No',
                'heart_disease_Yes':'HeartDisease:Yes',
                'age':'Age',
                'avg_glucose_level':'AverageGlucoseLevel',
                'bmi':'BMI',
                }

                qq=self.lime_local.data(0)
                # %% Get feature importance
                print("The probability of you getting a stroke is: ", qq.get('perf').get('predicted')*100, "%")
                # print(qq.get('perf').get('predicted'))
                mostInfluentalFeatures=[]
                for idx,i in enumerate(qq.get('scores')):
                #     print(idx)
                #     print(i)
                        if(i>0 and len(mostInfluentalFeatures)<3 and self.caseValues.get(qq.get('names')[idx])>0):
                                mostInfluentalFeatures.append(qq.get('names')[idx])
                print("The most influential features are:\n", mostInfluentalFeatures)
                wrapper={}
                wrapper['text']="The probability of you getting a stroke is: "+ str(int(qq.get('perf').get('predicted')*100))+ "%"+"\n"+"The most influential features are:\n"
                for i in mostInfluentalFeatures:
                        wrapper['text']+=switcher.get(i)+"\n"
                wrapper['features']=mostInfluentalFeatures
                return wrapper
                # print(mostInfluentalFeatures)

# # %% find strokesss
# for (idx,i) in enumerate(y_pred) :
#         if(i == 1):
#                 print(X_test[idx:idx+1])
#                 print (idx)

# # %% Apply lime
# # Initilize Lime for Tabular data
# lime = LimeTabular(predict_fn=rf.predict_proba, 
#                    data=X_train, 
#                    random_state=1)
# # Get local explanations
# lime_local = lime.explain_local(X_test[300:310], 
#                                 y_pred[300:310], 
#                                 name='LIME')

# show(lime_local)

# # %%
# print(lime_local.data(5))
# print(X_test[215:216])
# # print(y_pred[-1:])

# # %%

# # %%
# show(lime_local)

# # %%
# qq=lime_local.data(0)

# # %%
# print("The probability of you getting a stroke is: ", qq.get('perf').get('predicted')*100, "%")
# # print(qq.get('perf').get('predicted'))
# mostInfluentalFeatures=[]
# for idx,i in enumerate(qq.get('scores')):
# #     print(idx)
# #     print(i)
#     if(i>0 and len(mostInfluentalFeatures)<3):
#         mostInfluentalFeatures.append(qq.get('names')[idx])
# print("The most influential features are:\n", mostInfluentalFeatures)
# # print(mostInfluentalFeatures)

# # %% query the database for the explanations

