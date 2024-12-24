import csv
import random
import math


class Zoo:
    move = 1

    def __init__(self):
        # Zoo sınıfının başlatıcı metodunda, başlangıçta boş listeler ve sözlükler oluşturulur.
        self.animals = []  # Hayvanlar listesi
        self.births = []  # Doğumlar listesi
        self.deaths = []  # Ölümler listesi
        self.animal_counts = {}  # Hayvan türlerinin sayısını tutan bir sözlük

    def animal_add(self, species, gender, x, y):
        # Yeni bir hayvan ekleyen metot
        animal = {"species": species, "gender": gender, "x": x, "y": y}
        self.animals.append(animal)  # Yeni hayvanı animals listesine ekler

        # Yeni hayvan eklendiğinde türüne göre hayvan sayısını güncelle
        if species in self.animal_counts:
            self.animal_counts[species] += 1
        else:
            self.animal_counts[species] = 1

    def animal_move(self):
        # Hayvanların cinsine göre rastgele hareket etmesini sağlayan metot
        for animal in self.animals:
            if animal["species"] == 'sheep' or animal["species"] == 'cow' or animal["species"] == 'chicken':
                self.move = 2
            elif animal["species"] == 'wolf':
                self.move = 3
            elif animal["species"] == 'lion':
                self.move = 4
            else:
                self.move = 1
            dx = random.randint(-1 * self.move, 1 * self.move)
            dy = random.randint(-1 * self.move, 1 * self.move)
            animal["x"] = max(0, min(500, animal["x"] + dx))
            animal["y"] = max(0, min(500, animal["y"] + dy))

    def reproduce(self):
        # Hayvanların üremesini sağlayan metot
        new_animals = []
        for animal_1 in self.animals:
            for animal_2 in self.animals:
                if (animal_1 != animal_2 and animal_1["species"] == animal_2["species"]
                        and animal_1["gender"] != animal_2["gender"]):
                    distance = math.sqrt((animal_1["x"] - animal_2["x"]) ** 2 + (animal_1["y"] - animal_2["y"]) ** 2)
                    if distance <= 3:
                        new_species = animal_1["species"]
                        new_gender = random.choice(['male', 'female'])
                        new_x = random.randint(0, 500)
                        new_y = random.randint(0, 500)
                        new_animals.append({"species": new_species, "gender": new_gender, "x": new_x, "y": new_y})
                        self.births.append((new_species, new_gender, new_x, new_y))
                if animal_1["species"] == 'chicken' and animal_2["species"] == 'rooster':
                    distance = math.sqrt((animal_1["x"] - animal_2["x"]) ** 2 + (animal_1["y"] - animal_2["y"]) ** 2)
                    if distance <= 3:
                        new_species = random.choice(['chicken', 'rooster'])
                        if new_species == 'chicken':
                            new_gender = 'female'
                        else:
                            new_gender = 'male'
                        new_x = random.randint(0, 500)
                        new_y = random.randint(0, 500)
                        new_animals.append({"species": new_species, "gender": new_gender, "x": new_x, "y": new_y})
                        self.births.append((new_species, new_gender, new_x, new_y))
        # Yeni doğan hayvanları ekler
        self.animals.extend(new_animals)
        # Yeni doğan hayvanlar eklendikten sonra hayvan sayılarını güncelle
        for new_animal in new_animals:
            if new_animal["species"] in self.animal_counts:
                self.animal_counts[new_animal["species"]] += 1
            else:
                self.animal_counts[new_animal["species"]] = 1

    def remove_dead_animals(self):
        # Ölen hayvanları kaldıran metot
        new_animals = []
        for animal in self.animals:
            if not self.is_dead(animal):
                new_animals.append(animal)
            else:
                self.deaths.append((animal["species"], animal["gender"], animal["x"], animal["y"]))
                # Ölen hayvanı animals listesinden çıkarırken türüne göre hayvan sayısını güncelle
                self.animal_counts[animal["species"]] -= 1
        self.animals = new_animals

    def is_dead(self, animal):
        # Hayvanın ölüp ölmediğini kontrol eden metot
        if animal["species"] == 'sheep':
            for wolf in self.animals:
                if wolf["species"] == 'wolf' and math.sqrt(
                        (wolf["x"] - animal["x"]) ** 2 + (wolf["y"] - animal["y"]) ** 2) <= 4:
                    return True
            return False
        elif animal["species"] == 'chicken':
            for wolf in self.animals:
                if wolf["species"] == 'wolf' and math.sqrt(
                        (wolf["x"] - animal["x"]) ** 2 + (wolf["y"] - animal["y"]) ** 2) <= 4:
                    return True
            return False
        elif animal["species"] == 'rooster':
            for wolf in self.animals:
                if wolf["species"] == 'wolf' and math.sqrt(
                        (wolf["x"] - animal["x"]) ** 2 + (wolf["y"] - animal["y"]) ** 2) <= 4:
                    return True
            return False
        elif animal["species"] == 'cow':
            for lion in self.animals:
                if lion["species"] == 'lion' and math.sqrt(
                        (lion["x"] - animal["x"]) ** 2 + (lion["y"] - animal["y"]) ** 2) <= 5:
                    return True
            return False
        elif animal["species"] == 'sheep':
            for lion in self.animals:
                if lion["species"] == 'lion' and math.sqrt(
                        (lion["x"] - animal["x"]) ** 2 + (lion["y"] - animal["y"]) ** 2) <= 5:
                    return True
            return False
        elif animal["species"] != 'hunter':
            for hunter in self.animals:
                if hunter["species"] == 'hunter' and math.sqrt(
                        (hunter["x"] - animal["x"]) ** 2 + (hunter["y"] - animal["y"]) ** 2) <= 8:
                    return True
            return False
        else:
            return False

    def count_animals(self):
        # Hayvan sayılarını döndüren metot
        return self.animal_counts

    def print_animal_coordinates(self):
        # Hayvanların koordinatlarını yazdıran metot
        for animal in self.animals:
            print(f'{animal["species"]}: ({animal["x"]}, {animal["y"]})')

    def save_animal_data_to_csv(self, filename):
        # Hayvan verilerini CSV dosyasına kaydeden metot
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Species', 'gender', 'X', 'Y'])
            for animal in self.animals:
                writer.writerow([animal["species"], animal["gender"], animal["x"], animal["y"]])

    def save_deaths_to_csv(self, filename):
        # Ölümleri CSV dosyasına kaydeden metot
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Species', 'gender', 'X', 'Y'])
            writer.writerows(self.deaths)

    def save_births_to_csv(self, filename):
        # Doğumları CSV dosyasına kaydeden metot
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Species', 'gender', 'X', 'Y'])
            writer.writerows(self.births)


