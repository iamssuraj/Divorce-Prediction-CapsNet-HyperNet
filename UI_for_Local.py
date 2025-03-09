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

st.write('''Relationships are complicated—let’s see if yours is built to last or heading for trouble.''')

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
    income = st.number_input("What is your approximate income per annum? (in lakhs)", value=0, step=1, key=f"{gender}_income")
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
    if(male_responses[0]["age"] == None or female_responses[0]["age"] == None or male_responses[0]["height"] == None or female_responses[0]["height"] == None):
        return [], [] 
    else:
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
        st.divider()
        st.write("Submitted")
        model = load_model('my_model.h5', custom_objects={'CapsuleLayer': CapsuleLayer})

        male_percent = model.predict(np.array([male_persp]))
        female_percent = model.predict(np.array([female_persp]))
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

        st.markdown("Explanation to the table:")
        st.markdown('''
            The headers in the table above - 0 represents the likeliness of divorce, and 1 represents the
            likeliness of a successful marriage. So, the percentages indicate the likeliness of both the 
            outputs from both the individual's perspectives.
            ''')

        if (male_percent[0][1] + female_percent[0][1])/2 <= 0.50:
            st.title("Oops! There are things you can consider to make your relationship beautiful!💔")
        else:
            st.title("You're maintaining a happy relationship, keep it up!❤️")

        st.write('''
                 As per the data we've obtained, 
                 the following are the most contributing factors for unhappy marriage''')
        st.image("data:image/png;base64,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2JBkrFu3LsPjpqSkZBiLiIgwPD09jdTUVMMwDOPKlStGwYIFjRo1ahjXrl2zzpszZ44hyWjUqJF1bP78+YaTk5OxceNGm2NOnz7dkGRs3rw5w+PdcPXqVcPPz88IDQ01Ll++bB3//vvvDUnG8OHDrWM3vmc7duy46fEymztlyhTD29vb+rw7dOhgNG7c2DCMf17PVq1a2ez739fn6tWrRmhoqNGkSROb8bNnzxoFChQwHn30UePKlStG1apVjeLFixvx8fG3zPbxxx8bkoxly5Zl+TwMwzAGDBhgSLJ5fRMTE42SJUsawcHBRlpams1zPnHihM3+69aty/BeuPF+nTdvnnXsypUrRkBAgNG+fXvr2I4dOwxJRmRkZLay3nisxYsX24xXqVLF8PPzMy5evGgd27dvn+Hk5GR0797dOjZixAhDktGlSxe7Hu9mt7Nnz1rnZva+f/zxx41SpUpZ71+6dMnw9vY2atWqZfN+NIz/+3k1jOy/fjdz4+f4v7cRI0YYhmEYo0ePNry8vIwjR47Y7DdkyBAjT548RkxMzE2f183er15eXkaPHj0yZOnRo4dRokSJDOM3vhf/JslwcnIyfvvtN5vxXr16GUWKFDH++usvm/HOnTsbvr6+mb72AAAAwP2OpT4BAACAe1CzZs1UuHBhBQUFqXPnzsqbN6+WLVumokWL6ptvvlF6ero6duyov/76y3oLCAhQSEiI1q1bZ3MsNzc3PffcczZjS5cuVaFChdSvX78Mj33jTKTFixfL19dXjz76qM3jVK9eXXnz5s3wOA899JD17CtJKly4sMqVK6fjx49n6zl7eHhYv75xplSDBg2UkpKiw4cPS5J27typixcv6vnnn7e51lzXrl2VP39+m+MtXrxYFSpUUPny5W3y31g29b/5/23nzp06f/68XnrpJZvrhLVq1Urly5fPsJzl7ejYsaMuX76s77//XomJifr+++9vusynZPv6/P3334qPj1eDBg20e/dum3kBAQGaOnWqVq1apQYNGmjv3r2aPXu2fHx8bpknISFBkuTt7Z2t/D/++KNq1qxps+Rl3rx51adPH508eVK///57to7zX3nz5rW5xpyrq6tq1qyZ7fdRdp09e1Z79+5VeHi4ChQoYB2vVKmSHn300UyXRX3hhRfseozhw4dr1apVGW7/frx/f1/j4+P1119/qVGjRjp+/Lji4+MlSatWrVJiYqKGDBmS4bp1/1328k5fv1q1amXI2717d0n//Ew1aNBA+fPnt/mZatasmdLS0vTLL79k+rxu9X7NKY0aNdJDDz1kvW8YhpYuXaonn3xShmHY5H388ccVHx+fa1kAAAAAM7HUJwAAAHAPmjp1qsqWLStnZ2f5+/urXLlycnL65+/2oqOjZRiGQkJCMt3338tvSlLRokXl6upqM3bs2DGVK1fOpjz7r+joaMXHx8vPzy/T7efPn7e5X7x48Qxz8ufPn+F6gDfz22+/6a233tLatWutJdQNNwqQP/74Q5JUpkwZm+3Ozs4ZlmWMjo7WoUOHVLhw4Wzl/7cbj1OuXLkM28qXL69Nmzbd+slkQ+HChdWsWTN98cUXSklJUVpamp5++umbzv/+++/17rvvau/evTbXKMzsWnydO3fWggUL9MMPP6hPnz5q2rRplnluFIOJiYnZyv/HH3+oVq1aGcZvLN36xx9/KDQ0NFvH+rdixYpleE758+fX/v377T7Wrdzqe1yhQgWtXLlSycnJ8vLyso6XLFnSrscICwtTs2bNbjln8+bNGjFihLZs2aKUlBSbbfHx8fL19bUu9Zud1/NOX79ChQrdNHN0dLT279+frZ8pe96vOeG/35sLFy7o0qVLmjFjhmbMmJFlXgAAAMBRUPwBAAAA96CaNWvq4YcfznRbenq6LBaLfvrpp0yvxZY3b16b+/8+88Ye6enp8vPz08KFCzPd/t9f/t/sunBGNq6FdunSJTVq1Eg+Pj565513VLp0abm7u2v37t0aPHiw0tPTbyt/WFiYJkyYkOn2oKAgu4+Z05555hk9//zzio2NVYsWLWyuzfhvGzduVOvWrdWwYUN9+umnKlKkiFxcXBQZGakvvvgiw/yLFy9q586dkqTff/9d6enp1uL4ZsqXLy9JOnDggNq0aXNHz+vfblb0pKWlZTp+J++j3Ha7P0s3c+zYMTVt2lTly5fXhAkTFBQUJFdXV/3444+aOHHibb3vc/P1S09P16OPPqo33ngj0+1ly5aVZP/7NTP2vm/++7258dp169ZNPXr0yHSfSpUqZSsLAAAAcD+h+AMAAADuM6VLl5ZhGCpZsqT1F+23c4xt27bp2rVrGc4Q/Pec1atXq169ejlWeNzsl/nr16/XxYsX9c0336hhw4bW8RMnTtjMK1GihCTp6NGjaty4sXX8+vXrOnnypM0v8kuXLq19+/apadOmdp9ldONxoqKirEuD3hAVFWXdfqfatm2riIgIbd26VYsWLbrpvKVLl8rd3V0rV66Um5ubdTwyMjLT+X379lViYqLGjh2roUOHatKkSRo0aNAts9SvX1/58+fXl19+qTfffPOmBdINJUqUUFRUVIbxG8uy3niNbizBeunSJZt5N864ux05cdbYv7/H/3X48GEVKlTI5my/3PC///1PV65c0fLly23OmP3vMrSlS5eWJB08eDDD2a53U+nSpZWUlJTlWYz2vF9v9r3Mnz9/hveMlP33TeHCheXt7a20tLQs8wIAAACOhGv8AQAAAPeZdu3aKU+ePBo1alSGs3gMw9DFixezPEb79u31119/acqUKRm23Thmx44dlZaWptGjR2eYc/369Ux/KZ+VG0XKf/e9UTL9+/lcvXpVn376qc28hx9+WAULFtTMmTN1/fp16/jChQszLCnasWNH/fnnn5o5c2aGHJcvX1ZycvJNcz788MPy8/PT9OnTbZYp/Omnn3To0CG1atUqi2eaPXnz5tW0adM0cuRIPfnkkzedlydPHlksFpuznU6ePKlvv/02w9wlS5Zo0aJFGjdunIYMGaLOnTvrrbfe0pEjR26ZxdPTU4MHD9ahQ4c0ePDgTM8QW7BggbZv3y5JatmypbZv364tW7ZYtycnJ2vGjBkKDg62Xm/tRmn17+u/paWl3XT5xey42fvIHkWKFFGVKlU0d+5cm+McPHhQP//8s1q2bHnbx86uzN738fHxGQqyxx57TN7e3ho7dqxSU1Nttt3NMyE7duyoLVu2aOXKlRm2Xbp0yfozac/71cvLK9PvY+nSpRUfH2+zROnZs2e1bNmybGXNkyeP2rdvr6VLl+rgwYMZtl+4cCFbxwEAAADuN5zxBwAAANxnSpcurXfffVdDhw7VyZMn1aZNG3l7e+vEiRNatmyZ+vTpo9dee+2Wx+jevbvmzZunQYMGafv27WrQoIGSk5O1evVqvfTSS3rqqafUqFEjRUREaOzYsdq7d68ee+wxubi4KDo6WosXL9bHH398y2vSZaZKlSrKkyeP3n//fcXHx8vNzU1NmjRR3bp1lT9/fvXo0UP9+/eXxWLR/PnzM5Qarq6uGjlypPr166cmTZqoY8eOOnnypObMmaPSpUvbnD30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XnrpJX311VdKS0uTJOXJk0edOnXS1KlT5evra3JCAAAAW8nJyRo3bpzWrFmj8+fPKz093Wb78ePHTUoGAACQ0bfffqtFixapdu3aslgs1vGKFSvq2LFjJiYDgJxH8QcAJuvdu7f27Nmj77//XnXq1JEkbdmyRa+88ooiIiL01VdfmZwQAADAVu/evbVhwwY9++yzKlKkiM0v0AAAAO41Fy5ckJ+fX4bx5ORkPscAcDgWwzAMs0MAwIPMy8tLK1euVP369W3GN27cqObNmys5OdmkZAAAAJnLly+ffvjhB9WrV8/sKAAAAFlq2LChOnTooH79+snb21v79+9XyZIl1a9fP0VHR2vFihVmRwSAHMMZfwBgsoIFC2a6nKevr6/y589vQiIAAIBby58/vwoUKGB2DAAAgGwZM2aMWrRood9//13Xr1/Xxx9/rN9//12//vqrNmzYYHY8AMhRTmYHAIAH3VtvvaVBgwYpNjbWOhYbG6vXX39db7/9tonJAAAAMjd69GgNHz5cKSkpZkcBAADIUv369bV3715dv35dYWFh+vnnn+Xn56ctW7aoevXqZscDgBzFUp8AYLKqVavq6NGjunLliooXLy5JiomJkZubm0JCQmzm7t6924yIAAAANqpWrapjx47JMAwFBwfLxcXFZjufWQAAAADAHCz1CQAma9OmjdkRAAAA7MLnFwAAcD9JSEjIdNxiscjNzU2urq53OREA5B7O+AMAAAAAAAAAOCwnJydZLJabbi9WrJjCw8M1YsQIOTlxdSwA9zfO+AMAAAAA2O3SpUtasmSJjh07ptdff10FChTQ7t275e/vr6JFi5odDwAAwGrOnDkaNmyYwsPDVbNmTUnS9u3bNXfuXL311lu6cOGCxo8fLzc3N7355psmpwWAO8MZfwBgsrS0NE2cOFFff/21YmJidPXqVZvtcXFxJiUDAADI3P79+9WsWTP5+vrq5MmTioqKUqlSpfTWW28pJiZG8+bNMzsiAACAVdOmTRUREaGOHTvajH/99df67LPPtGbNGs2fP1/vvfeeDh8+bFJKAMgZnLcMACYbNWqUJkyYoE6dOik+Pl6DBg1Su3bt5OTkpJEjR5odDwAAIINBgwYpPDxc0dHRcnd3t463bNlSv/zyi4nJAAAAMvr1119VtWrVDONVq1bVli1bJEn169dXTEzM3Y4GADmO4g8ATLZw4ULNnDlTr776qpydndWlSxd9/vnnGj58uLZu3Wp2PAAAgAx27NihiIiIDONFixZVbGysCYkAAABuLigoSLNmzcowPmvWLAUFBUmSLl68qPz589/taACQ47jGHwCYLDY2VmFhYZKkvHnzKj4+XpL0xBNP6O233zYzGgAAQKbc3NyUkJCQYfzIkSMqXLiwCYkAAABubvz48erQoYN++ukn1ahRQ5K0c+dOHT58WEuWLJH0zx82derUycyYAJAjOOMPAExWrFgxnT17VpJUunRp/fzzz5L++cDp5uZmZjQAAIBMtW7dWu+8846uXbsmSbJYLIqJidHgwYPVvn17k9MBAADYat26taKiotSyZUvFxcUpLi5OLVq00OHDh/XEE09Ikl588UVNmDDB5KQAcOcshmEYZocAgAfZkCFD5OPjozfffFOLFi1St27dFBwcrJiYGA0cOFDjxo0zOyIAAICN+Ph4Pf3009q5c6cSExMVGBio2NhY1alTRz/++KO8vLzMjggAAAAADySKPwC4x2zZskVbtmxRSEiInnzySbPjAAAA3NTmzZu1b98+JSUlqVq1amrWrJnZkQAAAG4qJSVFMTExunr1qs14pUqVTEoEADmP4g8AAAAAkG3Xrl2Th4eH9u7dq9DQULPjAAAAZOnChQt67rnn9NNPP2W6PS0t7S4nAoDc42x2AAB4UKWnp+u3335TWFiYJGn69Ok2f3GWJ08evfjii3Jy4nKsAADg3uHi4qLixYvzCzIAAHDfGDBggC5duqRt27bpkUce0bJly3Tu3Dm9++67+uijj8yOBwA5ijP+AMAkX3zxhaZPn65ffvlFkuTt7a18+fLJ2fmfv8n466+/NGnSJPXq1cvMmAAAABnMmjVL33zzjebPn68CBQqYHQcAAOCWihQpou+++041a9aUj4+Pdu7cqbJly2r58uX64IMPtGnTJrMjAkCO4Yw/ADBJZGSk+vbtazO2YcMGlSpVStI/ZwAuWLCA4g8AANxzpkyZoqNHjyowMFAlSpSQl5eXzfbdu3eblAwAACCj5ORk+fn5SZLy58+vCxcuqGzZsgoLC+NzCwCHQ/EHACY5fPiwHn744Ztub9Sokd588827mAgAACB72rRpY3YEAACAbCtXrpyioqIUHBysypUr67PPPlNwcLCmT5+uIkWKmB0PAHIUS30CgEnc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OTlZkjRq1CglJSWZnAgA7g7O+AMAAAAA2OXGX817enrajF++fFkffvihhg8fLkn66aefVLRoUTMiAgCAB1yVKlX03HPPqX79+jIMQ+PHj1fevHkznXvjswsAOAKu8QcAAAAAsEuePHl09uxZ+fn52YxfvHhRfn5+SktLMykZAADAP6KiojRixAgdO3ZMu3fv1kMPPSRn54znwVgsFu3evduEhACQOyj+AAAAAAB2cXJy0rlz51S4cGGb8bVr16pTp066cOGCSckAAAAycnJyUmxsbIY/WgIAR8RSnwAAAACAbMmfP78sFossFovKli0ri8Vi3ZaWlqakpCS98MILJiYEAADIKD093ewIAHDXcMYfAAAAACBb5s6dK8Mw1LNnT02aNEm+vr7Wba6urgoODladOnVMTAgAAJC5+fPna/r06Tpx4oS2bNmiEiVKaOLEiSpVqpSeeuqp/9fe3QZpXd53H/5eCwsEhEVTHiMuIERAHgLFaEyIJfgUh0KGmpBoG0yJKdFIKRJLpopBQ1FmoISgJAZHhtaaWCfahqZACbVjSVMmIggqRh4EYlFqVkRACuzu/SK3m2wwCrrLv14cx8zO7HX+d9fP7Atmx991nmfReQBNxo4/AAAAjsuECROSJL169cqFF16YysrKgosAAN7eokWLMmPGjEyZMiWzZs1quI/49NNPz/z58w3+gLJixx8AAAAnrK6uLlu2bMmePXuOOT7r4x//eEFVAADHGjBgQP76r/86n/rUp9K+ffts2LAhvXv3zqZNm/IHf/AHefnll4tOBGgydvwBAABwQn7605/mqquuyo4dO/Lb7yUtlUoN76IHAPi/YPv27Rk6dOgx661bt86BAwcKKAJoPhVFBwAAAPDeMmnSpAwfPjybNm1KTU1NXnnllYaPmpqaovMAABrp1atX1q9ff8z68uXL079//5MfBNCM7PgDAADghDz33HN56KGH0qdPn6JTAADe1tSpU3P99dfn0KFDqa+vz9q1a/PAAw9k9uzZWbx4cdF5AE3K4A8AAIATcv7552fLli0GfwDAe8IXv/jFvO9978vNN9+cgwcP5qqrrkr37t3zzW9+M5/97GeLzgNoUqX6376QAQAAAN7Cww8/nJtvvjlf/epXM2jQoFRWVjZ6Pnjw4ILKAADe2sGDB7N///507ty56BSAZmHwBwAAwAmpqDj2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")
footer = """
    <style>
    a:hover
    {
        opacity:50%;
    }
    .footer 
    {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        text-align: center;
    }
    </style>
    <div class="footer">
        <p> Developed by <a style='display: block; text-align: center;' href="https://iamssuraj.netlify.app/" target="_blank"> Suraj Sanganbhatla </a> </p>
    </div>
"""
st.markdown(footer, unsafe_allow_html=True)