LEN_STEP_WATER: float = 1.38
LEN_STEP_LAND: float = 0.65
SECONDS_IN_MINUTE: int = 60


def toFixed(numObj: float, digits: int = 0) -> str:
    """Получить число с определенным кол-вом знаков после запятой."""

    return f"{numObj:.{digits}f}"


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
        self.duration = toFixed(float(duration), 3)
        self.distance = toFixed(distance, 3)
        self.speed = toFixed(speed, 3)
        self.calories = toFixed(calories, 3)

    def get_message(self) -> str:
        """Вернуть информационное сообщение о тренировке."""

        return (
            f"Тип тренировки: {self.training_type}; "
            f"Длительность: {self.duration} ч.; "
            f"Дистанция: {self.distance} км; "
            f"Ср. скорость: {self.speed} км/ч; "
            f"Потрачено ккал: {self.calories}."
        )


class Training:
    """Базовый класс тренировки."""

    MINUTES_IN_HOURS: int = 60

    M_IN_KM: int = 1000
    LEN_STEP: float = LEN_STEP_LAND

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        self.len_step = Training.LEN_STEP
        self.action = action
        self.duration = duration
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
    LEN_STEP = LEN_STEP_WATER
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
