pushd .\app
poetry run uvicorn main:app --reload
popd