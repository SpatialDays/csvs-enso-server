from ensoserver import config
from ensoserver.config import enso_source_url
from ensoserver.domain.model import Enso
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ensoserver.adapters import repository
from ensoserver.adapters.orm import metadata, start_mappers

from fastapi.middleware.cors import CORSMiddleware

from ensoserver.domain.services import obtain_enso_data_from_url

from fastapi.responses import StreamingResponse
import csv

start_mappers()
engine = create_engine(config.get_postgres_uri())
get_session = sessionmaker(bind=engine)
metadata.create_all(engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.put("/enso")
async def update_enso_values():
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    for ts, meiv2 in obtain_enso_data_from_url(url=enso_source_url):
        repo.add(Enso(ts, meiv2))
    session.commit()
    return jsonable_encoder({'number_enso_values': repo.count()})


@app.get("/enso")
async def get_enso_values():
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    enso_values = repo.list()
    if not enso_values:
        raise HTTPException(status_code=404, detail="No ENSO values found")

    csv_filename = 'enso.csv'
    with open(csv_filename, 'w', newline='') as file:
        csv_writer = csv.writer(file, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['Time', 'Multivariate ENSO Index Version 2 (MEI.v2)'])
        for enso in enso_values:
            csv_writer.writerow([enso.ts.isoformat(), enso.meiv2])

    return StreamingResponse(
        open(csv_filename, mode="rb"),
        media_type="text/csv",
        headers={
            f"Content-Disposition": f"attachment;filename={csv_filename}"
        }
    )
