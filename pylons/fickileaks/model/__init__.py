from sqlalchemy.orm import scoped_session, sessionmaker
import elixir

# replace the elixir session with our own
Session = scoped_session(sessionmaker(autoflush=True))
elixir.session = Session
elixir.options_defaults.update({
    'shortnames': True
})

# use the elixir metadata
metadata = elixir.metadata

# this will be called in config/environment.py
def init_model(engine):
    metadata.bind = engine

# import your entities, and set them up
from entities import *
elixir.setup_all()
