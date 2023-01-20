LEN_STEP_WATER = 1.38
LEN_STEP_LAND = 0.65
SECONDS_IN_MINUTE = 60
MINUTES_IN_HOURS = 60
SMETERS_IN_METERS = 100


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(
        self,
        training_type: str,
        duration: float,
        distance: float,
        speed: float,
        calories: float,
    ) -> None:
        self.training_type = training_type
        self.duration = round(duration, 3)
        self.distance = round(distance, 3)
        self.speed = round(speed, 3)
        self.calories = round(calories, 3)

    def get_message(self):
        return f"""
        Тип тренировки: {self.training_type};
        Длительность: {self.duration} ч.;
        Дистанция: {self.distance} км; Ср. скорость: {self.speed} км/ч;
        Потрачено ккал: {self.calories}.
        """


class Training:
    """Базовый класс тренировки."""

    M_IN_KM = 1000

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        # in meters
        self.len_step = 0
        self.action = action
        # in hours
        self.duration = duration
        # in kg
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.len_step / Training.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(
            self.__class__.__name__, self.duration, distance, speed, calories
        )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79
    LEN_STEP = LEN_STEP_LAND

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
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    LEN_STEP = LEN_STEP_LAND
    CALORIES_MEAN_SPEED_MULTIPLIER = 0.035
    CALORIES_MEAN_SPEED_SHIFT = 0.029

    def __init__(
        self, action: int, duration: float, weight: float, height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed()
        mean_speed_m_in_sec = (
            mean_speed
            * Training.M_IN_KM
            / (MINUTES_IN_HOURS * SECONDS_IN_MINUTE)
        )
        height_in_sm = self.height / SMETERS_IN_METERS
        duration_in_minutes = self.duration * MINUTES_IN_HOURS
        return (
            SportsWalking.CALORIES_MEAN_SPEED_MULTIPLIER * self.weight
            + (mean_speed_m_in_sec**2 / (height_in_sm))
            * SportsWalking.CALORIES_MEAN_SPEED_SHIFT
            * self.weight
        ) * duration_in_minutes


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = LEN_STEP_WATER
    CALORIES_MEAN_SPEED_MULTIPLIER = 1.1

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
            * 2
            * self.weight
            * self.duration
        )


traning_enum = {"SWM": Swimming, "RUN": Running, "WLK": SportsWalking}


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков. И вернуть обьект тренировки."""
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
