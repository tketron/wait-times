import requests

from models.entity import ChildrenResponse

great_america = '15805a4d-4023-4702-b9f2-3d3cab2e0c1e'
rakshasa = '2157582b-10f4-40d7-9e70-9629cbab5a7d'

def main():
    print("Hello from wait-times!")

    # Get all destinations
    # response = requests.get(f'https://api.themeparks.wiki/v1/entity/{great_america}')
    # data = response.json()
    # print(data)

    # Get Six Flags Great America
    response = requests.get(f'https://api.themeparks.wiki/v1/entity/{great_america}/children')
    data = ChildrenResponse.model_validate(response.json())
    attractions_data = [a for a in data.children if a.entityType == 'ATTRACTION']

    # print(attractions_data)

#     Rakshasa
    response = requests.get(f'https://api.themeparks.wiki/v1/entity/{rakshasa}')
    data = response.json()
    print(data)

if __name__ == "__main__":
    main()
