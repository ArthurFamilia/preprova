# Configurações da aplicação

SUPABASE_URL = "https://irnyfnklimdguwkxotbw.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlybnlmbmtsaW1kZ3V3a3hvdGJ3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDE5NzM5NzQsImV4cCI6MjA1NzU0OTk3NH0.m-bghlGXt2ZAAmKxyH_306LbMrvayHU3Bwx7NwKkn9U"
DB_PASSWORD = "sfgsg45645fghfg"
OPENAI_KEY = os.getenv("OPENAI_KEY")  # Carrega do ambiente

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Erro: SUPABASE_URL ou SUPABASE_KEY não estão configurados corretamente.")
