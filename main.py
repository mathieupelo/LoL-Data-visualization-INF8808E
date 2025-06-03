import requests
from PIL import Image
from io import BytesIO

url = "https://static.wikia.nocookie.net/leagueoflegends/images/d/d6/Azir_Render.png/revision/latest?cb=20231105071801"

response = requests.get(url)
img = Image.open(BytesIO(response.content))
img.show()
