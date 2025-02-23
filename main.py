from datetime import datetime as dt
from turtledemo.penrose import start
from wsgiref.validate import header_re

import requests

NUT_APP_ID = '9e8891de'
NUT_APP_KEY = '00a6d694f99a3c7c41c4290243b35221'
NUT_END_POINT = 'https://trackapi.nutritionix.com/v2/natural/exercise'

SHEETY_EXERCISE_END = 'https://api.sheety.co/6468d5dc7184d3ac9f2b8861e127bc0a/jazDhillonFoodExerciseLog1/exerciseLog'
SHEETY_FOOD_END = 'https://api.sheety.co/6468d5dc7184d3ac9f2b8861e127bc0a/jazDhillonFoodExerciseLog1/foodLog'
SHEETY_TOKEN = 'yomydudethi5ismyb34r3rc0d3'

auth_header = {
    'Authorization': 'Bearer ' + SHEETY_TOKEN,
    'Content-Type': 'application/json',
}

HEIGHT = 177

def main():
    today_date = dt.today().strftime('%d/%m/%Y')

    def birthday_calculator():

        today = dt.today()
        birthdate = dt(year=2005, month=5, day=9)

        age = today.year - birthdate.year

        return age

    def add_exercise_entry():
        is_running = True
        while is_running:
            weight_input = input("Enter weight or hit enter to continue: ")
            try:
                weight_input = float(weight_input)
                if weight_input < 0 or weight_input > 500:
                    continue
            except ValueError:
                continue
            finally:
                age = birthday_calculator()

            exercise_nat_input = input("What exercise did you do today?")
            time_of_exercise_input = input("What time did of exercise?\n[0-24] hours -> ")
            try:
                time_of_exercise_input = int(time_of_exercise_input)
            except ValueError:
                print("Invalid input\nDefaulting to None")
                time_of_exercise_input = None
            if exercise_nat_input == ' ' or '':
                continue

            nutri_header = {
                'x-app-id': NUT_APP_ID,
                'x-app-key': NUT_APP_KEY,
            }

            nutri_params = {
                'query': exercise_nat_input,
                'age': age,
                'weight_kg': weight_input,
                'height_cm': HEIGHT,
            }

            nut_post_response = requests.post(NUT_END_POINT, json=nutri_params, headers=nutri_header).json()
            # ----------------------- EXAMPLE RESPONSE ----------------------- 
            
            # print(nut_post_request.json())
            # {
            # 'exercises': [
            # {'tag_id': 252,
            # 'user_input': 'tennis',
            # 'duration_min': 120,
            # 'met': 7.3,
            # 'nf_calories': 1165.08,
            # 'photo': {'highres': 'https://d2xdmhkmkbyw75.cloudfront.net/exercise/252_highres.jpg',
            # 'thumb': 'https://d2xdmhkmkbyw75.cloudfront.net/exercise/252_thumb.jpg',
            # 'is_user_uploaded': False}, 'compendium_code': 15675, 'name': 'tennis',
            # 'description': None, 'benefits': None}]}
            exercise_data = nut_post_response['exercises'][-1]
            duration = exercise_data['duration_min']
            activity_name = exercise_data['user_input']
            met_intensity = exercise_data['met']
            calories_burnt = exercise_data['nf_calories']
            tag_id = exercise_data['tag_id']


            exercise_params = {
                "exerciselog": {
                    'tag': tag_id,
                    'date': today_date,
                    'exercise': activity_name,
                    'duration': duration,
                    'calories': calories_burnt,
                    'weight': weight_input,
                    'intensity': met_intensity,
                }
            }

            exercise_payload = requests.post(SHEETY_EXERCISE_END, json=exercise_params, headers=auth_header).json()
            if 'exerciseLog' in exercise_payload:
                is_running = False
            else:
                print("Something went wrong, try again!")

    def edit_entry():
        is_running = True


        while is_running:
            filter_dict = {}
            for i in range(8):
                sort_metric = input("What are you searching by:\n"
                                    "[Tag (t), Date (d), Exercise (e), Duration (du), Calories (c), Weight (w), Intensity (i)], STOP (leave empty)]\n")
                if sort_metric == '':
                    break
                elif sort_metric == 't':
                    filter_value = input("Tag searching by:\n")
                    filter_dict['Tag'] = filter_value
                elif sort_metric == 'd':
                    filter_value = input("Date searching by:\n")
                    filter_dict['Date'] = filter_value
                elif sort_metric == 'e':
                    filter_value = input("Exercise Name searching by:\n")
                    filter_dict['Exercise'] = filter_value
                elif sort_metric == 'c':
                    filter_value = input("Calories burnt searching by:\n")
                    filter_dict['Calories'] = filter_value
                elif sort_metric == 'i':
                    filter_value = input("Intensity searching by:\n")
                    filter_dict['Intensity'] = filter_value
                elif sort_metric == 'du':
                    filter_value = input("Duration searching by:\n")
                    filter_dict['Duration'] = filter_value
                elif sort_metric == 'w':
                    filter_value = input("Weight searching by:\n")
                    filter_dict['Weight'] = filter_value
                else:
                    print("Invalid input\nChoose from valid options")
                    break

            search_params = {f'filter[{key}]=' : value for key, value in filter_dict.items()} #still wrong
            # search_params = {
            #     'filter': [f"filter[{key}]={value}" for key, value in filter_dict.items()],
            # }
            get_response = requests.get(SHEETY_EXERCISE_END, json=search_params, headers=auth_header).json()
            print(get_response)
            should_continue = input("Would you like to continue? (y/n)")
            if should_continue == 'n':
                break

    #     TODO: Get edit row working, don't know how to format filter parameter to get valid response





    while True:
        birthday_calculator()
        action_input = input("What would you like to do?\n"
                             "=> Add Exercise [a]\n"
                             "=> Edit Exercise [e]\n"
                             "=> Delete Exercise [d]\n")
        if action_input == 'a':
            add_exercise_entry()
        elif action_input == 'e':
            edit_entry()





if __name__ == '__main__':
    main()
