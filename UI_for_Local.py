import numpy as np
import streamlit as st
from tensorflow.keras.models import load_model
from model_fetcher import CapsuleLayer
from tensorflow.keras import layers
import csv
st.markdown("""
<style>
body {
    border: 1px solid #CCCCCC; /* Light Gray */
    border-radius: 10px;
    padding: 20px;
}
.title {
    color: white;
    text-align: center;
    background-color: #4CBB17; /* Light Blue */
    padding: 10px;
    border-radius: 5px;
    margin-bottom: 25px;
}

.male_title{
    color: black;
    text-align: center;
    background-color: #ADD8E6; /* Light Blue */
    padding: 10px;
    border-radius: 5px;
    margin-bottom: 25px;
}
.female_title{
    color: black;
    text-align: center;
    background-color: #FF69B4; /* Light Blue */
    padding: 10px;
    border-radius: 5px;
    margin-bottom: 25px;
}
.btn{
    display:flex;

}
</style>
""", unsafe_allow_html=True)


# Displaying the title with added CSS class for color, center alignment, and background color
st.markdown('<h1 class="title">Unravelling Marital Destinies</h1>', unsafe_allow_html=True)

st.write('''
Welcome, dear visitors, to a journey of self-discovery and mutual understanding. Your presence here reflects your commitment to exploring companionship and shared destiny. Together, let's delve into marital harmony and societal cohesion. Embrace the diversity of experiences that shape our understanding of love and partnership. Each interaction contributes to our collective wisdom. Through introspection, we aim to illuminate the path towards enduring connections. Our journey is about acknowledging vulnerabilities and celebrating strengths. Together, we stand on the threshold of exploring the mysteries of love and commitment.
          Let's embark on this odyssey with courage and curiosity, embracing the challenges and triumphs ahead. With each step, we unravel the intricate tapestry of marital destinies.
''')

st.markdown('<h4>We request you and your partner to take a moment to fill the form and gain deeper insights into your relationship.</h4>', unsafe_allow_html=True)


male_responses = []
female_responses = []

def handle_form(gender):
    age = st.number_input("Please enter your age: ", value=None, step=1, key=f"{gender}_age", min_value=21, max_value=100)
    graduation_status = st.selectbox("Are you a graduate?", ("Select", "Yes", "No"), key=f"{gender}_graduation_status")
    work_status = st.selectbox("Are you a working individual?", ("Select", "Yes", "No"), key=f"{gender}_work_status")
    occupation = st.selectbox("Please choose your occupation.", ["Select", "Engineer", "Doctor", "Advocate/Lawyer", "Teacher/Professor/Lecturer", "Business Owner", "Police", "Actor", "Other"], key=f"{gender}_occupation")

    social_background = st.slider("How similar is your and your spouse's social background?", 1, 6, key=f"{gender}_social_background")
    st.write("1 - Definitely not | 6 - Yes, absolutely")

    marriage_type = st.slider("How would you define your marriage from below scale?", 1, 6, key=f"{gender}_marriage_type")
    st.write("1 - Arranged Marriage | 6 - Love Marriage")

    financial_status = st.selectbox("Are you financially independent?", ("Select", "Yes", "No"), key=f"{gender}_financial_status")
    mental_status = st.slider("How strong are you mentally?", 1, 6, key=f"{gender}_mental_status")
    st.write("1 - I'm emotionally weak | 6 - I'm mentally strong")
    children = st.selectbox("While taking important decisions like having children, do you think your spouse's opinion is important?", ("Select", "Yes", "No"), key=f"{gender}_children")
    height = st.number_input("What is your height? (in inches)", value=None, step=1, key=f"{gender}_height", min_value=20, max_value=107)
    income = st.number_input("What is your approximate income per annum? (in lakhs)", value=None, step=1, key=f"{gender}_income", min_value=0)
    interaction_with_spouse_family = st.slider("How close are you with your spouse's family?", 1, 6, key=f"{gender}_interaction_with_spouse_family")
    st.write("1 - Low interaction | 6 - High interaction")
    pre_marital_relation = st.selectbox("Do you have any pre-marital relationships?", ("Select", "Yes", "No"), key=f"{gender}_pre_marital_relation")
    time_before_marriage = st.selectbox("How many years did you spend with your spouse before marriage?", ["Select", "0-1", "2-4", "5-10", "10+"], key=f"{gender}_time_before_marriage")

    if gender == "Male":
        male_responses.append({
            "age": age,
            "graduation_status": graduation_status,
            "work_status": work_status,
            "occupation": occupation,
            "social_background": social_background,
            "marriage_type": marriage_type,
            "financial_status": financial_status,
            "mental_status": mental_status,
            "children": children,
            "height": height,
            "income": income,
            "interaction_with_spouse_family": interaction_with_spouse_family,
            "pre_marital_relation": pre_marital_relation,
            "time_before_marriage": time_before_marriage
        })
    elif gender == "Female":
        female_responses.append({
            "age": age,
            "graduation_status": graduation_status,
            "work_status": work_status,
            "occupation": occupation,
            "social_background": social_background,
            "marriage_type": marriage_type,
            "financial_status": financial_status,
            "mental_status": mental_status,
            "children": children,
            "height": height,
            "income": income,
            "interaction_with_spouse_family": interaction_with_spouse_family,
            "pre_marital_relation": pre_marital_relation,
            "time_before_marriage": time_before_marriage
        })

