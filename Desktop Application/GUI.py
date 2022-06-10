
# Import module
from tkinter import *
from strokeModel import Model
import sys
import logging
from knowledgeGraph import App

bolt_url = "bolt://localhost:7687"
user = "neo4j"
password = "thesis"
App.enable_log(logging.INFO, sys.stdout)
app = App(bolt_url, user, password)

model=Model()
model.loadData()
model.train()

# Create object
root = Tk()
root.title("Stroke Prediction")
# Adjust size
root.geometry( "280x600" )
# Change the label text
def show():
    data={}
    data['gender_Female']=1 if gender.get()=="Female" else 0
    data['gender_Male']=1 if gender.get()=="Male" else 0
    data['ever_married_No']=1 if married.get()=="No" else 0
    data['ever_married_Yes']=1 if married.get()=="Yes" else 0
    data['work_type_Govt_job']=1 if workType.get()=="Government Job" else 0
    data['work_type_Never_worked']=1 if workType.get()=="Never Worked" else 0
    data['work_type_Private']=1 if workType.get()=="Private" else 0
    data['work_type_Self-employed']=1 if workType.get()=="Self-Employed" else 0
    data['work_type_children']=1 if workType.get()=="Children" else 0
    data['Residence_type_Rural']=1 if residenceType.get()=="Rural" else 0
    data['Residence_type_Urban']=1 if residenceType.get()=="Urban" else 0
    data['smoking_status_Unknown']=1 if smokingStatus.get()=="Unknown" else 0
    data['smoking_status_formerly smoked']=1 if smokingStatus.get()=="Formerly Smoked" else 0
    data['smoking_status_never smoked']=1 if smokingStatus.get()=="Never Smoked" else 0
    data['smoking_status_smokes']=1 if smokingStatus.get()=="Smokes" else 0
    data['hypertension_No']=1 if hypertension.get()=="No" else 0
    data['hypertension_Yes']=1 if hypertension.get()=="Yes" else 0
    data['heart_disease_No']=1 if heartDisease.get()=="No" else 0
    data['heart_disease_Yes']=1 if heartDisease.get()=="Yes" else 0
    data['age']=int(age.get("1.0", "end-1c"))
    data['avg_glucose_level']=int(glucoseLevel.get("1.0", "end-1c"))
    data['bmi']=int(bmi.get("1.0", "end-1c"))
    print(data)
    model.explainCase(data)
    global wrapper 
    wrapper = model.getFeatures()
    label.config( text = wrapper['text'])
    Button( root , text = "Learn More Using Our Knowledge Graph!" , command = showExplanations ).grid(row=12, column=0,columnspan=2)


def switcher(argument):
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

    return switcher.get(argument, "nothing")

def showExplanations():
    global win 
    win = Toplevel()
    win.wm_title("Explanation")
    win.geometry("650x700")
    

    for idx,x in enumerate(wrapper['features']):
      res=app.getExplanation(switcher(x))
      if(res):
        print(res['n']['Explanation'])
        print(res['n']['MedicalDetails'])
        l = Label(win, text="Risk Factor "+str(idx+1)+": "+switcher(x),font=("Arial", 15))
        l.grid(row=idx*5, column=0)
        l = Label(win, text="Explanation:")
        l.grid(row=idx*5+1, column=0)
        l = Label(win, text=res['n']['Explanation'],wraplength=600)
        l.grid(row=idx*5+2, column=0)
        l = Label(win, text="Medical Details:")
        l.grid(row=idx*5+3, column=0)
        l = Label(win, text=res['n']['MedicalDetails'],wraplength=600)
        l.grid(row=idx*5+4, column=0)

    

    b = Button(win, text="Close", command=win.destroy)
    b.grid(row=16, column=0)

def getExplanation():
    
    print('called')
    res=app.getExplanation(riskFactor.get())
    if(res):
        print(res['n']['Explanation'])
        print(res['n']['MedicalDetails'])
        # l = Label(win, text=res['n']['Explanation'],wraplength=400)
        # l.grid(row=3, column=0)
        T1.delete('1.0',END)
        T1.insert('1.0','There is no Existing Explanation in our knowledge graph yet' if res['n']['Explanation']==None else res['n']['Explanation'])
        T2.delete('1.0',END)
        T2.insert('1.0','There is no Medical Details in our knowledge graph yet' if res['n']['MedicalDetails']==None else res['n']['MedicalDetails'])

      
def saveNewExplanation():
    app.modifyExplanation(riskFactor.get(),T1.get("1.0", "end-1c"),T2.get("1.0", "end-1c"))

