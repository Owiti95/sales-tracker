from models import Counter
from sqlalchemy.orm import Session

def create_counter(session: Session, name: str):
    new_counter = Counter(name=name)
    session.add(new_counter)
    session.commit()
    return new_counter

def get_all_counters(session: Session):
    return session.query(Counter).all()

def delete_counter(session: Session, counter_id: int):
    counter = session.query(Counter).filter(Counter.id == counter_id).first()
    if counter:
        session.delete(counter)
        session.commit()
    else:
        raise ValueError("Counter not found")
