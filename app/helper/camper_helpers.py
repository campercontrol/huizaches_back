def update_record_campers(db, camper_id):
    from model.campers import Camper, CamperRecord
    from schema.campers.camper_record_schema import CamperRecordModify
    from crud.camps.camper_in_camp_crud import (
        get_past_subscribe_by_camper,
        get_subscribe_by_camper,
    )
    from crud.campers.camper_record_crud import update_camper_record_by_id

    past_camps = get_past_subscribe_by_camper(db, camper_id)
    future_camps = get_subscribe_by_camper(db, camper_id)
    camper_record_id = (
        db.query(CamperRecord.id)
        .select_from(Camper)
        .join(CamperRecord, CamperRecord.id == Camper.record_id)
        .filter(Camper.id == camper_id)
        .first()
    )[0]
    camper_record_md = {
        #attend= len(future_camps),
        #attended= len(past_camps),
        #total= len(future_camps) + len(past_camps)
        "attend": 1,
        "attended": 1,
        "total": 1
    }
    print("#####################################################")
    print(camper_record_md)
    status = update_camper_record_by_id(db, camper_record_id, camper_record_md)
    return 1