st.markdown('<h2 class="male_title">Male Section</h2>', unsafe_allow_html=True)
handle_form("Male")

# Add female section
st.markdown('<h2 class="female_title">Female Section</h2>', unsafe_allow_html=True)
handle_form("Female")

submit_button = st.button("Submit")

def handle_input_data():
    male_persp = []
    male_persp.append(1)
    male_persp.append(male_responses[0]["age"]-female_responses[0]["age"])
    if(male_responses[0]["graduation_status"] == "Yes"):
        male_persp.append(1)
    else:
        male_persp.append(0)
    temp = male_responses[0]["occupation"]
    if(temp == "Other" or temp == "None"):
        male_persp.append(5)
    elif(temp=="Actor"):
        male_persp.append(0)
    elif(temp == "Advocate/Lawyer"):
        male_persp.append(1)
    elif(temp == "Business Owner"):
        male_persp.append(2)
    elif(temp == "Doctor"):
        male_persp.append(3)
    elif(temp == "Engineer"):
        male_persp.append(4)
    elif(temp == "Police"):
        male_persp.append(6)
    elif(temp == "Teacher/Professor/Lecturer"):
        male_persp.append(7)

    temp = female_responses[0]["occupation"]
    if(temp == "Other" or temp == "None"):
        male_persp.append(7)
    elif(temp=="Actor"):
        male_persp.append(0)
    elif(temp == "Advocate/Lawyer"):
        male_persp.append(1)
    elif(temp == "Business Owner"):
        male_persp.append(2)
    elif(temp == "Doctor"):
        male_persp.append(3)
    elif(temp == "Engineer"):
        male_persp.append(4)
    elif(temp == "Police"):
        male_persp.append(8)
    elif(temp == "Teacher/Professor/Lecturer"):
        male_persp.append(9)

    temp = female_responses[0]["graduation_status"]
    if(temp == "Yes"):
        male_persp.append(1)
    elif(temp == "No"):
        male_persp.append(0)

    temp = male_responses[0]["work_status"]
    if(temp == "Yes"):
        male_persp.append(1)
    elif(temp == "No"):
        male_persp.append(0)


    temp = female_responses[0]["work_status"]
    if(temp == "Yes"):
        male_persp.append(1)
    elif(temp == "No"):
        male_persp.append(0)

    temp = male_responses[0]["social_background"]
    male_persp.append(temp)


    temp = male_responses[0]["marriage_type"]
    male_persp.append(temp)


    temp = male_responses[0]["financial_status"]
    if(temp == "Yes"):
        male_persp.append(1)
    elif(temp == "No"):
        male_persp.append(0)


    temp = female_responses[0]["financial_status"]
    if(temp == "Yes"):
        male_persp.append(1)
    elif(temp == "No"):
        male_persp.append(0)


    temp = male_responses[0]["mental_status"]
    male_persp.append(temp)


    temp = female_responses[0]["mental_status"]
    male_persp.append(temp)

    temp = male_responses[0]["children"]
    if(temp == "Yes"):
        male_persp.append(1)
    elif(temp == "No"):
        male_persp.append(0)


    temp = abs(male_responses[0]["height"]-female_responses[0]["height"])
    male_persp.append(temp)

    temp = male_responses[0]["income"]
    male_persp.append(temp)

    temp = female_responses[0]["income"]
    male_persp.append(temp)

    temp = male_responses[0]["interaction_with_spouse_family"]
    male_persp.append(temp)


    temp = male_responses[0]["pre_marital_relation"]
    if(temp == "Yes"):
        male_persp.append(1)
    elif(temp == "No"):
        male_persp.append(0)

    temp = female_responses[0]["pre_marital_relation"]
    if(temp == "Yes"):
        male_persp.append(1)
    elif(temp == "No"):
        male_persp.append(0)

    temp = male_responses[0]["time_before_marriage"]
    if(temp == "0-1 "):
        male_persp.append(0)
    elif(temp == "10+"):
        male_persp.append(2)
    elif(temp == "2-4"):
        male_persp.append(3)
    elif(temp == "5-10"):
        male_persp.append(4)
    else:
        male_persp.append(1)



    # Considering female perspective
    female_persp = [0]
    female_persp.append(female_responses[0]["age"]-male_responses[0]["age"])
    if(female_responses[0]["graduation_status"] == "Yes"):
        female_persp.append(1)
    else:
        female_persp.append(0)
    temp = female_responses[0]["occupation"]
    if(temp == "Other" or temp == "None"):
        female_persp.append(5)
    elif(temp=="Actor"):
        female_persp.append(0)
    elif(temp == "Advocate/Lawyer"):
        female_persp.append(1)
    elif(temp == "Business Owner"):
        female_persp.append(2)
    elif(temp == "Doctor"):
        female_persp.append(3)
    elif(temp == "Engineer"):
        female_persp.append(4)
    elif(temp == "Police"):
        female_persp.append(6)
    elif(temp == "Teacher/Professor/Lecturer"):
        female_persp.append(7)

    temp = male_responses[0]["occupation"]
    if(temp == "Other" or temp == "None"):
        female_persp.append(7)
    elif(temp=="Actor"):
        female_persp.append(0)
    elif(temp == "Advocate/Lawyer"):
        female_persp.append(1)
    elif(temp == "Business Owner"):
        female_persp.append(2)
    elif(temp == "Doctor"):
        female_persp.append(3)
    elif(temp == "Engineer"):
        female_persp.append(4)
    elif(temp == "Police"):
        female_persp.append(8)
    elif(temp == "Teacher/Professor/Lecturer"):
        female_persp.append(9)

    temp = male_responses[0]["graduation_status"]
    if(temp == "Yes"):
        female_persp.append(1)
    elif(temp == "No"):
        female_persp.append(0)

    temp = female_responses[0]["work_status"]
    if(temp == "Yes"):
        female_persp.append(1)
    elif(temp == "No"):
        female_persp.append(0)


    temp = male_responses[0]["work_status"]
    if(temp == "Yes"):
        female_persp.append(1)
    elif(temp == "No"):
        female_persp.append(0)

    temp = female_responses[0]["social_background"]
    female_persp.append(temp)


    temp = female_responses[0]["marriage_type"]
    female_persp.append(temp)


    temp = female_responses[0]["financial_status"]
    if(temp == "Yes"):
        female_persp.append(1)
    elif(temp == "No"):
        female_persp.append(0)


    temp = male_responses[0]["financial_status"]
    if(temp == "Yes"):
        female_persp.append(1)
    elif(temp == "No"):
        female_persp.append(0)


    temp = female_responses[0]["mental_status"]
    female_persp.append(temp)


    temp = male_responses[0]["mental_status"]
    female_persp.append(temp)

    temp = female_responses[0]["children"]
    if(temp == "Yes"):
        female_persp.append(1)
    elif(temp == "No"):
        female_persp.append(0)


    temp = abs(female_responses[0]["height"]-male_responses[0]["height"])
    female_persp.append(temp)

    temp = female_responses[0]["income"]
    female_persp.append(temp)

    temp = male_responses[0]["income"]
    female_persp.append(temp)

    temp = female_responses[0]["interaction_with_spouse_family"]
    female_persp.append(temp)


    temp = female_responses[0]["pre_marital_relation"]
    if(temp == "Yes"):
        female_persp.append(1)
    elif(temp == "No"):
        female_persp.append(0)

    temp = male_responses[0]["pre_marital_relation"]
    if(temp == "Yes"):
        female_persp.append(1)
    elif(temp == "No"):
        female_persp.append(0)

    temp = female_responses[0]["time_before_marriage"]
    if(temp == "0-1 "):
        female_persp.append(0)
    elif(temp == "10+"):
        female_persp.append(2)
    elif(temp == "2-4"):
        female_persp.append(3)
    elif(temp == "5-10"):
        female_persp.append(4)
    elif(temp == "Select"):
        pass
    else:
        female_persp.append(1)

    # print("Inside function", len(male_persp), " ", len(female_persp))
    return male_persp, female_persp


