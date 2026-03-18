from enum import Enum

class TaskTagsEnum(Enum):
    PAINTING = "painting"
    CONSTRUCTION = "construction"
    CARPENTER = "carpenter"

class TaskStatus(Enum):
    POSTED = "posted"
    ASSIGNED = "assigned"
    COMPLETED = "completed"
    CANCELED = "canceled"
    INPROGRESS = "inprogress"
    
