from app.seed.seed_admin import run_seeders

def run_startup_tasks() -> None:
    run_seeders()