from pydantic import BaseModel
import json, os
    
class Database():
    def __init__(self, filename: str, object_type: BaseModel) -> None:
        self.file = f'./{filename}.json'
        if not os.path.exists(self.file):
            with open(self.file, 'w') as file:
                file.write('[]')
        self.object = object_type
    
    def load(self) -> dict[str, str]:
        with open(self.file, 'r', encoding='UTF-8') as file:
            return json.loads(file.read())

    def add(self, new_object: BaseModel) -> None:
        data = self.load()
        data.append(new_object.model_dump())
        with open(self.file, 'w', encoding='UTF-8') as file:
            file.write(json.dumps(data, indent=4))
    
    def get_by(self, field:str, value:str) -> any:
        return next((self.object(**object_data) for object_data in self.load() if object_data[field] == value), None)
    
    def within(self, field:str, value:str) -> bool:
        return next((True for object_data in self.load() if object_data[field] == value), False)
