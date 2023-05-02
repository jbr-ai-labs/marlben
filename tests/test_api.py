def test_import():
   import nmmo

def test_env_creation():
   import nmmo
   env = nmmo.Env()
   env.reset()
   env.step({})
