from enum import StrEnum


class BloomLevel(StrEnum):
    remember = "Remember"
    understand = "Understand"
    apply = "Apply"
    analyze = "Analyze"
    evaluate = "Evaluate"
    create = "Create"


class LearningLevel(StrEnum):
    beginner = "L1 Beginner"
    basic = "L2 Basic"
    intermediate = "L3 Intermediate"
    advanced = "L4 Advanced"
    expert = "L5 Expert"
