from dotenv import load_dotenv; load_dotenv()
from app.config import get_settings
s = get_settings()
print("use_encryption:", s.use_encryption)
print("base_url:", s.base_url)
print("protocol:", s.protocol)
print("root_url:", s.root_url)
print("verify_tls:", s.verify_tls)
print("database_url:", s.database_url[:50])
