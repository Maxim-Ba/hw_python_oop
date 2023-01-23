from dataclasses import dataclass, asdict
from typing import List, Dict, Type


SECONDS_IN_MINUTE: int = 60


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    DESCRIPTIONS_FOR_MESSGES = {
        "training_type": "Тип тренировки",
        "duration": "Длительность",
        "distance": "Дистанция",
        "speed": "Ср. скорость",
        "calories": "Потрачено ккал",
    }

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Вернуть информационное сообщение о тренировке."""

        return (
            "{0}: {1}; ".format(
                InfoMessage.DESCRIPTIONS_FOR_MESSGES["training_type"],
                asdict(self)["training_type"],
            )
            + "{0}: {1:.3f} ч.; ".format(
                InfoMessage.DESCRIPTIONS_FOR_MESSGES["duration"],
                asdict(self)["duration"],
            )
            + "{0}: {1:.3f} км; ".format(
                InfoMessage.DESCRIPTIONS_FOR_MESSGES["distance"],
                asdict(self)["distance"],
            )
            + "{0}: {1:.3f} км/ч; ".format(
                InfoMessage.DESCRIPTIONS_FOR_MESSGES["speed"],
                asdict(self)["speed"],
            )
            + "{0}: {1:.3f}.".format(
                InfoMessage.DESCRIPTIONS_FOR_MESSGES["calories"],
                asdict(self)["calories"],
            )
        )


@dataclass
class Training:
    """Базовый класс тренировки."""

    action: int
    duration: float
    weight: float

    MINUTES_IN_HOURS: int = 60
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    len_step = LEN_STEP

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.len_step / Training.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        raise NotImplementedError("Method must be defined")

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()

        return InfoMessage(
            type(self).__name__, self.duration, distance, speed, calories
        )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed()

        return (
            (
                Running.CALORIES_MEAN_SPEED_MULTIPLIER * mean_speed
                + Running.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight
            / Training.M_IN_KM
            * self.duration
            * Training.MINUTES_IN_HOURS
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_MEAN_SPEED_MULTIPLIER: float = 0.035
    CALORIES_MEAN_SPEED_SHIFT: float = 0.029
    TO_M_PER_SEC: float = 0.278
    SMETERS_IN_METERS: int = 100

    def __init__(
        self, action: int, duration: float, weight: float, height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed()
        mean_speed_m_in_sec = mean_speed * SportsWalking.TO_M_PER_SEC
        height_in_sm = self.height / SportsWalking.SMETERS_IN_METERS
        duration_in_minutes = self.duration * Training.MINUTES_IN_HOURS

        return (
            SportsWalking.CALORIES_MEAN_SPEED_MULTIPLIER * self.weight
            + (mean_speed_m_in_sec**2 / (height_in_sm))
            * SportsWalking.CALORIES_MEAN_SPEED_SHIFT
            * self.weight
        ) * duration_in_minutes


class Swimming(Training):
    """Тренировка: плавание."""

    KOEF_TWO_POOLS: int = 2
    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 1.1

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: float,
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.len_step = Swimming.LEN_STEP

    def get_mean_speed(self) -> float:

        return (
            self.length_pool
            * self.count_pool
            / Training.M_IN_KM
            / self.duration
        )

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed()

        return (
            (mean_speed + Swimming.CALORIES_MEAN_SPEED_MULTIPLIER)
            * Swimming.KOEF_TWO_POOLS
            * self.weight
            * self.duration
        )


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков. И вернуть обьект тренировки."""
    traning_enum: Dict[str, Type[Training]] = {
        "SWM": Swimming,
        "RUN": Running,
        "WLK": SportsWalking,
    }

    try:
        if workout_type not in traning_enum:
            raise ValueError
    except ValueError:
        print("Такого типа тренировки нет!")

    return traning_enum[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()
    print(info.get_message())


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