def main():
    # Ana işlemi yapan fonksiyon
    zoo = Zoo()
    # Başlangıçta belirlenen sayıda hayvan eklenir
    for X in range(15):
        zoo.animal_add('sheep', 'male', random.randint(0, 500), random.randint(0, 500))
        zoo.animal_add('sheep', 'female', random.randint(0, 500), random.randint(0, 500))
    for X in range(5):
        zoo.animal_add('cow', 'male', random.randint(0, 500), random.randint(0, 500))
        zoo.animal_add('cow', 'female', random.randint(0, 500), random.randint(0, 500))
    for X in range(10):
        zoo.animal_add('chicken', 'female', random.randint(0, 500), random.randint(0, 500))
    for X in range(10):
        zoo.animal_add('rooster', 'male', random.randint(0, 500), random.randint(0, 500))
    for X in range(5):
        zoo.animal_add('wolf', 'male', random.randint(0, 500), random.randint(0, 500))
        zoo.animal_add('wolf', 'female', random.randint(0, 500), random.randint(0, 500))
    for X in range(4):
        zoo.animal_add('lion', 'male', random.randint(0, 500), random.randint(0, 500))
        zoo.animal_add('lion', 'female', random.randint(0, 500), random.randint(0, 500))
    zoo.animal_add('hunter', 'male', random.randint(0, 500), random.randint(0, 500))
    # Başlangıçtaki hayvan verileri CSV dosyasına kaydedilir
    zoo.save_animal_data_to_csv('animal_data.csv')
    total_steps = 0
    while total_steps < 1000:
        # 1000 adıma kadar hayvanların hareketi, ölümü ve üremesi gerçekleştirilir
        print(f'Step {total_steps}')
        zoo.animal_move()
        zoo.remove_dead_animals()
        zoo.reproduce()
        total_steps += 1

    # Son durumu CSV dosyalarına kaydet
    zoo.save_deaths_to_csv('deaths.csv')
    zoo.save_births_to_csv('births.csv')
    zoo.save_animal_data_to_csv('animal_data_finally.csv')


if __name__ == "__main__":
    main()
