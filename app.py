import base64
import streamlit as st
import pickle

model = pickle.load(open('RFR_model.pkl', 'rb'))

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
     <style>
     .stApp {{
         background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
         background-size: cover
     }}
     </style>
     """,
        unsafe_allow_html=True
    )

add_bg_from_local("bg image car.jpg")

def main():
    new_title = '<p style="font-family:serif; color:black;border-radius:100px ;background-color: yellow;text-align: center; font-size: 42px;"><b>Car Price Predictor 🚘</b></p>'
    st.markdown(new_title, unsafe_allow_html=True)


    years = st.number_input('In which year car was purchased ?', 1990, 2023, step=1, key='year')
    Years_old = 2023 - years

    Present_Price = st.number_input('What is the current ex-showroom price of the car ?  (In ₹lakhs)', 0.00, 50.00,
                                    step=0.5, key='present_price')

    Kms_Driven = st.number_input('What is distance completed by the car in Kilometers ?', 0.00, 500000.00, step=500.00,
                                 key='drived')

    Owner = st.radio("The number of owners the car had previously ?", (0, 1, 3), key='owner')

    Fuel_Type_Petrol = st.selectbox('What is the fuel type of the car ?', ('Petrol', 'Diesel', 'CNG'), key='fuel')
    if (Fuel_Type_Petrol == 'Petrol'):
        Fuel_Type_Petrol = 1
        Fuel_Type_Diesel = 0
    elif (Fuel_Type_Petrol == 'Diesel'):
        Fuel_Type_Petrol = 0
        Fuel_Type_Diesel = 1
    else:
        Fuel_Type_Petrol = 0
        Fuel_Type_Diesel = 0

    Seller_Type_Individual = st.selectbox('Are you a dealer or an individual ?', ('Dealer', 'Individual'), key='dealer')
    if (Seller_Type_Individual == 'Individual'):
        Seller_Type_Individual = 1
    else:
        Seller_Type_Individual = 0

    Transmission_Mannual = st.selectbox('What is the Transmission Type ?', ('Manual', 'Automatic'), key='manual')
    if (Transmission_Mannual == 'Mannual'):
        Transmission_Mannual = 1
    else:
        Transmission_Mannual = 0

    if st.button("Estimate Price", key='predict'):
        try:
            Model = model  # get_model()
            prediction = Model.predict([[Present_Price, Kms_Driven, Owner, Years_old, Fuel_Type_Diesel,
                                         Fuel_Type_Petrol, Seller_Type_Individual, Transmission_Mannual]])
            output = round(prediction[0], 2)
            if output < 0:
                st.warning("You will be not able to sell this car !!")
            else:
                new_title = f'<p style="font-family:serif; color:black; font-size: 30px;border-radius:1000px ;background-color: #cbfc82; font-size: 30px;text-align: center"><b><u>You can sell the car for {output} lakhs 🙌</u></b></p>'
                st.markdown(new_title, unsafe_allow_html=True)

        except:
            st.warning("Opps!! Something went wrong\nTry again")


if __name__ == "__main__":
    main()