def modifyKnowledgeGraph():
    global win
    win = Toplevel()
    win.wm_title("Knowledge Graph")
    win.geometry("600x300")
    knowledgeGraphOptions = [
    'Gender:Female',
    'Gender:Male',
    'Marriage:No',
    'Marriage:Yes',
    'WorkType:GovernmentJob',
    'WorkType:NeverWorked',
    'WorkType:Private',
    'WorkType:SelfEmployed',
    'WorkType:Children',
    'ResidenceType:Rural',
    'ResidenceType:Urban',
    'SmokingStatus:Unknown',
    'SmokingStatus:Formerly',
    'SmokingStatus:Never',
    'SmokingStatus:Smoking',
    'Age',
    'Hypertension:No',
    'Hypertension:Yes',
    'HeartDisease:No',
    'HeartDisease:Yes',
    'AverageGlucoseLevel',
    'BMI',
    ]

    global riskFactor 
    riskFactor = StringVar()
    riskFactor.set(knowledgeGraphOptions[0])

    Label( win , text = "Choose a risk Factor" ).grid(row=0, column=0)
    drop = OptionMenu( win , riskFactor , *knowledgeGraphOptions )
    drop.grid(row=0, column=1)
    
    b = Button(win, text="Get Explanation", command=getExplanation)
    b.grid(row=0, column=2, columnspan=4)
    global T1,T2

    l = Label(win, text="Explanation:")
    l.grid(row=3, column=0)
    T1 = Text(win, height = 5, width = 52)
    T1.grid(row=3, column=1,columnspan=2)
    
    
    l = Label(win, text="Medical Details:")
    l.grid(row=4, column=0)
    T2 = Text(win, height = 5, width = 52)
    T2.grid(row=4, column=1,columnspan=2)

    b = Button(win, text="Save New Explanation", command=saveNewExplanation)
    b.grid(row=6, column=2, columnspan=4)

    x = Button(win, text="Close", command=win.destroy)
    x.grid(row=7, column=0)


# Dropdown menu options
genderOptions = [
    "Male",
    "Female"
]

defaultOptions = [
    "Yes",
    "No"
]

workOptions = [
    "Never Worked",
    "Government Job",
    "Private",
    "Self-Employed",
    "Children"
]

residenceOptions = [
    "Urban",
    "Rural"
]

smokingOptions = [
    "Unknown",
    "Formerly Smoked",
    "Never Smoked",
    "Smokes"
]
# datatype of menu text
gender = StringVar()
married = StringVar()
workType = StringVar()
residenceType = StringVar()
smokingStatus = StringVar()
heartDisease = StringVar()
hypertension = StringVar()
# initial menu text
gender.set( "Male" )
married.set("No")
workType.set("Never Worked")
residenceType.set("Urban")
smokingStatus.set("Unknown")
heartDisease.set("No")
hypertension.set("No")
# Create Dropdown menu
root.grid_columnconfigure(0, minsize=140)
root.grid_columnconfigure(1, minsize=140)
Label( root , text = "Gender" ).grid(row=0, column=0)
drop = OptionMenu( root , gender , *genderOptions )
drop.grid(row=0, column=1)

Label( root , text = "Married?" ).grid(row=1, column=0)
drop = OptionMenu( root , married , *defaultOptions )
drop.grid(row=1, column=1)

Label( root , text = "Work Type" ).grid(row=2, column=0)
drop = OptionMenu( root , workType , *workOptions )
drop.grid(row=2, column=1)

Label( root , text = "Residence Type" ).grid(row=3, column=0)
drop = OptionMenu( root , residenceType , *residenceOptions )
drop.grid(row=3, column=1)

Label( root , text = "Smoking Status" ).grid(row=4, column=0)
drop = OptionMenu( root , smokingStatus , *smokingOptions )
drop.grid(row=4, column=1)

Label( root , text = "Age" ).grid(row=5, column=0)
# age = Scale(root, from_=1, to=120, orient=HORIZONTAL)
# age.grid(row=5, column=1)

age = Text(root, height = 1, width = 5)
age.grid(row=5, column=1,columnspan=1)

Label( root , text = "Heart Disease" ).grid(row=6, column=0)
drop = OptionMenu( root , heartDisease , *defaultOptions )
drop.grid(row=6, column=1)

Label( root , text = "Hypertension" ).grid(row=7, column=0)
drop = OptionMenu( root , hypertension , *defaultOptions )
drop.grid(row=7, column=1)

Label( root , text = "Average Glucose Level" ).grid(row=8, column=0)
# glucoseLevel = Scale(root, from_=1, to=300, orient=HORIZONTAL)
# glucoseLevel.grid(row=8, column=1)

glucoseLevel = Text(root, height = 1, width = 5)
glucoseLevel.grid(row=8, column=1,columnspan=1)

Label( root , text = "BMI" ).grid(row=9, column=0)
# bmi = Scale(root, from_=1, to=60, orient=HORIZONTAL)
# bmi.grid(row=9, column=1)

bmi = Text(root, height = 1, width = 5)
bmi.grid(row=9, column=1,columnspan=1)

label = Label(root)
label.grid(row=11, column=0,columnspan=2)
e1 = Entry(root)

# T = Text(root, height = 5, width = 52)
# T.grid(row=12, column=0,columnspan=2)
  
# Create button, it will change label text
button = Button( root , text = "Get Stroke Probability" , command = show ).grid(row=10, column=0,columnspan=2)
Label( root , text = "Are you a doctor?" ).grid(row=13, column=0,columnspan=2)
Button( root , text = "Contribute To The Knowledge Graph" , command = modifyKnowledgeGraph ).grid(row=16, column=0,columnspan=2)
# Create Label
Label( root , text = " " ).grid(row=11, column=1)
  
# Execute tkinter
root.mainloop()