from dataclasses import dataclass
from typing import List, Dict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """
        Метод который возвращает строку сообщения
        с информацией о тренировке.
        """
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """
    Базовый класс тренировки.

    M_IN_KM = перевод метров в километры,
    LEN_STEP = длина шага в метрах,
    MIN_IN_H = перевод часов в минуты.
    """
    M_IN_KM: float = 1000
    LEN_STEP: float = 0.65
    MIN_IN_H: float = 60

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float) -> None:
        """
        Конструктор класса.

        Указание размерностей:

        action = кол-во совершенных действий,
        duration = время в часах,
        distance = расстояние в километрах.
        """
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """
    Тренировка: бег.

    LEN_STEP = длина шага в метрах.
    """
    LEN_STEP: float = 0.65
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: float = 100

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        """
        Конструктор класса.

        Указание размерностей:

        action = кол-во совершенных действий,
        duration = время в часах,
        weight = вес в кг,
        height = рост в сантиметрах.
        """
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (((self.CALORIES_WEIGHT_MULTIPLIER * self.weight)
                + ((self.get_mean_speed() * self.KMH_IN_MSEC)**2
                / (self.height / self.CM_IN_M))
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                * self.weight) * self.duration * self.MIN_IN_H)


class Swimming(Training):
    """
    Тренировка: плавание.

    LEN_STEP = длина одного гребка.
    """
    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    CALORIES_WEIGHT_MULTIPLIER: float = 2
    CALORIES_WEIGHT_SHIFT: float = 0.029

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        """
        Конструктор класса.

        Описание атрибутов:

        action = кол-во совершенных действий,
        duration = время в часах,
        weight = вес в кг,
        height = рост в сантиметрах,
        length_pool = длина бассейна в метрах,
        count_pool = сколько раз переплыл бассейн.
        """
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.CALORIES_WEIGHT_MULTIPLIER
                * self.weight * self.duration)


def read_package(workout_type: str, data: List[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    dictionary: Dict[str, list[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in dictionary:
        raise KeyError(f'Ошибка типа тренировки {workout_type}')
    return dictionary[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