if submit_button:
    male_persp, female_persp = handle_input_data()
    # print("At submit", len(male_persp), " ", len(female_persp))
    if len(male_persp)!=22 or len(female_persp) != 22:
      st.warning("Please fill all the fields!", icon="⚠️")
    else:
        st.write("Submitted")
        model = load_model('my_model.h5', custom_objects={'CapsuleLayer': CapsuleLayer})

        male_percent = model.predict([male_persp])
        female_percent = model.predict([female_persp])
        output_for_male = np.argmax(male_percent)
        output_for_female = np.argmax(female_percent)

        st.write("From male's perspective:")
        st.write(male_percent)
        st.write("From female's perspective:")
        st.write(female_percent)


        file_name = "data_from_UI.csv"
        temp_male_persp = list(male_persp.copy())
        temp_female_persp = list(female_persp.copy())
        temp_male_persp.append(output_for_male)
        temp_female_persp.append(output_for_female)


        # st.write(temp_male_persp)
        # st.write(temp_female_persp)
        with open(file_name, mode='a', newline='') as file:
            f_data = csv.writer(file)
            f_data.writerow(temp_male_persp)
            f_data.writerow(temp_female_persp)



        if (male_percent[0][1] + female_percent[0][1])/2 <= 0.50:
            st.title("Oops! There are things you can consider to make your relationship beautiful!💔")
        else:
            st.title("You're maintaining a happy relationship, keep it up!❤️")